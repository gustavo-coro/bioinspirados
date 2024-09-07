NUM_RUNS=1

FILE_ENTRADA="att48_d"
DATA_FILE="testes/$FILE_ENTRADA/arquivo_saida.txt"
SELECTION=8
CHANGE=8
CLONING=0.9

# Create directory if it doesn't exist
mkdir -p testes/$FILE_ENTRADA

# Create and write to the data file
rm $DATA_FILE
touch $DATA_FILE
#printf "$SELECTION\n$CHANGE\n$CLONING\n" >> $DATA_FILE

for (( i=1; i<=$NUM_RUNS; i++ ))
do
    echo "Generating data for run $i..."
    python src/clonalg.py entradas/$FILE_ENTRADA.txt $SELECTION $CHANGE $CLONING $DATA_FILE
done
