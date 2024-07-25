#python src/tsp.py "arquivo_entrada" populacao geracoes num_elite taxa_cruzamento taxa_mutacao tipo_cruzamento "arquivo_saida.txt"

NUM_RUNS=10

FILE_ENTRADA="lau15_dist"
DATA_FILE="testes/$FILE_ENTRADA/arquivo_saida1.txt"
POPULACAO=30
GERACOES=10000
NUM_ELITE=2
TAXA_CRUZAMENTO=1.0
TAXA_MUTACAO=0.00001
TIPO_CRUZAMENTO=0

# Create directory if it doesn't exist
mkdir -p testes/$FILE_ENTRADA

# Create and write to the data file
touch $DATA_FILE
printf "$POPULACAO\n$GERACOES\n$NUM_ELITE\n$TAXA_CRUZAMENTO\n$TAXA_MUTACAO\n$TIPO_CRUZAMENTO\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/tsp.py entradas/$FILE_ENTRADA.txt $POPULACAO $GERACOES $NUM_ELITE $TAXA_CRUZAMENTO $TAXA_MUTACAO $TIPO_CRUZAMENTO $DATA_FILE
done
