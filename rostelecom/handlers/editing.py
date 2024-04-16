from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.simple_row import make_row_keyboard

router = Router()

# Эти значения далее будут подставляться в итоговый текст, отсюда
# такая на первый взгляд странная форма прилагательных
available_action_names = ["Изменить данные", "Добавить данные", "Удалить данные","Вернуться"]
password="12345"


class EditState(StatesGroup):
    password_input = State()
    edition_state = State()
    
    change_state=State()
    adding_state=State()
    delete_state=State()



#@router.message(Command("adit"))
@router.message(F.text == "Редактировать")
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Введите пароль:"
    )
    # Устанавливаем пользователю состояние "выбирает название"
    await state.set_state(EditState.password_input)

# Этап выбора блюда #

#
@router.message(EditState.password_input, F.text.lower() == '12345')
async def aditing_data(message: Message, state: FSMContext):
    await state.update_data(edit_pass=message.text.lower())
    await message.answer(
        text="Доступ разрешен",
        reply_markup=make_row_keyboard(available_action_names)
    )
    await state.set_state(EditState.edition_state)


# В целом, никто не мешает указывать стейты полностью строками
# Это может пригодиться, если по какой-то причине 
# ваши названия стейтов генерируются в рантайме (но зачем?)
@router.message(EditState.password_input)
async def password_incorrectly(message: Message):
    await message.answer(
        text="Введите еще раз"
    )

# Этап выбора размера порции и отображение сводной информации #


@router.message(EditState.edition_state, F.text.in_(available_action_names))
async def edition_process(message: Message, state: FSMContext):
    #user_data = await state.get_data()
    if message.text in available_action_names[:-1]:
        await message.answer(
            text=f"{message.text.lower()}",
            reply_markup=make_row_keyboard(available_action_names)
            #reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(EditState.edition_state)
    else:
        await state.clear()
    # Сброс состояния и сохранённых данных у пользователя
    #await state.clear()


@router.message(EditState.edition_state,Command("exit"))
async def exit_for_edition(message: Message,state:FSMContext):
    await state.clear()