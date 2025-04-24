from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import feedparser

# Carregar variáveis de ambiente
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Menu principal
main_menu = [
    ["1️⃣ Últimas Notícias", "2️⃣ Escalação"],
    ["3️⃣ Agenda de Jogos", "4️⃣ Curiosidades"],
    ["5️⃣ Trivia", "6️⃣ Ranking"]
]
markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# Últimas notícias da FURIA via RSS
def buscar_noticias_furia():
    feed = feedparser.parse("https://www.hltv.org/rss/news")
    noticias = []
    for entry in feed.entries:
        if "FURIA" in entry.title.upper():
            noticias.append(f"📰 {entry.title}\n🔗 {entry.link}")
        if len(noticias) >= 5:
            break
    return noticias or ["📭 Nenhuma notícia recente da FURIA encontrada."]

# Ranking da FURIA no HLTV
def buscar_ranking_furia():
    url = "https://www.hltv.org/ranking/teams"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"⚠️ Erro ao acessar o ranking: {str(e)}"

    soup = BeautifulSoup(response.text, "html.parser")
    equipes = soup.select("div.ranked-team.standard-box")

    for idx, equipe in enumerate(equipes, start=1):
        nome_elem = equipe.select_one(".teamLine .name")
        pontos_elem = equipe.select_one(".points")
        if nome_elem and "FURIA" in nome_elem.text.upper():
            nome = nome_elem.text.strip()
            pontos = pontos_elem.text.strip() if pontos_elem else "sem dados"
            return f"🏆 A FURIA está em {idx}º lugar no ranking HLTV com {pontos}!"

    return "📉 A FURIA não está entre as 30 primeiras do ranking HLTV atualmente."

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá, fã da FURIA! O que você quer saber hoje?",
        reply_markup=markup
    )

# Menu
async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if "Últimas Notícias" in msg:
        await update.message.reply_text("📰 Buscando as últimas notícias da FURIA...")
        noticias = buscar_noticias_furia()
        for noticia in noticias:
            await update.message.reply_text(noticia)

    elif "Escalação" in msg:
        await update.message.reply_text("🎮 Jogadores da FURIA:\n- KSCERATO\n- yuurih\n- FalleN...")

    elif "Agenda" in msg:
        await update.message.reply_text("📅 Próximo jogo: FURIA vs. NAVI - 26/04 às 15h")

    elif "Curiosidades" in msg:
        await update.message.reply_text("🔥 Você sabia? A FURIA foi a 1ª equipe BR no top 3 do ranking HLTV em 2020.")

    elif "Trivia" in msg:
        await update.message.reply_text("❓ Trivia em breve! Prepare-se para testar seus conhecimentos.")

    elif "Ranking" in msg:
        await update.message.reply_text("📊 Consultando ranking da FURIA...")
        ranking = buscar_ranking_furia()
        await update.message.reply_text(ranking)

# Criar app
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

# Rodar bot
print("🤖 Bot da FURIA rodando...")
app.run_polling()