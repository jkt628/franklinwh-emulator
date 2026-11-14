from fastapi import APIRouter
from pydantic import BaseModel

from emulator import Response

router = APIRouter(prefix="/recommend")


class RecommendFlagResult(BaseModel):
    enableRecommend: int = 0
    recommendUrl: str | None = None
    recommendCodeMarkdown: str | None = None
    recommendText: str | None = None
    recommendImage: str | None = None


class RecommendFlagResponse(Response[RecommendFlagResult]):
    pass


@router.get("/recommendFlag")
async def get_recommend_flag() -> RecommendFlagResponse:
    return RecommendFlagResponse(result=RecommendFlagResult())
