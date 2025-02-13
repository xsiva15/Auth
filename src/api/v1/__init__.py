from fastapi import APIRouter
from .handlers import *


router_v1 = APIRouter(prefix="/v1")

router_v1.include_router(login_router)
router_v1.include_router(registration_router)
router_v1.include_router(recovery_router)

