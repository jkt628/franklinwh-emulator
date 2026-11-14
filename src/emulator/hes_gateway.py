from fastapi import APIRouter

from emulator import LoginTokenAuth, common, terminal

router = APIRouter(prefix="/hes-gateway")
router.include_router(common.router, dependencies=[LoginTokenAuth])
router.include_router(terminal.router)
