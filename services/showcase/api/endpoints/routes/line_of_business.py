import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.db.models.related import (
    LobReadWithSandbox,
    OutOfBandReadPopulated,
)
from api.db.repositories.out_of_band import OutOfBandRepository
from api.endpoints.dependencies.db import get_db
from api.db.repositories.line_of_business import LobRepository

from api.services import sandbox

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/lobs",
    status_code=status.HTTP_200_OK,
    response_model=List[LobReadWithSandbox],
)
async def get_line_of_businesses(
    sandbox_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> List[LobReadWithSandbox]:
    # this should take some query params, sorting and paging params...
    repo = LobRepository(db_session=db)
    items = await repo.get_in_sandbox(sandbox_id)
    return items


@router.get(
    "/lobs/{lob_id}",
    status_code=status.HTTP_200_OK,
    response_model=LobReadWithSandbox,
)
async def get_line_of_business(
    sandbox_id: UUID,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> LobReadWithSandbox:
    repo = LobRepository(db_session=db)
    item = await repo.get_by_id_with_sandbox(sandbox_id, lob_id)
    return item


@router.get(
    "/lobs/{lob_id}/out-of-band-msgs",
    status_code=status.HTTP_200_OK,
    response_model=List[OutOfBandReadPopulated],
)
async def get_out_of_band_messages(
    sandbox_id: UUID,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> OutOfBandReadPopulated:
    # make sure lob is in this sandbox...
    lob_repo = LobRepository(db_session=db)
    lob = await lob_repo.get_by_id_with_sandbox(sandbox_id, lob_id)
    # go get all oob messages for the lob (recipient or sender)
    oob_repo = OutOfBandRepository(db_session=db)
    items = await oob_repo.get_for_lob(lob_id=lob.id)
    return items


@router.post(
    "/lobs/{lob_id}/create-invitation/student",
    status_code=status.HTTP_200_OK,
    response_model=sandbox.InviteStudentResponse,
)
async def create_invitation_for_student(
    sandbox_id: UUID,
    lob_id: UUID,
    payload: sandbox.InviteStudentRequest,
    db: AsyncSession = Depends(get_db),
) -> sandbox.InviteStudentResponse:
    return await sandbox.create_invitation_for_student(
        sandbox_id=sandbox_id, lob_id=lob_id, payload=payload, db=db
    )


@router.post(
    "/lobs/{lob_id}/create-invitation/applicant",
    status_code=status.HTTP_200_OK,
    response_model=sandbox.InviteApplicantResponse,
)
async def create_invitation_for_applicant(
    sandbox_id: UUID,
    lob_id: UUID,
    payload: sandbox.InviteApplicantRequest,
    db: AsyncSession = Depends(get_db),
) -> sandbox.InviteStudentResponse:
    return await sandbox.create_invitation_for_applicant(
        sandbox_id=sandbox_id, lob_id=lob_id, payload=payload, db=db
    )


@router.post(
    "/lobs/{lob_id}/accept-invitation",
    status_code=status.HTTP_200_OK,
    response_model=sandbox.AcceptInvitationResponse,
)
async def accept_invitation(
    sandbox_id: UUID,
    lob_id: UUID,
    payload: sandbox.AcceptInvitationRequest,
    db: AsyncSession = Depends(get_db),
) -> sandbox.AcceptInvitationResponse:
    return await sandbox.accept_invitation(
        sandbox_id=sandbox_id, lob_id=lob_id, payload=payload, db=db
    )


@router.post(
    "/lobs/{lob_id}/make-issuer",
    status_code=status.HTTP_200_OK,
)
async def promote_to_issuer(
    sandbox_id: UUID,
    lob_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await sandbox.promote_lob_to_issuer(
        sandbox_id=sandbox_id, lob_id=lob_id, db=db
    )
