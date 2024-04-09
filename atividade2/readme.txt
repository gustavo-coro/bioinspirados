Algoritmo Genético com representação real
por: Gustavo Henriques da Cunha

Para executar o código, segue o comando:
python alg_genetico_nreal.py "arquivo_saida.txt" execucao geracoes populacao taxa_cruzamento taxa_mutacao selec_cruzamento selec_elitismo
selec_cruzamento = (1 para alfa-beta) e (0 para alfa)
selec_elitismo = (1 para ter elitismo) e (0 para nao ter)

EX:
python alg_genetico_nreal.py "arquivo_saida.txt" 1 100 100 0.8 0.01 1 1

Ele retorna no arquivo de saída o número da execução e o melhor fit gerado.
No terminal ele irá imprimir os dois melhores de cada geração e no final o valor do melhor.
Para testar o programa várias vezes, usar o arquivo 'auto.sh', onde é possível mudar a quantidade de execuções e os parâmetros de entrada.
O arquivo 'analise.py' verifica os testes gerados, imprime no terminal uma tabela com as execuções ordenadas e gera os gráficos da melhor execução.