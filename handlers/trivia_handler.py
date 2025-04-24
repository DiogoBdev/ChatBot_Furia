import json
import random
from telegram import Update
from telegram.ext import ContextTypes

with open("trivia.json", "r", encoding="utf-8") as f:
    perguntas = json.load(f)

frases_acerto = [
    "🔥 É isso! Tá afiado igual o arT!",
    "🎯 Bala certeira! Bora que bora!",
    "🏆 Essa foi de MVP!"
]

frases_erro = [
    "💔 Essa passou raspando!",
    "😓 Não foi dessa vez, mas a próxima é nossa!",
    "📉 Pega visão e tenta de novo, FURIOSO!"
]

async def iniciar_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = random.choice(perguntas)
    opcoes = "\n".join([f"{idx + 1}. {op}" for idx, op in enumerate(pergunta["opcoes"])])

    context.user_data["pergunta_atual"] = pergunta

    await update.message.reply_text(
        f"🧠 *{pergunta['pergunta']}*\n\n{opcoes}",
        parse_mode="Markdown"
    )

async def verificar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta_atual = context.user_data.get("pergunta_atual")
    if not pergunta_atual:
        return

    resposta_usuario = update.message.text.strip()
    resposta_certa = pergunta_atual["resposta_certa"]

    if resposta_usuario.lower() == resposta_certa.lower() or resposta_usuario == str(pergunta_atual["opcoes"].index(resposta_certa) + 1):
        await update.message.reply_text(f"✅ {random.choice(frases_acerto)}")
    else:
        await update.message.reply_text(
            f"❌ {random.choice(frases_erro)}\nA resposta certa era: *{resposta_certa}*",
            parse_mode="Markdown"
        )

    context.user_data.clear()