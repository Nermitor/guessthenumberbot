import asyncio  # Работа с асинхронностью
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command  # Фильтр для /start, /...
from aiogram.types import Message  # Тип сообщения

from config import config  # Config

API_TOKEN = config.token

bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Менеджер бота

statistic = {
    # 1: {
    #     'win': 0,
    #     'lose': 0
    # }
}


# dp.message - обработка сообщений
# Command(commands=['start'] Фильтр для сообщений, берём только /start
@dp.message(Command(commands=['start']))  # Берём только сообщения, являющиеся командой /start
async def start_command(message: Message):  # message - сообщение, которое прошло через фильтр
    await message.answer(
        "Привет, сыграем в игру - я загадал число от 1 до 3, а ты угадывай\n")  # Отвечаем на полученное сообщение


@dp.message(Command(commands=['statistics']))
async def get_statistics(message: Message):
    current_user_stats = statistic[message.chat.id]
    await message.answer(f'Побед {current_user_stats["win"]}\nПоражений: {current_user_stats["lose"]}')


@dp.message()
async def handle_number(message: Message):
    if message.text.isdigit():
        number = random.randint(1, 3)  # генерируем число только после ответа пользователя, а не до.
        chat_id = message.chat.id
        if not chat_id in statistic:
            statistic[chat_id] = {
                'lose': 0,
                'win': 0
            }
        if number == int(message.text):
            await message.answer('Да! Вы угадали. Я перезагадал число')
            statistic[chat_id]['win'] += 1
        else:
            await message.answer('Нет! Вы не угадали((( Я перезагадал число')
            statistic[chat_id]['lose'] += 1


async def main():
    try:
        print('Bot Started')
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':  # Если мы запускаем конкретно этот файл.
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
