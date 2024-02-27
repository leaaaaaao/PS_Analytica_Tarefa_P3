# Tarefa de Programação - P3
## Descrição
A proposta foi desenvolver uma API com duas rotas, descritas em mais detalhes na seção de rotas. A implementação foi feita na linguagem Python, utilizando o framework Flask.

## Dependências e uso
Para iniciar a API, é necessário ter o Python e o Flask instalados em sua máquina. Para instalar o Flask, faça
```sh
pip install Flask
```

No terminal. A instalação do Python pode variar dependendo do SO.

Com as dependências instaladas, rode o comando
```
flask --app apiAnalytica run
```

Após isso, a API deve estar ativa e escutando em http://127.0.0.1:5000.

## Rotas
### GET
```/municipio-bairros```
Para essa rota, as requisições devem obrigatoriamente conter o seguinte parâmetro de query:
```
municipio=NOME-DO-MUNICIPIO
```

Caso não contenha, será retornada uma mensagem de erro alertando isso ao usuário. No caso de uma requisição correta, o retorno deverá ser um JSON no formato:
```json
{
    "municipio": "NOME-DO-MUNICIPIO",
    "bairros": [
        "NOME DO BAIRRO 1",
        "NOME DO BAIRRO 2",
        "NOME DO BAIRRO 3",
        ...
    ]
}
```
Ou uma mensagem informando que o município não foi encontrado na base do IBGE. (O nome deve ser escrito exatamente como registrado na base).

No JSON, _NOME-DO-MUNICIPIO_ é o valor passado no parâmetro _municipio_ e _NOME DO BAIRRO X_ são bairros desse município, segundo a API do IBGE.


### POST
```/age```

Requisições para essa rota devem conter no body um JSON com o seguinte formato:
```json
{
    "name": "Nome Sobrenome",
    "birthdate": "YYYY-MM-DD",
    "date": "YYYY-MM-DD"
}
```
Observe que _name_ não precisa ter sobrenome, ou seja, não é obrigatório ter espaço. Além disso, as datas _date_ e _birthdate_ devem ser fornecidas no formato ISO 8601, em um dos padrões abaixo.
```json
"YYYY-MM-DD"
"YYYYMMDD"
"YYYYWWWD"
```
Onde Y é um dígito de 0 a 9 referente ao ano, M ao mês e D ao dia. Já em WWW, o primeiro W seria o caracter 'W' literal, e os demais, o número de semanas passadas desde o início do ano. Além disso, _date_ deve ser uma data futura. No caso de alguma das regras ser desrespeitadas, é retornada uma mensagem de erro descrevendo o problema.


No caso de uma requisição correta, o retorno também será um JSON, com o formato:
```json
{
    quote: "Olá, Nome Sobrenome! Você tem X anos e em DD/MM/YYYY você terá Y anos.",
    ageNow: X,
    ageThen: Y
}
```

Onde "Nome Sobrenome" é o nome passado como parâmetro no body da requisição, _X_ é a idade que alguém nascido em _birthdate_ tem hoje, _DD/MM/YYYY_ é _date_, a data futura passada no body da requisição, e _Y_ é a idade que essa pessoa terá em _date_. Observe que _date_ é passada em um formato (YYYY-MM-DD) e retornada em outro (DD/MM/YYYY).

## Implementação
Para a rota de municipios, o programa realiza requisições à api de localidades do IBGE, disponível em https://servicodados.ibge.gov.br/api/v1/localidades. Mais especificamente, foram utilizadas as rotas ```/municipios```, para listar todos os municípios, e ```/municipios/{idMunicipio}/subdistritos```, para listar os bairros. Mais informações disponíveis no link.

Já para a rota de idade, utilizei a biblioteca "datetime" do Python para validar e manipular as datas. Optei por não calcular a idade usando subtração de datas, pois o retorno dessa operação nessa biblioteca é uma diferença em dias, tornando difícil calcular a idade com precisão em certos "casos de borda", considerando anos bissextos. Assim, o método usado foi calcular a diferença apenas entre os anos, e depois checar se o aniversário da pessoa nesse ano já passou, ajustando a idade conforme a situação (subtrai-se 1 do resultado encontrado caso o aniversário ainda não tenha chegado).