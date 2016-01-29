# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime

def verificaTopico(id):
	conn = sqlite3.connect('topicos.db')
	conn.text_factory = str
	c = conn.cursor()
	c.execute("create table if not exists topicos (data text, id text)")
	c.execute("select 1 from topicos where id = ?", (id,))
	data = c.fetchall()
	jaVerificado = True
	if len(data) == 0:
		jaVerificado = False
		c.execute('insert into topicos values(?, ?)', (datetime.datetime.now(), id))
		conn.commit()
	conn.close()
	return jaVerificado

def gafanhotoAdrenaline(spyList, arquivoSaida):	
	#na black friday o forum separa as promoções em outras áreas
	links = ['http://adrenaline.uol.com.br/forum/forums/for-sale.221/']
	threadsReplace = "http://adrenaline.uol.com.br/forum/threads"
	for link in links:
		r = requests.get(link)
		soup = BeautifulSoup(r.text, "html.parser")
		topics = soup.find_all('li', class_='discussionListItem')
		for topic in topics:						
			if any(substring.upper() in str(topic).upper() for substring in spyList):								
				if verificaTopico(str(topic.get("id"))) == False:
					text = str(topic.find("h3"))
					arquivoSaida.write(text.replace("threads", threadsReplace))

def gafanhotoMob(spyList, arquivoSaida):	
	link = "http://www.hardmob.com.br/promocoes/"	
	r = requests.get(link)
	soup = BeautifulSoup(r.text, "html.parser")
	topics = soup.find_all("h3", class_="threadtitle")
	for topic in topics:
		if any(substring.upper() in str(topic).upper() for substring in spyList):
			if verificaTopico(str(topic.find("a", class_="title").get("id"))) == False:
				text = str(topic)
				arquivoSaida.write(text)
				
arquivoSaida = open("promocoes.html", "w")
arquivoSaida.write("<meta charset='utf-8' />")
with open('gafanhoto.spy') as spyList:
    lines = spyList.read().splitlines()
gafanhotoAdrenaline(lines, arquivoSaida)
gafanhotoMob(lines, arquivoSaida)
arquivoSaida.close()
