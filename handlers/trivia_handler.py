import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import json

def carregar_perguntas():
    with open('data/trivia_questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def iniciar_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    perguntas = carregar_perguntas()
    random.shuffle(perguntas)
    context.user_data['trivia'] = perguntas
    context.user_data['idx'] = 0
    context.user_data['score'] = 0

    await enviar_pergunta(update, context)

async def enviar_pergunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    idx = context.user_data['idx']
    perguntas = context.user_data['trivia']
    pergunta_obj = perguntas[idx]

    teclado = [[f"{i+1}. {opt}"] for i, opt in enumerate(pergunta_obj['opcoes'])]
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)

    texto = f"{pergunta_obj['pergunta']}\n\n" + \
            "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(pergunta_obj['opcoes'])])

    await update.message.reply_text(texto, reply_markup=markup)

async def verificar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if 'trivia' not in context.user_data:
        return

    texto = update.message.text.strip()
    idx = context.user_data['idx']
    perguntas = context.user_data['trivia']
    pergunta_obj = perguntas[idx]


    correta = pergunta_obj['resposta']

    if isinstance(correta, int):
        correta_texto = pergunta_obj['opcoes'][correta]
    else:
        correta_texto = str(correta)

    if texto and texto[0].isdigit():
        escolha = int(texto.split('.')[0]) - 1
        resposta_texto = pergunta_obj['opcoes'][escolha] if 0 <= escolha < len(pergunta_obj['opcoes']) else None
    else:
        resposta_texto = texto

    if resposta_texto == correta_texto:
        context.user_data['score'] += 1
        await update.message.reply_text("✅ Resposta certa!")
    else:
        await update.message.reply_text(f"❌ Resposta errada. A resposta certa era: {correta_texto}")


    context.user_data['idx'] += 1
    if context.user_data['idx'] < len(perguntas):
        await enviar_pergunta(update, context)
    else:

        score = context.user_data['score']
        total = len(perguntas)
        await update.message.reply_text(f"🏁 Quiz concluído! Você acertou {score}/{total}.")

        for key in ['trivia', 'idx', 'score']:
            context.user_data.pop(key, None)