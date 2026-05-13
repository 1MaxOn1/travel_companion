from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from agent.llm_agent import LLMTravelAgent

router = Router()

agent = LLMTravelAgent()

class Form(StatesGroup):
    destination = State()
    dates = State()
    budget = State()
    interests = State()
    generating = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Form.destination)
    await message.answer("Привет! Давай спланируем твоё путешествие.\n\nКуда хочешь поехать? (город или страна)")

@router.message(Form.destination)
async def process_destination(message: Message, state: FSMContext):
    await state.update_data(destination=message.text.strip())
    await state.set_state(Form.dates)
    await message.answer("Отлично! Теперь введи даты поездки (например, 13.05.2026 – 13.06.2026)")

@router.message(Form.dates)
async def process_dates(message: Message, state: FSMContext):
    await state.update_data(dates=message.text.strip())
    await state.set_state(Form.budget)
    builder = InlineKeyboardBuilder()
    builder.button(text="Экономный", callback_data="budget_economy")
    builder.button(text="Средний", callback_data="budget_medium")
    builder.button(text="Комфортный", callback_data="budget_comfort")
    await message.answer("Выбери бюджет поездки:", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("budget_"))
async def process_budget(callback: CallbackQuery, state: FSMContext):
    budget_map = {
        "budget_economy": "экономный",
        "budget_medium": "средний",
        "budget_comfort": "комфортный"
    }
    choice = budget_map[callback.data]
    await state.update_data(budget=choice)
    await callback.message.edit_text(f"Бюджет: {choice}")
    await state.set_state(Form.interests)
    await callback.message.answer("Что тебя интересует? Напиши через запятую (например: пляжи, рестораны, достопримечательности, история, шопинг)")
    await callback.answer()

@router.message(Form.interests)
async def process_interests(message: Message, state: FSMContext):
    await state.update_data(interests=message.text.strip())
    data = await state.get_data()
    await state.set_state(Form.generating)
    await message.answer("Собираю информацию и строю план, подожди немного...")

    prompt = f"""
Составь детальный план путешествия на основе следующих параметров:
- Направление: {data['destination']}
- Даты: {data['dates']}
- Бюджет: {data['budget']}
- Интересы: {data['interests']}

Используй поиск в интернете, чтобы найти:
1. Актуальные авиабилеты (цены, ссылки).
2. Варианты проживания (отели, хостелы) с ценами и ссылками.
3. Достопримечательности и активности, соответствующие интересам.
4. Рестораны и кафе (особенно если указаны рестораны в интересах).
5. Погоду и визовые требования (если применимо).

Выведи план в красивом структурированном виде с разделами:
- Перелёт
- Проживание
- Маршрут по дням (кратко)
- Бюджет (примерный)
- Полезные ссылки

Каждый пункт должен содержать реальные ссылки, полученные из поиска.
"""
    answer = await agent.process_message(prompt, prompt)

    MAX_LEN = 4000
    if len(answer) > MAX_LEN:
        for i in range(0, len(answer), MAX_LEN):
            chunk = answer[i:i+MAX_LEN]
            await message.answer(chunk)
    else:
        await message.answer(answer)
    await state.clear()

@router.message(Form.generating)
async def handle_generating(message: Message):
    await message.answer("План уже формируется, ожидайте.")