from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import requests
import feedparser
from bs4 import BeautifulSoup
from handlers.trivia_handler import iniciar_trivia, verificar_resposta

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

main_menu = [
    ["🗞️ Últimas Notícias", "👥 Escalação"],
    ["📆 Agenda de Jogos", "💡 Curiosidades"],
    ["🧠 Trivia", "📈 Ranking"]
]
markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

def buscar_noticias_furia():
    feed = feedparser.parse("https://www.hltv.org/rss/news")
    noticias = [f"📰 {entry.title}\n🔗 {entry.link}" for entry in feed.entries if "FURIA" in entry.title.upper()]
    return noticias[:5] or ["📭 Nenhuma notícia recente da FURIA encontrada."]

def buscar_ranking_furia():
    try:
        html = requests.get("https://www.hltv.org/ranking/teams", headers={"User-Agent": "Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")
        for i, team in enumerate(soup.select(".ranked-team"), 1):
            name = team.select_one(".teamLine .name")
            if name and "FURIA" in name.text.upper():
                pontos = team.select_one(".points").text if team.select_one(".points") else "sem dados"
                return f"🏆 A FURIA está em {i}º lugar no ranking HLTV com {pontos}!"
    except Exception as e:
        return f"⚠️ Erro ao acessar ranking: {str(e)}"
    return "📉 A FURIA não está entre as 30 primeiras do ranking HLTV."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Seja bem-vindo ao *Bot da FURIA*!\n\nO que você quer saber hoje, FURIOSO? 👊",
        parse_mode="Markdown",
        reply_markup=markup
    )

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if "Últimas Notícias" in msg:
        for n in buscar_noticias_furia():
            await update.message.reply_text(n)
    elif "Escalação" in msg:
        await update.message.reply_text("👥 Escalação atual:\n- FalleN\n- arT\n- yuurih\n- KSCERATO\n- chelo")
    elif "Agenda" in msg:
        await update.message.reply_text("📆 Próximo jogo: FURIA vs. NAVI - 26/04 às 15h")
    elif "Curiosidades" in msg:
        await update.message.reply_text("💡 A FURIA foi a 1ª equipe BR no top 3 do HLTV em 2020.")
    elif "Trivia" in msg:
        await iniciar_trivia(update, context)
    elif "Ranking" in msg:
        await update.message.reply_text(buscar_ranking_furia())

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, verificar_resposta))

print("🤖 Bot da FURIA rodando com estilo!")
app.run_polling()