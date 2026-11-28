import random
import time
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from emulator import (
    APower,
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


class standard:
    d = "%Y-%m-%d"
    t = "%H:%M:%S"
    dt = d + " " + t


class Entrance(BaseModel):
    show: bool
    key: str


class GetAppGlobalConfigResult(BaseModel):
    entrance: list[Entrance]
    tip: bool | None = None
    isAppVersion1User: bool = False
    openFastCommission: bool | None = None
    showTouTemplate: bool = False


GetAppGlobalConfigResponse = Response[GetAppGlobalConfigResult]


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


EmptyResponse = Response[list[BaseModel]]


@router.get("/appObtainAdvertiseLst")
async def appObtainAdvertiseLst() -> EmptyResponse:
    return EmptyResponse(result=[])


class DeviceInfoResult(BaseModel):
    gatewayId: str
    date: str  # "2026-11-24",
    deviceTime: str  # "2026-11-24 06:20:24",
    countryId: int = 2
    provinceId: int = 67
    offGirdFlag: int = 0
    sysHdVersion: str = "103"
    sysHdVersionInt: int = 103
    realSysHdVersion: str = "FranklinWH System1.3"
    protocolVer: str = "V1.12.44"
    installerId: int = 1
    serviceVoltageFlag: int | None = None
    offMessage: str | None = None
    genEn: int
    chooseFinancierId: int = 0
    firstName: str
    lastName: str
    fhpSn: str
    gridPhaseConSet: int = 0
    activeStatus: int = 1
    emsDeviceVer: int = 1
    solarFlag: bool = True
    solarTipMsg: str = ""
    v2lModeEnable: int = 0
    v2lRunState: int = 0
    newHomeFlag: int | None = None
    sleepStatus: int | None = None
    zoneInfo: str
    peHwVerList: list[int]
    fixedPowerTotal: float
    fixedPowerAverage: float
    totalCap: float
    apowerList: list[APower]
    blackSleepFlag: bool = False
    mpptEnFlag: bool = False
    apbox20Num: int = 0
    equipType: int = 122
    msaInstallStartDetectTime: str | None = None


DeviceInfoResponse = Response[DeviceInfoResult]


@router.get("/getDeviceInfoV2")
async def getDeviceInfoV2(user: LoginUser, gatewayId: str) -> DeviceInfoResponse:
    site, gateway = user.site(gatewayId)
    fixedPowerTotal = totalCap = 0.0
    for p in gateway.aPower:
        fixedPowerTotal += p.ratedPwr
        totalCap += p.rateBatCap
    fixedPowerAverage = fixedPowerTotal / len(gateway.aPower)
    result = DeviceInfoResult(
        gatewayId=gatewayId,
        date=datetime.now(UTC).strftime(standard.d),
        deviceTime=datetime.now(site.tz).strftime(standard.dt),
        genEn=int(gateway.has_generator),
        firstName=user.PII.firstName,
        lastName=user.PII.lastName,
        fhpSn=",".join([p.id for p in gateway.aPower]),
        zoneInfo=str(site.tz),
        peHwVerList=[2 for p in gateway.aPower],
        fixedPowerTotal=fixedPowerTotal / 1000.0,
        fixedPowerAverage=fixedPowerAverage / 1000.0,
        totalCap=totalCap / 1000.0,
        apowerList=gateway.aPower,
    )
    return DeviceInfoResponse(result=result)


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


class BackupHistorySummaryResult(BaseModel):
    longestDuration: int = 43210
    totalBackup: int = 160
    totalDuration: int = 156987

    class LastRecord(BaseModel):
        id: int = 2833896
        gatewayId: str
        chargeType: int = 2
        energy: float = 0.0
        startSoc: int = 95
        endSoc: int = 95
        chargeDate: str = "2026-11-18 09:46:01"
        startTime: str = "2026-11-18 09:46:01"
        endTime: str = "2026-11-18 09:49:41"
        second: int = 220
        chargeTime: None = None
        chargeHour: None = None
        chour: None = None
        cminute: None = None
        csecond: None = None
        # cSpell:words chour cminute csecond

    lastRecord: LastRecord


BackupHistorySummaryResponse = Response[BackupHistorySummaryResult]


@router.get("/backupHistorySummary")
async def backupHistorySummary(gatewayId: str) -> BackupHistorySummaryResponse:
    return BackupHistorySummaryResponse(
        result=BackupHistorySummaryResult(
            lastRecord=BackupHistorySummaryResult.LastRecord(gatewayId=gatewayId)
        )
    )


class GatewaySystemSettingResult(BaseModel):
    gatewayId: str
    gridPhaseConSet: int = 0
    electricSupply: int = 200
    ratedGridVolt: int = 0
    ratedGridHz: int = 0
    offGridFlag: int = 0
    gridExportEnable: int = 0
    apowerChPw: int = 20000
    apowerDishPw: int = 20000
    apowerNumber: int
    countryId: int = 2
    emsDeviceVer: int = 1
    bsRelyEn: int = 0
    threePhPvEnb: int = 0
    mpanGridEnb: int = 0
    backupSolution: int = 0
    mainPanelRate: int = 200
    pcsSetFlag: bool = True
    rsdEnable: int = 0


GatewaySystemSettingResponse = Response[GatewaySystemSettingResult]


@router.get("/getGatewaySystemSetting")
async def getGatewaySystemSetting(
    user: LoginUser, gatewayId: str
) -> GatewaySystemSettingResponse:
    _, gateway = user.site(gatewayId)
    return GatewaySystemSettingResponse(
        result=GatewaySystemSettingResult(
            gatewayId=gatewayId, apowerNumber=len(gateway.aPower)
        )
    )


class HotSpotResult(BaseModel):
    id: int
    gatewayId: str  # "10060005A02X24320195",
    ssid: str  # "AP_X24320195",
    password: str  # "A02X24320195"


HotSpotResponse = Response[HotSpotResult]


@router.get("/getHotSpotInfo/v2")
async def getHotSpotInfoV2(gatewayId: str) -> HotSpotResponse:
    return HotSpotResponse(
        result=HotSpotResult(
            id=int(gatewayId[-5:]),
            gatewayId=gatewayId,
            ssid="AP_" + gatewayId[-9:],
            password=gatewayId[-12:],
        )
    )


ShowTipResponse = Response[None]


@router.get("/getShowTip")
async def getShowTip(type: int) -> ShowTipResponse:
    return ShowTipResponse(result=None)


class ChargePowerDetailsResult(BaseModel):
    batterySoc: float = 92.842
    touMinSoc: int = 20
    currentStateDuration: float = 117.27
    highEnergyConsumption: float = 2.55
    averageEnergyConsumption: float = 28.7
    currentTime: str = "4 day 21 hour 16 minute"
    highEnergyTime: str = "2 hour 33 minute"
    averageTime: str = "1 day 4 hour 42 minute"


ChargePowerDetailsResponse = ResponseWithTotal[ChargePowerDetailsResult]


@router.get("/chargePowerDetails")
async def chargePowerDetails(gatewayId: str) -> ChargePowerDetailsResponse:
    # TODO: use actual stats
    return ChargePowerDetailsResponse(result=ChargePowerDetailsResult())


GetHomeGatewayListResponse = ResponseWithTotal[list[HomeGateway]]


@router.get("/getHomeGatewayList", dependencies=[LoginTokenAuth])
async def get_home_gateway_list(user: LoginUser) -> GetHomeGatewayListResponse:
    result = [
        HomeGateway(
            id=gateway.id,
            name=gateway.name,
            address=site.address or "",
            zipCode=site.zipCode,
            zoneInfo=str(site.tz),
            deviceTime=datetime.now(site.tz).strftime(standard.dt),
            account=user.account,
        )
        for site in user.sites
        for gateway in site.gateways
    ]
    return GetHomeGatewayListResponse(result=result, total=len(result))


GetPersonalInfoResponse = ResponseWithTotal[users.PII]


@router.get("/getPersonalInfo", dependencies=[LoginTokenAuth])
async def get_personal_info(user: LoginUser) -> GetPersonalInfoResponse:
    return GetPersonalInfoResponse(result=user.PII)


class SelectBenefitInfoResult(BaseModel):
    fuelConversion: float = 0.0
    evMileageConversion: float = 0.0
    treeConversion: float = 0.0
    carbonReduction: float = 0.0
    batFeedEarnList: list[float] = [0.00049874]
    batLoadEarnModList: list[float] = [0.23626775]
    batLoadEarnList: list[float] = [-0.15412097]
    solarFeedEarnList: list[float] = [0.0]
    solarLoadEarnList: list[float] = [0.0]
    solarToHouseList: list[float] = [0.0]
    solarToGridList: list[float] = [0.0]
    apowerToHouseList: list[float] = [0]
    apowerToGridList: list[float] = [0.022]
    dayTimeList: list[str]
    currency: str | None = None
    priceFlag: bool = True


SelectBenefitInfoResponse = Response[SelectBenefitInfoResult]


@router.get("/bill/electric/selectBenefitInfo")
async def selectBenefitInfo(type: int, dayTime: str) -> SelectBenefitInfoResponse:
    if type != 1:
        raise HTTPException(400, detail="Bad type")
    if dayTime != time.strftime("%Y-%m-%d"):
        return SelectBenefitInfoResponse(
            result=SelectBenefitInfoResult(
                batFeedEarnList=[],
                batLoadEarnModList=[],
                batLoadEarnList=[],
                solarFeedEarnList=[],
                solarLoadEarnList=[],
                solarToHouseList=[],
                solarToGridList=[],
                apowerToHouseList=[],
                apowerToGridList=[],
                dayTimeList=[dayTime],
            )
        )
    return SelectBenefitInfoResponse(
        result=SelectBenefitInfoResult(dayTimeList=[dayTime])
    )


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


GetMessagesResponse = ResponseWithTotal[list[Message]]


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
