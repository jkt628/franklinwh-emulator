"""Implement the FranklinWH API server."""

from datetime import datetime

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel

from emulator import ResponseWithTotal, login

router = APIRouter(prefix="/initialize")


class PostLoginResult(BaseModel):
    affiliateCompany: list[str] = []
    availableMfaMethods: list[str] | None = None
    currentType: int = 0
    distributorId: int | None = None
    email: str
    failureVersion: str | None = None
    installerId: int | None = None
    maskedEmail: bool | None = None
    mfaEmail: str | None = None
    mfaEnforceInfo: bool | None = None
    mfaMethod: str | None = None
    mfaRequired: bool | None = None
    mfaSetupRequired: bool | None = None
    mfaToken: str | None = None
    needAgreeTerm: bool = False
    needConsent: bool = False
    ninetyDaysPwdUpdate: int = 0
    passwordUpdateFlag: int = 0
    policyContent: str | None = None
    policyCountry: str | None = None
    policyLanguage: str | None = None
    policyVersion: str | None = None
    roles: list[str] = []
    serviceVoltageFlag: int | None = None
    surveyFlag: int = 0
    token: str
    userId: int = 1
    userTypes: list[int] = [0]
    version: str = "1.0.0"


class PostLoginResponse(ResponseWithTotal[PostLoginResult]):
    pass


@router.post("/appUserOrInstallerLogin")
async def post_login(
    account: str | None = None,
    opt_device: str | None = None,
    opt_system_version: str | None = None,
    password: str | None = None,
    software_version: str | None = None,
    type: str | None = None,
    user_type: str | None = None,
    client_id: str | None = None,
    lang: str | None = None,
    logintoken: str | None = None,
    optdevice: str | None = None,
    optdevicename: str | None = None,
    optsource: str | None = None,
    optsystemversion: str | None = None,
    opttime: datetime | None = None,
    softwareversion: str | None = None,
    account2: str = Form(alias="account", default=None),
    password2: str = Form(alias="password", default=None),
    lang2: str = Form(alias="lang", default=None),
    type2: str = Form(alias="type", default=None),
) -> PostLoginResponse:
    if account is None:
        if account2 is None:
            raise HTTPException(status_code=500, detail="Missing account")
        account = account2
    if password is None:
        if password2 is None:
            raise HTTPException(status_code=500, detail="Missing password")
        password = password2

    try:
        token, user = login(account, password)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=e.args[0])
    return PostLoginResponse.model_validate(
        {
            "result": {
                "email": account,
                "token": token,
                "userId": user.userId,
            },
            "total": 1,
        }
    )
