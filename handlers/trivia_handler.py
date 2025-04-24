import json
import random
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

# Carrega perguntas do JSON (ajusta o path conforme sua estrutura)
BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "..", "trivia.json"), encoding="utf-8") as f:
    todas_perguntas = json.load(f)

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
    # Embaralha e armazena a lista
    perguntas = todas_perguntas.copy()
    random.shuffle(perguntas)
    context.user_data["trivia_list"] = perguntas
    context.user_data["trivia_idx"] = 0
    context.user_data["score"] = 0

    # Envia a primeira pergunta
    await _enviar_pergunta(update, context)

async def _enviar_pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data["trivia_idx"]
    perguntas = context.user_data["trivia_list"]
    pergunta = perguntas[idx]

    # Teclado de opções
    teclado = [[opt] for opt in pergunta["opcoes"]]
    markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)

    # Envia a pergunta
    await update.message.reply_text(
        f"🧠 *{pergunta['pergunta']}*",
        parse_mode="Markdown",
        reply_markup=markup
    )

async def verificar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Se não estiver no meio de uma trivia, ignora
    if "trivia_list" not in context.user_data:
        return

    idx = context.user_data["trivia_idx"]
    perguntas = context.user_data["trivia_list"]
    pergunta = perguntas[idx]
    resposta_certa = pergunta["resposta_certa"]

    resposta_usuario = update.message.text.strip()

    # Comparação (insensível a maiúsculas)
    acertou = resposta_usuario.lower() == resposta_certa.lower()

    # Responde acerto/erro
    if acertou:
        context.user_data["score"] += 1
        await update.message.reply_text(f"✅ {random.choice(frases_acerto)}")
    else:
        await update.message.reply_text(
            f"❌ {random.choice(frases_erro)}\nA resposta certa era: *{resposta_certa}*",
            parse_mode="Markdown"
        )

    # Avança índice
    context.user_data["trivia_idx"] += 1

    # Próxima pergunta ou fim de trivia
    if context.user_data["trivia_idx"] < len(perguntas):
        await _enviar_pergunta(update, context)
    else:
        score = context.user_data["score"]
        total = len(perguntas)
        # Finaliza e remove teclado
        await update.message.reply_text(
            f"🏁 Quiz concluído! Você acertou {score}/{total}.",
            reply_markup=ReplyKeyboardRemove()
        )
        # Limpa estado
        for key in ("trivia_list", "trivia_idx", "score"):
            context.user_data.pop(key, None)