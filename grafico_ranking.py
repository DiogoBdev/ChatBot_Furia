import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import io
from telegram import InputFile, Update
from telegram.ext import ContextTypes

async def gerar_grafico_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Requisição ao site da HLTV para pegar o ranking
        html = requests.get(
            "https://www.hltv.org/ranking/teams",
            headers={"User-Agent": "Mozilla/5.0"}
        ).text
        soup = BeautifulSoup(html, "html.parser")

        equipes = []
        pontos = []
        for i, team in enumerate(soup.select(".ranked-team"), 1):
            name = team.select_one(".teamLine .name")
            if name:
                equipes.append(name.text.strip())
                points = team.select_one(".points").text.strip()
                pontos.append(int(points.replace(",", "")) if points != "sem dados" else 0)

            if len(equipes) >= 10:  # Limita a exibição para as 10 primeiras equipes
                break

        # Criação do gráfico de barras
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(equipes, pontos, color='gold')

        # Personaliza o gráfico para a FURIA
        if 'FURIA' in equipes:
            idx_furia = equipes.index('FURIA')
            ax.barh(idx_furia, pontos[idx_furia], color='blue')

        ax.set_xlabel('Pontos')
        ax.set_title('Ranking das Equipes - HLTV')

        # Salva o gráfico em um buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        # Envia a imagem para o Telegram
        await update.message.reply_photo(photo=InputFile(buf, filename="ranking_furia.png"))

    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro ao acessar o ranking: {str(e)}")
