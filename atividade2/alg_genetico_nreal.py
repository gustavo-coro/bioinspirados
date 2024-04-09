from io import TextIOWrapper
import math
import random
import copy
import numpy
import numpy.random as npr
import sys

def cria_populacao_inicial(x_min:int, x_max:int, npop:int, x_n:int) -> list :
    pop = list()
    for i in range(npop):
        indiv_temp = list()
        for j in range(x_n):
            indiv_temp.append(random.uniform(x_min, x_max))
        pop.append(indiv_temp)
    return pop

def avalia_populacao(pop:list, x_n:int) -> list:
    fit = []
    for x in pop:
        x_sum = 0
        for x_i in x:
            x_sum += (x_i**2)
        cos_sum = 0
        for x_i in x:
            cos_sum += math.cos(2*math.pi*x_i)
        f_x = -20*(math.e**(-0.2*math.sqrt((1/x_n)*x_sum))) - math.e**((1/x_n)*cos_sum) + 20 + math.e
        fit.append(f_x)
    return fit

def seleciona_pais(npop:int, fit:list, pop:list, num_pais:int) -> list:
    pais = []
    cont = 0

    fit_normalizado = [1 / (f) for f in fit]
    fit_total = sum(fit_normalizado)

    while cont < num_pais:
        roleta = [f/fit_total for f in fit_normalizado]
        pai = npr.choice(range(npop), p=roleta)
        if cont != 0:
            while pai == pais[cont-1]:
                pai = npr.choice(range(npop), p=roleta)
        pais.append(pai)
        cont += 1
    
    return pais

def cruzamento_blx_alfa(pais:list, pop:list, pc:float, alfa:float) -> list:
    pop_intermediaria = []
    for p1, p2 in zip(*[iter(pais)]*2):
        r = random.random()
        if r > pc:
            pop_intermediaria.append(pop[p1])
            pop_intermediaria.append(pop[p2])
            continue
        if fit[p1] <= fit[p2]:
            x = pop[p1]
            y = pop[p2]
        else:
            x = pop[p2]
            y = pop[p1]
        d = [abs(x_i - y_i) for x_i,y_i in zip(x,y)]
        f1 = []
        f2 = []
        for x_i, y_i, d_i in zip(x,y,d):
            f1.append(random.uniform(min(x_i, y_i)-alfa*d_i, max(x_i, y_i)+alfa*d_i))
            f2.append(random.uniform(min(x_i, y_i)-alfa*d_i, max(x_i, y_i)+alfa*d_i))
                
        pop_intermediaria.append(f1)
        pop_intermediaria.append(f2)
    return pop_intermediaria
    
def cruzamento_blx_alfa_beta(pais:list, pop:list, pc:float, alfa:float, beta:float) -> list:
    pop_intermediaria = []
    for p1, p2 in zip(*[iter(pais)]*2):
        r = random.random()
        if r > pc:
            pop_intermediaria.append(pop[p1])
            pop_intermediaria.append(pop[p2])
            continue
        if fit[p1] <= fit[p2]:
            x = pop[p1]
            y = pop[p2]
        else:
            x = pop[p2]
            y = pop[p1]
        d = [abs(x_i - y_i) for x_i,y_i in zip(x,y)]
        f1 = []
        f2 = []
        for x_i, y_i, d_i in zip(x,y,d):
            if x_i <= y_i:
                f1.append(random.uniform(x_i-alfa*d_i, y_i+beta*d_i))
                f2.append(random.uniform(x_i-alfa*d_i, y_i+beta*d_i))
            else:
                f1.append(random.uniform(y_i-beta*d_i, x_i+alfa*d_i))
                f2.append(random.uniform(y_i-beta*d_i, x_i+alfa*d_i))
        pop_intermediaria.append(f1)
        pop_intermediaria.append(f2)
    return pop_intermediaria

def mutacao(pop:list, pm:float, x_min:int, x_max:int) -> list:
    pop_intermediaria = []
    for i in pop:
        temp_inv = []
        for j in i:
            r = random.random()
            if(r<=pm):
                j = random.uniform(x_min, x_max)
            temp_inv.append(j)
        pop_intermediaria.append(temp_inv)
    return pop_intermediaria

def elitismo(pop:list, fit:list, nelite:int) -> list:
    elites = []
    sorted_list = sorted(fit, reverse=False)
    melhores = sorted_list[0:nelite]
    print(melhores)
    for i in melhores:
        pos = fit.index(i)
        elites.append(pop[pos])
    print()
    return elites


if len(sys.argv) != 9:
    print("Erro na passagem de parâmetros!")
    exit()

best_per_generation_file = open(sys.argv[1], "a+")

nger = int(sys.argv[3])
# npop + nelite = par
npop = int(sys.argv[4])
nelite = 2

pop = []
pop_intermediaria = []
pais = []
fit = []

pc = float(sys.argv[5])

alfa = 1.2
beta = 0.7

pm = float(sys.argv[6])

seleciona_cruzamento = bool(sys.argv[7])
define_elitismo = bool(sys.argv[8])

x_min = -2 
x_max = 2
x_n = 3 # numero de termos no somatorio

pop = cria_populacao_inicial(x_min, x_max, npop, x_n)

geracoes = 0
while(geracoes != nger):
    print("Geracao: ", geracoes)
    fit = avalia_populacao(pop, x_n)
    
    pais = seleciona_pais(npop, fit, pop, npop-nelite)
    if (seleciona_cruzamento):
        pop_intermediaria = cruzamento_blx_alfa_beta(pais, copy.deepcopy(pop), pc, alfa, beta)
    else:
        pop_intermediaria = cruzamento_blx_alfa(pais, copy.deepcopy(pop), pc, 0.5)

    pop_intermediaria = mutacao(pop_intermediaria, pm, x_min, x_max)

    if (define_elitismo):
        nova_populacao = elitismo(pop, fit, nelite)

    nova_populacao.extend(pop_intermediaria)
    pop = nova_populacao

    geracoes += 1

best_solution = sorted(fit, reverse=False)[0]
pos = fit.index(best_solution)
best = pop[pos]
print()
print("Melhor: ", best)
print("Fit: ", best_solution)

best_per_generation_file.write("%s;%s\n" %(sys.argv[2], format(best_solution, "e")))
best_per_generation_file.close()