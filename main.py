import asyncio
import json
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import database.main as db
import request.main as req
from handlers import check
from translate import translate

# Загрузка конфига
with open("config.json", "r") as f:
    config = json.load(f)

token = config["bot_token"]
bot = Bot(token=token)
dp = Dispatcher()


class Form(StatesGroup):
    url = State()


# Класс для кнопок (keyboards)
class Keyboards:
    @staticmethod
    def start(user_id):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=translate(user_id, "btn_check_url"), callback_data="check")],
            [InlineKeyboardButton(text=translate(user_id, "btn_settings"), callback_data="settings")]
        ])

    @staticmethod
    def settings(user_id):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=translate(user_id, "btn_change_url"), callback_data="chg_url")],
            [InlineKeyboardButton(text=translate(user_id, "btn_autosend"), callback_data="auto_send")],
            [InlineKeyboardButton(text=translate(user_id, "btn_lang"), callback_data="lang")]
        ])

    @staticmethod
    def languages(user_id):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=translate(user_id, "lang_ru"), callback_data="set_lang_ru")],
            [InlineKeyboardButton(text=translate(user_id, "lang_ua"), callback_data="set_lang_ua")],
            [InlineKeyboardButton(text=translate(user_id, "lang_en"), callback_data="set_lang_en")],
            [InlineKeyboardButton(text=translate(user_id, "lang_de"), callback_data="set_lang_de")],
            [InlineKeyboardButton(text=translate(user_id, "lang_fr"), callback_data="set_lang_fr")]
        ])


@dp.message(Command("start"))
async def start(message: Message):
    new_usr = db.chk_usr(message.from_user.id)
    if new_usr == 0:
        db.add_usr(message.from_user.id, config['default_language'])
        print(f"[MAIN] User {message.from_user.id} has been added successfully.")

    text = translate(message.from_user.id, "start")
    await message.answer(text, reply_markup=Keyboards.start(message.from_user.id))
    print(f"[MAIN] User {message.from_user.id} started bot.")


@dp.callback_query(lambda call: call.data == "check")
async def check_url(call: CallbackQuery):
    usr_link = db.get_link(call.from_user.id)
    status = await req.chk_website(usr_link[0])

    if status:
        text = translate(call.from_user.id, "url_work").format(url=usr_link[0])
        print(f"[MAIN] URL {usr_link[0]} is working.")
    else:
        text = translate(call.from_user.id, "url_error").format(url=usr_link[0])
        print(f"[MAIN] URL {usr_link[0]} is not working.")

    await call.message.answer(text)
    print(f"[MAIN] Checked URL {usr_link}.")
    await call.answer()

# ----------------------- SETTINGS [URL]
@dp.callback_query(lambda call: call.data == "settings")
async def settings(call: CallbackQuery):
    text = translate(call.from_user.id, "settings_msg")
    await call.message.answer(text, reply_markup=Keyboards.settings(call.from_user.id))
    print(f"[MAIN] User {call.message.from_user.id} has opened settings.")
    await call.answer()

@dp.callback_query(lambda call: call.data == "chg_url")
async def chg_url(call: CallbackQuery, state: FSMContext):
    text = translate(call.from_user.id, "settings_url")
    await call.message.answer(text)
    await state.set_state(Form.url)
    print(f"[MAIN] User {call.message.from_user.id} is changing URL.")
    await call.answer()


@dp.message(Form.url)
async def upd_url(message: Message, state: FSMContext):
    send = db.get_send(message.from_user.id)
    db.chg_usr(message.text, send[0], message.from_user.id)
    text = translate(message.from_user.id, "settings_url_done").format(url=message.text)
    print(f"[MAIN] User {message.from_user.id} has changed URL to {message.text}")
    await message.answer(text)
    await state.clear()


# ----------------------- SETTINGS [Autosend]
@dp.callback_query(lambda call: call.data == "auto_send")
async def auto_send(call: CallbackQuery):
    link = db.get_link(call.from_user.id)
    send = db.get_send(call.from_user.id)

    if send[0] == 0:
        text = translate(call.from_user.id, "settings_autosend_enable")
        print(f"[MAIN] User {call.message.from_user.id} has enabled automatic send.")
        db.chg_usr(link[0], 1, call.from_user.id)
    else:
        text = translate(call.from_user.id, "settings_autosend_disable")
        print(f"[MAIN] User {call.message.from_user.id} has disabled automatic send.")
        db.chg_usr(link[0], 0, call.from_user.id)

    await call.message.answer(text)
    await call.answer()


# ----------------------- SETTINGS [Language]
@dp.callback_query(lambda call: call.data == "lang")
async def lang_menu(call: CallbackQuery):
    text = translate(call.from_user.id, "settings_lang")
    await call.message.answer(text, reply_markup=Keyboards.languages(call.from_user.id))
    print(f"[MAIN] User {call.message.from_user.id} is changing language.")
    await call.answer()


@dp.callback_query(lambda call: call.data.startswith("set_lang_"))
async def set_language(call: CallbackQuery):
    lang_code = call.data.split("_")[-1]  # Получаем ru/ua/en/de/fr
    db.chg_lang(call.from_user.id, lang_code)
    text = translate(call.from_user.id, "lang_msg")
    print(f"[MAIN] User {call.message.from_user.id} has changed language to {lang_code}.")
    await call.message.answer(text)
    await call.answer()


async def main():
    db.init()
    print("[MAIN] Bot started.")
    asyncio.create_task(check.main(bot, config['check_interval']))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())