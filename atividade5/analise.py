import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

class Teste:
    def __init__(self, iteracoes:int, alfa:float, beta:float, taxa_evaporacao:float, q:int, w:int, melhores:list):
        self.iteracoes = iteracoes
        self.alfa = alfa
        self.beta = beta
        self.taxa_evaporacao = taxa_evaporacao
        self.q = q
        self.w = w
        self.melhores = melhores
        self.media = np.mean(self.melhores)
        self.desvio = np.std(self.melhores)

testes = list()

for i in range(1, 13):
    file_path = f"testes/dantizig42_d/teste{i}.txt"
    iteracoes = np.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    alfa = np.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=float)
    beta = np.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=float)
    taxa_evaporacao = np.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    q = np.loadtxt(file_path, delimiter=';', skiprows=4, max_rows=1, dtype=int)
    w = np.loadtxt(file_path, delimiter=';', skiprows=5, max_rows=1, dtype=int)
    melhores = np.loadtxt(file_path, delimiter=';', skiprows=6, dtype=int)
    teste = Teste(iteracoes, alfa, beta, taxa_evaporacao, q, w, melhores)
    testes.append(teste)

testes = sorted(testes, key=lambda teste: teste.media, reverse=False)

data = []
for teste in testes:
    t = [teste.iteracoes, teste.alfa, teste.beta, teste.taxa_evaporacao, teste.q, teste.w, "{:.2f}".format(teste.media), "{:.2f}".format(teste.desvio)]
    data.append(t)

df = pd.DataFrame(data, columns=['Iterações', 'α', 'β', 'ρ', 'Q', 'W', 'Media', 'Desvio'])

# Plot the table and save it as an image
fig, ax = plt.subplots(figsize=(11, 6))  # set size frame
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f7f7f7"] * len(df.columns))

# Set font size for the table
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)

plt.savefig("testes_table_42.png")
plt.show()

'''
data_melhor = np.loadtxt("testes/lau15_dist/arquivo_saida.txt", delimiter=';', skiprows=1, dtype=float)

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
plt.xlabel("Geração")
plt.ylabel("Aptidão")
plt.legend()
plt.show()

execucoes_melhor = np.genfromtxt("testes/lau15_dist/teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Gerações")
gf_execucoes.set_ylabel("Aptidão")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex, label=("Execução" + str(i)))

plt.legend()
plt.show()'''