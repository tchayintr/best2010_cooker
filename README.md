# Thai BEST2010 Corpus Cooker
#### _best2010_cooker_

A tool for extracting segmented words from Thai segmented BEST2010 corpus.

#### Data formats
- **sl**: sentence line
- **wl**: word line

#### Usage
```
usage: best2010_cooker.py [-h] [--quiet] --input_data INPUT_DATA
                          [--output_data OUTPUT_DATA]
                          [--input_data_format INPUT_DATA_FORMAT]
                          [--output_data_format OUTPUT_DATA_FORMAT]
                          [--sentence_len_threshold SENTENCE_LEN_THRESHOLD]
                          [--gen_ne_vocab] [--gen_abbr_vocab]
                          [--include_empty_line]

optional arguments:
  -h, --help            show this help message and exit
  --quiet, -q           Do not report on screen
  --input_data INPUT_DATA, -i INPUT_DATA
                        File path to input data
  --output_data OUTPUT_DATA, -o OUTPUT_DATA
                        File path to output data
  --input_data_format INPUT_DATA_FORMAT, -f INPUT_DATA_FORMAT
                        Choose format of input data among from 'txt' (Default:
                        txt)
  --output_data_format OUTPUT_DATA_FORMAT
                        Choose format of output data among from 'wl' and 'sl'
                        (Default: sl)
  --sentence_len_threshold SENTENCE_LEN_THRESHOLD
                        Sentence length threshold. Sentences whose length are
                        lower than the threshold are ignored (Default: 1)
  --gen_ne_vocab        Specify to generate NE vocabulary
  --gen_abbr_vocab      Specify to generate abbreviation (ABBR) vocabulary
  --include_empty_line  Specify to inclde empty line
usage: best2010_cooker.py [-h] [--quiet] --input_data INPUT_DATA
                          [--output_data OUTPUT_DATA]
                          [--input_data_format INPUT_DATA_FORMAT]
                          [--output_data_format OUTPUT_DATA_FORMAT]
                          [--sentence_len_threshold SENTENCE_LEN_THRESHOLD]
  ```

  #### Example outputs
  ```
  Start time: 20201214_1706
  
  ### arguments
  # quiet=False
  # input_data=data/best2010-full.txt
  # output_data=cooked/
  # input_data_format=txt
  # output_data_format=sl
  # sentence_len_threshold=1
  # gen_ne_vocab=True
  # gen_abbr_vocab=True

  
  save cooked data: cooked/cooked_best2010_20201214_1706.sl
  save cooked data: cooked/cooked_best2010_20201214_1706.sl
  save cooked abbreviation data: cooked/cooked_best2010_20201214_1706.ne.vocab
  save cooked abbreviation data: cooked/cooked_best2010_20201214_1706.abbr.vocab

  ### report
  # [PRE] line: 148737 ...
  # [PRE] sent: 148737 ...
  # [POST] sent: 148720 ...
  # [POST] ne: 36148 ...
  # [POST] abbreviation: 742 ...
  # [POST] word: 5030836 ...
  # [POST] char: 20012984 ...
  # [POST] words/sent: min=1 max=378 avg=33.82756858526089
  # [POST] chars/sent: min=1 max=1991 avg=134.56820871436256
  # [POST] chars/word: min=1 max=101 avg=3.978063288089693
  ```
