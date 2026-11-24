"""Implement the FranklinWH API server."""

from fastapi import APIRouter
from pydantic import BaseModel

from emulator import LoginUser, Response, ResponseWithTotal

router = APIRouter(prefix="/common")


class Accessory(BaseModel):
    id: str
    sn: str
    accessoryType: int
    loadOption: None = None
    gerOption: None = None
    accessorySecondType: None = None
    accessoryNo: None = None
    createTime: str = "2026-01-01 00:00:00"


GetAccessoryListResponse = ResponseWithTotal[list[Accessory]]


@router.get("/getAccessoryList")
async def getAccessoryList(user: LoginUser, gatewayId: str) -> GetAccessoryListResponse:
    accessories = []
    gateway = user.gateway(gatewayId)
    x = gateway.stats.circuits.sn
    if x:
        accessories.append(Accessory(id=gatewayId, sn=x, accessoryType=4))
    x = gateway.stats.generator.sn
    if x:
        accessories.append(Accessory(id=gatewayId, sn=x, accessoryType=3))
    return GetAccessoryListResponse(result=accessories, total=len(accessories))


class PageByType(BaseModel):
    id: int
    dictType: str
    title: str
    content: str
    otherParams: str | None = None


GetPageByTypeResponse = Response[list[PageByType]]


@router.get("/getPageByTypeList")
async def getPageByTypeList(typeList: str) -> GetPageByTypeResponse:
    return GetPageByTypeResponse(
        result=[
            PageByType(
                id=120,
                dictType="sdcpSwitchModeTip",
                title="",
                content="Switching to other mode will result in not participating in Solar Battery Savings Program,which will impact receiving the incentive credit.We recommend to keep the current mode.",
            ),
            PageByType(
                id=113,
                dictType="modeListPageVppTip",
                title="VPP event day",
                content="Prior to the VPP event, the system will charge and standby for maximum event output/discharge. Charging modes will comply with PCS settings and utility agreement.",
            ),
            PageByType(
                id=115,
                dictType="modeListPageVppExitTip",
                title="VPP event ",
                content="Setting: opt-out To participate, select the event and opt-in.",
            ),
        ]
    )


class PowerCapConfig(BaseModel):
    id: int
    modelName: str
    peHwVersion: int
    ratedCap: int
    chargePower: int
    dischargePower: int
    derateFlag: int


GetPowerCapConfigListResponse = ResponseWithTotal[list[PowerCapConfig]]


@router.get("/getPowerCapConfigList")
async def getPowerCapConfigList() -> GetPowerCapConfigListResponse:
    return GetPowerCapConfigListResponse.model_validate(
        {
            "result": [
                {
                    "id": 1,
                    "modelName": "aPower X",
                    "peHwVersion": 0,
                    "ratedCap": 13600,
                    "chargePower": 5000,
                    "dischargePower": 5000,
                    "derateFlag": 0,
                },
                {
                    "id": 2,
                    "modelName": "aPower X",
                    "peHwVersion": 2,
                    "ratedCap": 13600,
                    "chargePower": 5000,
                    "dischargePower": 5000,
                    "derateFlag": 0,
                },
                {
                    "id": 3,
                    "modelName": "aPower 2",
                    "peHwVersion": 20,
                    "ratedCap": 15000,
                    "chargePower": 8000,
                    "dischargePower": 10000,
                    "derateFlag": 1,
                },
                {
                    "id": 4,
                    "modelName": "aPower S",
                    "peHwVersion": 21,
                    "ratedCap": 15000,
                    "chargePower": 8000,
                    "dischargePower": 10000,
                    "derateFlag": 1,
                },
                {
                    "id": 5,
                    "modelName": "aPower 2 (SH)",
                    "peHwVersion": 22,
                    "ratedCap": 15000,
                    "chargePower": 8000,
                    "dischargePower": 11500,
                    "derateFlag": 1,
                },
                {
                    "id": 6,
                    "modelName": "aPower X",
                    "peHwVersion": 4,
                    "ratedCap": 15000,
                    "chargePower": 5000,
                    "dischargePower": 5000,
                    "derateFlag": 0,
                },
            ],
            "total": 6,
        }
    )


class DeviceRunLog(BaseModel):
    alarmCode: str
    logName: str
    enLogName: str


SelectDeviceRunLogListResponse = ResponseWithTotal[list[DeviceRunLog]]


selectDeviceRunLogListResponse = SelectDeviceRunLogListResponse.model_validate_json("""
{
  "result": [
    {
      "alarmCode": "1001",
      "logName": "\u7535\u7f51\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "Relay Normally Close Failure of Grid"
    },
    {
      "alarmCode": "1002",
      "logName": "\u7535\u7f51\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "Relay Normally Open Failure of Grid"
    },
    {
      "alarmCode": "1003",
      "logName": "\u6cb9\u673a\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "Relay Normally Close Failure of Generator"
    },
    {
      "alarmCode": "1004",
      "logName": "\u6cb9\u673a\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "Relay Normally Open Failure of Generator"
    },
    {
      "alarmCode": "1005",
      "logName": "EPO\u7d27\u6025\u505c\u673a",
      "enLogName": "EPO Emergency Shutdown"
    },
    {
      "alarmCode": "1006",
      "logName": "\u6cb9\u673a\u6545\u969c",
      "enLogName": "Generator Failure"
    },
    {
      "alarmCode": "1007",
      "logName": "\u5907\u7535\u6545\u969c",
      "enLogName": "Backup Power Failure"
    },
    {
      "alarmCode": "1008",
      "logName": "FHP \u603b\u529f\u7387\u6545\u969c",
      "enLogName": "Total Power Failure of FHP"
    },
    {
      "alarmCode": "1009",
      "logName": "DSP\u4e0eARM\u53cc\u5411\u901a\u4fe1\u6545\u969c",
      "enLogName": "EMS Internal Communication Abnormality"
    },
    {
      "alarmCode": "100A",
      "logName": "\u5149\u4f0f\u7535\u8868\u901a\u4fe1\u6545\u969c",
      "enLogName": "Communications Fault of Photovoltaic Electricity Meter"
    },
    {
      "alarmCode": "100B",
      "logName": "\u5e02\u7535\u7535\u8868\u901a\u4fe1\u6545\u969c",
      "enLogName": "Communications Fault of Grid Electricity Meter"
    },
    {
      "alarmCode": "100C",
      "logName": "\u6269\u5c55\u7535\u8868\u901a\u4fe1\u6545\u969c",
      "enLogName": "Communications Fault of Spare Electricity Meter"
    },
    {
      "alarmCode": "100D",
      "logName": "\u5916\u90e8 485 \u901a\u4fe1\u6545\u969c",
      "enLogName": "Communications Fault of External 485"
    },
    {
      "alarmCode": "100E",
      "logName": "CAN\u901a\u4fe1\u7efc\u5408\u6545\u969c",
      "enLogName": "CAN communication comprehensive failure"
    },
    {
      "alarmCode": "100F",
      "logName": "\u5907\u7535\u6bcd\u7ebf\u7535\u538b\u5f02\u5e38",
      "enLogName": "Bus Voltage Abnormal of Backup Power"
    },
    {
      "alarmCode": "1010",
      "logName": "\u5e02\u7535\u7535\u8868CT\u5f02\u5e38",
      "enLogName": "Mains Meter CT Abnormal"
    },
    {
      "alarmCode": "1011",
      "logName": "\u7cfb\u7edf\u7535\u91cf\u4f4e\u4e8e\u5b89\u5168\u4fdd\u62a4\u7535\u91cf",
      "enLogName": "The system battery is lower than the safety protection battery"
    },
    {
      "alarmCode": "1017",
      "logName": "Bus Bar\u8fc7\u6d41\u6545\u969c",
      "enLogName": "Bus Bar over Current Fault"
    },
    {
      "alarmCode": "101A",
      "logName": "\u8fdc\u7aef\u8d1f\u8f7d\u4fa7\u5149\u4f0f\u7535\u88681\u901a\u4fe1\u6545\u969c",
      "enLogName": "Remote load-side solar meter 1 communications fault"
    },
    {
      "alarmCode": "101B",
      "logName": "\u8fdc\u7aef\u8d1f\u8f7d\u4fa7\u5149\u4f0f\u7535\u88682\u901a\u4fe1\u6545\u969c",
      "enLogName": "Remote load-side solar meter 2 communications fault"
    },
    {
      "alarmCode": "101C",
      "logName": "\u8fdc\u7aef\u7535\u7f51\u4fa7\u5149\u4f0f\u7535\u8868\u901a\u4fe1\u6545\u969c",
      "enLogName": "Remote grid-side solar meter communications fault"
    },
    {
      "alarmCode": "1020",
      "logName": "\u53d1\u7535\u673a\u542f\u52a8\u5f02\u5e38",
      "enLogName": "Generator starts abnormally"
    },
    {
      "alarmCode": "1022",
      "logName": "\u53d1\u7535\u673a\u8f93\u51fa\u8fc7\u8f7d",
      "enLogName": "Generator output overload"
    },
    {
      "alarmCode": "1023",
      "logName": "\u53d1\u7535\u673a\u505c\u6b62\u5931\u8d25",
      "enLogName": "Generator stop failed"
    },
    {
      "alarmCode": "1024",
      "logName": "\u53d1\u7535\u673aCT\u6545\u969c",
      "enLogName": "Generator CT failure"
    },
    {
      "alarmCode": "1025",
      "logName": "aPower\u7a7a\u5f00\u8fc7\u8f7d",
      "enLogName": "aPower air switch overload"
    },
    {
      "alarmCode": "1026",
      "logName": "\u9ed1\u542f\u52a8\u677f\u6545\u969c",
      "enLogName": "Black boot board fault"
    },
    {
      "alarmCode": "1027",
      "logName": "\u667a\u80fd\u8d1f\u8f7d\u7ee7\u7535\u56681\u5e38\u5f00\u6545\u969c",
      "enLogName": "Smart circuit relay 1 normally open fault"
    },
    {
      "alarmCode": "1028",
      "logName": "\u667a\u80fd\u8d1f\u8f7d\u7ee7\u7535\u56681\u5e38\u95ed\u6545\u969c",
      "enLogName": "Smart circuit relay 1 normally closed fault"
    },
    {
      "alarmCode": "2001",
      "logName": "\u4e91\u901a\u4fe1\u8fde\u63a5\u6545\u969c",
      "enLogName": "Clouds Communication Connection Fault"
    },
    {
      "alarmCode": "2003",
      "logName": "CAN \u786c\u7ebf\u65ad\u7ebf\u6545\u969c",
      "enLogName": "CAN hard wire disconnection fault"
    },
    {
      "alarmCode": "2004",
      "logName": "aPower#1 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#1 Communication   Abnormal"
    },
    {
      "alarmCode": "2005",
      "logName": "aPower#2 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#2 Communication   Abnormal"
    },
    {
      "alarmCode": "2006",
      "logName": "aPower#3 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#3 Communication   Abnormal"
    },
    {
      "alarmCode": "2007",
      "logName": "aPower#4 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#4 Communication   Abnormal"
    },
    {
      "alarmCode": "2008",
      "logName": "aPower#5 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#5 Communication   Abnormal"
    },
    {
      "alarmCode": "2009",
      "logName": "aPower#6 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#6 Communication   Abnormal"
    },
    {
      "alarmCode": "200A",
      "logName": "aPower#7 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#7 Communication   Abnormal"
    },
    {
      "alarmCode": "200B",
      "logName": "aPower#8 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#8 Communication   Abnormal"
    },
    {
      "alarmCode": "200C",
      "logName": "aPower#9 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#9 Communication   Abnormal"
    },
    {
      "alarmCode": "200D",
      "logName": "aPower#10 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#10 Communication   Abnormal"
    },
    {
      "alarmCode": "200E",
      "logName": "aPower#11 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#11 Communication   Abnormal"
    },
    {
      "alarmCode": "200F",
      "logName": "aPower#12 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#12 Communication   Abnormal"
    },
    {
      "alarmCode": "2010",
      "logName": "aPower#13 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#13 Communication   Abnormal"
    },
    {
      "alarmCode": "2011",
      "logName": "aPower#14 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#14 Communication   Abnormal"
    },
    {
      "alarmCode": "2012",
      "logName": "aPower#15 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#15 Communication   Abnormal"
    },
    {
      "alarmCode": "2013",
      "logName": "aPower#16 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#16 Communication   Abnormal"
    },
    {
      "alarmCode": "2014",
      "logName": "aPower#17 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#17 Communication   Abnormal"
    },
    {
      "alarmCode": "2015",
      "logName": "aPower#18 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#18 Communication   Abnormal"
    },
    {
      "alarmCode": "2016",
      "logName": "aPower#19 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#19 Communication   Abnormal"
    },
    {
      "alarmCode": "2017",
      "logName": "aPower#20 \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "aPower#20 Communication   Abnormal"
    },
    {
      "alarmCode": "2100",
      "logName": "CPU\u4f7f\u7528\u7387\u8fc7\u9ad8",
      "enLogName": "High CPU Usage"
    },
    {
      "alarmCode": "2104",
      "logName": "4G\u6a21\u5757\u672a\u63a5",
      "enLogName": "4G module not connected"
    },
    {
      "alarmCode": "2105",
      "logName": "SIM\u5361\u672a\u63d2\u5165",
      "enLogName": "SIM card not inserted"
    },
    {
      "alarmCode": "2106",
      "logName": "Wifi\u6a21\u5757\u672a\u63a5",
      "enLogName": "Wifi module is not connected"
    },
    {
      "alarmCode": "2107",
      "logName": "Wifi\u6a21\u5757\u5f02\u5e38",
      "enLogName": "The Wifi module is abnormal"
    },
    {
      "alarmCode": "3001",
      "logName": "\u5e02\u7535\u6545\u969c",
      "enLogName": "Grid Abnormal"
    },
    {
      "alarmCode": "3002",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u8fc7\u9891\u4fdd\u62a4",
      "enLogName": "Grid Level 1 Over-Frequency Protection"
    },
    {
      "alarmCode": "3003",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u6b20\u9891\u4fdd\u62a4",
      "enLogName": "Grid Level 1 Under-Frequency Protection"
    },
    {
      "alarmCode": "3004",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u8fc7\u9891\u4fdd\u62a4",
      "enLogName": "Grid Level 2 Over-Frequency Protection"
    },
    {
      "alarmCode": "3005",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u6b20\u9891\u4fdd\u62a4",
      "enLogName": "Grid Level 2 Under-Frequency Protection"
    },
    {
      "alarmCode": "3006",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "Grid Level 1 Overvoltage Protection"
    },
    {
      "alarmCode": "3007",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u6b20\u538b\u4fdd\u62a4",
      "enLogName": "Grid Level 1 Undervoltage Protection"
    },
    {
      "alarmCode": "3008",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "Grid Level 2 Overvoltage Protection"
    },
    {
      "alarmCode": "3009",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u6b20\u538b\u4fdd\u62a4",
      "enLogName": "Grid Level 2 Undervoltage Protection"
    },
    {
      "alarmCode": "300A",
      "logName": "\u5e02\u7535\u5feb\u901f\u77ac\u65f6\u503c\u4e00\u7ea7\u4f4e\u538b\u4fdd\u62a4",
      "enLogName": "Grid Fast Instantaneous Value Level 1 Low-Voltage Protection  "
    },
    {
      "alarmCode": "300B",
      "logName": "\u5e02\u7535\u5feb\u901f\u77ac\u65f6\u503c\u4e8c\u7ea7\u4f4e\u538b\u4fdd\u62a4",
      "enLogName": "Grid Fast Instantaneous Value Level 2 Low Voltage Protection "
    },
    {
      "alarmCode": "300C",
      "logName": "\u5e02\u7535\u5feb\u901f\u77ac\u65f6\u503c\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "Grid Fast Instantaneous High Voltage Protection"
    },
    {
      "alarmCode": "300D",
      "logName": "\u5e02\u7535\u8fc7\u538b\u5341\u5206\u949f\u4fdd\u62a4",
      "enLogName": "Grid Overvoltage Protection (For Ten Minutes)"
    },
    {
      "alarmCode": "300E",
      "logName": "\u5e02\u7535\u4e09\u7ea7\u6b20\u538b",
      "enLogName": "Mains Three-Level Undervoltage Protection"
    },
    {
      "alarmCode": "300F",
      "logName": "\u5e02\u7535\u4e0d\u5e73\u8861\u4fdd\u62a4",
      "enLogName": "Grid Unbalance Protection"
    },
    {
      "alarmCode": "3010",
      "logName": "\u5e02\u7535\u9501\u76f8\u5f02\u5e38",
      "enLogName": "Grid Phase Lock Abnormal"
    },
    {
      "alarmCode": "3011",
      "logName": "\u5e02\u7535\u5feb\u68c0\u6545\u969c",
      "enLogName": "Grid Quick Check Fault"
    },
    {
      "alarmCode": "3012",
      "logName": "\u5e02\u7535\u5305\u7edc\u68c0\u6d4b\u6389\u7535",
      "enLogName": "Grid Envelope Detection Power Fault"
    },
    {
      "alarmCode": "3014",
      "logName": "\u5e02\u7535\u5e45\u503c\u5feb\u68c0\u6545\u969c",
      "enLogName": "Grid Voltage Amplitude  Quick Inspection Fault"
    },
    {
      "alarmCode": "3015",
      "logName": "\u6cb9\u673a\u7ee7\u7535\u5668\u53cd\u9988\u89e6\u70b9\u5f02\u5e38",
      "enLogName": "Generator Relay Feedback Contact Abnormal"
    },
    {
      "alarmCode": "3017",
      "logName": "\u5e02\u7535\u76f4\u6d41\u5206\u91cf\u5feb\u68c0\u6545\u969c",
      "enLogName": "Grid DC Component Quick Inspection Fault"
    },
    {
      "alarmCode": "3018",
      "logName": "PE\u5728\u7ebf\u53f0\u6570\u8fc7\u591a",
      "enLogName": "Parallel number more than the set value"
    },
    {
      "alarmCode": "3019",
      "logName": "PE\u5728\u7ebf\u53f0\u6570\u6709\u6389\u7ebf",
      "enLogName": "Parallel number less than the set value"
    },
    {
      "alarmCode": "301A",
      "logName": "\u53d1\u7535\u673a\u5feb\u68c0\u5f02\u5e38",
      "enLogName": "Generator Quick Check Abnormal"
    },
    {
      "alarmCode": "301B",
      "logName": "\u53d1\u7535\u673a\u9501\u76f8\u5931\u8d25",
      "enLogName": "Generator Phase Lock Failure"
    },
    {
      "alarmCode": "301C",
      "logName": "\u53d1\u7535\u673a\u8f93\u51fa\u4e0d\u7a33",
      "enLogName": "The generator output is unstable"
    },
    {
      "alarmCode": "301D",
      "logName": "aPower\u8131\u79bb\u53d1\u7535\u673a\u7cfb\u7edf",
      "enLogName": "aPower disconnects from the generator system"
    },
    {
      "alarmCode": "301E",
      "logName": "\u9ed1\u542f\u52a8\u677f\u6545\u969c",
      "enLogName": "Black Boot Board Fault"
    },
    {
      "alarmCode": "301F",
      "logName": "DRM0\u72b6\u6001",
      "enLogName": "DRM0 state"
    },
    {
      "alarmCode": "3020",
      "logName": "\u53d1\u7535\u673a\u6545\u969c\u9000\u51fa",
      "enLogName": "Generator Withdraws due to Failure"
    },
    {
      "alarmCode": "3021",
      "logName": "DSP\u5916\u73afCAN\u901a\u4fe1\u6545\u969c",
      "enLogName": "High-speed CAN Communication Failure"
    },
    {
      "alarmCode": "3022",
      "logName": "EMS DSP\u63a7\u5236\u5e02\u7535\u7ee7\u7535\u5668\u53cd\u9988\u89e6\u70b9\u5f00\u8def\u6545\u969c",
      "enLogName": "Grid Relay Contact Abnormal"
    },
    {
      "alarmCode": "3023",
      "logName": "\u5149\u4f0f\u7ee7\u7535\u5668\u5f02\u5e38\u65ad\u5f00",
      "enLogName": "Solar Relay is Disconnected Abnormally"
    },
    {
      "alarmCode": "3024",
      "logName": "\u5e02\u7535\u76f8\u5236\u5f02\u5e38",
      "enLogName": "Incorrect Service Voltage Setting Detected"
    },
    {
      "alarmCode": "3025",
      "logName": "\u5e02\u7535\u76f8\u5e8f\u5f02\u5e38",
      "enLogName": "Mains phase sequence abnormal"
    },
    {
      "alarmCode": "3030",
      "logName": "\u9ed1\u542f\u52a8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "Normally open fault of black start relay"
    },
    {
      "alarmCode": "3031",
      "logName": "\u5730\u533a\u8bbe\u7f6e\u9519\u8bef",
      "enLogName": "Region setting error"
    },
    {
      "alarmCode": "4101",
      "logName": "1\u53f7PE \u9006\u53d8\u6545\u969c",
      "enLogName": "NO.1 PE Inverter Fault"
    },
    {
      "alarmCode": "4102",
      "logName": "1\u53f7PE \u9006\u53d8\u7535\u538b\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overvoltage Protection of Invertor Voltage"
    },
    {
      "alarmCode": "4103",
      "logName": "1\u53f7PE \u9006\u53d8\u7535\u538b\u6b20\u538b\u4fdd\u62a4",
      "enLogName": "NO.1 PE Undervoltage Protection of Invertor Voltage"
    },
    {
      "alarmCode": "4104",
      "logName": "1\u53f7PE \u9006\u53d8\u77ac\u65f6\u503c\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overvoltage Protection of Instantaneous voltage of Invertor"
    },
    {
      "alarmCode": "4105",
      "logName": "1\u53f7PE \u9006\u53d8\u7535\u538b\u76f4\u6d41\u5206\u91cf\u8fc7\u5927\u4fdd\u62a4",
      "enLogName": "NO.1 PE Inverter Voltage DC Component Excessive Protection"
    },
    {
      "alarmCode": "4106",
      "logName": "1\u53f7PE \u9006\u53d8\u77ed\u8def\u4fdd\u62a4",
      "enLogName": "NO.1 PE Short Circuit Protection of Invertor"
    },
    {
      "alarmCode": "4107",
      "logName": "1\u53f7PE \u9006\u53d8\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Inverter Overload Protection"
    },
    {
      "alarmCode": "4108",
      "logName": "1\u53f7PE \u9006\u53d8\u9650\u6d41\u65f6\u95f4\u8fc7\u957f\u4fdd\u62a4",
      "enLogName": "NO.1 PE Current Limiting Overtime Protection of Invertor"
    },
    {
      "alarmCode": "4109",
      "logName": "1\u53f7PE \u9006\u53d8\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overtemperature Protection of Invertor"
    },
    {
      "alarmCode": "410A",
      "logName": "1\u53f7PE \u9006\u53d8\u786c\u4ef6\u8fc7\u6d41\u4fdd\u62a4",
      "enLogName": "NO.1 PE Inverter Hardware Overcurrent Protection"
    },
    {
      "alarmCode": "410B",
      "logName": "1\u53f7PE \u9006\u53d8\u77ac\u65f6\u503c\u8fc7\u6d41\u4fdd\u62a4",
      "enLogName": "NO.1 PE Instantaneous OverCurrent Protection of Invertor"
    },
    {
      "alarmCode": "410C",
      "logName": "1\u53f7PE \u9006\u53d8\u7535\u6d41\u76f4\u6d41\u5206\u91cf\u8fc7\u5927\u4fdd\u62a4",
      "enLogName": "NO.1 PE Inverter Current DC Component Excessive Protection"
    },
    {
      "alarmCode": "410D",
      "logName": "1\u53f7PE \u9006\u53d8\u81ea\u9501\u4fdd\u62a4",
      "enLogName": "NO.1 PE Inverter Self-Locking Protection"
    },
    {
      "alarmCode": "410E",
      "logName": "1\u53f7PE \u9006\u53d8\u6bcd\u7ebf\u9884\u5145\u7535\u6545\u969c",
      "enLogName": "NO.1 PE Pre-Charge Failure of Invertor Bus"
    },
    {
      "alarmCode": "410F",
      "logName": "1\u53f7PE PE \u8f93\u51fa\u7ee7\u7535\u5668\u77ed\u8def\u6545\u969c",
      "enLogName": "NO.1 PE PE Output Relay Short Circuit Fault"
    },
    {
      "alarmCode": "4110",
      "logName": "1\u53f7PE PE \u8f93\u51fa\u7ee7\u7535\u5668\u5f00\u8def\u6545\u969c",
      "enLogName": "NO.1 PE PE Output Relay Open Circuit Fault"
    },
    {
      "alarmCode": "4111",
      "logName": "1\u53f7PE \u8f93\u51fa\u6545\u969c",
      "enLogName": "NO.1 PE Output Fault"
    },
    {
      "alarmCode": "4112",
      "logName": "1\u53f7PE \u8f93\u51fa\u56de\u8def\u5f02\u5e38",
      "enLogName": "NO.1 PE Output Circuit Abnormal"
    },
    {
      "alarmCode": "4113",
      "logName": "1\u53f7PE \u8f93\u51fa\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Output Overload Protection"
    },
    {
      "alarmCode": "4114",
      "logName": "1\u53f7PE \u8f93\u51fa\u8fc7\u8f7d\u544a\u8b66",
      "enLogName": "NO.1 PE Output Overload Warning"
    },
    {
      "alarmCode": "4115",
      "logName": "1\u53f7PE \u8f93\u51fa\u7ee7\u7535\u5668\u5f02\u5e38",
      "enLogName": "NO.1 PE Output Relay Abnormal"
    },
    {
      "alarmCode": "4116",
      "logName": "1\u53f7PE 105%\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overload Protection of 105%"
    },
    {
      "alarmCode": "4117",
      "logName": "1\u53f7PE 120%\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overload Protection of 120%"
    },
    {
      "alarmCode": "4118",
      "logName": "1\u53f7PE 160%\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overload Protection of 160%"
    },
    {
      "alarmCode": "4119",
      "logName": "1\u53f7PE 200%\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overload Protection of 200%"
    },
    {
      "alarmCode": "411A",
      "logName": "1\u53f7PE RCD\u8fc7\u8f7d\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overload Protection"
    },
    {
      "alarmCode": "411B",
      "logName": "1\u53f7PE \u8f93\u51fa\u8fc7\u8f7d",
      "enLogName": "NO.1 PE Output Overload"
    },
    {
      "alarmCode": "411C",
      "logName": "1\u53f7PE \u8f93\u51fa\u8fc7\u8f7d20\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 PE Lock after 20 times of output overload"
    },
    {
      "alarmCode": "411D",
      "logName": "1\u53f7PE \u534a\u6ce2\u8fc7\u8f7d",
      "enLogName": "NO.1 PE Half-wave Overload"
    },
    {
      "alarmCode": "4121",
      "logName": "1\u53f7PE \u5e76\u8054\u7ebf\u6389\u7ebf\u4fdd\u62a4",
      "enLogName": "NO.1 PE Parallel Line Drop Protection"
    },
    {
      "alarmCode": "4122",
      "logName": "1\u53f7PE \u5e76\u673a\u65e0\u5197\u4f59",
      "enLogName": "NO.1 PE Parallel without redundancy"
    },
    {
      "alarmCode": "4123",
      "logName": "1\u53f7PE \u53cc\u603b\u7ebf\u7cfb\u7edf\u79bb\u7ebf",
      "enLogName": "NO.1 PE Dual bus system offline"
    },
    {
      "alarmCode": "4124",
      "logName": "1\u53f7PE \u672c\u5730\u5173\u673a",
      "enLogName": "NO.1 PE Local Shutdown"
    },
    {
      "alarmCode": "4125",
      "logName": "1\u53f7PE \u4e0eIBG_EMU\u901a\u8baf\u6545\u969c",
      "enLogName": "NO.1 PE Communication Abnormal of IBG_EMU"
    },
    {
      "alarmCode": "4126",
      "logName": "1\u53f7PE \u96f6\u7ebf\u5f00\u8def",
      "enLogName": "NO.1 PE N Line Open"
    },
    {
      "alarmCode": "4127",
      "logName": "1\u53f7PE \u7cfb\u7edf\u73af\u5883\u6e29\u5ea6\u8fc7\u9ad8",
      "enLogName": "NO.1 PE System Ambient Over Temperature"
    },
    {
      "alarmCode": "4128",
      "logName": "1\u53f7PE PE_IBG\u56de\u8def\u5f02\u5e38",
      "enLogName": "NO.1 PE Electrical Fault between aPower and aGate"
    },
    {
      "alarmCode": "4129",
      "logName": "1\u53f7PE PE\u9ad8\u901fcan\u901a\u8baf\u5f02\u5e38",
      "enLogName": "NO.1 PE aPower CAN Communications Fault"
    },
    {
      "alarmCode": "412A",
      "logName": "1\u53f7PE PE \u5149\u4f0f\u8d85\u914d",
      "enLogName": "NO.1 PE PE Photovoltaic Overprovisioning"
    },
    {
      "alarmCode": "412B",
      "logName": "1\u53f7PE \u79bb\u7f51\u5149\u4f0f\u5145\u7535\u8d85\u65f6",
      "enLogName": "NO.1 PE Off-grid Solar Charging Timeout"
    },
    {
      "alarmCode": "412C",
      "logName": "1\u53f7PE INV\u4fa7V\u7248\u672c\u4e0d\u517c\u5bb9\u6545\u969c",
      "enLogName": "NO.1 PE V version incompatibility fault on the INV side"
    },
    {
      "alarmCode": "412D",
      "logName": "1\u53f7PE CPU2\u5fc3\u8df3\u56de\u4f20\u6545\u969c",
      "enLogName": "NO.1 PE CPU2 Heartbeat Return Fault"
    },
    {
      "alarmCode": "412E",
      "logName": "1\u53f7PE \u5e02\u7535\u5b9e\u9645\u76f8\u7535\u538b\u8fc7\u538b\u544a\u8b66",
      "enLogName": "NO.1 PE Actual grid phase voltage overvoltage alarm"
    },
    {
      "alarmCode": "412F",
      "logName": "1\u53f7PE \u8f85\u6e90\u7ee7\u7535\u5668\u5373\u5c06\u65ad\u5f00",
      "enLogName": "NO.1 PE Auxiliary relay is about to be disconnected"
    },
    {
      "alarmCode": "4131",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u6545\u969c",
      "enLogName": "NO.1 PE Bus Fault"
    },
    {
      "alarmCode": "4132",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u77ac\u65f6\u8fc7\u538b",
      "enLogName": "NO.1 PE Instantaneous Overvoltage of Bus"
    },
    {
      "alarmCode": "4133",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u77ac\u65f6\u6b20\u538b \uff08\u4e0d\u540c\u8f93\u5165\u7535\u538b\u4e0d\u540c\uff09",
      "enLogName": "NO.1 PE Instantaneous Undervoltage of Bus"
    },
    {
      "alarmCode": "4134",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u4f4e\u538b\u6162\u68c0",
      "enLogName": "NO.1 PE Bus Low Voltage Slow Inspection"
    },
    {
      "alarmCode": "4135",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u8fc7\u538b\u6162\u68c0",
      "enLogName": "NO.1 PE Slow Detection Of Bus Overvoltage"
    },
    {
      "alarmCode": "4136",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u4e0d\u5e73\u8861",
      "enLogName": "NO.1 PE Bus Unbalance"
    },
    {
      "alarmCode": "4137",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u786c\u4ef6\u6545\u969c",
      "enLogName": "NO.1 PE Hardware Failure of Bus"
    },
    {
      "alarmCode": "4138",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u8dcc\u843d\u5feb\u68c0",
      "enLogName": "NO.1 PE Large Instantaneous Fluctuations In Bus Voltage"
    },
    {
      "alarmCode": "4139",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u4f4e\u538b\u6162\u68c0",
      "enLogName": "NO.1 PE Bus Low Voltage(Slow)"
    },
    {
      "alarmCode": "413A",
      "logName": "1\u53f7PE INV\u4fa7\u6bcd\u7ebf\u51b2\u51fb\u8fc7\u538b\u6545\u969c",
      "enLogName": "NO.1 PE INV side bus surge overvoltage fault"
    },
    {
      "alarmCode": "4141",
      "logName": "1\u53f7PE \u9006\u53d8\u76f8 A \u77ed\u8def",
      "enLogName": "NO.1 PE L1 Short Circuit"
    },
    {
      "alarmCode": "4142",
      "logName": "1\u53f7PE \u9006\u53d8\u76f8 B \u77ed\u8def",
      "enLogName": "NO.1 PE L2 Short Circuit"
    },
    {
      "alarmCode": "4143",
      "logName": "1\u53f7PE \u9006\u53d8\u76f8AB\u77ed\u8def",
      "enLogName": "NO.1 PE L1\uff0cL2 Short Circuit"
    },
    {
      "alarmCode": "4148",
      "logName": "1\u53f7PE \u9006\u53d8\u6563\u70ed\u8fc7\u6e29",
      "enLogName": "NO.1 PE Inverter Heat Over Temperature"
    },
    {
      "alarmCode": "4149",
      "logName": "1\u53f7PE \u9006\u53d8IGBT\u8fc7\u6e29",
      "enLogName": "NO.1 PE Inverter IGBT over temperature"
    },
    {
      "alarmCode": "414A",
      "logName": "1\u53f7PE \u524d\u7ea7\u9501\u9006\u53d8",
      "enLogName": "NO.1 PE PE Lock Inverter"
    },
    {
      "alarmCode": "414B",
      "logName": "1\u53f7PE \u9006\u53d8\u9501\u76f8\u5f02\u5e38",
      "enLogName": "NO.1 PE Inverter Phase Lock Abnormal"
    },
    {
      "alarmCode": "414C",
      "logName": "1\u53f7PE PE\u76f8\u5e8f\u5f02\u5e38",
      "enLogName": "NO.1 PE Phase Abnormal of PE"
    },
    {
      "alarmCode": "414D",
      "logName": "1\u53f7PE DC/DC\u6545\u969c\u5173\u9006\u53d8",
      "enLogName": "NO.1 PE DC/DC Fault Off Inverter"
    },
    {
      "alarmCode": "414E",
      "logName": "1\u53f7PE \u534f\u8bae\u4e0d\u5339\u914d\u6545\u969c",
      "enLogName": "NO.1 PE Protocol Mismatch Fault"
    },
    {
      "alarmCode": "4150",
      "logName": "1\u53f7PE \u7cfb\u7edf\u5730\u5740\u51b2\u7a81\u6545\u969c",
      "enLogName": "NO.1 PE System address conflict fault"
    },
    {
      "alarmCode": "4151",
      "logName": "1\u53f7PE BuckBoost \u6545\u969c\u7efc\u5408",
      "enLogName": "NO.1 PE Buckboost Fault Synthesis"
    },
    {
      "alarmCode": "4152",
      "logName": "1\u53f7PE \u603b\u6bcd\u7ebf\u8fc7\u538b\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Quick Inspection Failure of Bus"
    },
    {
      "alarmCode": "4153",
      "logName": "1\u53f7PE \u6b63\u6bcd\u7ebf\u8fc7\u538b\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Quick Inspection Failure of Bus+"
    },
    {
      "alarmCode": "4154",
      "logName": "1\u53f7PE \u8d1f\u6bcd\u7ebf\u8fc7\u538b\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Quick Inspection Failure of Bus-"
    },
    {
      "alarmCode": "4155",
      "logName": "1\u53f7PE \u603b\u6bcd\u7ebf\u8fc7\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Slow Inspection Failure of Bus"
    },
    {
      "alarmCode": "4156",
      "logName": "1\u53f7PE \u6b63\u6bcd\u7ebf\u8fc7\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Slow Inspection Failure of Bus+"
    },
    {
      "alarmCode": "4157",
      "logName": "1\u53f7PE \u8d1f\u6bcd\u7ebf\u8fc7\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overvoltage Slow Inspection Failure of Bus-"
    },
    {
      "alarmCode": "4158",
      "logName": "1\u53f7PE \u6b63\u6bcd\u7ebf\u6b20\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Undervoltage Slow Inspection Failure of Bus+"
    },
    {
      "alarmCode": "4159",
      "logName": "1\u53f7PE \u8d1f\u6bcd\u7ebf\u6b20\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Undervoltage Slow Inspection Failure of Bus-"
    },
    {
      "alarmCode": "415A",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u8fc7\u538b\u786c\u4ef6\u6545\u969c",
      "enLogName": "NO.1 PE Hardware OverVoltage Failure of Bus"
    },
    {
      "alarmCode": "415B",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u7f13\u51b2\u5b8c\u6210",
      "enLogName": "NO.1 PE Bus Buffer Completed"
    },
    {
      "alarmCode": "415E",
      "logName": "1\u53f7PE BuckBoost \u653e\u7535\u8fc7\u6d41\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overcurrent Quick Inspection Failure of BuckBoost Discharge"
    },
    {
      "alarmCode": "415F",
      "logName": "1\u53f7PE BuckBoost \u5145\u7535\u8fc7\u6d41\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overcurrent Quick Inspection Failure of BuckBoost Charge"
    },
    {
      "alarmCode": "4160",
      "logName": "1\u53f7PE BuckBoost \u653e\u7535\u8fc7\u6d41\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overcurrent Slow Inspection Failure of BuckBoost Discharge"
    },
    {
      "alarmCode": "4161",
      "logName": "1\u53f7PE BuckBoost \u5145\u7535\u8fc7\u6d41\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Overcurrent Slow Inspection Failure of BuckBoost Charge"
    },
    {
      "alarmCode": "4163",
      "logName": "1\u53f7PE \u6bcd\u7ebf\u7535\u538b\u7a33\u5b9a\u6807\u5fd7",
      "enLogName": "NO.1 PE Bus Voltage Stability Sign"
    },
    {
      "alarmCode": "4164",
      "logName": "1\u53f7PE Midbus \u786c\u4ef6\u8fc7\u538b\u6545\u969c",
      "enLogName": "NO.1 PE Hardware Overvoltage Fault"
    },
    {
      "alarmCode": "4165",
      "logName": "1\u53f7PE \u529f\u7387\u5668\u4ef6\u4e0d\u517c\u5bb9\u6545\u969c",
      "enLogName": "NO.1 PE PE Control Board Software Version Mismatch"
    },
    {
      "alarmCode": "4166",
      "logName": "1\u53f7PE \u603b\u6bcd\u7ebf\u6b20\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE Undervoltage Slow Inspection Failure of Bus"
    },
    {
      "alarmCode": "4167",
      "logName": "1\u53f7PE BuckBoost\u9650\u6d41\u8d85\u65f6\u6545\u969c",
      "enLogName": "NO.1 PE Current Limiting Overtime Failure of BuckBoost"
    },
    {
      "alarmCode": "4168",
      "logName": "1\u53f7PE BMS-SOP\u9650\u529f\u7387\u4fdd\u62a4",
      "enLogName": "NO.1 PE Power Limiting Protection of BMS-SOP"
    },
    {
      "alarmCode": "4169",
      "logName": "1\u53f7PE DC\u4fa7\u6bcd\u7ebf\u51b2\u51fb\u8fc7\u538b\u6545\u969c",
      "enLogName": "NO.1 PE DC side bus surge overvoltage fault"
    },
    {
      "alarmCode": "4171",
      "logName": "1\u53f7PE LLC \u6545\u969c\u7efc\u5408",
      "enLogName": "NO.1 PE LLC Fault Synthesis"
    },
    {
      "alarmCode": "4172",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u8fc7\u538b\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE LLC Bus Overvoltage Quick Detection Fault"
    },
    {
      "alarmCode": "4173",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u8fc7\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE LLC Bus Overvoltage Slow Detection Fault"
    },
    {
      "alarmCode": "4174",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u4f4e\u538b\u5feb\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE LLC Bus Low Voltage Quick Detection Fault"
    },
    {
      "alarmCode": "4175",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u4f4e\u538b\u6162\u68c0\u6545\u969c",
      "enLogName": "NO.1 PE LLC Bus Low Voltage Slow Detection Fault"
    },
    {
      "alarmCode": "4176",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u6b63\u5411\u7f13\u51b2\u5b8c\u6210",
      "enLogName": "NO.1 PE LLC Bus Positive Buffering Completed"
    },
    {
      "alarmCode": "4177",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf Buck \u7f13\u51b2\u5b8c\u6210",
      "enLogName": "NO.1 PE LLC Bus Buck Buffer Completed"
    },
    {
      "alarmCode": "4178",
      "logName": "1\u53f7PE LLC \u786c\u4ef6\u8fc7\u6d41\u6545\u969c",
      "enLogName": "NO.1 PE Hardware Overcurrent Failure of LLC Converter"
    },
    {
      "alarmCode": "4179",
      "logName": "1\u53f7PE LLC \u6bcd\u7ebf\u9ad8\u538b\u9a71\u52a8\u5c01\u9501",
      "enLogName": "NO.1 PE High Bus Voltage"
    },
    {
      "alarmCode": "417A",
      "logName": "1\u53f7PE LLC \u7535\u6c60\u9ad8\u538b\u9a71\u52a8\u5c01\u9501",
      "enLogName": "NO.1 PE Battery Pack Voltage Too High"
    },
    {
      "alarmCode": "4181",
      "logName": "1\u53f7PE \u7535\u6c60\u8fc7\u538b\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overvoltage Protection of Battery"
    },
    {
      "alarmCode": "4182",
      "logName": "1\u53f7PE \u7535\u6c60\u4f4e\u538b\u4fdd\u62a4",
      "enLogName": "NO.1 PE Undervoltage Protection of Battery"
    },
    {
      "alarmCode": "4183",
      "logName": "1\u53f7PE \u7535\u6c60\u8fc7\u538b\u544a\u8b66",
      "enLogName": "NO.1 PE Overvoltage Warning of Battery"
    },
    {
      "alarmCode": "4184",
      "logName": "1\u53f7PE \u7535\u6c60\u4f4e\u538b\u544a\u8b66",
      "enLogName": "NO.1 PE Undervoltage Warning of Battery"
    },
    {
      "alarmCode": "4185",
      "logName": "1\u53f7PE \u7535\u6c60\u672a\u63a5",
      "enLogName": "NO.1 PE Battery Unconnected"
    },
    {
      "alarmCode": "4192",
      "logName": "1\u53f7PE DC \u53d8\u6362\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overtemperature Protection of DC Convertor"
    },
    {
      "alarmCode": "4193",
      "logName": "1\u53f7PE \u8f85\u6e90 12V \u5f02\u5e38\u4fdd\u62a4",
      "enLogName": "NO.1 PE 12V Abnornal Protection of APS"
    },
    {
      "alarmCode": "4194",
      "logName": "1\u53f7PE BMS \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "NO.1 PE Communication Abnormal of BMS"
    },
    {
      "alarmCode": "4195",
      "logName": "1\u53f7PE FPGA \u901a\u4fe1\u5f02\u5e38",
      "enLogName": "NO.1 PE PE Control Board Failure"
    },
    {
      "alarmCode": "4196",
      "logName": "1\u53f7PE \u9006\u53d8\u6545\u969c",
      "enLogName": "NO.1 PE Inverter Fault"
    },
    {
      "alarmCode": "4197",
      "logName": "1\u53f7PE \u672c\u5730\u5173\u673a",
      "enLogName": "NO.1 PE aPower Shut down Manually"
    },
    {
      "alarmCode": "4198",
      "logName": "1\u53f7PE \u4e09\u6b21\u9501\u5b9a\u6545\u969c",
      "enLogName": "NO.1 PE Inverter Locked(Three Faults)"
    },
    {
      "alarmCode": "419A",
      "logName": "1\u53f7PE \u7cfb\u7edfEPO\u6545\u969c",
      "enLogName": "NO.1 PE System EPO failure"
    },
    {
      "alarmCode": "419B",
      "logName": "1\u53f7PE BMS\u7efc\u5408\u6545\u969c",
      "enLogName": "NO.1 PE BMS comprehensive failure"
    },
    {
      "alarmCode": "419C",
      "logName": "1\u53f7PE \u6a21\u5757\u5185\u90e8\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "NO.1 PE Overtemperature Protection of Inner Module"
    },
    {
      "alarmCode": "419D",
      "logName": "1\u53f7PE PE\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf\u6545\u969c",
      "enLogName": "NO.1 PE PE Temperature Sensor Disconnection Fault"
    },
    {
      "alarmCode": "419E",
      "logName": "1\u53f7PE DC\u4fa7V\u7248\u672c\u4e0d\u517c\u5bb9\u6545\u969c",
      "enLogName": "NO.1 PE V version incompatibility fault on the DC side"
    },
    {
      "alarmCode": "6102",
      "logName": "1\u53f7BMS SOC\u8fc7\u4f4e",
      "enLogName": "NO.1 BMS Low SOC"
    },
    {
      "alarmCode": "6103",
      "logName": "1\u53f7BMS \u5145\u7535\u8fc7\u6d41",
      "enLogName": "NO.1 BMS Charge Overcurrent"
    },
    {
      "alarmCode": "6104",
      "logName": "1\u53f7BMS \u5145\u7535\u51b2\u51fb\u7535\u6d41\u4fdd\u62a4\uff08\u786c\u4ef6\u89e6\u53d1\u9608\u503c\uff09",
      "enLogName": "NO.1 BMS Charge Overcurrent\uff08Hardware Trigger\uff09"
    },
    {
      "alarmCode": "6105",
      "logName": "1\u53f7BMS \u98ce\u673a\u5145\u7535\u8fc7\u6d41(\u786c\u4ef6\u89e6\u53d1\u9608\u503c)",
      "enLogName": "NO.1 BMS Wind Power Charge over Current(Hardware Trigger)"
    },
    {
      "alarmCode": "6106",
      "logName": "1\u53f7BMS \u653e\u7535\u8fc7\u6d41",
      "enLogName": "NO.1 BMS Discharge Overcurrent"
    },
    {
      "alarmCode": "6107",
      "logName": "1\u53f7BMS \u653e\u7535\u77ed\u8def\u8fc7\u6d41\u4fdd\u62a4\uff08\u786c\u4ef6\u89e6\u53d1\u9608\u503c\uff09",
      "enLogName": "NO.1 BMS Discharge Overcurrent\uff08Hardware Trigger\uff09"
    },
    {
      "alarmCode": "6108",
      "logName": "1\u53f7BMS \u98ce\u673a\u653e\u7535\u8fc7\u6d41(\u786c\u4ef6\u89e6\u53d1\u9608\u503c)",
      "enLogName": "NO.1 BMS Wind Power Discharge over Current(Hardware Trigger)"
    },
    {
      "alarmCode": "610A",
      "logName": "1\u53f7BMS \u5355\u4f53\u6b20\u538b",
      "enLogName": "NO.1 BMS Cell Under Voltage"
    },
    {
      "alarmCode": "610B",
      "logName": "1\u53f7BMS \u7535\u6c60\u7ec4\u8fc7\u538b",
      "enLogName": "NO.1 BMS Battery Pack Over Voltage"
    },
    {
      "alarmCode": "610C",
      "logName": "1\u53f7BMS \u7535\u6c60\u7ec4\u6b20\u538b",
      "enLogName": "NO.1 BMS Battery Pack Under Voltage"
    },
    {
      "alarmCode": "610D",
      "logName": "1\u53f7BMS \u5145\u7535\u9ad8\u6e29",
      "enLogName": "NO.1 BMS Charge Over Temperature"
    },
    {
      "alarmCode": "610E",
      "logName": "1\u53f7BMS \u5145\u7535\u4f4e\u6e29",
      "enLogName": "NO.1 BMS Charge Under Temperature"
    },
    {
      "alarmCode": "610F",
      "logName": "1\u53f7BMS \u975e\u5145\u9ad8\u6e29",
      "enLogName": "NO.1 BMS Discharge Over Temperature"
    },
    {
      "alarmCode": "6110",
      "logName": "1\u53f7BMS \u975e\u5145\u4f4e\u6e29",
      "enLogName": "NO.1 BMS Discharge Under Temperature"
    },
    {
      "alarmCode": "6111",
      "logName": "1\u53f7BMS \u73af\u5883\u9ad8\u6e29",
      "enLogName": "NO.1 BMS Environment Over Temperature"
    },
    {
      "alarmCode": "6112",
      "logName": "1\u53f7BMS LED\u672a\u63a5",
      "enLogName": "NO.1 BMS LED not connected"
    },
    {
      "alarmCode": "6113",
      "logName": "1\u53f7BMS MOS \u9ad8\u6e29",
      "enLogName": "NO.1 BMS Mosfet Over Temperature"
    },
    {
      "alarmCode": "6114",
      "logName": "1\u53f7BMS \u5355\u4f53\u538b\u5dee\u5927",
      "enLogName": "NO.1 BMS Excessive Voltage Difference"
    },
    {
      "alarmCode": "6115",
      "logName": "1\u53f7BMS \u5355\u4f53\u6e29\u5dee\u5927",
      "enLogName": "NO.1 BMS Excessive Temperature Difference"
    },
    {
      "alarmCode": "6116",
      "logName": "1\u53f7BMS \u5355\u4f53\u7535\u538b\u65ad\u7ebf",
      "enLogName": "NO.1 BMS Cell Voltage Break Line"
    },
    {
      "alarmCode": "6117",
      "logName": "1\u53f7BMS \u5355\u4f53\u6e29\u5ea6\u65ad\u7ebf/\u77ed\u8def",
      "enLogName": "NO.1 BMS Cell Temperature Break Line"
    },
    {
      "alarmCode": "6118",
      "logName": "1\u53f7BMS \u9501\u5b9a\u6545\u969c",
      "enLogName": "NO.1 BMS Lock Fault"
    },
    {
      "alarmCode": "6119",
      "logName": "1\u53f7BMS \u786c\u4ef6\u81ea\u68c0\u6545\u969c",
      "enLogName": "NO.1 BMS Hardware Fault"
    },
    {
      "alarmCode": "611A",
      "logName": "1\u53f7BMS \u603b\u538b\u5f02\u5e38",
      "enLogName": "NO.1 BMS Pack Voltage Abnormal"
    },
    {
      "alarmCode": "611B",
      "logName": "1\u53f7BMS \u9884\u5145\u5931\u8d25",
      "enLogName": "NO.1 BMS Precharge Failed"
    },
    {
      "alarmCode": "611C",
      "logName": "1\u53f7BMS MOS \u7ba1\u77ed\u8def",
      "enLogName": "NO.1 BMS Mosfet Short Circuit"
    },
    {
      "alarmCode": "611D",
      "logName": "1\u53f7BMS \u8865\u7535\u53e3\u8fc7\u6d41",
      "enLogName": "NO.1 BMS Supply Port Overcurrent"
    },
    {
      "alarmCode": "611F",
      "logName": "1\u53f7BMS PE \u7aef\u53cd\u538b",
      "enLogName": "NO.1 BMS Pe Port Reverse"
    },
    {
      "alarmCode": "6121",
      "logName": "1\u53f7BMS \u76f4\u6d41\u7edd\u7f18\u6f0f\u7535\u4fdd\u62a4",
      "enLogName": "NO.1 BMS Electric Leakage"
    },
    {
      "alarmCode": "6122",
      "logName": "1\u53f7BMS \u8fc7\u5145\u7535\u5931\u6548\u4fdd\u62a4",
      "enLogName": "NO.1 BMS Cell Ultra Under Voltage"
    },
    {
      "alarmCode": "6123",
      "logName": "1\u53f7BMS \u8fc7\u653e\u7535\u5931\u6548\u4fdd\u62a4",
      "enLogName": "NO.1 BMS Over-discharge failure protection"
    },
    {
      "alarmCode": "6124",
      "logName": "1\u53f7BMS PE\u4e0eBMS\u901a\u8baf\u5f02\u5e38",
      "enLogName": "NO.1 BMS Abnormal Communication Between PE and BMS"
    },
    {
      "alarmCode": "6125",
      "logName": "1\u53f7BMS \u4e0eAFE\u901a\u4fe1\u6545\u969c",
      "enLogName": "NO.1 BMS BMS Control Board Hardware Failure"
    },
    {
      "alarmCode": "612A",
      "logName": "1\u53f7BMS SOC\u8bef\u5dee\u8fc7\u5927",
      "enLogName": "NO.1 BMS Large SOC Deviation"
    },
    {
      "alarmCode": "612B",
      "logName": "1\u53f7BMS SOH \u8fc7\u4f4e",
      "enLogName": "NO.1 BMS Low SOH"
    },
    {
      "alarmCode": "612C",
      "logName": "1\u53f7BMS \u6e29\u5ea6\u5f02\u5e38\u4fdd\u62a4",
      "enLogName": "NO.1 BMS Abnormal Temperature Protection"
    },
    {
      "alarmCode": "612D",
      "logName": "1\u53f7BMS AFE_SPI\u6545\u969c",
      "enLogName": "NO.1 BMS BMS Control Board Hardware Failure"
    },
    {
      "alarmCode": "612F",
      "logName": "1\u53f7BMS \u52a0\u70ed\u819c\u6e29\u5ea6\u65ad\u7ebf\u6545\u969c",
      "enLogName": "NO.1 BMS Heating Film Temperature Disconnection Fault"
    },
    {
      "alarmCode": "3016",
      "logName": "\u5e02\u7535\u5207\u6362\u5f02\u5e38",
      "enLogName": "Abnormal switching of utility power"
    },
    {
      "alarmCode": "101D",
      "logName": "\u4e09\u76f8\u5149\u4f0f\u7535\u8868\u901a\u8baf\u6545\u969c",
      "enLogName": "Three-phase PV meter communication failure"
    },
    {
      "alarmCode": "101E",
      "logName": "\u4e09\u76f8\u5e02\u7535\u7535\u8868\u901a\u8baf\u6545\u969c",
      "enLogName": "Three-phase mains meter communication failure"
    },
    {
      "alarmCode": "6132",
      "logName": "1\u53f7BMS BMS\u5730\u5740\u51b2\u7a81\u68c0\u6d4b\u6545\u969c",
      "enLogName": "NO.1 BMS BMS Address Conflict Fault"
    },
    {
      "alarmCode": "5101",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u8fc7\u538b",
      "enLogName": "NO.1 MPPT Overvoltage on PV Branch 1"
    },
    {
      "alarmCode": "5104",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u957f\u65f6\u95f4\u9010\u6ce2\u9650\u6d41",
      "enLogName": "NO.1 MPPT PV branch 1 long time wave by wave current limiting"
    },
    {
      "alarmCode": "5105",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u9010\u6ce2\u9650\u6d41\u9501\u5b9a",
      "enLogName": "NO.1 MPPT PV branch 1 is locked by wave current limiting"
    },
    {
      "alarmCode": "5106",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u53cd\u63a5\u6545\u969c",
      "enLogName": "NO.1 MPPT The reverse connection of PV branch 1 is faulty"
    },
    {
      "alarmCode": "5107",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u7535\u6d41\u53cd\u5411",
      "enLogName": "NO.1 MPPT PV branch 1 current reverse"
    },
    {
      "alarmCode": "5108",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u7535\u6d41\u96f6\u6f02\u8fc7\u5927",
      "enLogName": "NO.1 MPPT PV branch 1 current zero drift is too large"
    },
    {
      "alarmCode": "5109",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u7684RSD\u65ad\u5f00\u5931\u8d25",
      "enLogName": "NO.1 MPPT The RSD of PV branch 1 fails to be disconnected"
    },
    {
      "alarmCode": "510B",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u7684AFCI\u81ea\u68c0\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The AFCI self-test of PV branch 1 is abnormal"
    },
    {
      "alarmCode": "5111",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u8fc7\u538b",
      "enLogName": "NO.1 MPPT PV branch 2 overvoltage"
    },
    {
      "alarmCode": "5113",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u8fc7\u6d41",
      "enLogName": "NO.1 MPPT Solar branch 2 overcurrent"
    },
    {
      "alarmCode": "5114",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u957f\u65f6\u95f4\u9010\u6ce2\u9650\u6d41",
      "enLogName": "NO.1 MPPT PV branch 2 long time wave by wave current limiting"
    },
    {
      "alarmCode": "5115",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u9010\u6ce2\u9650\u6d41\u9501\u5b9a",
      "enLogName": "NO.1 MPPT PV branch 2 is locked by wave current limiting"
    },
    {
      "alarmCode": "5116",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u53cd\u63a5\u6545\u969c",
      "enLogName": "NO.1 MPPT The reverse connection of PV branch 2 is faulty"
    },
    {
      "alarmCode": "5117",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u7535\u6d41\u53cd\u5411",
      "enLogName": "NO.1 MPPT PV branch 2 current reverse"
    },
    {
      "alarmCode": "5118",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u7535\u6d41\u96f6\u6f02\u8fc7\u5927",
      "enLogName": "NO.1 MPPT PV branch 2 current zero drift is too large"
    },
    {
      "alarmCode": "5119",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u7684RSD\u65ad\u5f00\u5931\u8d25",
      "enLogName": "NO.1 MPPT The RSD of PV branch 2 fails to be disconnected"
    },
    {
      "alarmCode": "511B",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u7684AFCI\u81ea\u68c0\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The AFCI self-test of PV branch 2 is abnormal"
    },
    {
      "alarmCode": "5121",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u8fc7\u538b",
      "enLogName": "NO.1 MPPT PV branch 3 overvoltage"
    },
    {
      "alarmCode": "5123",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u8fc7\u6d41",
      "enLogName": "NO.1 MPPT Solar branch 3 overcurrent"
    },
    {
      "alarmCode": "5124",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u957f\u65f6\u95f4\u9010\u6ce2\u9650\u6d41",
      "enLogName": "NO.1 MPPT PV branch 3 long time wave by wave current limiting"
    },
    {
      "alarmCode": "5125",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u9010\u6ce2\u9650\u6d41\u9501\u5b9a",
      "enLogName": "NO.1 MPPT PV branch 3 is locked by wave current limiting"
    },
    {
      "alarmCode": "5126",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u53cd\u63a5\u6545\u969c",
      "enLogName": "NO.1 MPPT The reverse connection of PV branch 3 is faulty"
    },
    {
      "alarmCode": "5127",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u7535\u6d41\u53cd\u5411",
      "enLogName": "NO.1 MPPT PV branch 3 current reverse"
    },
    {
      "alarmCode": "5128",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u7535\u6d41\u96f6\u6f02\u8fc7\u5927",
      "enLogName": "NO.1 MPPT PV branch 3 current zero drift is too large"
    },
    {
      "alarmCode": "5129",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u7684RSD\u65ad\u5f00\u5931\u8d25",
      "enLogName": "NO.1 MPPT The RSD of PV branch 3 fails to be disconnected"
    },
    {
      "alarmCode": "512B",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u7684AFCI\u81ea\u68c0\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The AFCI self-test of PV branch 3 is abnormal"
    },
    {
      "alarmCode": "5131",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u8fc7\u538b",
      "enLogName": "NO.1 MPPT PV branch 4 overvoltage"
    },
    {
      "alarmCode": "5133",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u8fc7\u6d41",
      "enLogName": "NO.1 MPPT Solar branch 4 overcurrent"
    },
    {
      "alarmCode": "5134",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u957f\u65f6\u95f4\u9010\u6ce2\u9650\u6d41",
      "enLogName": "NO.1 MPPT PV branch 4 long time wave by wave current limiting"
    },
    {
      "alarmCode": "5135",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u9010\u6ce2\u9650\u6d41\u9501\u5b9a",
      "enLogName": "NO.1 MPPT PV branch 4 is locked by wave current limiting"
    },
    {
      "alarmCode": "5136",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u53cd\u63a5\u6545\u969c",
      "enLogName": "NO.1 MPPT The reverse connection of PV branch 4 is faulty"
    },
    {
      "alarmCode": "5137",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u7535\u6d41\u53cd\u5411",
      "enLogName": "NO.1 MPPT PV branch 4 current reverse"
    },
    {
      "alarmCode": "5138",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u7535\u6d41\u96f6\u6f02\u8fc7\u5927",
      "enLogName": "NO.1 MPPT PV branch 4 current zero drift is too large"
    },
    {
      "alarmCode": "5139",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u7684RSD\u65ad\u5f00\u5931\u8d25",
      "enLogName": "NO.1 MPPT The RSD of PV branch 4 fails to be disconnected"
    },
    {
      "alarmCode": "513B",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u7684AFCI\u81ea\u68c0\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The AFCI self-test of PV branch 4 is abnormal"
    },
    {
      "alarmCode": "5141",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u529f\u7387\u8d85\u9650",
      "enLogName": "NO.1 MPPT The PV power exceeds the limit"
    },
    {
      "alarmCode": "5143",
      "logName": "1\u53f7MPPT \u7edd\u7f18\u963b\u6297\u8fc7\u4f4e\u6545\u969c",
      "enLogName": "NO.1 MPPT The insulation impedance is too low"
    },
    {
      "alarmCode": "5144",
      "logName": "1\u53f7MPPT \u62c9\u5f27\u9501\u5b9a\u6545\u969c",
      "enLogName": "NO.1 MPPT The arc lock fault occurs"
    },
    {
      "alarmCode": "5151",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u9ad8\u538b\u5c01\u6ce2",
      "enLogName": "NO.1 MPPT DC busbar high voltage sealing wave"
    },
    {
      "alarmCode": "5152",
      "logName": "1\u53f7MPPT PE\u4fa7\u6bcd\u7ebf\u8fc7\u538b",
      "enLogName": "NO.1 MPPT PE side bus overvoltage"
    },
    {
      "alarmCode": "5153",
      "logName": "1\u53f7MPPT PE\u4fa7\u6bcd\u7ebf\u6b20\u538b",
      "enLogName": "NO.1 MPPT PE side bus undervoltage"
    },
    {
      "alarmCode": "5154",
      "logName": "1\u53f7MPPT PV\u4fa7\u6bcd\u7ebf\u8fc7\u538b",
      "enLogName": "NO.1 MPPT The bus on the PV side is overvoltage"
    },
    {
      "alarmCode": "5155",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u7535\u6d41\u96f6\u6f02\u8fc7\u5927",
      "enLogName": "NO.1 MPPT DC bus current zero drift is too large"
    },
    {
      "alarmCode": "5156",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u9884\u5145\u6545\u969c",
      "enLogName": "NO.1 MPPT The DC bus precharge is faulty"
    },
    {
      "alarmCode": "5157",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u8fc7\u6d41",
      "enLogName": "NO.1 MPPT DC bus overcurrent"
    },
    {
      "alarmCode": "5158",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u7ee7\u7535\u5668\u5f00\u8def",
      "enLogName": "NO.1 MPPT DC bus relay is open"
    },
    {
      "alarmCode": "5159",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u7ee7\u7535\u5668\u77ed\u8def",
      "enLogName": "NO.1 MPPT DC bus relay short circuit"
    },
    {
      "alarmCode": "515A",
      "logName": "1\u53f7MPPT \u76f4\u6d41\u6bcd\u7ebf\u7ee7\u7535\u5668\u81ea\u68c0\u6545\u969c",
      "enLogName": "NO.1 MPPT DC bus relay self-test fault"
    },
    {
      "alarmCode": "5161",
      "logName": "1\u53f7MPPT \u8154\u6e29\u8fc7\u9ad8",
      "enLogName": "NO.1 MPPT Cavity overtemperature"
    },
    {
      "alarmCode": "5162",
      "logName": "1\u53f7MPPT \u8154\u6e29\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf",
      "enLogName": "NO.1 MPPT Cavity temperature The temperature sensor is disconnected"
    },
    {
      "alarmCode": "5163",
      "logName": "1\u53f7MPPT \u6563\u70ed\u56681\u7684\u6e29\u5ea6\u8fc7\u9ad8",
      "enLogName": "NO.1 MPPT The temperature of heat sink 1 is too high"
    },
    {
      "alarmCode": "5164",
      "logName": "1\u53f7MPPT \u6563\u70ed\u56681\u7684\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf",
      "enLogName": "NO.1 MPPT The temperature sensor of radiator 1 is disconnected"
    },
    {
      "alarmCode": "5165",
      "logName": "1\u53f7MPPT \u6563\u70ed\u56682\u7684\u6e29\u5ea6\u8fc7\u9ad8",
      "enLogName": "NO.1 MPPT The temperature of heat sink 2 is too high"
    },
    {
      "alarmCode": "5166",
      "logName": "1\u53f7MPPT \u6563\u70ed\u56682\u7684\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf",
      "enLogName": "NO.1 MPPT The temperature sensor of radiator 2 is disconnected"
    },
    {
      "alarmCode": "5171",
      "logName": "1\u53f7MPPT 12V\u8f85\u6e90\u6b20\u538b",
      "enLogName": "NO.1 MPPT 12V secondary source undervoltage"
    },
    {
      "alarmCode": "5172",
      "logName": "1\u53f7MPPT \u786c\u4ef6\u7248\u672c\u53f7\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The hardware version is abnormal"
    },
    {
      "alarmCode": "5173",
      "logName": "1\u53f7MPPT \u4e0eAFCI\u7684SCI\u5f02\u5e38",
      "enLogName": "NO.1 MPPT SCI abnormalities with AFCI"
    },
    {
      "alarmCode": "5174",
      "logName": "1\u53f7MPPT \u4e0ePE\u7684SCI\u5f02\u5e38",
      "enLogName": "NO.1 MPPT SCI abnormalities with PE"
    },
    {
      "alarmCode": "5175",
      "logName": "1\u53f7MPPT \u4e0ePE\u7684SCI\u534f\u8bae\u4e0d\u5339\u914d",
      "enLogName": "NO.1 MPPT The SCI protocol does not match that of the PE"
    },
    {
      "alarmCode": "5176",
      "logName": "1\u53f7MPPT \u4f4e\u901fCAN\u901a\u8baf\u5f02\u5e38",
      "enLogName": "NO.1 MPPT The low-speed CAN communication is abnormal"
    },
    {
      "alarmCode": "5177",
      "logName": "1\u53f7MPPT \u4f4e\u901fCAN\u534f\u8bae\u4e0d\u5339\u914d",
      "enLogName": "NO.1 MPPT The low-speed CAN protocol does not match"
    },
    {
      "alarmCode": "5178",
      "logName": "1\u53f7MPPT PE-MPPT\u5feb\u901f\u4fdd\u62a4",
      "enLogName": "NO.1 MPPT PE-MPPT fast protection"
    },
    {
      "alarmCode": "5179",
      "logName": "1\u53f7MPPT \u5916\u6269Flash\u53c2\u6570\u5b58\u50a8\u533a\u5931\u6548",
      "enLogName": "NO.1 MPPT The expanded Flash parameter store fails"
    },
    {
      "alarmCode": "517A",
      "logName": "1\u53f7MPPT \u4e0ePE\u5730\u5740\u4e0d\u5339\u914d",
      "enLogName": "NO.1 MPPT The PE address does not match"
    },
    {
      "alarmCode": "517B",
      "logName": "1\u53f7MPPT CLA\u5fc3\u8df3\u6545\u969c",
      "enLogName": "NO.1 MPPT The CLA heartbeat is faulty"
    },
    {
      "alarmCode": "5147",
      "logName": "1\u53f7MPPT RSD\u7535\u538b\u5f02\u5e38",
      "enLogName": "NO.1 MPPT RSD voltage fault"
    },
    {
      "alarmCode": "5145",
      "logName": "1\u53f7MPPT AFCI\u81ea\u68c0\u5f02\u5e38",
      "enLogName": "NO.1 MPPT AFCI selfcheck fault"
    },
    {
      "alarmCode": "513C",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def4\u8fc7\u538b2\u7ea7",
      "enLogName": "NO.1 MPPT PV branch 4 overvoltage L2"
    },
    {
      "alarmCode": "512C",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def3\u8fc7\u538b2\u7ea7",
      "enLogName": "NO.1 MPPT PV branch 3 overvoltage L2"
    },
    {
      "alarmCode": "511C",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def2\u8fc7\u538b2\u7ea7",
      "enLogName": "NO.1 MPPT PV branch 2 overvoltage L2"
    },
    {
      "alarmCode": "510C",
      "logName": "1\u53f7MPPT \u5149\u4f0f\u652f\u8def1\u8fc7\u538b2\u7ea7",
      "enLogName": "NO.1 MPPT PV branch 1 overvoltage L2"
    },
    {
      "alarmCode": "41E2",
      "logName": "1\u53f7PE PE\u5411\u6cb9\u673a\u653e\u7535\u4fdd\u62a4\u6545\u969c",
      "enLogName": "NO.1 PE PE discharge protection fault to oil engine"
    },
    {
      "alarmCode": "41E3",
      "logName": "1\u53f7PE PE\u548cMPPT\u7684\u901a\u4fe1\u534f\u8bae\u7248\u672c\u4e0d\u5339\u914d",
      "enLogName": "NO.1 PE The communication protocol versions of PE and MPPT do not match"
    },
    {
      "alarmCode": "41E4",
      "logName": "1\u53f7PE PE\u548cMPPT\u7684SCI\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "NO.1 PE Abnormal SCI communication between PE and MPPT"
    },
    {
      "alarmCode": "41F1",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u7a81\u53d830mA\u8fc7\u5927\u6545\u969c",
      "enLogName": "NO.1 PE Leakage current sudden change of 30mA, excessive fault"
    },
    {
      "alarmCode": "41F2",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u7a81\u53d860mA\u8fc7\u5927\u6545\u969c",
      "enLogName": "NO.1 PE Leakage current sudden change of 60mA, excessive fault"
    },
    {
      "alarmCode": "41F3",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u7a81\u53d8150mA\u8fc7\u5927\u6545\u969c",
      "enLogName": "NO.1 PE Leakage current sudden change of 150mA, excessive fault"
    },
    {
      "alarmCode": "41F4",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u6301\u7eed300mA\u8fc7\u5927\u6545\u969c",
      "enLogName": "NO.1 PE Continuous leakage current of 300mA, excessive fault"
    },
    {
      "alarmCode": "41F5",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u81ea\u68c0\u5931\u8d25",
      "enLogName": "NO.1 PE Leakage current self-test failed"
    },
    {
      "alarmCode": "41F6",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u9501\u5b9a\u6545\u969c",
      "enLogName": "NO.1 PE Multiple sudden changes in leakage current locking"
    },
    {
      "alarmCode": "41E0",
      "logName": "1\u53f7PE PE\u6545\u969c\u5f55\u6ce2\u529f\u80fd\u5f02\u5e38\u5173\u95ed",
      "enLogName": "NO.1 PE PE fault recording function abnormal shutdown"
    },
    {
      "alarmCode": "1032",
      "logName": "\u672a\u68c0\u6d4b\u5230\u5149\u4f0f\u7535\u6d41",
      "enLogName": "No PV Current Detected"
    },
    {
      "alarmCode": "1033",
      "logName": "apbox1\u5149\u4f0fCT\u65ad\u5f00",
      "enLogName": "apbox1 solar ct unclamped"
    },
    {
      "alarmCode": "1034",
      "logName": "apbox2\u5149\u4f0fCT\u65ad\u5f00",
      "enLogName": "apbox2 solar Ct unclamped"
    },
    {
      "alarmCode": "1035",
      "logName": "NEM\u5149\u4f0f\u7535\u8868CT\u65ad\u5f00",
      "enLogName": "second solar meter CT unclamped"
    },
    {
      "alarmCode": "1036",
      "logName": "meterKit\u7535\u8868CT\u65ad\u5f00",
      "enLogName": "meterKit CT unclamped"
    },
    {
      "alarmCode": "1037",
      "logName": "\u5e02\u7535\u7535\u8868CT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of grid CT is inaccurate"
    },
    {
      "alarmCode": "1038",
      "logName": "\u8fd1\u7aef\u5149\u4f0fCT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of agatePv CT is inaccurate"
    },
    {
      "alarmCode": "1039",
      "logName": "apbox1\u5149\u4f0fCT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of apbox1 CT is inaccurate"
    },
    {
      "alarmCode": "103A",
      "logName": "apbox2\u5149\u4f0fCT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of apbox2 CT is inaccurate"
    },
    {
      "alarmCode": "103B",
      "logName": "NEM\u5149\u4f0f\u7535\u8868CT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of NEM solar CT is inaccurate"
    },
    {
      "alarmCode": "103C",
      "logName": "meterKit\u7535\u8868CT\u6d4b\u91cf\u4e0d\u51c6",
      "enLogName": "measurement of meterKit CT is inaccurate"
    },
    {
      "alarmCode": "2108",
      "logName": "\u7f51\u5173\u5730\u5740\u51b2\u7a81",
      "enLogName": "Gateway IP conflict"
    },
    {
      "alarmCode": "41E5",
      "logName": "1\u53f7PE aPower\uff08\u975e\u5e38\u89c4\u63a5\u7ebf\uff09\u9ed1\u542f\u52a8\u5173\u673a",
      "enLogName": "NO.1 PE black start shutdown"
    },
    {
      "alarmCode": "41E6",
      "logName": "1\u53f7PE \u9010\u6ce2\u9650\u6d41\u8fc7\u8f7d\u6545\u969c",
      "enLogName": "NO.1 PE Wave-by-wave current limiting overload fault"
    },
    {
      "alarmCode": "303E",
      "logName": "24V\u6389\u7535\u68c0\u6d4b",
      "enLogName": "24V power failure detection"
    },
    {
      "alarmCode": "303F",
      "logName": "MSA\u81ea\u52a8\u8bc6\u522b\u9519\u8bef",
      "enLogName": "MSA automatic recognition error"
    },
    {
      "alarmCode": "3040",
      "logName": "CND\u6025\u505c",
      "enLogName": "CND emergency stop"
    },
    {
      "alarmCode": "3041",
      "logName": "CND\u5185\u90e8\u8fc7\u6e29",
      "enLogName": "IslandDER over temperature"
    },
    {
      "alarmCode": "3042",
      "logName": "CND\u7ee7\u7535\u5668\u9a71\u52a8\u7535\u5bb9\u5bb9\u91cf\u4e0d\u8db3",
      "enLogName": "Insufficient capacitance of CND relay drive capacitor"
    },
    {
      "alarmCode": "3043",
      "logName": "CND\u9632\u96f7\u5668\u6545\u969c",
      "enLogName": "CND lightning arrester malfunction"
    },
    {
      "alarmCode": "3044",
      "logName": "EQB\u9a71\u52a8\u7535\u5bb9\u5bb9\u91cf\u4e0d\u8db3",
      "enLogName": "Insufficient EQB drive capacitor capacity"
    },
    {
      "alarmCode": "3045",
      "logName": "MSA\u7c7b\u578b\u8bbe\u7f6e\u4e0d\u5339\u914d",
      "enLogName": "MSA type settings do not match"
    },
    {
      "alarmCode": "3046",
      "logName": "RSD\u6309\u952e\u751f\u6548",
      "enLogName": "RSD Button Pushed"
    },
    {
      "alarmCode": "103D",
      "logName": "\u8fd1\u7aef\u5149\u4f0fCT\u53cd\u5411",
      "enLogName": "aGate PV CT  direction reverse"
    },
    {
      "alarmCode": "103E",
      "logName": "aPbox1 \u5149\u4f0fCT\u53cd\u5411",
      "enLogName": "aPbox1 CT direction reverse"
    },
    {
      "alarmCode": "103F",
      "logName": "aPbox2 \u5149\u4f0fCT\u53cd\u5411",
      "enLogName": "aPbox2 CT direction reverse"
    },
    {
      "alarmCode": "1040",
      "logName": "NEM\u5149\u4f0fCT\u53cd\u5411",
      "enLogName": "second solar CT direction reverse"
    },
    {
      "alarmCode": "1041",
      "logName": "meterkit \u5149\u4f0fCT\u53cd\u5411",
      "enLogName": "meterkit solar CT direction reverse"
    },
    {
      "alarmCode": "1042",
      "logName": "\u5e02\u7535\u7535\u8868CT\u76f8\u4f4d\u76f8\u53cd",
      "enLogName": "grid CT phase cross"
    },
    {
      "alarmCode": "1043",
      "logName": "\u5e02\u7535\u7535\u8868L1 CT\u65ad\u5f00",
      "enLogName": "grid meter L1 CT unclamped"
    },
    {
      "alarmCode": "1044",
      "logName": "\u5e02\u7535\u7535\u8868L2 CT\u65ad\u5f00",
      "enLogName": "grid meter L2 CT unclamped"
    },
    {
      "alarmCode": "1045",
      "logName": "\u5e02\u7535\u7535\u8868CT\u5168\u65ad\u5f00",
      "enLogName": "Grid meter CT All  unclamped"
    },
    {
      "alarmCode": "1046",
      "logName": "\u5e02\u7535\u7535\u8868L1 CT\u53cd\u5411",
      "enLogName": "grid meter L1 CT direction reverse"
    },
    {
      "alarmCode": "1047",
      "logName": "\u5e02\u7535\u7535\u8868L2 CT\u53cd\u5411",
      "enLogName": "grid meter L2 CT direction reverse"
    },
    {
      "alarmCode": "1048",
      "logName": "\u5e02\u7535\u7535\u8868CT\u5168\u53cd\u5411",
      "enLogName": "grid meter all CT  direction reverse"
    },
    {
      "alarmCode": "41c0",
      "logName": "1\u53f7PE \u7cfb\u7edf\u81ea\u68c0",
      "enLogName": "NO.1 PE system selfcheck"
    },
    {
      "alarmCode": "7101",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31A\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub A-phase overcurrent of access port 1"
    },
    {
      "alarmCode": "7102",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31B\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub B-phase overcurrent of access port 1"
    },
    {
      "alarmCode": "7103",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32A\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub A-phase overcurrent of access port 2"
    },
    {
      "alarmCode": "7104",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32B\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub B-phase overcurrent of access port 2"
    },
    {
      "alarmCode": "7105",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33A\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub A-phase overcurrent of access port 3"
    },
    {
      "alarmCode": "7106",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33B\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub B-phase overcurrent of access port 3"
    },
    {
      "alarmCode": "7107",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34A\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub A-phase overcurrent of access port 4"
    },
    {
      "alarmCode": "7108",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34B\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub B-phase overcurrent of access port 4"
    },
    {
      "alarmCode": "7109",
      "logName": "1\u53f7aHub \u5907\u7535\u4e3b\u652f\u8defA\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub A-phase overcurrent of backup power main branch"
    },
    {
      "alarmCode": "710A",
      "logName": "1\u53f7aHub \u5907\u7535\u4e3b\u652f\u8defB\u76f8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub B-phase overcurrent of backup power main branch"
    },
    {
      "alarmCode": "7112",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31 B\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally open fault of access port 1"
    },
    {
      "alarmCode": "7111",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31 A\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally open fault of access port 1"
    },
    {
      "alarmCode": "7113",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32 A\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally open fault of access port 2"
    },
    {
      "alarmCode": "7114",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32 B\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally open fault of access port 2"
    },
    {
      "alarmCode": "7115",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33 A\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally open fault of access port 3"
    },
    {
      "alarmCode": "7116",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33 B\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally open fault of access port 3"
    },
    {
      "alarmCode": "7117",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 A\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally open fault of access port 4"
    },
    {
      "alarmCode": "7118",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 B\u76f8\u7ee7\u7535\u5668\u5e38\u5f00\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally open fault of access port 4"
    },
    {
      "alarmCode": "7121",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31 A\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally closed fault of access port 1"
    },
    {
      "alarmCode": "7122",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31 B\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally closed fault of access port 1"
    },
    {
      "alarmCode": "7123",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32 A\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally closed fault of access port 2"
    },
    {
      "alarmCode": "7124",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32 B\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally closed fault of access port 2"
    },
    {
      "alarmCode": "7125",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33 A\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally closed fault of access port 3"
    },
    {
      "alarmCode": "7126",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33 B\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally closed fault of access port 3"
    },
    {
      "alarmCode": "7127",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 A\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub A-phase relay normally closed fault of access port 4"
    },
    {
      "alarmCode": "7128",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 B\u76f8\u7ee7\u7535\u5668\u5e38\u95ed\u6545\u969c",
      "enLogName": "NO.1 aHub B-phase relay normally closed fault of access port 4"
    },
    {
      "alarmCode": "7132",
      "logName": "1\u53f7aHub \u786c\u4ef6\u7248\u672c\u53f7\u5339\u914d\u9519\u8bef",
      "enLogName": "NO.1 aHub Hardware version of apbox2.0 matching error"
    },
    {
      "alarmCode": "7133",
      "logName": "1\u53f7aHub \u4e0eEMS DSP\u5fc3\u8df3\u6545\u969c",
      "enLogName": "NO.1 aHub aHub and slave DSP heartbeat failure"
    },
    {
      "alarmCode": "7134",
      "logName": "1\u53f7aHub \u4e0eEMS\u5fc3\u8df3\u6545\u969c",
      "enLogName": "NO.1 aHub heartbeat fault for apbox2.0 and EMS"
    },
    {
      "alarmCode": "7135",
      "logName": "1\u53f7aHub \u7535\u8868\u901a\u4fe1\u6545\u969c",
      "enLogName": "NO.1 aHub meter communication failure"
    },
    {
      "alarmCode": "7136",
      "logName": "1\u53f7aHub CLA\u901a\u4fe1\u6545\u969c",
      "enLogName": "NO.1 aHub CLA communication failure"
    },
    {
      "alarmCode": "7137",
      "logName": "1\u53f7aHub \u6545\u969c\u5f55\u6ce2\u529f\u80fd\u5f02\u5e38\u5173\u95ed",
      "enLogName": "NO.1 aHub fault recording function abnormal shutdown"
    },
    {
      "alarmCode": "7138",
      "logName": "1\u53f7aHub \u5916\u90e8FLASH\u5f02\u5e38\u4fdd\u62a4",
      "enLogName": "NO.1 aHub External FLASH Exception Protection"
    },
    {
      "alarmCode": "7139",
      "logName": "1\u53f7aHub \u73af\u5883\u6e29\u5ea6\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "NO.1 aHub environmental over temperature protection"
    },
    {
      "alarmCode": "713A",
      "logName": "1\u53f7aHub \u94dc\u6392\u6e29\u5ea6\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "NO.1 aHub copper bar over temperature protection"
    },
    {
      "alarmCode": "713B",
      "logName": "1\u53f7aHub \u73af\u5883\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf\u4fdd\u62a4",
      "enLogName": "NO.1 aHub Environmental temperature sensor disconnection protection"
    },
    {
      "alarmCode": "713C",
      "logName": "1\u53f7aHub \u94dc\u6392\u6e29\u5ea6\u4f20\u611f\u5668\u65ad\u7ebf\u4fdd\u62a4",
      "enLogName": "NO.1 aHub Copper bar temperature sensor disconnection protection"
    },
    {
      "alarmCode": "713E",
      "logName": "1\u53f7aHub \u5149\u4f0f\u7ee7\u7535\u5668\u5f02\u5e38\u65ad\u5f00",
      "enLogName": "NO.1 aHub PV relay abnormal disconnection"
    },
    {
      "alarmCode": "1016",
      "logName": "\u4e3b\u914d\u7535\u76d8\u7535\u6d41100%\u8d85\u9650",
      "enLogName": "Busbar overcurrent fault in the main panel"
    },
    {
      "alarmCode": "41E7",
      "logName": "1\u53f7PE MPPT\u8001\u5316\u671f\u95f4\u529f\u7387\u5f02\u5e38",
      "enLogName": "NO.1 PE Abnormal Power During MPPT Aging"
    },
    {
      "alarmCode": "41E8",
      "logName": "1\u53f7PE \u7eaf\u5e76\u673a\u7248\u672c\u4e0d\u5339\u914d",
      "enLogName": "NO.1 PE Pure Parallel Version Mismatch"
    },
    {
      "alarmCode": "41E9",
      "logName": "1\u53f7PE \u6df7\u5408\u5e76\u673a\u7248\u672c\u4e0d\u5339\u914d",
      "enLogName": "NO.1 PE Mixed Parallel Version Mismatch"
    },
    {
      "alarmCode": "710B",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33\u52304 A\u76f8\u5c40\u90e8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub Local overcurrent in phase A of access ports 3 to 4"
    },
    {
      "alarmCode": "710C",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33\u52304 B\u76f8\u5c40\u90e8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub Local overcurrent in phase B of access ports 3 to 4"
    },
    {
      "alarmCode": "710D",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32\u52303 A\u76f8\u5c40\u90e8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub Local overcurrent in phase A of access ports 2 to 3"
    },
    {
      "alarmCode": "710E",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32\u52303 B\u76f8\u5c40\u90e8\u8fc7\u6d41",
      "enLogName": "NO.1 aHub Local overcurrent in phase A of access ports 2 to 3"
    },
    {
      "alarmCode": "7140",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31  A\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase A overcurrent of access port 1 locked 5 times"
    },
    {
      "alarmCode": "7141",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e31  B\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase B overcurrent of access port 1 locked 5 times"
    },
    {
      "alarmCode": "7142",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32  A\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase A overcurrent of access port 2 locked 5 times"
    },
    {
      "alarmCode": "7143",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e32  B\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase B overcurrent of access port 2 locked 5 times"
    },
    {
      "alarmCode": "7144",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33  A\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase A overcurrent of access port 3 locked 5 times"
    },
    {
      "alarmCode": "7145",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e33  B\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase B overcurrent of access port 3 locked 5 times"
    },
    {
      "alarmCode": "7146",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34  A\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase A overcurrent of access port 4 locked 5 times"
    },
    {
      "alarmCode": "7147",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34  B\u76f8\u8fc7\u6d415\u6b21\u9501\u5b9a",
      "enLogName": "NO.1 aHub Phase B overcurrent of access port 4 locked 5 times"
    },
    {
      "alarmCode": "7150",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 A\u76f8CT\u5f00\u8def",
      "enLogName": "NO.1 aHub The A-phase CT of access port 4 is open circuit"
    },
    {
      "alarmCode": "7151",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 B\u76f8CT\u5f00\u8def",
      "enLogName": "NO.1 aHub The B-phase CT of access port 4 is open circuit"
    },
    {
      "alarmCode": "7152",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 A\u76f8CT\u77ed\u8def",
      "enLogName": "NO.1 aHub The A-phase CT of access port 4 is close circuit"
    },
    {
      "alarmCode": "7153",
      "logName": "1\u53f7aHub \u63a5\u5165\u53e34 B\u76f8CT\u77ed\u8def",
      "enLogName": "NO.1 aHub The B-phase CT of access port 4 is close circuit"
    },
    {
      "alarmCode": "2109",
      "logName": "aHub\u8fde\u7eed\u5347\u7ea7\u5931\u8d251\u6b21",
      "enLogName": "aHub_upgrade_fail1"
    },
    {
      "alarmCode": "210A",
      "logName": "aHub\u8fde\u7eed\u5347\u7ea7\u5931\u8d252\u6b21",
      "enLogName": "aHub_upgrade_fail2"
    },
    {
      "alarmCode": "210B",
      "logName": "aHub\u8fde\u7eed\u5347\u7ea7\u5931\u8d253\u6b21(\u4ee5\u4e0a)",
      "enLogName": "aHub_upgrade_fail3"
    },
    {
      "alarmCode": "3047",
      "logName": "EMS\u4e0e1\u53f7aHub\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "EMS communication with aHub 1 is abnormal"
    },
    {
      "alarmCode": "3048",
      "logName": "EMS\u4e0e2\u53f7aHub\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "EMS communication with aHub 2 is abnormal"
    },
    {
      "alarmCode": "3049",
      "logName": "EMS\u4e0e3\u53f7aHub\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "EMS communication with aHub 3 is abnormal"
    },
    {
      "alarmCode": "304A",
      "logName": "EMS\u4e0e4\u53f7aHub\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "EMS communication with aHub 4 is abnormal"
    },
    {
      "alarmCode": "304B",
      "logName": "V2L\u7535\u538b\u7c7b\u578b\u4e0eAPP\u8bbe\u7f6e\u4e0d\u5339\u914d",
      "enLogName": "V2L voltage type does not match APP settings"
    },
    {
      "alarmCode": "304C",
      "logName": "CND\u8fde\u63a5\u7ebf\u65ad\u7ebf\u6545\u969c",
      "enLogName": "CND link disconnection fault"
    },
    {
      "alarmCode": "304D",
      "logName": "EQB\u8fde\u63a5\u7ebf\u65ad\u7ebf\u6545\u969c",
      "enLogName": "EQB link disconnection fault"
    },
    {
      "alarmCode": "304E",
      "logName": "\u667a\u80fd\u8d1f\u8f7d\u7aef\u53e3\u7535\u538b\u5f02\u5e38",
      "enLogName": "Abnormal voltage at the intelligent load port"
    },
    {
      "alarmCode": "304F",
      "logName": "DIF\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "DIF communication abnormality"
    },
    {
      "alarmCode": "1300",
      "logName": "\u5e02\u7535\u7efc\u5408\u6545\u969c",
      "enLogName": "Grid Abnormal"
    },
    {
      "alarmCode": "1301",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u8fc7\u9891",
      "enLogName": "Grid Level 1 Over-Frequency Protection"
    },
    {
      "alarmCode": "1302",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u6b20\u9891",
      "enLogName": "Grid Level 1 Under-Frequency Protection"
    },
    {
      "alarmCode": "1303",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u8fc7\u9891",
      "enLogName": "Grid Level 2 Over-Frequency Protection"
    },
    {
      "alarmCode": "1304",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u6b20\u9891",
      "enLogName": "Grid Level 2 Under-Frequency Protection"
    },
    {
      "alarmCode": "1305",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u8fc7\u538b",
      "enLogName": "Grid Level 1 Overvoltage Protection"
    },
    {
      "alarmCode": "1306",
      "logName": "\u5e02\u7535\u4e00\u7ea7\u6b20\u538b",
      "enLogName": "Grid Level 1 Undervoltage Protection"
    },
    {
      "alarmCode": "1307",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u8fc7\u538b",
      "enLogName": "Grid Level 2 Overvoltage Protection"
    },
    {
      "alarmCode": "1308",
      "logName": "\u5e02\u7535\u4e8c\u7ea7\u6b20\u538b",
      "enLogName": "Grid Level 2 Undervoltage Protection"
    },
    {
      "alarmCode": "130B",
      "logName": "\u5e02\u7535\u4f4e\u901f\u77ac\u65f6\u503c\u9ad8\u538b",
      "enLogName": "Grid Fast Instantaneous High Voltage Protection"
    },
    {
      "alarmCode": "130D",
      "logName": "\u5e02\u7535\u4e09\u7ea7\u6b20\u538b",
      "enLogName": "Mains Three-Level Undervoltage Protection"
    },
    {
      "alarmCode": "130F",
      "logName": "\u9501\u76f8\u5f02\u5e38",
      "enLogName": "Grid Phase Lock Abnormal"
    },
    {
      "alarmCode": "1310",
      "logName": "\u5e02\u7535\u5feb\u68c0\u6d4b\u6545\u969c",
      "enLogName": "Grid Quick Check Fault"
    },
    {
      "alarmCode": "1311",
      "logName": "\u6709\u6548\u503c\u6ed1\u7a97\u5feb\u68c0",
      "enLogName": "Grid Envelope Detection Power Fault"
    },
    {
      "alarmCode": "1320",
      "logName": "\u5176\u4ed6\u6545\u969c\u5b57\u6c47\u603b",
      "enLogName": "Summary of other fault words"
    },
    {
      "alarmCode": "1322",
      "logName": "\u7535\u7f51\u65ad\u7ebf\u6545\u969c",
      "enLogName": "grid disconnection fault"
    },
    {
      "alarmCode": "1330",
      "logName": "CND\u5185\u90e8\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "Internal overheating of CND"
    },
    {
      "alarmCode": "1331",
      "logName": "CND\u9a71\u52a8\u7535\u8def\u5f02\u5e38",
      "enLogName": "Insufficient capacitance of CND relay drive capacitor"
    },
    {
      "alarmCode": "1332",
      "logName": "CND\u9632\u96f7\u5668\u6545\u969c",
      "enLogName": "CND lightning arrester malfunction"
    },
    {
      "alarmCode": "1333",
      "logName": "CND\u6025\u505c\u6545\u969c",
      "enLogName": "CND emergency stop"
    },
    {
      "alarmCode": "1334",
      "logName": "CND\u65ad\u7ebf\u6545\u969c",
      "enLogName": "CND disconnection fault"
    },
    {
      "alarmCode": "1344",
      "logName": "\u5907\u7535\u7535\u538b\u5f02\u5e38",
      "enLogName": "Abnormal backup voltage"
    },
    {
      "alarmCode": "1345",
      "logName": "IBGCAN\u901a\u4fe1\u5f02\u5e38",
      "enLogName": "IBG CAN communication abnormality"
    },
    {
      "alarmCode": "1347",
      "logName": "\u7535\u7f51\u4e8c\u7ea7\u8fc7\u538b\u4e09\u6b21\u9501\u6b7b\u6545\u969c",
      "enLogName": "Power grid secondary overvoltage three times locking fault"
    },
    {
      "alarmCode": "1348",
      "logName": "\u7535\u7f51\u5feb\u68c0\u516b\u6b21\u9501\u6b7b\u6545\u969c",
      "enLogName": "Eight times of power grid fast inspection locking fault"
    },
    {
      "alarmCode": "1350",
      "logName": "DIF 12V\u6389\u7535\u6545\u969c",
      "enLogName": "DIF 12V power failure"
    },
    {
      "alarmCode": "1351",
      "logName": "DIF 24V\u6389\u7535\u6545\u969c",
      "enLogName": "DIF 24V power failure"
    },
    {
      "alarmCode": "1352",
      "logName": "DIF\u677f\u4e0a\u8fc7\u6e29\u4fdd\u62a4",
      "enLogName": "Over temperature protection on DIF board"
    },
    {
      "alarmCode": "1354",
      "logName": "DIF\u4e0eEMS DSP\u901a\u8baf\u5f02\u5e38",
      "enLogName": "DIF and DSP communication abnormality"
    },
    {
      "alarmCode": "1355",
      "logName": "DIF\u4e0eEMS\u901a\u8baf\u5f02\u5e38",
      "enLogName": "DIF and EMS communication abnormality"
    },
    {
      "alarmCode": "1356",
      "logName": "DSP\u786c\u4ef6\u7248\u672c\u9519\u8bef",
      "enLogName": "DSP hardware version error"
    },
    {
      "alarmCode": "1360",
      "logName": "\u5e02\u7535\u7ee7\u7535\u5668\u5e38\u5f00",
      "enLogName": "Relay Normally Open Failure of Grid"
    },
    {
      "alarmCode": "1361",
      "logName": "\u5e02\u7535\u7ee7\u7535\u5668\u5e38\u95ed",
      "enLogName": "Relay Normally Close Failure of Grid"
    },
    {
      "alarmCode": "41EC",
      "logName": "1\u53f7PE PE\u68c0\u6d4bN\u7ebf\u4e22\u5931",
      "enLogName": "NO.1 PE PE detects N line loss"
    },
    {
      "alarmCode": "41EB",
      "logName": "1\u53f7PE \u529f\u7387\u7b49\u7ea7\u8bbe\u7f6e\u9519\u8bef",
      "enLogName": "NO.1 PE Power level setting error"
    },
    {
      "alarmCode": "1056",
      "logName": "\u53d6\u7535\u529f\u7387\u8d85\u8fc7\u9650\u5236\u503c\u5207\u9664\u8d1f\u8f7d",
      "enLogName": "Overload of the grid power input system"
    },
    {
      "alarmCode": "41F0",
      "logName": "1\u53f7PE \u6f0f\u7535\u6d41\u7a81\u53d830mA\u8fc7\u5927\u6545\u969c",
      "enLogName": "NO.1 PE Leakage current sudden change of 30mA, excessive fault"
    },
    {
      "alarmCode": "1055",
      "logName": "\u9988\u7f51\u529f\u7387\u8d85\u8fc7\u9650\u5236\u503c\u5207\u9664\u5149\u4f0f",
      "enLogName": "PV is cut off when feed\u2011in power exceeds the limit."
    },
    {
      "alarmCode": "1053",
      "logName": "\u5e02\u7535\u7aef\u53e3\u7535\u6d41\u8fc7\u8f7d",
      "enLogName": "Mains port current overload."
    },
    {
      "alarmCode": "1054",
      "logName": "\u53d1\u7535\u673a\u53e3\u5927\u8d1f\u8f7d\u76d8\u8fc7\u8f7d",
      "enLogName": "Generator port large load panel overload."
    },
    {
      "alarmCode": "5148",
      "logName": "1\u53f7MPPT \u7edd\u7f18\u963b\u6297\u68c0\u6d4b\u7535\u8def\u5f02\u5e38",
      "enLogName": "NO.1 MPPT Insulation impedance detection circuit abnormal"
    }
  ]
}
    """)
selectDeviceRunLogListResponse.total = len(selectDeviceRunLogListResponse.result)


@router.get("/selectDeviceRunLogList")
async def selectDeviceRunLogList() -> SelectDeviceRunLogListResponse:
    return selectDeviceRunLogListResponse
