import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, LabeledPrice, PreCheckoutQuery, SuccessfulPayment,
    InlineKeyboardMarkup, InlineKeyboardButton
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "").strip()
PRICE = int(os.getenv("VIP_THEME_PRICE_STARS", "50"))

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

# Demo only: in-memory state resets on restart. Use a database in production.
vip_owners: set[int] = set()

def menu_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Купить VIP-золотую тему", callback_data="buy_vip")],
        [InlineKeyboardButton(text="🎮 Открыть демо-игру", url="https://example.com/replace-with-your-miniapp-url")]
    ])

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🖤✨ Добро пожаловать в UP CASINO!\n\n"
        "Играй в бесплатную демо-игру и оформляй цифровые косметические улучшения.\n"
        "В демо-игре используются только бесплатные виртуальные монеты; "
        "денежных ставок и вывода средств нет.",
        reply_markup=menu_keyboard()
    )

@dp.message(Command("vip"))
async def buy_vip(message: Message, bot: Bot):
    prices = [LabeledPrice(label="VIP Gold Theme", amount=PRICE)]
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="UP CASINO — VIP Gold Theme",
        description="Цифровая косметическая тема для интерфейса Mini App. Не даёт игрового преимущества.",
        payload=f"vip_theme:{message.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices,
    )

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery, bot: Bot):
    expected = f"vip_theme:{query.from_user.id}"
    if query.invoice_payload != expected:
        await bot.answer_pre_checkout_query(query.id, ok=False, error_message="Не удалось проверить заказ.")
        return
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payment: SuccessfulPayment = message.successful_payment
    if payment.invoice_payload == f"vip_theme:{message.from_user.id}" and payment.currency == "XTR":
        vip_owners.add(message.from_user.id)
        await message.answer(
            "✨ Оплата прошла успешно! VIP Gold Theme активирована для этого демо-бота.\n"
            "Сохраните это сообщение. В production нужно хранить entitlement и charge ID в базе данных."
        )

@dp.message(Command("paysupport"))
async def pay_support(message: Message):
    await message.answer(
        "Поддержка платежей UP CASINO.\n"
        "Напишите администратору бота и укажите дату платежа и Telegram payment charge ID, если он доступен."
    )

async def main():
    if not TOKEN or TOKEN == "put_your_bot_token_here":
        raise RuntimeError("Set BOT_TOKEN in .env before starting the bot.")
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
