#!/bin/bash

NUM_RUNS=10  # Number of times to run each parameter combination

FILE_ENTRADA="lau15_dist"
BASE_DIR="testes/$FILE_ENTRADA"
DATA_FILE_TEMPLATE="$BASE_DIR/arquivo_saida_run"

POPULACAO_VALUES=(20 30 40)
GERACOES_VALUES=(5000 10000 15000)
NUM_ELITE_VALUES=(0 2 4)
TAXA_CRUZAMENTO_VALUES=(1.0 0.8 0.6)
TAXA_MUTACAO_VALUES=(0.0001 0.001 0.01)
TIPO_CRUZAMENTO_VALUES=(0 1)

# Create base directory if it doesn't exist
mkdir -p $BASE_DIR

for POPULACAO in "${POPULACAO_VALUES[@]}"; do
    for GERACOES in "${GERACOES_VALUES[@]}"; do
        for NUM_ELITE in "${NUM_ELITE_VALUES[@]}"; do
            for TAXA_CRUZAMENTO in "${TAXA_CRUZAMENTO_VALUES[@]}"; do
                for TAXA_MUTACAO in "${TAXA_MUTACAO_VALUES[@]}"; do
                    for TIPO_CRUZAMENTO in "${TIPO_CRUZAMENTO_VALUES[@]}"; do
                        GOOD_RESULTS=()
                        for (( i=1; i<=$NUM_RUNS; i++ )); do
                            TEMP_FILE="${DATA_FILE_TEMPLATE}_${POPULACAO}_${GERACOES}_${NUM_ELITE}_${TAXA_CRUZAMENTO}_${TAXA_MUTACAO}_${TIPO_CRUZAMENTO}_${i}.txt"

                            echo "Running with POPULACAO=$POPULACAO, GERACOES=$GERACOES, NUM_ELITE=$NUM_ELITE, TAXA_CRUZAMENTO=$TAXA_CRUZAMENTO, TAXA_MUTACAO=$TAXA_MUTACAO, TIPO_CRUZAMENTO=$TIPO_CRUZAMENTO (Run $i)"
                            python src/tsp.py entradas/$FILE_ENTRADA.txt $POPULACAO $GERACOES $NUM_ELITE $TAXA_CRUZAMENTO $TAXA_MUTACAO $TIPO_CRUZAMENTO $TEMP_FILE

                            # Evaluate the result and decide if it's acceptable
                            RESULT=$(tail -n 1 $TEMP_FILE)  # Example: read the last line of the output file
                            echo "Result: $RESULT"

                            # Implement your criteria here
                            if (( $(echo "$RESULT < 380" | bc -l) )); then
                                echo "Good result: $RESULT"
                                GOOD_RESULTS+=($RESULT)
                            fi

                            # Clean up temporary file
                            rm $TEMP_FILE
                        done

                        if [ ${#GOOD_RESULTS[@]} -eq $NUM_RUNS ]; then
                            FINAL_DATA_FILE="${DATA_FILE_TEMPLATE}_${POPULACAO}_${GERACOES}_${NUM_ELITE}_${TAXA_CRUZAMENTO}_${TAXA_MUTACAO}_${TIPO_CRUZAMENTO}_final.txt"
                            {
                                echo "$POPULACAO"
                                echo "$GERACOES"
                                echo "$NUM_ELITE"
                                echo "$TAXA_CRUZAMENTO"
                                echo "$TAXA_MUTACAO"
                                echo "$TIPO_CRUZAMENTO"
                                for RESULT in "${GOOD_RESULTS[@]}"; do
                                    echo "$RESULT"
                                done
                            } > $FINAL_DATA_FILE
                        fi
                    done
                done
            done
        done
    done
done
