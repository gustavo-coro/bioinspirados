import math
import random

def cria_populacao_inicial(npop:int) -> list :
    pop = list()
    for i in range(npop):
        indiv_temp = list()
        for j in range(18):
            indiv_temp.append(random.randint(0,1))
        pop.append(indiv_temp)
    return pop

def binario_para_inteiro(bin:list) -> int:
    res = 0
    for i in range(6):
        res += (2**i) * bin[i]
    return res

def representacao_populacao(x_min:int, x_max:int, nums_bin:list) -> list:
    x_i = list()
    for i in range(3):
        rg_fn = (i + 1) * 6
        rg_in = i * 6
        num = binario_para_inteiro(nums_bin[rg_in:rg_fn])
        x = x_min + (((x_max - x_min)/((2**6) - 1)) * num)
        x_i.append(x)
    return x_i

def avalia_populacao(npop:int, pop:list) -> list:
    fit = []
    for idv in pop:
        x = representacao_populacao(-2, 2, idv)
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
    pv = 0.9
    cont = 0
    pop_set = set()
    for i in range(npop):
        pop_set.add(i)
    for i in range(npop):
        if (cont == num_pais):
            break
        vencedor = 0
        p1 = random.randrange(0, len(pop_set))
        p2 = random.randrange(0, len(pop_set))
        while(pop[p1] == pop[p2]):
            p2 = random.randrange(0, len(pop_set))
        p1 = list(pop_set)[p1]
        p2 = list(pop_set)[p2]
        r = random.random()
        if(fit[p1] <= fit[p2]):
            vencedor = p1
            if(r>pv):
                vencedor = p2
        else:
            vencedor = p2
            if(r>pv):
                vencedor = p1
        pais.append(vencedor)
        pop_set.discard(vencedor)
        cont += 1
    return pais
    
def cruzamento(pais:list, pop:list) -> list:
    pop_intermediaria = []
    for p1, p2 in zip(*[iter(pais)]*2):
        p1_end = pop[p2]
        p2_end = pop[p1]
        p1_end[12:18] = pop[p1][12:18]
        p2_end[12:18] = pop[p2][12:18]
        p1_start = pop[p2]
        p2_start = pop[p1]
        p1_start[0:6] = pop[p1][0:6]
        p2_start[0:6] = pop[p2][0:6]
        pop_intermediaria.append(p1_end)
        pop_intermediaria.append(p2_end)
        pop_intermediaria.append(p1_start)
        pop_intermediaria.append(p2_start)
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

def elitismo(pop:list, fit:list, nelite:int):
    elites = []
    sorted_list = sorted(fit, reverse=False)
    maiores = sorted_list[0:nelite]
    print(maiores)
    for i in maiores:
        pos = fit.index(i) # provavelmente onde esta o erro
        elites.append(pop[pos])
    print()
    return elites
    

npop = 100
nger = 20
nelite = 4
pop = []
pop_intermediaria = []

pais = []
fit = []

fc = 1.0
pm = 0.05

pop = cria_populacao_inicial(npop)

geracoes = 0
while(geracoes != nger):
    print("Geracao: ", geracoes)
    fit = avalia_populacao(npop, pop)
    pais = seleciona_pais(npop, fit, pop, 48)
    pop_intermediaria = cruzamento(pais, pop)
    pop_intermediaria = mutacao(pop_intermediaria, pm)
    nova_populacao = elitismo(pop, fit, nelite)
    for i in pop_intermediaria:
        nova_populacao.append(i)
    pop = nova_populacao
    geracoes += 1