"""Implement the FranklinWH API server."""

from fastapi import APIRouter
from pydantic import BaseModel

from emulator import ResponseWithTotal

router = APIRouter(prefix="/common")


class PowerCapConfig(BaseModel):
    id: int
    modelName: str
    peHwVersion: int
    ratedCap: int
    chargePower: int
    dischargePower: int
    derateFlag: int


class GetPowerCapConfigListResponse(ResponseWithTotal[list[PowerCapConfig]]):
    pass


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
