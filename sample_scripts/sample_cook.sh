############################################
# txt input

INPUT_DATA=data/best2010-full.txt
OUTPUT_DATA=cooked/
INPUT_FORMAT=txt
OUTPUT_FORMAT=sl
SENTENCE_LEN_THRESHOLD=1

python3 src/best2010_cooker.py \
    --input_data $INPUT_DATA \
    --output_data $OUTPUT_DATA \
    --input_data_format $INPUT_FORMAT \
    --output_data_format $OUTPUT_FORMAT \
    --sentence_len_threshold $SENTENCE_LEN_THRESHOLD \
