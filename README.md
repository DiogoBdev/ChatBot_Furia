# 🤖 Bot da FURIA

Este projeto é um chatbot desenvolvido com Python e a biblioteca `python-telegram-bot`, criado especialmente para um **desafio da organização FURIA Esports**. O objetivo foi criar uma experiência interativa para fãs de CS:GO com funcionalidades informativas e divertidas.

## ✅ Projeto concluído com êxito!

---

## 🚀 Funcionalidades

- 🗞️ Últimas notícias sobre a FURIA
- 👥 Escalação atual do time
- 📆 Agenda de jogos
- 💡 Curiosidades sobre a organização
- 🧠 Trivia com perguntas sobre a FURIA
- 📈 Consulta ao ranking HLTV

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- BeautifulSoup4
- Feedparser
- Docker (para empacotamento e execução isolada)

---

## 🐳 Rodando com Docker

1. **Construa a imagem Docker:**

   ```bash
   docker build -t furia-bot .
   ```

2. **Execute o container (substitua `SEU_TOKEN_DO_BOT` pelo seu token real):**

   ```bash
   docker run --rm -e BOT_TOKEN=SEU_TOKEN_DO_BOT -it furia-bot
   ```

---

## 📁 Organização do Projeto

```
furia-bot/
├── bot.py                 # Arquivo principal do bot
├── handlers/              # Módulos para cada funcionalidade (trivia, ranking, etc)
│   └── trivia_handler.py
├── trivia.json            # Base de dados com perguntas da trivia
├── requirements.txt       # Dependências do projeto
├── Dockerfile             # Para build Docker
├── .env.example           # Exemplo de variável de ambiente
└── README.md              # Este arquivo
```

---

## 📦 Repositório

O código-fonte está disponível no GitHub:  
🔗 [github.com/DiogoBDev](https://github.com/DiogoBDev)

---

## 🏁 Conclusão

Este projeto foi desenvolvido com dedicação para um **desafio oficial da FURIA Esports**, sendo finalizado com sucesso e atendendo aos critérios propostos com excelência!

---