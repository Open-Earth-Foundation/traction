from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api import acapy_utils as au
from api.tenant_security import (
    oauth2_scheme,
)


router = APIRouter()


class ConnectionProtocolType(str, Enum):
    Connections = "connections/1.0"
    DIDExchange = "didexchange/1.0"


class ConnectionStateType(str, Enum):
    start = "start"
    init = "init"
    invitation = "invitation"
    request = "request"
    response = "response"
    active = "active"
    completed = "completed"
    abandoned = "abandoned"
    error = "error"


class ConnectionRoleType(str, Enum):
    inviter = "inviter"
    invitee = "invitee"
    requester = "requester"
    responder = "responder"


class Connection(BaseModel):
    endpoint: str | None = None
    accept: str
    alias: str | None = None
    connection_id: str
    connection_protocol: str
    created_at: str
    error_msg: str | None = None
    inbound_connection_id: str | None = None
    invitation_key: str
    invitation_mode: str
    invitation_msg_id: str | None = None
    my_did: str | None = None
    request_id: str | None = None
    rfc23_state: str
    routing_state: str | None = None
    state: str
    their_did: str | None = None
    their_label: str | None = None
    their_public_did: str | None = None
    their_role: str | None = None
    updated_at: str


class Invitation(BaseModel):
    connection_id: str
    invitation: dict
    invitation_url: str


class BasicMessage(BaseModel):
    content: str


@router.get("/", response_model=list[Connection])
async def get_connections(
    alias: Optional[str] = None,
    connection_protocol: Optional[ConnectionProtocolType] = None,
    invitation_key: Optional[str] = None,
    my_did: Optional[str] = None,
    connection_state: Optional[ConnectionStateType] = None,
    their_did: Optional[str] = None,
    their_role: Optional[ConnectionRoleType] = None,
    # note we don't need the token here but we need to make sure it gets set
    _token: str = Depends(oauth2_scheme),
):
    params = {
        "alias": alias,
        "connection_protocol": connection_protocol,
        "invitation_key": invitation_key,
        "my_did": my_did,
        "connection_state": connection_state,
        "their_did": their_did,
        "their_role": their_role,
    }
    connections = await au.acapy_GET("connections", params=params)
    return connections["results"]


@router.post("/create-invitation", response_model=Invitation)
async def create_invitation(
    alias: str | None = None,
    # note we don't need the token here but we need to make sure it gets set
    _token: str = Depends(oauth2_scheme),
):
    params = {"alias": alias}
    invitation = await au.acapy_POST(
        "connections/create-invitation", data={}, params=params
    )
    return invitation


@router.post("/receive-invitation", response_model=Connection)
async def receive_invitation(
    payload: dict,
    alias: str | None = None,
    # note we don't need the token here but we need to make sure it gets set
    _token: str = Depends(oauth2_scheme),
):
    params = {"alias": alias}
    connection = await au.acapy_POST(
        "connections/receive-invitation", data=payload, params=params
    )
    return connection


@router.post("/send-message", response_model=dict)
async def send_message(
    payload: BasicMessage,
    connection_id: str | None = None,
    alias: str | None = None,
    # note we don't need the token here but we need to make sure it gets set
    _token: str = Depends(oauth2_scheme),
):
    if not connection_id:
        lookup_params = {"alias": alias}
        connections = await au.acapy_GET("connections", params=lookup_params)
        connection_id = connections["results"][0]["connection_id"]
    message = {"content": payload.content}
    response = await au.acapy_POST(
        f"connections/{connection_id}/send-message", data=message
    )
    return response
