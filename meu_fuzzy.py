import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definindo as variáveis de entrada
metragem = ctrl.Antecedent(np.arange(110, 1001, 1), 'metragem')
distancia_av = ctrl.Antecedent(np.arange(0, 5001, 1), 'distancia_av')
distancia_praia = ctrl.Antecedent(np.arange(0, 5001, 1), 'distancia_praia')

# Definindo a variável de saída
preco = ctrl.Consequent(np.arange(42400, 3000000, 1), 'preco')

# Definindo as funções de pertinência para metragem
metragem['pequeno'] = fuzz.trimf(metragem.universe, [110, 110, 400])
metragem['medio'] = fuzz.trimf(metragem.universe, [300, 500, 700])
metragem['grande'] = fuzz.trimf(metragem.universe, [600, 1000, 5000])

# Definindo as funções de pertinência para distancia_av
distancia_av['perto'] = fuzz.trimf(distancia_av.universe, [0, 0, 500])
distancia_av['medio'] = fuzz.trimf(distancia_av.universe, [500, 1000, 1500])
distancia_av['longe'] = fuzz.trimf(distancia_av.universe, [1500, 5000, 5000])

# Definindo as funções de pertinência para distancia_praia
distancia_praia['perto'] = fuzz.trimf(distancia_praia.universe, [0, 0, 800])
distancia_praia['medio'] = fuzz.trimf(distancia_praia.universe, [800, 1150, 1500])
distancia_praia['longe'] = fuzz.trimf(distancia_praia.universe, [1500, 5000, 5000])

# Definindo as funções de pertinência para preco
preco['baixo'] = fuzz.trimf(preco.universe, [42400, 42400, 400000])
preco['medio'] = fuzz.trimf(preco.universe, [480000, 650000, 700000])
preco['alto'] = fuzz.trimf(preco.universe, [700000, 1400000, 1400000])

# Definindo as regras fuzzy
rules = [
    ctrl.Rule(metragem['pequeno'] & distancia_av['perto'] & distancia_praia['perto'], preco['alto']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['perto'] & distancia_praia['medio'], preco['medio']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['perto'] & distancia_praia['longe'], preco['medio']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['medio'] & distancia_praia['perto'], preco['medio']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['medio'] & distancia_praia['medio'], preco['baixo']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['medio'] & distancia_praia['longe'], preco['baixo']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['longe'] & distancia_praia['perto'], preco['medio']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['longe'] & distancia_praia['medio'], preco['baixo']),
    ctrl.Rule(metragem['pequeno'] & distancia_av['longe'] & distancia_praia['longe'], preco['baixo']),
    ctrl.Rule(metragem['medio'] & distancia_av['perto'] & distancia_praia['perto'], preco['alto']),
    ctrl.Rule(metragem['medio'] & distancia_av['perto'] & distancia_praia['medio'], preco['medio']),
    ctrl.Rule(metragem['medio'] & distancia_av['perto'] & distancia_praia['longe'], preco['medio']),
    ctrl.Rule(metragem['medio'] & distancia_av['medio'] & distancia_praia['perto'], preco['medio']),
    ctrl.Rule(metragem['medio'] & distancia_av['medio'] & distancia_praia['medio'], preco['medio']),
    ctrl.Rule(metragem['medio'] & distancia_av['medio'] & distancia_praia['longe'], preco['baixo']),
    ctrl.Rule(metragem['medio'] & distancia_av['longe'] & distancia_praia['perto'], preco['medio']),
    ctrl.Rule(metragem['medio'] & distancia_av['longe'] & distancia_praia['medio'], preco['baixo']),
    ctrl.Rule(metragem['medio'] & distancia_av['longe'] & distancia_praia['longe'], preco['baixo']),
    ctrl.Rule(metragem['grande'] & distancia_av['perto'] & distancia_praia['perto'], preco['alto']),
    ctrl.Rule(metragem['grande'] & distancia_av['perto'] & distancia_praia['medio'], preco['alto']),
    ctrl.Rule(metragem['grande'] & distancia_av['perto'] & distancia_praia['longe'], preco['medio']),
    ctrl.Rule(metragem['grande'] & distancia_av['medio'] & distancia_praia['perto'], preco['alto']),
    ctrl.Rule(metragem['grande'] & distancia_av['medio'] & distancia_praia['medio'], preco['alto']),
    ctrl.Rule(metragem['grande'] & distancia_av['medio'] & distancia_praia['longe'], preco['medio']),
    ctrl.Rule(metragem['grande'] & distancia_av['longe'] & distancia_praia['perto'], preco['medio']),
    ctrl.Rule(metragem['grande'] & distancia_av['longe'] & distancia_praia['medio'], preco['medio']),
    ctrl.Rule(metragem['grande'] & distancia_av['longe'] & distancia_praia['longe'], preco['medio']),
]

# Criando o sistema de controle
preco_ctrl = ctrl.ControlSystem(rules)
precificacao = ctrl.ControlSystemSimulation(preco_ctrl)

# Função para predizer o preço de um terreno com base na metragem, distancia_av, e distancia_praia
def predizer_preco(metragem_val, distancia_av_val, distancia_praia_val):
    precificacao.input['metragem'] = metragem_val
    precificacao.input['distancia_av'] = distancia_av_val
    precificacao.input['distancia_praia'] = distancia_praia_val
    precificacao.compute()
    return precificacao.output['preco']

# Testando o sistema fuzzy com exemplos coletados
terrenos = [
    {'metragem': 493.5, 'distancia_av': 989, 'distancia_praia': 443, 'preco_real': 600000},
    {'metragem': 1000, 'distancia_av': 2400, 'distancia_praia': 1200, 'preco_real': 600000},
    {'metragem': 300, 'distancia_av': 1260, 'distancia_praia': 1830, 'preco_real': 144500},
    {'metragem': 262.5, 'distancia_av': 1560, 'distancia_praia': 1120, 'preco_real': 212000},
    {'metragem': 360, 'distancia_av': 778, 'distancia_praia': 2520, 'preco_real': 220000},
    {'metragem': 1000, 'distancia_av': 600, 'distancia_praia': 2200, 'preco_real': 850000},
    {'metragem': 750, 'distancia_av': 300, 'distancia_praia': 900, 'preco_real': 1050000},
    {'metragem': 650, 'distancia_av': 315, 'distancia_praia': 1550, 'preco_real': 750000},
    {'metragem': 250, 'distancia_av': 2500, 'distancia_praia': 4260, 'preco_real': 228000},
    {'metragem': 500, 'distancia_av': 243, 'distancia_praia': 1510, 'preco_real': 650000},
    {'metragem': 250, 'distancia_av': 164, 'distancia_praia': 1270, 'preco_real': 480000},
    {'metragem': 1200, 'distancia_av': 475, 'distancia_praia': 10, 'preco_real': 800000},
    {'metragem': 300, 'distancia_av': 1380, 'distancia_praia': 1260, 'preco_real': 170000},
    {'metragem': 434, 'distancia_av': 1180, 'distancia_praia': 1770, 'preco_real': 278568},
    {'metragem': 300, 'distancia_av': 1200, 'distancia_praia': 1750, 'preco_real': 286200},
    {'metragem': 300, 'distancia_av': 1050, 'distancia_praia': 266, 'preco_real': 350000},
    {'metragem': 250, 'distancia_av': 1520, 'distancia_praia': 300, 'preco_real': 450000},
    #{'metragem': 315, 'distancia_av': 1510, 'distancia_praia': 1400, 'preco_real': 160000} #pagina 7 procure-se imovel terrenos cassino
]

precos_reais = []
precos_estimados = []

for terreno in terrenos:
    preco_estimado = predizer_preco(terreno['metragem'], terreno['distancia_av'], terreno['distancia_praia'])
    precos_reais.append(terreno['preco_real'])
    precos_estimados.append(preco_estimado)
    print(f"Metragem: {terreno['metragem']}m², Distância à Avenida: {terreno['distancia_av']}m, Distância à Praia: {terreno['distancia_praia']}m, Preço Real: R${terreno['preco_real']}, Preço Estimado: R${preco_estimado:.0f}")

# Calculando a correlação
correlacao = np.corrcoef(precos_reais, precos_estimados)[0, 1]

# Gerando o gráfico de correlação
plt.figure(figsize=(10, 6))
plt.scatter(precos_reais, precos_estimados, color='blue')
plt.plot([min(precos_reais), max(precos_reais)], [min(precos_reais), max(precos_reais)], color='red', linestyle='--')
plt.title('Correlação entre Preços Reais e Estimados')
plt.xlabel('Preços Reais')
plt.ylabel('Preços Estimados')
plt.grid(True)
plt.show()

print(f"Índice de correlação: {correlacao:.2f}")
