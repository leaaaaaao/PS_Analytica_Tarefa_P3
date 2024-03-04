from datetime import date

BAD_REQUEST = 400

def getFormData(request):
    nome = request.form.get('name')
    aniversario = request.form.get('birthdate')
    dataFutura = request.form.get('date')

    if not nome or not dataFutura or not aniversario:
        return {'erro': ('Erro: Esperados três parâmetros. (Nome, data de nascimento e uma data futura. Consulte o README para mais detalhes sobre a formatação.)', BAD_REQUEST)}

    try:
        aniversario = date.fromisoformat(aniversario)
        dataFutura = date.fromisoformat(dataFutura)
    except:
        return {'erro': ('Erro: Formato das datas inválido. As datas devem seguir o padrão ISO 8601. Mais detalhes no README.', BAD_REQUEST)}

    hoje = date.today()
    if dataFutura < hoje:
        return {'erro': ('Erro: \'date\' deve ser uma data no futuro.', BAD_REQUEST)}

    return {'nome': nome, 'aniversario': aniversario, 'dataFutura': dataFutura}


def getIdades(aniversario, dataFutura):
    hoje = date.today()

    idade = hoje.year - aniversario.year
    aniversarioEsseAno = date.fromisoformat("{:04d}-{:02d}-{:02d}".format(hoje.year, aniversario.month, aniversario.day))
    if hoje < aniversarioEsseAno: # Ainda não fez aniversário esse ano
        idade -= 1

    idadeFutura = dataFutura.year - aniversario.year
    aniversarioFuturo = date.fromisoformat("{:04d}-{:02d}-{:02d}".format(dataFutura.year, aniversario.month, aniversario.day))
    if dataFutura < aniversarioFuturo: # Ainda não vai ter feito aniversário nesse ano
        idadeFutura -= 1
    
    return idade, idadeFutura