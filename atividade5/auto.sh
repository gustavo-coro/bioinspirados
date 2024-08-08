#python src/tsp.py "arquivo_entrada" populacao geracoes num_elite taxa_cruzamento taxa_mutacao tipo_cruzamento "arquivo_saida.txt"

NUM_RUNS=10

FILE_ENTRADA="lau15_dist"
DATA_FILE="testes/$FILE_ENTRADA/arquivo_saida.txt"
ITERACOES=100
ALFA=1.0
BETA=5.0
TAXA_EVAPORACAO=0.5
Q=100
W=5

# Create directory if it doesn't exist
mkdir -p testes/$FILE_ENTRADA

# Create and write to the data file
touch $DATA_FILE
printf "$ITERACOES\n$ALFA\n$BETA\n$TAXA_EVAPORACAO\n$Q\n$W\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/tsp_as.py entradas/$FILE_ENTRADA.txt $ITERACOES $ALFA $BETA $TAXA_EVAPORACAO $Q $W $DATA_FILE
done