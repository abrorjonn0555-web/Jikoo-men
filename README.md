# UP CASINO — Telegram Mini App starter

A minimal black-and-gold Telegram Mini App with a free-play slot demo and a Telegram bot that can sell a **non-random digital cosmetic** (VIP gold theme) for Telegram Stars.

## Important product choice
Telegram Stars are a payment method (`XTR`), not a user-owned in-app balance that your bot can freely transfer. This starter does **not** accept Stars as bets, does not let users buy wagering credits, and has no cash-out or real-money prizes. The slot demo uses free demo coins only. Stars purchase unlocks a cosmetic theme.

## Contents
- `web/index.html` — responsive Mini App interface (black/gold)
- `bot.py` — Telegram bot, `/start`, Stars invoice for VIP theme, payment confirmation
- `requirements.txt`
- `.env.example`

## 1. Create your bot
1. Open https://t.me/BotFather in Telegram.
2. Run `/newbot`, follow the prompts, and copy the bot token.
3. Keep the token private. Never paste it into public chats or commit it to source control.

## 2. Configure and run the bot
Python 3.11+ recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `BOT_TOKEN`.
Then:
```bash
python bot.py
```

The bot sends a Stars invoice for a digital cosmetic. On successful payment, it records the Telegram user ID and confirms the purchase. This sample stores purchase state in memory; use a database for production.

## 3. Host the Mini App
The `web` folder must be served over HTTPS. For example, deploy it to a static host you control. Do not put the bot token in frontend code.

In BotFather:
1. `/mybots` → choose your bot.
2. Bot Settings → Configure Mini App (wording can vary), or set the menu button.
3. Set the HTTPS URL for `web/index.html`.

For local visual testing, open `web/index.html` in a browser. Telegram-specific user data is only available inside Telegram.

## 4. Connect payment button to the bot
The included Mini App demonstrates the design and free-play slot UI. For a production checkout, the frontend should request an invoice link from your backend and open it with Telegram's `openInvoice` API. The simple bot invoice currently works from the bot chat using `/vip`.

## Production checklist
- Validate Telegram Mini App `initData` on the server before trusting user identity.
- Persist orders and entitlements in a database.
- Use HTTPS, rate limits, structured logs, backups, and secure secret storage.
- Implement `/paysupport`, refund handling (`refundStarPayment`) and order reconciliation.
- Add privacy policy, terms, support contact, age/access controls as required for your jurisdiction and Telegram policies.
- Do not use client-side balances as authoritative; game results and entitlement checks must be server-side.
- Review current Telegram Stars and Mini App rules before launch.

Official docs:
- Mini Apps: https://core.telegram.org/bots/webapps
- Stars payments: https://core.telegram.org/bots/payments-stars
