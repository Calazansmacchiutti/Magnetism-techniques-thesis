import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.stats import linregress

# Dados de entrada fornecidos
dados_x = np.array([72.2, 80.2, 84.2, 90.2, 94.2])
dados_y = np.array([0.01, 0.003, 0.001, 3.0003E-4, 1E-4])

# Aplicando log-transform nos dados
dados_y_log = np.log(dados_y)
dados_x_log = np.log(dados_x)

# Função de equação linear (y = a + b * x)
def linear_eq(x, a, b):
    return a + b * x

# Função para calcular o erro entre a equação linear e os dados log-transformados
def erro_eq_linear(parametros, x, y):
    a = parametros[0]
    b = parametros[1]
    return linear_eq(x, a, b) - y

# Ajuste da curva aos dados usando a equação linear
parametros_iniciais = [1.0, -1.0]  # Valores iniciais para a e b
ajuste = least_squares(erro_eq_linear, parametros_iniciais, args=(dados_x_log, dados_y_log), max_nfev=5000)

# Obtendo os parâmetros a e b da equação linear ajustada
a = ajuste.x[0]
b = ajuste.x[1]

# Calculando os parâmetros da lei de potência (a_original = exp(a) e b_original = b)
a_original = np.exp(a)

# Valor de y desejado para extrapolação
y_desejado = 10

# Realizando bootstrap para obter distribuições dos parâmetros a e b da equação linear
num_bootstraps = 1000  # Número de reamostragens
parametros_bootstrap = np.zeros((num_bootstraps, 2))

for i in range(num_bootstraps):
    indices_amostra = np.random.choice(len(dados_x_log), size=len(dados_x_log), replace=True)
    x_amostra = dados_x_log[indices_amostra]
    y_amostra = dados_y_log[indices_amostra]

    ajuste_bootstrap = least_squares(erro_eq_linear, parametros_iniciais, args=(x_amostra, y_amostra), max_nfev=5000)
    parametros_bootstrap[i] = ajuste_bootstrap.x

# Calculando intervalos de confiança para os parâmetros a e b da equação linear
a_ci = np.percentile(parametros_bootstrap[:, 0], [2.5, 97.5])
b_ci = np.percentile(parametros_bootstrap[:, 1], [2.5, 97.5])

# Realizando bootstrap para obter distribuição do valor extrapolado
x_extrapolado_bootstraps = (y_desejado / np.exp(parametros_bootstrap[:, 0])) ** (1 / parametros_bootstrap[:, 1])
x_extrapolado = (y_desejado / a_original) ** (1 / b)

# Calculando intervalo de confiança para o valor extrapolado
x_extrapolado_ci = np.percentile(x_extrapolado_bootstraps, [2.5, 97.5])

# Imprimindo os parâmetros estimados e seus intervalos de confiança
print("Parâmetros estimados:")
print(f"a = {a_original:.3f}, 95% CI: [{np.exp(a_ci[0]):.3f}, {np.exp(a_ci[1]):.3f}]")
print(f"b = {b:.3f}, 95% CI: [{b_ci[0]:.3f}, {b_ci[1]:.3f}]")

# Imprimindo valor extrapolado e intervalo de confiança
print(f"Valor de x extrapolado para y = {y_desejado}: {x_extrapolado:.3f}, 95% CI: [{x_extrapolado_ci[0]:.3f}, {x_extrapolado_ci[1]:.3f}]")

# Cálculo do coeficiente de determinação (R²)
slope, intercept, r_value, p_value, std_err = linregress(dados_x, dados_y)
r_squared = r_value ** 2

# Cálculo do erro quadrático médio (MSE)
y_ajustado = a_original * np.power(dados_x, b)
mse = np.mean((dados_y - y_ajustado) ** 2)

# Cálculo do erro padrão da estimativa (EPE)
residuos = dados_y - y_ajustado
epe = np.std(residuos, ddof=2)

# Imprimindo as métricas
print(f"Coeficiente de Determinação (R²): {r_squared:.3f}")
print(f"Erro Quadrático Médio (MSE): {mse:.3f}")
print(f"Erro Padrão da Estimativa (EPE): {epe:.3f}")

# Plot dos pontos de dados originais e a curva ajustada da lei de potência
plt.scatter(dados_x, dados_y, label='Dados Originais')
plt.plot(dados_x, y_ajustado, label='Lei de Potência Ajustada', color='red')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.title('Ajuste de Lei de Potência')
plt.show()
