import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd

class Teste:
    def __init__(self, nger:int, npop:int, pc:float, pm:float, elitismo:int, tc:int, melhores:list):
        self.npop = npop
        self.nger = nger
        self.elitismo = elitismo
        self.pc = pc
        self.pm = pm
        self.tc = tc
        self.melhores = melhores
        self.media = np.mean(self.melhores)
        self.desvio = np.std(self.melhores)

testes = list()

for i in range(1, 214):
    file_path = f"testes/lau15_dist/teste{i}.txt"
    npop = np.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    nger = np.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    elitismo = np.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=int)
    pc = np.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    pm = np.loadtxt(file_path, delimiter=';', skiprows=4, max_rows=1, dtype=float)
    tc = np.loadtxt(file_path, delimiter=';', skiprows=5, max_rows=1, dtype=int)
    melhores = np.loadtxt(file_path, delimiter=';', skiprows=6, dtype=int)
    teste = Teste(nger, npop, pc, pm, elitismo, tc, melhores)
    testes.append(teste)

testes = sorted(testes, key=lambda teste: teste.media, reverse=False)
testes = testes[:50]
data = []
for teste in testes:
    t = [teste.nger, teste.npop, teste.pc, teste.pm, teste.elitismo, "Roulette" if (teste.tc == 0) else "Tournament", teste.media, "{:.2f}".format(teste.desvio)]
    data.append(t)

df = pd.DataFrame(data, columns=['Gerações', 'População', 'P. de Cruzamento', 'P. de Mutação', 'N Elite', 'T. Cruzamento', 'Media', 'Desvio'])

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
plt.show()