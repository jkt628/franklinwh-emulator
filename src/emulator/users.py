"""users: associate account (email) with user data and support logintoken authentication."""

import asyncio
import hashlib
import secrets
from collections import UserDict
from typing import Annotated, Final
from zoneinfo import ZoneInfo

import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from emulator import Gateway, Site

from .rwlockeddict import RWLockedDict

leader: Final = "APP_ACCOUNT::"


# known accounts (email)
JANE_DOE: Final = "jane@doe.com"
JOHN_DOE: Final = "john@doe.com"

_passwords = {
    JANE_DOE: "JaneDoe",
    JOHN_DOE: "JohnDoe",
}
for k, v in _passwords.items():
    _passwords[k] = hashlib.md5(bytes(v, "ascii")).hexdigest()


class PII(BaseModel):
    userName: str | None = None
    contactNumber: str | None = None
    userAddress: str | None = None
    region: str | None = None
    lat: str | None = None
    lon: str | None = None
    firstName: str
    lastName: str
    zipCode: str | None = "27025"
    country: str | None = "United States"
    province: str | None = "North Carolina"
    city: str | None = "Pleasantville"
    addressSecondLast: str | None = None
    alphaCode: str | None = "AS,US,PR,GU,VI,UM,PR,MP"
    addressFinish: str | None = None
    avatar: str | None = None


class User(BaseModel):
    account: str
    userId: int
    PII: PII
    sites: list[Site]


_users: dict[str, User] = {
    JANE_DOE: User(
        account=JANE_DOE,
        userId=987654,
        PII=PII(
            contactNumber="+1-987-555-6543",
            userAddress="987654 Main Street",
            firstName="Jane",
            lastName="Doe",
            avatar="https://tr.rbxcdn.com/30DAY-Avatar-5D3112D29FE230F31350D3346E66000E-Png/352/352/Avatar/Png/noFilter",
        ),
        sites=[
            Site(
                gateways=[
                    Gateway(
                        id="10060005A02X24987654",
                        name="Home",
                    ),
                ],
            ),
            Site(
                address="987655 Deer View Road, Boulder, Colorado, United States",
                zipCode="80302",
                tz=ZoneInfo("America/Denver"),
                gateways=[
                    Gateway(
                        id="10060005A02X24987655",
                        name="Cabin",
                    ),
                ],
            ),
        ],
    ),
    JOHN_DOE: User(
        account=JOHN_DOE,
        userId=654321,
        PII=PII(
            contactNumber="+1-654-555-3210",
            userAddress="654321 Main Street",
            firstName="John",
            lastName="Doe",
            avatar="https://tr.rbxcdn.com/30DAY-Avatar-9A3C11044D5172166CEFC75C64ECD14E-Png/352/352/Avatar/Png/noFilter",
        ),
        sites=[
            Site(
                gateways=[
                    Gateway(
                        id="10060005A02X24654321",
                        name="654321 Main Street",
                    ),
                ],
            ),
        ],
    ),
}
for u in _users.values():
    u.PII.addressFinish = (
        f"{u.PII.userAddress}, {u.PII.city}, {u.PII.province}, {u.PII.country}"
    )
    u.sites[0].address = u.PII.addressFinish
    for site in u.sites:
        site.id = int(site.gateways[0].id[-6:])
        site.name = site.gateways[0].name


logintoken = APIKeyHeader(name="logintoken")


def get_current_account(logintoken: str = Security(logintoken)) -> User:
    if not logintoken.startswith(leader):
        raise HTTPException(status_code=401, detail="Invalid token format")
    account = _tokens.verify_token(logintoken[len(leader) :])
    if account is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return _users[account]


LoginTokenAuth = Depends(get_current_account)
LoginUser = Annotated[User, LoginTokenAuth]


class Tokens(RWLockedDict):
    def add(self, account, token) -> None:
        """
        Add token for account.

        The account points to the token and the token points to the account.
        This allows for easy lookup of either and verifies the account uses the latest token.

        :param account: email address of the account
        :param token: token string
        :type account: str
        :type token: str
        """
        with self.locked_context().gen_wlock():
            UserDict.__setitem__(self, token, account)
            UserDict.__setitem__(self, account, token)

    def verify_token(self, token: str) -> str | None:
        """
        Verify token points to account and vice versa.

        Return account if this predicate holds, otherwise None.

        :param token: token string
        :type token: str
        :return: account | None
        :rtype: str | None
        """
        account = self.get(token)
        if account is None or self.get(account) != token:
            return None
        return account


_tokens = Tokens()


def login(account: str, password: str) -> tuple[str, User]:
    """
    Generate a token for the given account and password.

    :param account: email address of the account
    :param password: password of the account
    :type account: str
    :type password: str
    :return: token string
    :rtype: str
    :raises ValueError: if account or password is invalid
    """
    if password is None or _passwords.get(account) != password:
        raise ValueError("Invalid account or password")
    payload = {account: password}
    token = jwt.encode(payload, secrets.token_bytes(32), algorithm="HS256")
    _tokens.add(account, token)
    return leader + token, _users[account]


async def logout():
    while True:
        await asyncio.sleep(10 * 60)  # 10 minutes
        _tokens.clear()
