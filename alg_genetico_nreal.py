import math
import random
import copy
import numpy.random as npr

def cria_populacao_inicial(x_min:int, x_max:int, npop:int) -> list :
    pop = list()
    for i in range(npop):
        indiv_temp = list()
        for j in range(3):
            indiv_temp.append(random.uniform(x_min, x_max))
        pop.append(indiv_temp)
    return pop

def avalia_populacao(pop:list) -> list:
    fit = []
    for x in pop:
        x_sum = 0
        for x_i in x:
            x_sum += (x_i**2)
        cos_sum = 0
        for x_i in x:
            cos_sum += math.cos(2*math.pi*x_i)
        f_x = -20*(math.e**(-0.2*math.sqrt((1/3)*x_sum))) - math.e**((1/3)*cos_sum) + 20 + math.e
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
    
def cruzamento(pais:list, pop:list, pc:float, alfa:float, beta:float) -> list:
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
    

npop = 100 # tem que ser par
nger = 100
nelite = 2 # tem que ser par

pop = []
pop_intermediaria = []
pais = []
fit = []

pc = 1.0

alfa = 1.2
beta = 0.7

pm = 0.05

x_min = -2
x_max = 2

pop = cria_populacao_inicial(x_min, x_max, npop)

geracoes = 0
while(geracoes != nger):
    print("Geracao: ", geracoes)
    fit = avalia_populacao(pop)

    pais = seleciona_pais(npop, fit, pop, npop-nelite)
    pop_intermediaria = cruzamento(pais, copy.deepcopy(pop), pc, alfa, beta)

    pop_intermediaria = mutacao(pop_intermediaria, pm, x_min, x_max)

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

