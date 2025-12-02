import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise RuntimeError("Missing BOT_TOKEN or OPENAI_API_KEY")

# 初始化新版 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""

    try:
        # GPT-4o mini 调用格式
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一个中文助手，所有回答必须使用中文"},
                {"role": "user", "content": user_text}
            ],
            max_tokens=300,
        )

        bot_reply = completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"OpenAI 调用失败: {e}")
        bot_reply = "OpenAI 服务错误，请稍后再试。"

    await update.message.reply_text(bot_reply)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 监听所有文字消息
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    logger.info("🤖 Telegram GPT-4o mini 机器人已启动")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
