from aiogram import types, Router
from handlers.stb import trophy,casino,cool,tada,imp
from aiogram.types import ReactionTypeEmoji
from handlers.stb import is_win
router = Router()

@router.message()
async def reaction(message: types.Message):
    emo = await is_win(message)
    if emo is not None:
        await message.react([ReactionTypeEmoji(emoji=emo)])


