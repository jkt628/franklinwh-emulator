from fastapi import APIRouter
from pydantic import BaseModel

from emulator import LoginUser, ResponseWithTotal

router = APIRouter(prefix="/site/list")


class DeviceInfo(BaseModel):
    gatewayName: str
    gatewayId: str
    completeAddress: str
    status: int = 1
    sysHdVersion: str = "103"
    agateNum: int = 1
    apowerNum: int = 0


class SiteAndDeviceInfoResult(BaseModel):
    siteId: int
    siteName: str
    completeAddress: str
    basicDeviceInfoVOList: list[DeviceInfo]


SiteAndDeviceInfoResponse = ResponseWithTotal[list[SiteAndDeviceInfoResult]]


@router.get("/siteAndDeviceInfo")
async def get_site_and_device_info(
    user: LoginUser, pageNum: int, pageSize: int, userAccount: str, userId: int
) -> SiteAndDeviceInfoResponse:
    result = [
        SiteAndDeviceInfoResult(
            siteId=site.id or 0,
            siteName=site.gateways[0].name,
            completeAddress=site.address or "",
            basicDeviceInfoVOList=[
                DeviceInfo(
                    gatewayName=gateway.name,
                    gatewayId=gateway.id,
                    completeAddress=site.address or "",
                    apowerNum=len(gateway.aPower),
                )
                for gateway in site.gateways
            ],
        )
        for site in user.sites
    ]
    return SiteAndDeviceInfoResponse(result=result, total=len(result))
