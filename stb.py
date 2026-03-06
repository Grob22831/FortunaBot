from aiogram import types
import emoji

trottling_time = 2
Dice_time = 2
token = "8382438634:AAETHCpd59xnA_QZoMLkvDvuYlJzrzrhnWI"




#emojy
casino = emoji.emojize(":slot_machine:")
trophy = emoji.emojize(":trophy:")
cool = emoji.emojize("😎")
tada = emoji.emojize("🎉")
imp = emoji.emojize("👏")
omg = emoji.emojize("😱")



async def is_win(message: types.Message):
    if message.dice and message.dice.emoji == casino:
        if int(message.dice.value) == 64:
            return trophy
        elif int(message.dice.value) == 1:
            return imp
        elif int(message.dice.value) == 22:
            return tada
        elif int(message.dice.value) == 43:
            return cool
    return None