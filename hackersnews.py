import requests 
from bs4 import BeautifulSoup 
from creds import headers, url
import csv 


def respuesta():
	r = requests.get(url, headers = headers)
	if r.status_code == 200:
		print("respuesta exitosa")
		return r.text 
	else:
		print("error en la solicitud")

html = respuesta()
score = 0
comentarios = 0

def obtener_lista():
	lista = []
	if html:
		soup = BeautifulSoup(html, "html.parser")
		noticias = soup.find_all('tr', class_="athing")
		for noticia in noticias:
			titulo = noticia.find('span', class_='titleline').text
			url = noticia.find('span', class_='titleline').find('a').get('href')
			syc = noticia.find_next_sibling()
			try:
				score_tag = syc.find("span", class_ = "score").text
				score_clean = score_tag.replace('points', '').strip()
				score = int(score_clean)
			except Exception as e:
				print(e)
				print("Sin score")
			try: 
				coments_tag = syc.find(attrs={'class': 'subline'}).text
				info = coments_tag.split('|')
				coments= info[-1]
				coment_clean= coments.replace('comments', '').strip()
				comentarios = int(coment_clean)
			except:
				print("sin comentarios")

			lista.append({
				"titulo": titulo, 
				"url": url,
				"score": score, 
				"comentarios": comentarios
				})
		return lista

Las_noticias = obtener_lista()

with open("noticias.csv", "w", newline='', encoding='utf-8') as f:
	writer = csv.DictWriter(f, fieldnames=["titulo", "url", "score", "comentarios"])
	writer.writeheader()
	writer.writerows(Las_noticias)
