
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import os
import telebot
import logging

load_dotenv()

CHAVE_API = os.getenv('CHAVE_API', '')
bot =  telebot.TeleBot(CHAVE_API)

hora = datetime.now().strftime("%H:%M")

lista = []

async def noticias() -> bool:
    response = requests.get('https://www.jw.org/pt/noticias/')

    raw_html = response.text
    parsed_html = BeautifulSoup(raw_html, 'html.parser')

    data = parsed_html.select('div.synopsis')

    if data is not None:
        with open('news.txt', 'w+', encoding='utf-8') as arquivo:
            
            for d in data:
                noticia = (d.get_text(separator= ' -> ',strip=True))
                
                link = d.select_one('div.synopsis > div > h3 > a')
                if link is not None:
                    
                    texto = str(link['href'])
                    # print(data)
                    arquivo.write('\n\nNoticia:\n\n')
                    arquivo.write(noticia)
                    
                    
            arquivo.write('\n\nwww.jw.org/pt/noticias/') 
            print('Noticias Atualizadas')   
            return True
        logging.error('Falha ao gerar arquivo de Noticias')
        return False
    logging.error('Falha: Dados estão vazios - news')
    return False

async def texto_diario() -> bool:
    response = requests.get('https://wol.jw.org/pt/wol/h/r5/lp-t')

    raw_html = response.text
    parsed_html = BeautifulSoup(raw_html, 'html.parser')

    data = parsed_html.select_one('#dailyText')
    if data is not None:
        texto_dia = data.get_text()
        with open('texto.txt', 'w+', encoding='utf-8') as arquivo:
            
            arquivo.write(texto_dia)

        print('Texto diario atualizado')
        return True
    logging.error('Falha: Dados estão vazios - daily text')
    return False
        

@bot.message_handler(commands=['news'])
def envia_mensagem(mensagem):
    bot.send_message(mensagem.chat.id, 'Carregando...')
    # if hora == '08:00':
    # if asyncio.run(texto_diario()):
    #     with open('texto.txt', 'r', encoding='utf-8') as arquivo:
            
    #         bot.send_message(mensagem.chat.id, arquivo.read())
    if asyncio.run(noticias()):
        with open('news.txt', 'r', encoding='utf-8') as arquivo:
            
            bot.send_message(mensagem.chat.id, arquivo.read())
        return True
    return False

def send_in_our(mensagem):
    return True
        

@bot.message_handler(func=send_in_our)
def recebe_mensagem(mensagem,):
    bot.reply_to(mensagem, '/news')

bot.polling()