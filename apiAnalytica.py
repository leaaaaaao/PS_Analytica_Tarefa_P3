from flask import Flask, request
import json
from age import getFormData, getIdades
from municipios import getMunicipioId, getBairros

url_ibge = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
ordena_ibge = '?orderBy=nome'

app = Flask(__name__)

@app.post("/age")
def age():
	form = getFormData(request)
	if form.get('erro'):
		return form['erro']

	nome, aniversario, dataFutura = form.values()

	idade, idadeFutura = getIdades(aniversario, dataFutura)
	
	resposta = {
		'quote': f'Olá, {nome}! Você tem {idade} anos e em {dataFutura} você terá {idadeFutura} anos.',
		'ageNow': idade,
		'ageThen': idadeFutura
	}

	return json.dumps(resposta)


@app.get('/municipio-bairros')
def municipio_bairros():
	resposta = dict()
	resposta['municipio'] = request.args.get('municipio')

	if not resposta['municipio']:
		return "ERRO: Parâmetro 'municipio' obrigatório"

	idMunicipio, err = getMunicipioId(resposta['municipio'])
	if err:
		return err
	
	resposta['bairros'], err = getBairros(idMunicipio)
	if err: 
		return err

	return json.dumps(resposta)
