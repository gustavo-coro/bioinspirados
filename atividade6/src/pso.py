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
    def __init__(self, numero_particulas:int, numero_dimensoes:int, iteracoes:int, taxa_aprendizado_cognitiva:float, taxa_aprendizado_social:float, ponderacao_inercia:float):
        self.numero_particulas = numero_particulas
        self.numero_dimensoes = numero_dimensoes
        self.iteracoes = iteracoes
        self.taxa_aprendizado_cognitiva = taxa_aprendizado_cognitiva
        self.taxa_aprendizado_social = taxa_aprendizado_social
        self.ponderacao_inercia = ponderacao_inercia
        self.funcao_avaliacao = restrigin.RastriginFunction(self.numero_dimensoes)

        self.particulas = []

        for i in range(self.numero_particulas):
            solucao = self.funcao_avaliacao.random_solution()
            aptidao = self.funcao_avaliacao.evaluate_solution(solucao)
            particula = Particula(solucao, solucao, aptidao, aptidao)
            self.particulas.append(particula)

        self.melhor_global = copy.deepcopy(min(self.particulas, key = lambda p : p.aptidao))

    def get_melhor_global(self) -> Particula:
        return self.melhor_global
    
    def atualiza_velocidade(self, particula:Particula):
        for j in range(self.numero_dimensoes):
            r1 = random.random()
            r2 = random.random()

            particula.velocidade[j] = self.ponderacao_inercia * particula.velocidade[j]

            # duvida sobre o pi TODO:
            particula.velocidade[j] += self.taxa_aprendizado_cognitiva * r1 * (particula.coordenadas_melhor[j] - particula.coordenadas[j])
            particula.velocidade[j] += self.taxa_aprendizado_social * r2 * (self.melhor_global.coordenadas[j] - particula.coordenadas[j])
    
    def atualiza_posicao(self, particula:Particula):
        for j in range(self.numero_dimensoes):
            particula.coordenadas[j] = particula.coordenadas[j] + particula.velocidade[j]
            if (particula.coordenadas[j] > self.funcao_avaliacao.max_bound):
                particula.coordenadas[j] = self.funcao_avaliacao.max_bound
            elif (particula.coordenadas[j] < self.funcao_avaliacao.min_bound):
                particula.coordenadas[j] = self.funcao_avaliacao.min_bound

    def rodar_algoritmo(self):

        iter_without_change = 0
        for iteracao in range(self.iteracoes):
            if (iter_without_change > 350):
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

                self.atualiza_velocidade(self.particulas[i])
                self.atualiza_posicao(self.particulas[i])
                self.particulas[i].aptidao = self.funcao_avaliacao.evaluate_solution(self.particulas[i].coordenadas)
            
            print("Avaliação = ", pso.get_melhor_global().aptidao_melhor)
            iter_without_change += 1
                

iteracoes = 50000
numero_particulas = 500
numero_dimensoes = 5
taxa_aprendizado_cognitiva = 0.8
taxa_aprendizado_social = 3.1
ponderacao_inercia = 0.03

pso = Pso(numero_particulas, numero_dimensoes, iteracoes, taxa_aprendizado_cognitiva, taxa_aprendizado_social, ponderacao_inercia)
pso.rodar_algoritmo()
print("Melhor = ", pso.get_melhor_global().coordenadas_melhor)
print("Avaliação = ", pso.get_melhor_global().aptidao_melhor)
