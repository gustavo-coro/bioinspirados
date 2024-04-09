#python alg_genetico_nreal.py "arquivo_saida.txt" execucao geracoes 
#populacao taxa_cruzamento taxa_mutacao selec_cruzamento selec_elitismo
#selec_cruzamento = (1 para alfa-beta) e (0 para alfa)
#selec_elitismo = (1 para ter elitismo) e (0 para nao ter)

NUM_RUNS=10 
DATA_FILE="teste.txt"
GERACOES=100
POPULACAO=100
TAXA_CRUZAMENTO=0.8
TAXA_MUTACAO=0.01
SELEC_CRUZAMENTO=1
SELEC_ELITISMO=1

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python alg_genetico_nreal.py $DATA_FILE $i $GERACOES $POPULACAO $TAXA_CRUZAMENTO $TAXA_MUTACAO $SELEC_CRUZAMENTO $SELEC_ELITISMO
done