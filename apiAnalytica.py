from flask import Flask, request
import json
from age import getFormData, getIdades
from municipios import getMunicipioId, getBairros

url_ibge = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
ordena_ibge = '?orderBy=nome'

BAD_REQUEST = 400

app = Flask(__name__)

@app.route('/')
def index():
    return '''<h2>A API está ativa!</h2>
	<p>Acesse /age ou /municipio-bairros seguindo as instruções do README para
	utilizá-la</p>'''

@app.post("/age")
def age():
	form = getFormData(request)
	if form.get('erro'):
		return form['erro']

	nome, aniversario, dataFutura = form.values()

	idade, idadeFutura = getIdades(aniversario, dataFutura)
	
	resposta = {
		'quote': f'Olá, {nome}! Você tem {idade} anos e em {dataFutura.strftime("%d/%m/%y")} você terá {idadeFutura} anos.',
		'ageNow': idade,
		'ageThen': idadeFutura
	}

	return json.dumps(resposta)


@app.get('/municipio-bairros')
def municipio_bairros():
	resposta = dict()
	resposta['municipio'] = request.args.get('municipio')

	if not resposta['municipio']:
		return "ERRO: Parâmetro 'municipio' obrigatório", BAD_REQUEST

	idMunicipio, err = getMunicipioId(resposta['municipio'])
	if err:
		return err
	
	resposta['bairros'], err = getBairros(idMunicipio)
	if err: 
		return err

	return json.dumps(resposta)
