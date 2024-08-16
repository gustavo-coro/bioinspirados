NUM_RUNS=1

DATA_FILE="testes/teste_grafico.txt"
ITERACOES=250
NUM_PARTICULAS=100
NUM_DIMENSOES=2
C1=1.2
C2=4.1
W=0.02
TOPOLOGIA=0

# Create directory if it doesn't exist
mkdir -p testes

# Create and write to the data file
touch $DATA_FILE
#printf "$ITERACOES\n$NUM_PARTICULAS\n$NUM_DIMENSOES\n$C1\n$C2\n$W\n$TOPOLOGIA\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/pso.py $ITERACOES $NUM_PARTICULAS $NUM_DIMENSOES $C1 $C2 $W $TOPOLOGIA $DATA_FILE $i
done