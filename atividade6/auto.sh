NUM_RUNS=10

DATA_FILE="testes/teste1.txt"
ITERACOES=100
NUM_PARTICULAS=500
NUM_DIMENSOES=5
C1=0.8
C2=3.1
W=0.03

# Create directory if it doesn't exist
mkdir -p testes

# Create and write to the data file
touch $DATA_FILE
printf "$ITERACOES\n$NUM_PARTICULAS\n$NUM_DIMENSOES\n$C1\n$C2\n$W\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/pso.py $ITERACOES $NUM_PARTICULAS $NUM_DIMENSOES $C1 $C2 $W $DATA_FILE
done