import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

class Teste:
    def __init__(self, iteracoes:int, num_particulas:int, num_dimensoes:int, c1:float, c2:int, w:float, topologia:int, melhores:list):
        self.iteracoes = iteracoes
        self.num_particulas = num_particulas
        self.num_dimensoes = num_dimensoes
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.topologia = topologia
        self.melhores = melhores
        self.media = np.mean(self.melhores)
        self.desvio = np.std(self.melhores)

dir = "testes/"
testes = list()

for i in range(1, 45):
    file_path = f"{dir}teste{i}.txt"
    iteracoes = np.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    num_particulas = np.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    num_dimensoes = np.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=int)
    c1 = np.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    c2 = np.loadtxt(file_path, delimiter=';', skiprows=4, max_rows=1, dtype=float)
    w = np.loadtxt(file_path, delimiter=';', skiprows=5, max_rows=1, dtype=float)
    topologia = np.loadtxt(file_path, delimiter=';', skiprows=6, max_rows=1, dtype=int)
    melhores = np.loadtxt(file_path, delimiter=';', skiprows=7, dtype=float)
    teste = Teste(iteracoes, num_particulas, num_dimensoes, c1, c2, w, topologia, melhores)
    testes.append(teste)

testes = sorted(testes, key=lambda teste: (teste.media, teste.desvio, teste.num_particulas), reverse=False)[:30]

data = []
for teste in testes:
    t = [teste.iteracoes, teste.num_particulas, teste.num_dimensoes, teste.c1, teste.c2, teste.w, "M. Global" if (teste.topologia == 0) else "V. Adjacente", "{:.2f}".format(teste.media), "{:.2f}".format(teste.desvio)]
    data.append(t)

df = pd.DataFrame(data, columns=['Iterações', 'N. Partículas', 'N. Dimensões', 'C\u2081', 'C\u2082', 'W', 'Topologia', 'Média', 'Desvio'])

# Plot the table and save it as an image
fig, ax = plt.subplots(figsize=(11, 6))  # set size frame
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', colColours=["#f7f7f7"] * len(df.columns))

# Set font size for the table
the_table.auto_set_font_size(False)
the_table.set_fontsize(10)
the_table.auto_set_column_width([0,1,2,6])

plt.savefig(f"{dir}testestable.png")
plt.show()


data_melhor = np.loadtxt(f"{dir}arquivo_saida_tp1.txt", delimiter=';', skiprows=1, dtype=float)

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
plt.savefig(f"{dir}analisemelhor_tp1.png")
plt.show()

execucoes_melhor = np.genfromtxt(f"{dir}teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Gerações")
gf_execucoes.set_ylabel("Aptidão")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex[:200], label=("Execução" + str(i)))

plt.legend()
plt.savefig(f"{dir}execucoesmelhor.png")
plt.show() 