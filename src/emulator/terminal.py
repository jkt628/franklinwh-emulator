import random
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from emulator import (
    LoginTokenAuth,
    LoginUser,
    Response,
    ResponseWithTotal,
    initialize,
    recommend,
    site_list,
    users,
)

router = APIRouter(prefix="/terminal")
router.include_router(initialize.router)
router.include_router(recommend.router, dependencies=[LoginTokenAuth])
router.include_router(site_list.router, dependencies=[LoginTokenAuth])


class Entrance(BaseModel):
    show: bool
    key: str


class GetAppGlobalConfigResult(BaseModel):
    entrance: list[Entrance]
    tip: bool | None = None
    isAppVersion1User: bool = False
    openFastCommission: bool | None = None
    showTouTemplate: bool = False


class GetAppGlobalConfigResponse(Response[GetAppGlobalConfigResult]):
    pass


@router.get("/getAppGlobalConfig", dependencies=[LoginTokenAuth])
async def get_app_global_config() -> GetAppGlobalConfigResponse:
    return GetAppGlobalConfigResponse.model_validate(
        {
            "result": {
                "entrance": [
                    {"show": True, "key": "smart_assistant"},
                    {"show": True, "key": "smart_assistant_floating"},
                ],
            },
        }
    )


class HomeGateway(BaseModel):
    id: str
    status: int = 1
    connType: int = 3
    name: str
    loadOption: int = 1
    gerOption: int = 1
    groupId: str | None = None
    groupName: str | None = None
    groupFlag: int = 0
    account: str
    protocolVer: str = "V1.12.44"
    version: str = "V10R11B40D00_SYS_aPower1X_20_2S_"
    address: str
    activeStatus: int = 1
    simCardStatus: int = 2
    activeTime: int = 1736883067000
    installTime: int | None = None
    createTime: int = 1723426754000
    realSysHdVersion: str = "FranklinWH System1.3"
    sysHdVersion: str = "103"
    zoneInfo: str
    deviceTime: str
    countryId: int = 2
    provinceId: int = 67
    benefitShowFlag: int = 1
    isJoinJA12: bool = False
    zipCode: str


class GetHomeGatewayListResponse(ResponseWithTotal[list[HomeGateway]]):
    pass


@router.get("/getHomeGatewayList", dependencies=[LoginTokenAuth])
async def get_home_gateway_list(user: LoginUser) -> GetHomeGatewayListResponse:
    result = [
        HomeGateway(
            id=gateway.id,
            name=gateway.name,
            address=site.address or "",
            zipCode=site.zipCode,
            zoneInfo=str(site.tz),
            deviceTime=datetime.now(site.tz).strftime("%Y-%m-%d %H:%M:%S"),
            account=user.account,
        )
        for site in user.sites for gateway in site.gateways 
    ]
    return GetHomeGatewayListResponse(result=result, total=len(result))


class GetPersonalInfoResponse(ResponseWithTotal[users.PII]):
    pass


@router.get("/getPersonalInfo", dependencies=[LoginTokenAuth])
async def get_personal_info(user: LoginUser) -> GetPersonalInfoResponse:
    return GetPersonalInfoResponse(result=user.PII)


class Message(BaseModel):
    id: int = 6420864
    title: str = "Grid restored"
    type: int = 1
    subType: int = 0
    gatewayId: str
    gatewayName: str
    content: str = "Grid power has been restored."
    notice: str | None = "Happy Birthday, Liz!"
    userMessageId: int = 6420864
    readStatus: int = 1
    creationTime: str = "2026-11-18 05:59:07"
    deviceSendTime: str = "2026-11-18 01:59:08"
    startTime: str = "2026-11-18-05:59:07"
    jumpScheme: str | None = None
    pictureUrl: str | None = None
    displayTime: str = "2026-11-18 01:59:08"


class GetMessagesResponse(ResponseWithTotal[list[Message]]):
    pass


@router.get("/selectTerPushMessageListApp", dependencies=[LoginTokenAuth])
async def get_messages(
    user: LoginUser, pageNum: int, pageSize: int
) -> GetMessagesResponse:
    return GetMessagesResponse(
        result=[
            Message(
                gatewayId=user.sites[0].gateways[0].id,
                gatewayName=user.sites[0].gateways[0].name,
            )
        ],
        total=1,
    )


class UnreadMessageCountResponse(ResponseWithTotal[int]):
    def __init__(self, result: int, total: int):
        super().__init__(result=result, total=total)


@router.get("/selectTerPushMessageUnreadCount", dependencies=[LoginTokenAuth])
async def get_unread_message_count(user: LoginUser) -> UnreadMessageCountResponse:
    return UnreadMessageCountResponse(result=int(random.random() < 0.02), total=1)
