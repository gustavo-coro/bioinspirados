NUM_RUNS=10

FILE_ENTRADA="lau15_dist"
DATA_FILE="testes/$FILE_ENTRADA/teste6.txt"
S=5
B1=1
B2=1
ALFA=0.03

# Create directory if it doesn't exist
mkdir -p testes/$FILE_ENTRADA

# Create and write to the data file
touch $DATA_FILE
printf "$S\n$B1\n$B2\n$ALFA\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/scatter_search.py entradas/$FILE_ENTRADA.txt $S $B1 $B2 $ALFA $DATA_FILE
done
