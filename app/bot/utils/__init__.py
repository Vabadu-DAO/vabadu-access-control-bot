import asyncio
from contextlib import suppress
from decimal import Decimal
from typing import Sequence, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from pytonapi.utils import userfriendly_to_raw, to_amount

from app.db.models import MemberDB, TokenDB, UserDB


async def user_is_holder(user: UserDB, tokens: Sequence[TokenDB]):
    member_checks = []

    for token in tokens:
        member_address = (
            userfriendly_to_raw(user.wallet_address)
            if user and user.wallet_address
            else None
        )
        if token.holders and token.holders.get(member_address, 0) >= token.min_amount:
            member_checks.append(True)
        else:
            member_checks.append(False)

    return all(member_checks)


async def kick_member(bot: Bot, member: MemberDB) -> None:
    with suppress(TelegramBadRequest):
        await bot.ban_chat_member(member.chat_id, member.user_id)
        await asyncio.sleep(.2)
        await bot.unban_chat_member(member.chat_id, member.user_id)
        await asyncio.sleep(.2)


def amount_string(amount: int, decimals: Optional[int] = None) -> str:
    amount = to_amount(amount, decimals=decimals)  # type: ignore
    return "{:.9}".format(Decimal(str(amount)))
