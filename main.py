import os
import certifi
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from g4f.client import Client

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

client = Client()


# Определение состояний
class Form(StatesGroup):
    question = State()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Привет, задай один вопрос:")
    await state.set_state(Form.question)


# Обработчик вопроса пользователя
@dp.message(Form.question)
async def handle_question(message: types.Message, state: FSMContext):
    await message.answer("Обрабатываю твой вопрос...")

    # Отправка запроса к g4f
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message.text}],
        web_search=False
    )

    # Отправка ответа пользователю
    await message.answer(response.choices[0].message.content)

    # Очистка состояния
    await state.clear()


# Запуск бота
if __name__ == "__main__":
    os.environ["SSL_CERT_FILE"] = certifi.where()
    dp.run_polling(bot)
    