############################################
# txt input

INPUT_DATA=data/best2010-sample.txt
OUTPUT_DATA=cooked/
INPUT_FORMAT=txt
OUTPUT_FORMAT=sl
SENTENCE_LEN_THRESHOLD=1

python3 src/cooker.py \
    --input_data $INPUT_DATA \
    --output_data $OUTPUT_DATA \
    --input_data_format $INPUT_FORMAT \
    --output_data_format $OUTPUT_FORMAT \
    --sentence_len_threshold $SENTENCE_LEN_THRESHOLD \
    --denoise \
    --gen_common_vocab \
    --gen_ne_vocab \
    --gen_ab_vocab \
    --gen_div_data \
    # --exclude_empty_line \
    # --quiet
