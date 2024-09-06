import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

class Teste:
    def __init__(self, s:int, b1:int, b2:int, alfa:float, melhores:list):
        self.s = s
        self.b1 = b1
        self.b2 = b2
        self.alfa = alfa
        self.melhores = melhores
        self.media = np.mean(self.melhores)
        self.desvio = np.std(self.melhores)


testes = list()

for i in range(1, 6):
    file_path = f"testes/lau15_dist/teste{i}.txt"
    s = np.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    b1 = np.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    b2 = np.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=int)
    alfa = np.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    melhores = np.loadtxt(file_path, delimiter=';', skiprows=6, dtype=int)
    teste = Teste(s, b1, b2, alfa, melhores)
    testes.append(teste)

testes = sorted(testes, key=lambda teste: (teste.media, teste.s, teste.b1, teste.b2), reverse=False)

data = []
for teste in testes:
    t = [teste.s, teste.b1, teste.b2, teste.alfa, "{:.2f}".format(teste.media), "{:.2f}".format(teste.desvio)]
    data.append(t)

df = pd.DataFrame(data, columns=['S', 'B1', 'B2', 'α', 'Media', 'Desvio'])

# Plot the table and save it as an image
fig, ax = plt.subplots(figsize=(11, 6))  # set size frame
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f7f7f7"] * len(df.columns))

# Set font size for the table
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)


plt.show()

data_melhor = np.loadtxt("testes/dantizig42_d/arquivo_saida.txt", delimiter=';', skiprows=1, dtype=float)

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
plt.savefig("analise_melhor_42.png")
plt.show()

execucoes_melhor = np.genfromtxt("testes/dantizig42_d/teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Iteração")
gf_execucoes.set_ylabel("Distância")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex, label=("Execução" + str(i)))

plt.legend()
plt.savefig("teste_melhor_42.png")
plt.show()