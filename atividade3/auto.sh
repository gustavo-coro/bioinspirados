#python mochila.py "arquivo_entrada" "arquivo_saida.txt" populacao geracoes num_elite taxa_cruzamento taxa_mutacao

NUM_RUNS=1

FILE_ENTRADA="p08"
DATA_FILE="testes/$FILE_ENTRADA/arquivo_saida.txt"
POPULACAO=200
GERACOES=250
NUM_ELITE=2
TAXA_CRUZAMENTO=0.8
TAXA_MUTACAO=0.20

#printf "$POPULACAO\n$GERACOES\n$NUM_ELITE\n$TAXA_CRUZAMENTO\n$TAXA_MUTACAO\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python mochila.py entradas/$FILE_ENTRADA $DATA_FILE $POPULACAO $GERACOES $NUM_ELITE $TAXA_CRUZAMENTO $TAXA_MUTACAO
done