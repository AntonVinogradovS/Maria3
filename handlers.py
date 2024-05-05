import random
from aiogram import types, Router
from aiogram import Dispatcher
from aiogram.filters.command import Command, CommandStart
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F
#from database import insert_payment, read_payment_by_id, read_payment, delete_payment_by_id
from datetime import datetime, timedelta


from createBot import bot
#from database import insert_data
TEST_TOKEN = '390540012:LIVE:50461'
PRICE1 = types.LabeledPrice(label="Подписка на закрытый канал", amount=999*100)  # в копейках (руб)

user_router = Router()
def kb():
    buttons = [[
        types.InlineKeyboardButton(text="Российская карта", callback_data="rus_card"),
        types.InlineKeyboardButton(text="Иностранная карта", callback_data="foreign_card")
    ]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def kb2(id):
    buttons = [[
        types.InlineKeyboardButton(text="Подтвердить", callback_data=f"good_{id}"),
        types.InlineKeyboardButton(text="Отклонить", callback_data=f"deny"),
    ]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(text='Привет! С помощью этого бота ты можешь получить доступ к закрытому каналу <b>Лунный чатик</b>.\n\nСтоимость при оплате <b>российской картой</b> - 999₽\nСтоимость при оплате <b>иностранной картой</b> - 15$\nВыбери удобный способ оплаты.',parse_mode='HTML', reply_markup=kb())
    print(message.from_user.id)

@user_router.callback_query(F.data == 'rus_card')
async def pay_1(callback: types.CallbackQuery):
    await bot.send_invoice(callback.message.chat.id,
                           title="Подписка на канал",
                           description="Активация подписки",
                           provider_token=TEST_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE1],
                           #start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    
@user_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    #print("1")

@user_router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    print(message.successful_payment.total_amount)
    await message.answer('Спасибо за оплату!\nhttps://t.me/+X7ecS_RUTJI5ZDNi')

@user_router.callback_query(F.data == "foreign_card")
async def pay_2(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Необходимо произвести оплату на PayPal по адресу `malinov.yoga@gmail.com` и отправить *скриншот оплаты*.",parse_mode='MarkDown')

@user_router.message(F.photo)
async def mes_photo(message: types.Message):
    print(message.from_user.id)
    await message.answer(text='После проверки я пришлю вам ссылку на канал.')
    await bot.send_photo(chat_id=54787745, photo=message.photo[-1].file_id, reply_markup=kb2(message.from_user.id))

@user_router.callback_query(F.data.startswith('good'))
async def pay_2(callback: types.CallbackQuery):
    print(callback.data.split('_')[1])
    await bot.send_message(chat_id=callback.data.split('_')[1], text="Спасибо за оплату!\nhttps://t.me/+X7ecS_RUTJI5ZDNi")
    await callback.message.delete()

@user_router.callback_query(F.data == 'deny')
async def deny_user(callback: types.CallbackQuery):
    await callback.message.delete()

#54787745