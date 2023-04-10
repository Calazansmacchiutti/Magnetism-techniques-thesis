import numpy as np

# Valores dos momentos magnéticos dos íons
Co2_plus = np.array([3.87, 1.73])
Co3_plus = np.array([4.89, 2.88])
Mn3_plus = np.array([4.89, 2.88])
Mn4_plus = np.array([3.87])

# Limites das porcentagens a e b
limite_min = 0.3
limite_max = 0.6

# Valor de Meff fornecido
valor_meff = 5.44

# Função para calcular o momento magnético efetivo
def calcular_meff(a, b):
    meff = np.sqrt(a * (Co2_plus[0]**2) + (1-a) * (Co3_plus[0]**2) + b * (Mn4_plus[0]**2) + (1-b) * (Mn3_plus[0]**2))
    return meff

melhores_combinacoes = [] # lista para armazenar as melhores combinações
melhores_erros = [] # lista para armazenar os melhores erros

# Loop para realizar as combinações dos valores de Co2_plus, Co3_plus e Mn3_plus
for co2 in Co2_plus:
    for co3 in Co3_plus:
        for mn3 in Mn3_plus:
            for b in np.arange(limite_min, limite_max + 0.01, 0.01):
                for a in np.arange(max(limite_min, b - 0.05), min(limite_max, b + 0.05) + 0.01, 0.01):
                    # Testa os valores de a e b
                    meff = np.sqrt(a * (co2**2) + (1-a) * (co3**2) + b * (Mn4_plus[0]**2) + (1-b) * (mn3**2))
                    erro_percentual = np.abs((meff - valor_meff) / valor_meff) * 100
                    
                    # aceita erro de no máximo 5%
                    if erro_percentual <= 5: 
                        # Armazena a combinação, o erro e os valores dos íons na lista de melhores combinações
                        melhores_combinacoes.append((a, b, co2, co3, mn3))
                        melhores_erros.append(erro_percentual)

# Ordena as melhores combinações com base nos erros em ordem crescente
melhores_combinacoes = [melhores_combinacoes[i] for i in np.argsort(melhores_erros)]
melhores_erros.sort()

# Imprime as 5 melhores combinações e seus respectivos erros
print("As 5 melhores combinações de a e b são:")
for i in range(10):
    print("Possibilidade {}: coef. a = {:.2f}, b = {:.2f},     ions Co2+ = {:.2f}, Co3_plus = {:.2f}, Mn3_plus = {:.2f}, Erro = {:.2f}%".format(
        i+1, melhores_combinacoes[i][0], melhores_combinacoes[i][1], melhores_combinacoes[i][2],
        melhores_combinacoes[i][3], melhores_combinacoes[i][4], melhores_erros[i]))
