from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import requests
import feedparser
from bs4 import BeautifulSoup
from handlers.trivia_handler import iniciar_trivia, verificar_resposta
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from grafico_ranking import gerar_grafico_ranking

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
    noticias = [
        f"📰 {entry.title}\n🔗 {entry.link}"
        for entry in feed.entries
        if "FURIA" in entry.title.upper()
    ]
    return noticias[:5] or ["📭 Nenhuma notícia recente da FURIA encontrada."]

def gerar_grafico_ranking():
    teams = ['Vitality', 'FaZe', 'G2', 'FURIA', 'NAVI', 'Cloud9', 'Astralis', 'Liquid', 'ENCE', 'Heroic']
    points = [950, 910, 875, 830, 800, 790, 760, 730, 710, 690]

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(teams[::-1], points[::-1], color=['#ffffff' if team != 'FURIA' else '#FF0000' for team in teams[::-1]])

    for bar, team in zip(bars, teams[::-1]):
        if team == 'FURIA':
            bar.set_color('#FF0000')

    ax.set_title('Top 10 Times - Ranking HLTV', fontsize=16, color='white', pad=20)
    ax.set_xlabel('Pontos', fontsize=12, color='white')
    ax.tick_params(colors='white', labelsize=10)
    fig.tight_layout()

    logo_path = "furia_logo_simples.png"
    if os.path.exists(logo_path):
        logo = mpimg.imread(logo_path)
        fig.figimage(logo, xo=fig.bbox.xmax - 150, yo=fig.bbox.ymax - 100, alpha=0.6, zorder=10)

    output_path = "grafico_furia_rank_custom.png"
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close()
    return output_path

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
        await update.message.reply_text(
            "👥 Escalação atual:\n- FalleN\n- arT\n- yuurih\n- KSCERATO\n- chelo"
        )
    elif "Agenda" in msg:
        await update.message.reply_text("📆 Próximo jogo: FURIA vs. NAVI - 26/04 às 15h")
    elif "Curiosidades" in msg:
        await update.message.reply_text("💡 A FURIA foi a 1ª equipe BR no top 3 do HLTV em 2020.")
    elif "Trivia" in msg:
        await iniciar_trivia(update, context)
    elif "Ranking" in msg:
        await update.message.reply_text("⏳ Gerando gráfico de ranking, segura aí...")
        try:
            imagem = gerar_grafico_ranking()
            with open(imagem, "rb") as img:
                await update.message.reply_photo(photo=img, caption="📊 Ranking HLTV atualizado!")
        except Exception as e:
            await update.message.reply_text(f"⚠️ Erro ao gerar ranking: {e}")

async def texto_geral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("trivia_list"):
        await verificar_resposta(update, context)
    else:
        await handle_response(update, context)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, texto_geral))

print("🤖 Bot da FURIA rodando!")
app.run_polling()
