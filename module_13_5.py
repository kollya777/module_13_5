from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

api = ''
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup()
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.add(button_2)
start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация')]
    ], resize_keyboard=True
)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(
        'Привет! Я бот, помогающий твоему здоровью. Нажми кнопку "Рассчитать", сколько ккалорий в день тебе нужно употреблять',
        reply_markup=kb)


@dp.message_handler(text='Рассчитать', state=None)
async def set_age(message: types.Message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


# Функция для установки роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (см):')
    await UserState.growth.set()


# Функция для установки веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (кг):')
    await UserState.weight.set()


# Функция для расчета и отправки нормы калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)

    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    # Расчет по формуле Миффлина-Сан Жеора для мужчин
    calories = int(10 * weight + 6.25 * growth - 5 * age + 5)

    await message.answer(f"Ваша норма калорий: {calories} ккалорий в день")
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    print('Получено новое сообщение')
    await message.answer('Введите команду \start, чтобы начать общение')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)