#import asyncio
from aiogram.filters import Command
import emoji
from aiogram import  Bot, Router, types
#
#router = Router()
#
#
#@router.inline_query()
#async def inline_handler(query: types.InlineQuery):
#    text = query.query or "пустой запрос"
#    result  = emoji.emojize(":slot_machine:")
#    if text == "cas":
#        await query.answer(results=result, cache_time=1)
