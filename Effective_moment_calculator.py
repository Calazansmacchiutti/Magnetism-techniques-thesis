import numpy as np

# Valores dos momentos magnéticos dos íons em High spin/Low Spin
Co2_plus = np.array([3.87, 1.73])
Co3_plus = np.array([4.89, 2.88])
Mn3_plus = np.array([4.89, 2.88])
Mn4_plus = np.array([3.87])

# Limites dos valores dos coeficientes a e b
limite_min = 0.3
limite_max = 0.7

# Valor de Meff obtido do fitlinear do inverso da susceptibilidade magnética
valor_meff = 4.73

# Equação do momento efetivo total definido como função
def calcular_meff(a, b):
    meff = np.sqrt(a * (Co2_plus[0]**2) + (1-a) * (Co3_plus[0]**2) + b * (Mn4_plus[0]**2) + (1-b) * (Mn3_plus[0]**2))
    return meff

melhor_valor_meff = float('inf') # inicializando com um valor infinito
melhor_a = None
melhor_b = None

# Loop para realizar as combinações dos valores de Co2_plus, Co3_plus e Mn3_plus
for co2 in Co2_plus:
    for co3 in Co3_plus:
        for mn3 in Mn3_plus:
            for b in np.arange(limite_min, limite_max + 0.01, 0.01):
                for a in np.arange(max(limite_min, b - 0.05), min(limite_max, b + 0.05) + 0.01, 0.01):
                    # Testa os valores de a e b
                    meff = np.sqrt(a * (co2**2) + (1-a) * (co3**2) + b * (Mn4_plus[0]**2) + (1-b) * (mn3**2))
                    erro_percentual = np.abs((meff - valor_meff) / valor_meff) * 100

                    if erro_percentual <= 5: # aceita erro de no máximo 5%
                        if erro_percentual < melhor_valor_meff:
                            melhor_valor_meff = erro_percentual
                            melhor_a = a
                            melhor_b = b
                            melhor_co2 = co2
                            melhor_co3 = co3
                            melhor_mn3 = mn3

print("Melhor valor de Co2+: {:.2f}".format(melhor_co2))
print("Melhor valor de Co3+: {:.2f}".format(melhor_co3))
print("Melhor valor de Mn3+: {:.2f}".format(melhor_mn3))
print("Melhor valor do coef. a: {:.2f}".format(melhor_a))
print("Melhor valor do coef. b: {:.2f}".format(melhor_b))
