from zoneinfo import ZoneInfo

from pydantic import BaseModel

from emulator import Gateway


class Site(BaseModel):
    id: int | None = None
    name: str | None = None
    address: str | None = None
    gateways: list[Gateway]
    zipCode: str = "27025"
    tz: ZoneInfo = ZoneInfo("America/New_York")
