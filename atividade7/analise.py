import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

class Teste:
    def __init__(self, n:int, d:int, beta:float, melhores:list):
        self.n = n
        self.d = d
        self.beta = beta
        self.melhores = melhores
        self.media = np.mean(self.melhores)
        self.desvio = np.std(self.melhores)


testes = list()

for i in range(1, 21):
    file_path = f"testes/att48_d/teste{i}.txt"
    n = np.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    d = np.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    beta = np.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=float)
    melhores = np.loadtxt(file_path, delimiter=';', skiprows=3, dtype=int)
    teste = Teste(n, d, beta, melhores)
    testes.append(teste)

testes = sorted(testes, key=lambda teste: (teste.media, teste.n, teste.d, teste.beta), reverse=False)

data = []
for teste in testes:
    t = [teste.n, teste.d, teste.beta, "{:.2f}".format(teste.media), "{:.2f}".format(teste.desvio)]
    data.append(t)

df = pd.DataFrame(data, columns=['n', 'd', 'β', 'Media', 'Desvio'])

# Plot the table and save it as an image
fig, ax = plt.subplots(figsize=(11, 6))  # set size frame
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f7f7f7"] * len(df.columns))

# Set font size for the table
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)


plt.show()

data_melhor = np.loadtxt("testes/att48_d/arquivo_saida.txt", delimiter=';', skiprows=1, dtype=float)

y = [[],[],[],[]]
for d in data_melhor:
    y[0].append(d[0])
    y[1].append(d[1])
    y[2].append(d[2])
    y[3].append(d[3])

plt.plot(y[0], label="Melhor")
plt.plot(y[1], label="Pior")
plt.plot(y[2], label="Média")
plt.plot(y[3], label="Mediana")
plt.xlabel("Iteração")
plt.ylabel("Distância")
plt.legend()
plt.savefig("analise_melhor_48.png")
plt.show()

execucoes_melhor = np.genfromtxt("testes/att48_d/teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Iteração")
gf_execucoes.set_ylabel("Distância")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex, label=("Execução" + str(i)))

plt.legend()
plt.savefig("teste_melhor_48.png")
plt.show()