import json
import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

# Carrega as perguntas de trivia do arquivo JSON
with open("trivia.json", "r", encoding="utf-8") as f:
    perguntas = json.load(f)

# Frases de acerto e erro
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

# Função para iniciar a trivia
async def iniciar_trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = random.choice(perguntas)  # Escolhe uma pergunta aleatória
    
    # Cria as opções como botões
    teclado = [[opt] for opt in pergunta["opcoes"]]  # Cada opção em uma linha
    markup = ReplyKeyboardMarkup(teclado, one_time_keyboard=True, resize_keyboard=True)
    
    # Armazena a pergunta atual
    context.user_data["pergunta_atual"] = pergunta
    
    # Envia a pergunta com as opções de resposta como botões
    await update.message.reply_text(
        f"🧠 *{pergunta['pergunta']}*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Função para verificar a resposta do usuário
async def verificar_resposta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta_atual = context.user_data.get("pergunta_atual")
    if not pergunta_atual:
        return  # Se não houver pergunta atual, retorna

    resposta_usuario = update.message.text.strip()
    resposta_certa = pergunta_atual["resposta_certa"]

    # Verifica se a resposta do usuário é correta
    if resposta_usuario.lower() == resposta_certa.lower():
        await update.message.reply_text(f"✅ {random.choice(frases_acerto)}")
    else:
        await update.message.reply_text(
            f"❌ {random.choice(frases_erro)}\nA resposta certa era: *{resposta_certa}*",
            parse_mode="Markdown"
        )

    # Limpa o estado da pergunta atual
    context.user_data.clear()
    # Remove o teclado após a resposta
    await update.message.reply_text(
        "✅ Trivia finalizada!",
        reply_markup=ReplyKeyboardRemove()  # Remove o teclado de opções
    )