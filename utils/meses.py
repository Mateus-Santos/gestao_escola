#Função para retornar número do mês:
def mes_numero(mes):
  mes = str.lower(mes)
  meses = {
    'janeiro': 1,
    'fevereiro': 2,
    'março': 3,
    'abril': 4,
    'maio': 5,
    'junho': 6,
    'julho': 7,
    'agosto': 8,
    'setembro': 9,
    'outubro': 10,
    'novembro': 11,
    'dezembro': 12,
  }
  return meses[mes]

#Função para retornar o nome do mês:
def numero_mes(n_mes):
  mes = str.lower(n_mes)
  meses = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro',
  }
  return meses[mes]