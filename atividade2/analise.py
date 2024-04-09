import numpy
from tabulate import tabulate
import matplotlib.pyplot as plt

class Teste:
    def __init__(self, nger:int, npop:int, pc:float, pm:float, cruzamento:bool, elitismo:bool, melhores:list):
        self.nger = nger
        self.npop = npop
        self.pc = pc
        self.pm = pm
        self.cruzamento = cruzamento
        self.elitismo = elitismo
        self.melhores = melhores
        self.media = numpy.mean(self.melhores)
        self.desvio = numpy.std(self.melhores)
    

testes = list()

for i in range(1,21):
    file_path = "testes/teste" + str(i) + ".txt"
    nger = numpy.loadtxt(file_path, delimiter=';', skiprows=0, max_rows=1, dtype=int)
    npop = numpy.loadtxt(file_path, delimiter=';', skiprows=1, max_rows=1, dtype=int)
    pc = numpy.loadtxt(file_path, delimiter=';', skiprows=2, max_rows=1, dtype=float)
    pm = numpy.loadtxt(file_path, delimiter=';', skiprows=3, max_rows=1, dtype=float)
    cruzamento = numpy.loadtxt(file_path, delimiter=';', skiprows=4, max_rows=1, dtype=bool)
    elitismo = numpy.loadtxt(file_path, delimiter=';', skiprows=5, max_rows=1, dtype=bool)
    melhores = numpy.loadtxt(file_path, delimiter=';', skiprows=6, usecols=1)
    teste = Teste(nger, npop, pc, pm, cruzamento, elitismo, melhores)
    testes.append(teste)


testes = sorted(testes, key=lambda teste: teste.media, reverse=False)
    
data = []
for teste in testes:
    t = [teste.nger, teste.npop, teste.pc, teste.pm, "BLX-αβ" if teste.cruzamento else "BLX-α", "True" if teste.elitismo else "False", teste.media, teste.desvio]
    data.append(t)

print(tabulate(data, headers=['Gerações', 'População', 'Prob. de Cruzamento', 'Prob. de Mutação', 'Cruzamento', 'Elitismo', 'Media', 'Desvio'], tablefmt='orgtbl'))

data_melhor = numpy.loadtxt("testes/arquivo_saida.txt", delimiter=';', skiprows=1, dtype=float)

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

execucoes_melhor = numpy.genfromtxt("testes/teste_melhor.txt", delimiter=';', dtype=None)

gf_execucoes = plt.subplot()
gf_execucoes.set_xlabel("Gerações")
gf_execucoes.set_ylabel("Aptidão")

for i in range(1,11):
    ex = [exec[1] for exec in execucoes_melhor if (exec[0] == i)]
    gf_execucoes.plot(ex, label=("Execução" + str(i)))

plt.legend()
plt.show()