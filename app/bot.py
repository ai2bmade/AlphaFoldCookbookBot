import asyncio
import base64
import logging
import os

from openai import AsyncOpenAI
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "").strip() or "gpt-5.4-mini"

SYSTEM_INSTRUCTIONS = """You are the AlphaFold Cookbook support bot, a patient step-by-step guide for absolute beginners.
Help learners complete one small foundation at a time so they can eventually solve harder problems on their own.

When a learner sends an error message or screenshot:
1. State what probably happened in one plain-English sentence.
2. Give numbered troubleshooting steps with exact clicks, text, or commands.
3. Say what successful output should look like.
4. Ask for the next screenshot or exact error only when necessary.

Keep answers concise and practical. Never invent protein identifiers, FASTA sequences, binding sites, confidence values, or research findings. Ask the learner to verify biological facts with authoritative sources such as UniProt, NCBI, PDB, or AlphaFold DB. Clearly distinguish an AI prediction from experimental evidence. Do not provide medical, diagnostic, treatment, laboratory-safety, or investment advice. Never request API keys, passwords, bot tokens, or other secrets."""


def split_message(text: str, limit: int = 4000) -> list[str]:
    text = text.strip()
    if not text:
        return ["I could not prepare a response. Please send the error again."]
    parts: list[str] = []
    while len(text) > limit:
        split_at = text.rfind("\n", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        parts.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        parts.append(text)
    return parts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "Welcome to the AlphaFold Cookbook! 🧬\n\n"
        "This bot supports you as you work through each step. Send the step number, the exact error message, or a screenshot. I’ll explain what happened and guide you through the next small action.\n\n"
        "Please remove API keys, passwords, email addresses, and private data before sending anything."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "How to ask for help:\n"
        "1. Tell me which cookbook step you are on.\n"
        "2. Paste the complete error, or attach one screenshot.\n"
        "3. Tell me what you expected to happen.\n\n"
        "I provide educational troubleshooting, not medical or investment advice."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if not update.effective_message:
        return
    ai_status = "ready" if OPENAI_API_KEY else "waiting for OPENAI_API_KEY"
    await update.effective_message.reply_text(
        f"Support bot status: {ai_status}\nModel: {OPENAI_MODEL}"
    )


async def ask_openai(text: str, image_data_url: str | None = None) -> str:
    if not OPENAI_API_KEY:
        return (
            "The support bot is online, but its AI connection has not been configured yet. "
            "Please ask the cookbook administrator to add OPENAI_API_KEY in Coolify."
        )

    content: list[dict[str, str]] = [{"type": "input_text", "text": text}]
    if image_data_url:
        content.append({"type": "input_image", "image_url": image_data_url})

    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    response = await client.responses.create(
        model=OPENAI_MODEL,
        instructions=SYSTEM_INSTRUCTIONS,
        input=[{"role": "user", "content": content}],
    )
    return response.output_text


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if not message:
        return

    prompt = (message.text or message.caption or "Please diagnose this screenshot.").strip()
    image_data_url = None

    if message.photo:
        photo = message.photo[-1]
        telegram_file = await context.bot.get_file(photo.file_id)
        image_bytes = await telegram_file.download_as_bytearray()
        encoded = base64.b64encode(image_bytes).decode("ascii")
        image_data_url = f"data:image/jpeg;base64,{encoded}"

    await context.bot.send_chat_action(
        chat_id=message.chat_id,
        action=ChatAction.TYPING,
    )

    try:
        reply = await ask_openai(prompt, image_data_url)
    except Exception:
        LOGGER.exception("Failed to prepare Telegram reply")
        reply = (
            "The support bot encountered a temporary problem. "
            "Please try again in a moment. If it continues, send the same error as plain text."
        )

    for part in split_message(reply):
        await message.reply_text(part)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    LOGGER.error("Telegram update failed: %s", update, exc_info=context.error)


def run() -> None:
    if not BOT_TOKEN:
        LOGGER.warning("TELEGRAM_BOT_TOKEN is not configured; bot worker is waiting.")
        while True:
            asyncio.run(asyncio.sleep(3600))

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(
        MessageHandler((filters.TEXT | filters.PHOTO) & ~filters.COMMAND, answer)
    )
    application.add_error_handler(error_handler)
    LOGGER.info("Starting AlphaFold Cookbook Telegram bot with long polling")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    run()
