from aiogram.utils.executor import start_polling
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "5660718931:AAGVyK98fQ0LAH__13wVjZLrQZu_U_TAR2M"
API_URL1 = "http://127.0.0.1:8000/get/"
API_URL = "http://127.0.0.1:8000/send/"
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=storage)

logging.basicConfig(level=logging.INFO)



class Registration(StatesGroup):
    fullname = State()
    work = State()
    date_of_birth = State()
    email = State()
    phone_number = State()
start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("👤 Ro‘yxatdan o'tish"))

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("👋 Salom! Ushbu bot orqali ro‘yxatdan o‘tishingiz mumkin.", reply_markup=start_keyboard)


@dp.message_handler(Text(equals="👤 Ro‘yxatdan o'tish", ignore_case=True), state="*")
async def start_registration(message: types.Message):
    await Registration.fullname.set()
    await message.answer("👤 To‘liq ismingizni kiriting:")
    print("Registration")
@dp.message_handler(state=Registration.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await Registration.next()
    print("Registration")
    await message.answer("👨‍💼 Ish joyingiz yoki kasbingizni kiriting:")

@dp.message_handler(state=Registration.work)
async def get_work(message: types.Message, state: FSMContext):
    await state.update_data(work=message.text)
    await Registration.next()
    await message.answer("📅 Tug‘ilgan kuningizni kiriting (YYYY-MM-DD):\n 2002-10-30")

# 📌 Tug‘ilgan sanani olish
@dp.message_handler(state=Registration.date_of_birth)
async def get_date_of_birth(message: types.Message, state: FSMContext):
    await state.update_data(date_of_birth=message.text)
    await Registration.next()
    await message.answer("📧 Emailingizni kiriting: \n admin@gmail.com")
@dp.message_handler(state=Registration.email)
async def get_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await Registration.next()
    await message.answer("📞 Telefon raqamingizni kiriting:\n for:+9989123456")
@dp.message_handler(state=Registration.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)

    # Foydalanuvchi ma'lumotlarini olish
    user_data = await state.get_data()


    # API ga POST so‘rov yuborish
    response = requests.post(API_URL, json=user_data)
    print(response.status_code)
    print(response.json())

    if response.status_code == 201:
        await message.answer("✅ Ro‘yxatdan muvaffaqiyatli o‘tdingiz!", reply_markup=start_keyboard)
        try:
            response = requests.get(API_URL1)

            if response.status_code == 200:
                with open("exce/users.xlsx", "wb") as f:
                    f.write(response.content)

                with open("exce/users.xlsx", "rb") as doc:
                    await bot.send_document(message.chat.id, doc, caption="📂 Excel fayl tayyor!")
            else:
                await message.answer("❌ Excel faylni olishda xatolik yuz berdi.")
        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")

    else:
        await message.answer("❌ Xatolik yuz berdi. Qaytadan urunib ko‘ring!")

    # Holatni tugatish
    await state.finish()

#
# @dp.message_handler(Command("export"))
# async def export_excel(message: types.Message):
#     try:
#         response = requests.get(API_URL)
#
#         if response.status_code == 200:
#             with open("exce/users.xlsx", "wb") as f:
#                 f.write(response.content)
#
#             with open("exce/users.xlsx", "rb") as doc:
#                 await bot.send_document(message.chat.id, doc, caption="📂 Excel fayl tayyor!")
#         else:
#             await message.answer("❌ Excel faylni olishda xatolik yuz berdi.")
#     except Exception as e:
#         await message.answer(f"⚠️ Xatolik: {e}")

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)
