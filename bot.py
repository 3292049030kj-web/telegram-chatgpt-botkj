import os
import logging
import asyncio
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("请在 Render 设置 BOT_TOKEN 和 OPENAI_API_KEY 环境变量!")

client = OpenAI(api_key=OPENAI_API_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=300
        )
        bot_reply = completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"OpenAI 请求失败: {e}")
        bot_reply = "OpenAI 服务出错，请稍后再试。"

    await update.message.reply_text(bot_reply)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    logger.info("Bot 已启动，正在监听消息…")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
