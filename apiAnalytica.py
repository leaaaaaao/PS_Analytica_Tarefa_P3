from flask import Flask, request
from datetime import date
import requests
import json

url_ibge = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
ordena_ibge = '?orderBy=nome'

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<p>Hello, World!</p>"

@app.post("/age")
def age():
	nome = request.form.get('name', '')
	aniversario = request.form.get('birthdate', '')
	dataFutura = request.form.get('date', '')

	if not nome or not dataFutura or not aniversario: # TODO Outros erros
		return "Erro: Esperados três parâmetros. (Nome, data de nascimento e uma data futura)" # TODO detalhar
	
	try:
		aniversario = date.fromisoformat(aniversario)
		dataFutura = date.fromisoformat(dataFutura)
	except:
		return "Erro: Formato das datas inválido" # TODO detalhar

	hoje = date.today()

	if dataFutura < hoje:
		return "Erro: 'date' deve ser uma data no futuro" # TODO detalhar

	idade = hoje.year - aniversario.year
	aniversarioEsseAno = date.fromisoformat("{:04d}-{:02d}-{:02d}".format(hoje.year, aniversario.month, aniversario.day))
	if hoje < aniversarioEsseAno: # Ainda não fez aniversário esse ano
		idade -= 1

	idadeFutura = dataFutura.year - aniversario.year
	aniversarioFuturo = date.fromisoformat("{:04d}-{:02d}-{:02d}".format(dataFutura.year, aniversario.month, aniversario.day))
	if dataFutura < aniversarioFuturo: # Ainda não vai ter feito aniversário nesse ano
		idadeFutura -= 1


	resposta = dict()
	resposta['quote'] = f"Olá, {nome}! Você tem {idade} anos e em {dataFutura} você terá {idadeFutura} anos."
	resposta['ageNow'] = idade
	resposta['ageThen'] = idadeFutura

	return json.dumps(resposta)


@app.get('/municipio-bairros')
def municipio_bairros():
	resposta = dict()
	nomeMunicipio = request.args.get('municipio', '')
	if not nomeMunicipio:
		return "ERRO: Parâmetro 'municipio' obrigatório"
	
	resposta['municipio'] = nomeMunicipio

	municipios = requests.get(url_ibge)	# TODO Error handling
	municipios = municipios.json()
	bairros = []
	nomesBairros = []
	for municipio in municipios:
		if municipio['nome'] == nomeMunicipio:
			bairros = requests.get(url_ibge + f"/{municipio['id']}" + "/subdistritos" + ordena_ibge) # TODO Error handling
			bairros = bairros.json()
			break
	for bairro in bairros:
		nomesBairros.append(bairro['nome'])
	
	resposta['bairros'] = nomesBairros

	return json.dumps(resposta)
