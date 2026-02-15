from aiogram.filters import Command
from aiogram import  Bot, Router, types,F
Stack = []


router = Router()
#Команда /start, просто выводит то, что умеет
#декоратор, показывает к чему привязана функция, или я хз, без него не работает
@router.message(Command("start"))
async def start(message: types.Message):
        await message.answer("Привет, солнышко")
        await  message.answer('Вот что я умею\n:'
                              '--Напиши в чат:"Крутка" или "Лудка",  я прокручу тебе казино несколько раз\n'
                              '--Напиши в чат "Крутка" или "Лудка" с указанием числа после, я прокручу определенное количество раз\n'
                              '--Напиши /tell "id чата" "сообщение" - выведу в чате сообщение если я в нем есть\n'
                              )




