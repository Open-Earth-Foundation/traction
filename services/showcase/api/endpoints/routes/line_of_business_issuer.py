import logging
import time
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.endpoints.dependencies.db import get_db
from api.db.repositories.line_of_business import LobRepository
from api.db.repositories.student import StudentRepository
from api.db.repositories.job_applicant import ApplicantRepository

from api.services import traction

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/students/{student_id}/issue-degree",
    status_code=status.HTTP_200_OK,
)
async def issue_degree(
    sandbox_id: UUID,
    lob_id: UUID,
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    s_repo = StudentRepository(db_session=db)
    lob_repo = LobRepository(db_session=db)

    student = await s_repo.get_by_id_in_sandbox(sandbox_id, student_id)
    faber = await lob_repo.get_by_id_with_sandbox(sandbox_id, lob_id)

    attrs = [
        {"name": "company_id", "value": student.student_id},
        {"name": "name", "value": student.name},
        {"name": "date", "value": student.date.date().strftime("%d-%m-%Y")},
    ]

    resp = await traction.tenant_issue_credential(
        faber.wallet_id,
        faber.wallet_key,
        str(student.connection_id),
        alias="BC_Gov",
        cred_def_id=str(faber.cred_def_id),
        attributes=attrs,
    )
    # we will need some info for revoking this (rev_reg_id, cred_rev_id)
    logger.info("issue credential response")
    logger.info(resp)
    return resp

@router.post(
    "/students/{org_id}/issue-ghg",
    status_code=status.HTTP_200_OK,
)
async def issue_ghg(
    sandbox_id: UUID,
    lob_id: UUID,
    org_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    a_repo = ApplicantRepository(db_session=db)
    lob_repo = LobRepository(db_session=db)

    org = await a_repo.get_by_id_in_sandbox(sandbox_id, org_id)
    print(org)
    cas = await lob_repo.get_by_id_with_sandbox(sandbox_id, lob_id)
    print(cas)
    attrs = [
        {"name": "facility_emissions_scope1_co2e", "value": "1000"},
        {"name": "credential_reporting_date_start", "value": int(time.time())},
        {"name": "credential_reporting_date_end", "value": int(time.time())},
        {"name": "facility_name", "value": "Copper Mountain"},
        {"name": "facility_country", "value": "Canada"},
        {"name": "organization_name", "value": org.name},
        {"name": "facility_jurisdiction", "value": "BC"},
    ]

    resp = await traction.tenant_issue_credential(
        cas.wallet_id,
        cas.wallet_key,
        str(org.connection_id),
        alias="Cas",
        cred_def_id=str(cas.cred_def_id),
        attributes=attrs,
    )
    # we will need some info for revoking this (rev_reg_id, cred_rev_id)
    logger.info("issue credential response")
    logger.info(resp)
    return resp


@router.post(
    "/students/{student_id}/revoke-degree",
    status_code=status.HTTP_200_OK,
)
async def revoke_degree(
    sandbox_id: UUID,
    lob_id: UUID,
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    s_repo = StudentRepository(db_session=db)
    lob_repo = LobRepository(db_session=db)

    student = await s_repo.get_by_id_in_sandbox(sandbox_id, student_id)
    issuer = await lob_repo.get_by_id_with_sandbox(sandbox_id, lob_id)

    issued_credentials = await traction.tenant_get_issued_credentials(
        issuer.wallet_id, issuer.wallet_key
    )
    # find the credential for this student's connection id
    # and the issuer's cred def id.
    cred = next(
        (
            x
            for x in issued_credentials
            if str(x["credential"]["connection_id"]) == str(student.connection_id)
            and str(x["credential"]["cred_def_id"]) == str(issuer.cred_def_id)
        ),
        None,
    )
    if cred:
        await traction.tenant_revoke_credential(
            issuer.wallet_id,
            issuer.wallet_key,
            cred["credential"]["rev_reg_id"],
            cred["credential"]["cred_rev_id"],
            f"Revoked by {issuer.name}.",
        )

    return


@router.get(
    "/issued-credentials",
    status_code=status.HTTP_200_OK,
)
async def get_issued_credentials(
    sandbox_id: UUID,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    lob_repo = LobRepository(db_session=db)
    lob = await lob_repo.get_by_id_with_sandbox(sandbox_id, lob_id)

    # call traction to see what credentials we've issued.
    resp = await traction.tenant_get_issued_credentials(
        lob.wallet_id,
        lob.wallet_key,
    )

    return resp
