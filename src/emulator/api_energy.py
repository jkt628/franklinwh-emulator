import time

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from emulator import Response

router = APIRouter(prefix="/api-energy")


class GetFhpElectricDataResult(BaseModel):
    deviceTimeArray: list[str]
    kwhSuArray: list[float] = [0.0]
    kwhGenArray: list[float] = [0.0]
    kwhUtiInArray: list[float] = [7.365]
    kwhUtiOutArray: list[float] = [0.0]
    kwhFhpChgArray: list[float] = [6.305]
    kwhFhpDiArray: list[float] = [1.434]
    kwhLoadArray: list[float] = [2.499]
    kwhGridLoadArray: list[float] = [1.122]
    kwhSolarLoadArray: list[float] = [0.0]
    kwhFhpLoadArray: list[float] = [1.374]
    kwhGenLoadArray: list[float] = [0.0]
    gridChBatArray: list[float] = [6.241]
    batOutGridArray: list[float] = [0.0]
    genChBatArray: list[float] = [0.0]
    soChBatArray: list[float] = [0.0]
    soOutGridArray: list[float] = [0.0]
    proximalSolarWhArray: list[float] = [0]
    mpptWhArray: list[float] = [0]
    # cSpell:words Engy Arry
    mpptEngyArryArray: list[None] = [None]
    remoteSolarWhTotalArray: list[float] = [0.0]
    meterkitPvWhArray: list[float] = [0]
    secondaryPvWhArray: list[float] = [0]
    mpanPv1Wh: list[float] = [0]
    mpanPv2Wh: list[float] = [0]
    apbox20PvWh: list[None] = [None]
    kwhV2lArray: list[float] = [0]
    kwhV2lToFhpArray: list[float] = [0]
    kwhV2lToHomeArray: list[float] = [0]


GetFhpElectricDataResponse = Response[GetFhpElectricDataResult]


@router.get("/electric/getFhpElectricData")
async def getFhpElectricData(
    gatewayId: str, type: int, dayTime: str
) -> GetFhpElectricDataResponse:
    if type != 1:
        raise HTTPException(400, detail="Bad type")
    if dayTime != time.strftime("%Y-%m-%d"):
        return GetFhpElectricDataResponse(
            result=GetFhpElectricDataResult(
                deviceTimeArray=[dayTime],
                kwhSuArray=[],
                kwhGenArray=[],
                kwhUtiInArray=[],
                kwhUtiOutArray=[],
                kwhFhpChgArray=[],
                kwhFhpDiArray=[],
                kwhLoadArray=[],
                kwhGridLoadArray=[],
                kwhSolarLoadArray=[],
                kwhFhpLoadArray=[],
                kwhGenLoadArray=[],
                gridChBatArray=[],
                batOutGridArray=[],
                genChBatArray=[],
                soChBatArray=[],
                soOutGridArray=[],
                proximalSolarWhArray=[],
                mpptWhArray=[],
                mpptEngyArryArray=[],
                remoteSolarWhTotalArray=[],
                meterkitPvWhArray=[],
                secondaryPvWhArray=[],
                mpanPv1Wh=[],
                mpanPv2Wh=[],
                apbox20PvWh=[],
                kwhV2lArray=[],
                kwhV2lToFhpArray=[],
                kwhV2lToHomeArray=[],
            )
        )
    return GetFhpElectricDataResponse(
        # TODO: this is all probably supposed to align with Stats somehow
        result=GetFhpElectricDataResult(deviceTimeArray=[dayTime])
    )
