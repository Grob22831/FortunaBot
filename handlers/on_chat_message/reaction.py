from aiogram import types, Router
from handlers.stb import trophy,casino,cool,tada,imp
from aiogram.types import ReactionTypeEmoji
from handlers.stb import is_win
router = Router()
from handlers.database_ip import get_chat_rules_dict

#оставляет реакции на слот машину других игроков, если там выигрыш конечно
@router.message()
async def reaction(message: types.Message):
    rules = await get_chat_rules_dict(message.chat.id)
    if rules['m_reactions'] == 0:
        return
    emo = await is_win(message)
    if emo is not None:
        await message.react([ReactionTypeEmoji(emoji=emo)])


