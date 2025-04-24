import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import os

def gerar_grafico_ranking(path_saida="ranking_furia.png"):
    url = "https://www.hltv.org/ranking/teams"
    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")

    times = []
    pontos = []

    for team in soup.select(".ranked-team")[:10]:
        nome = team.select_one(".name").text.strip()
        pts = team.select_one(".points").text.strip().replace(" points", "")
        times.append(nome)
        pontos.append(int(pts))

    cores = ["#000000" if "FURIA" not in nome.upper() else "#00ff00" for nome in times]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(times[::-1], pontos[::-1], color=cores[::-1])
    plt.title("Top 10 Ranking HLTV - Destaque para FURIA", fontsize=14, fontweight="bold", color="#000000")
    plt.xlabel("Pontos", fontsize=12)
    plt.tight_layout()

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 10, bar.get_y() + bar.get_height()/2, str(width), va='center', fontsize=10)

    plt.savefig(path_saida, dpi=150)
    plt.close()
    return path_saida
