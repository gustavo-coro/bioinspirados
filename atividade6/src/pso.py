import random
import numpy
import numpy.random as npr
import sys
import rastrigin
import copy
    
class Particula:
    def __init__(self, coordenadas:list, coordenadas_melhor:list, aptidao:float, aptidao_melhor:float):
        self.coordenadas = coordenadas
        self.velocidade = []
        self.coordenadas_melhor = coordenadas_melhor
        self.aptidao = aptidao
        self.aptidao_melhor = aptidao_melhor

        for i in range(len(self.coordenadas)):
            self.velocidade.append(0.0)

    def set_nova_coordenada(self, nova_coordenada:list):
        self.coordenadas = nova_coordenada

    def set_nova_coordenadas_melhor(self, nova_coordenadas_melhor:list):
        self.coordenadas_melhor = nova_coordenadas_melhor

    def set_nova_velocidade(self, nova_velocidade):
        self.velocidade = nova_velocidade

class Pso:
    def __init__(self, numero_particulas:int, numero_dimensoes:int, iteracoes:int, max_iter_without_change:int, taxa_aprendizado_cognitiva:float, taxa_aprendizado_social:float, ponderacao_inercia:float, escolhe_topologia:int = 0):
        self.numero_particulas = numero_particulas
        self.numero_dimensoes = numero_dimensoes
        self.iteracoes = iteracoes
        self.max_iter_without_change = max_iter_without_change
        self.taxa_aprendizado_cognitiva = taxa_aprendizado_cognitiva
        self.taxa_aprendizado_social = taxa_aprendizado_social
        self.ponderacao_inercia = ponderacao_inercia
        self.funcao_avaliacao = rastrigin.RastriginFunction(self.numero_dimensoes)
        self.escolhe_topologia = escolhe_topologia

        self.particulas = []

        for i in range(self.numero_particulas):
            solucao = self.funcao_avaliacao.random_solution()
            aptidao = self.funcao_avaliacao.evaluate_solution(solucao)
            particula = Particula(solucao, solucao, aptidao, aptidao)
            self.particulas.append(particula)

        self.melhor_global = copy.deepcopy(min(self.particulas, key = lambda p : p.aptidao))

    def get_melhor_global(self) -> Particula:
        return self.melhor_global
    
    def atualiza_velocidade(self, particula:Particula, coordenadas_melhor_vizinho:list):
        for j in range(self.numero_dimensoes):
            r1 = random.random()
            r2 = random.random()

            particula.velocidade[j] = self.ponderacao_inercia * particula.velocidade[j]

            particula.velocidade[j] += self.taxa_aprendizado_cognitiva * r1 * (particula.coordenadas_melhor[j] - particula.coordenadas[j])
            particula.velocidade[j] += self.taxa_aprendizado_social * r2 * (coordenadas_melhor_vizinho[j] - particula.coordenadas[j])

    
    def atualiza_posicao(self, particula:Particula):
        for j in range(self.numero_dimensoes):
            particula.coordenadas[j] = particula.coordenadas[j] + particula.velocidade[j]
            particula.coordenadas[j] = max(self.funcao_avaliacao.min_bound, min(self.funcao_avaliacao.max_bound, particula.coordenadas[j]))

    def rodar_algoritmo(self):

        iter_without_change = 0
        for iteracao in range(self.iteracoes):
            if (iter_without_change > self.max_iter_without_change):
                break
            for i in range(self.numero_particulas):

                if (self.particulas[i].aptidao < self.particulas[i].aptidao_melhor):
                    self.particulas[i].coordenadas_melhor = self.particulas[i].coordenadas
                    self.particulas[i].aptidao_melhor = self.particulas[i].aptidao

                    if (self.particulas[i].aptidao < self.melhor_global.aptidao_melhor):
                        self.melhor_global.coordenadas_melhor = self.particulas[i].coordenadas
                        self.melhor_global.aptidao_melhor = self.particulas[i].aptidao
                        self.melhor_global.coordenadas = self.particulas[i].coordenadas
                        self.melhor_global.aptidao = self.particulas[i].aptidao

                        iter_without_change = 0

                if (self.escolhe_topologia == 0):
                    self.atualiza_velocidade(self.particulas[i], self.melhor_global.coordenadas_melhor)
                else:
                    anterior = i - 1
                    proximo = i + 1

                    if (i == (len(self.particulas) - 1)):
                        proximo = 0

                    if (self.particulas[anterior].aptidao_melhor <= self.particulas[proximo].aptidao_melhor):
                        self.atualiza_velocidade(self.particulas[i], self.particulas[anterior].coordenadas_melhor)
                    else:
                        self.atualiza_velocidade(self.particulas[i], self.particulas[proximo].coordenadas_melhor)
    
                self.atualiza_posicao(self.particulas[i])
                self.particulas[i].aptidao = self.funcao_avaliacao.evaluate_solution(self.particulas[i].coordenadas)
            
            print("Avaliação = ", pso.get_melhor_global().aptidao_melhor)
            iter_without_change += 1
                

iteracoes = int(sys.argv[1])
max_iter_without_change = 1000
numero_particulas = int(sys.argv[2])
numero_dimensoes = int(sys.argv[3])
taxa_aprendizado_cognitiva = float(sys.argv[4])
taxa_aprendizado_social = float(sys.argv[5])
ponderacao_inercia = float(sys.argv[6])
escolhe_topologia = int(sys.argv[7])


pso = Pso(numero_particulas, numero_dimensoes, iteracoes, max_iter_without_change, taxa_aprendizado_cognitiva, taxa_aprendizado_social, ponderacao_inercia, escolhe_topologia)
pso.rodar_algoritmo()
print("Melhor = ", pso.get_melhor_global().coordenadas_melhor)
print("Avaliação = ", pso.get_melhor_global().aptidao_melhor)

