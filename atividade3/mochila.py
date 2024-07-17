import math
import random
import copy
import numpy
import numpy.random as npr
import sys
from io import TextIOWrapper

class Item:
    def __init__(self, peso:int, valor:int):
        self.peso = peso
        self.valor = valor

def cria_populacao_inicial(npop:int, nitems:int) -> list:
    pop = list()
    for i in range(npop):
        indiv_temp = list()
        for j in range(nitems):
            indiv_temp.append(random.randint(0,1))
        pop.append(indiv_temp)
    return pop

def avalia_populacao(npop:int, pop:list, items:list, capacidade:int) -> list:
    fit = []
    for i in range(npop):
        fit_atual = 0
        peso_atual = 0
        idv = pop[i]
        for j in range(len(pop[i])):
            if(idv[j] == 1):
                fit_atual += items[j].valor
                peso_atual += items[j].peso
        if (peso_atual > capacidade):
            #fit_atual = fit_atual * (1 - ((peso_atual - capacidade)/capacidade))
            fit_atual = fit_atual - (fit_atual * (peso_atual - capacidade))
        fit.append(fit_atual)
    return fit

def seleciona_pais(npop:int, fit:list, pop:list, num_pais:int) -> list:
    pais = []
    while len(pais) < num_pais:
        vencedor = 0
        p1 = random.randrange(0, npop)
        p2 = random.randrange(0, npop)
        while(pop[p1] == pop[p2]):
            p2 = random.randrange(0, npop)
        if(fit[p1] <= fit[p2]):
            vencedor = p1
        else:
            vencedor = p2
        pais.append(vencedor)

        p1 = random.randrange(0, npop)
        while(pop[p1] == pop[vencedor]):
            p1 = random.randrange(0, npop)
        p2 = random.randrange(0, npop)
        while(pop[p2] == pop[vencedor]):
            p2 = random.randrange(0, npop)
        while(pop[p1] == pop[p2]):
            p2 = random.randrange(0, npop)
        if(fit[p1] <= fit[p2]):
            vencedor = p1
        else:
            vencedor = p2
        pais.append(vencedor)
    return pais

def cruzamento(pais:list, pop:list, nitems:int, npontos:int, pc:float) -> list:
    pop_intermediaria = []
    for p1, p2 in zip(*[iter(pais)]*2):
        r1 = random.randint(0, nitems - npontos)
        p1_end = pop[p2]
        p2_end = pop[p1]
        r = random.random()
        if(r<pc):
            p1_end[r1:r1+npontos] = pop[p1][r1:r1+npontos]
            p2_end[r1:r1+npontos] = pop[p2][r1:r1+npontos]
        pop_intermediaria.append(p1_end)
        pop_intermediaria.append(p2_end)
    return pop_intermediaria

def mutacao(pop:list, pm:float) -> list:
    pop_intermediaria = []
    for i in pop:
        temp_inv = []
        for j in i:
            r = random.random()
            if(r<=pm):
                if(j == 0):
                    j = 1
                else:
                    j = 0
            temp_inv.append(j)
        pop_intermediaria.append(temp_inv)
    return pop_intermediaria

def elitismo(pop:list, fit:list, nelite:int) -> list:
    elites = []
    sorted_list = sorted(fit, reverse=True)
    melhores = sorted_list[0:nelite]
    print(melhores)
    for i in melhores:
        pos = fit.index(i)
        elites.append(pop[pos])
    print()
    return elites

problema = "entradas/p08"
npop = 200 #numero da populacao
nger = 500 #numero de geracoes
npontos = 2 #numero de pontos no cruzamento
nelite = 2 #numero do elitismo
pc = 0.8 #probabilidade de cruzamento
pm = 0.25 #probabilidade de mutacao


path = problema + "_c.txt"
capacidade = int(numpy.loadtxt(path, dtype=int))

path = problema + "_p.txt"
valores = list(numpy.loadtxt(path, dtype=int))

path = problema + "_s.txt"
melhor_solucao = list(numpy.loadtxt(path, dtype=int))

path = problema + "_w.txt"
pesos = list(numpy.loadtxt(path, dtype=int))

nitems = len(valores)

items = list()
for i in range(nitems):
    item = Item(pesos[i], valores[i])
    items.append(item)

pop = cria_populacao_inicial(npop, nitems)

geracoes = 0
while(geracoes != nger):
    fit = avalia_populacao(npop, pop, items, capacidade)
    pais = seleciona_pais(npop, fit, pop, npop-nelite)
    pop_intermediaria = cruzamento(pais, copy.deepcopy(pop), nitems, npontos, pc)
    pop_intermediaria = mutacao(pop_intermediaria, pm)
    nova_populacao = elitismo(pop, fit, nelite)
    nova_populacao.extend(pop_intermediaria)
    pop = nova_populacao
    geracoes += 1

best_solution = sorted(fit, reverse=True)[0]
pos = fit.index(best_solution)
best = pop[pos]
print()
print("Melhor Achado:\t", best)
print("Fit: ", best_solution)
print("Melhor Solucao:\t", melhor_solucao)