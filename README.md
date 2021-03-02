# Thai BEST2010 Corpus Cooker
#### _best2010_cooker_

A tool for extracting segmented words from Thai segmented BEST2010 corpus.

#### Data formats
- **sl**: sentence line
- **wl**: word line

#### Usage
```
usage: cooker.py [-h] [--quiet] --input_data INPUT_DATA
                 [--output_data OUTPUT_DATA]
                 [--input_data_format INPUT_DATA_FORMAT]
                 [--output_data_format OUTPUT_DATA_FORMAT]
                 [--sentence_len_threshold SENTENCE_LEN_THRESHOLD] [--denoise]
                 [--gen_ne_vocab] [--gen_ab_vocab] [--exclude_empty_line]
                 [--gen_div_data]

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
  --denoise             Specify to deeply clean the input data (original data
                        denoising) see README.md for more details
  --gen_ne_vocab        Specify to generate NE vocabulary
  --gen_ab_vocab        Specify to generate abbreviation (AB) vocabulary
  --exclude_empty_line  Specify to exclude empty line
  --gen_div_data        Specify to generate division data (train, valid, test)
                        see README.md for more details
```

#### Example outputs
```
Start time: 20210302_1201
(core) chayintr@cpu06:~/workspace/scripts/cooker/best2010$ ./sample_scripts/sample_cook.sh

### arguments
# quiet=False
# input_data=data/best2010-sample.txt
# output_data=cooked
# input_data_format=txt
# output_data_format=sl
# sentence_len_threshold=1
# denoise=True
# gen_ne_vocab=True
# gen_ab_vocab=True
# exclude_empty_line=False
# gen_div_data=True

save cooked data: cooked/cooked_best2010_20210302_1201.sl
save cooked train data: cooked/cooked_best2010_20210302_1201.train.sl
save cooked valid data: cooked/cooked_best2010_20210302_1201.valid.sl
save cooked test data: cooked/cooked_best2010_20210302_1201.test.sl
save cooked NE data: cooked/cooked_best2010_20210302_1201.ne.vocab
save cooked abbreviation data: cooked/cooked_best2010_20210302_1201.ab.vocab
### report
# [PRE] line: 50 ...
# [PRE] sent: 50 ...
# [POST] sent: 50 ...
# [POST] train-div: 44 ...
# [POST] valid-div: 4 ...
# [POST] test-div: 2 ...
# [POST] ne: 7 ...
# [POST] abbreviation: 1 ...
# [POST] word: 4020 ...
# [POST] char: 15977 ...
# [POST] words/sent: min=2 max=177 avg=80.4
# [POST] chars/sent: min=6 max=708 avg=319.54
# [POST] chars/word: min=1 max=20 avg=3.9743781094527364
Elapsed time: 0.112333 sec.
```

#### Data divisions (shuffled)
Merged from article, encyclopedia, news, and novel domains, respectively.
See `src/divs.py` for train, validation, and test indices referred to the original data.

#### Denoise (noisy data based on the original data)
13 cases (34 lines) were found to be noise data (incorrect annotation).
Each number refers to the line number in the original data
- <NE>w1</NE → <NE>w1</NE>
    - 5558 5559 5562 5913 6547 6567 6717 6737 
- <NE>w1>w2</NE> → <NE>w1 w2</NE>
    - 5603
- <NE>NE>w1</NE> → <NE>w1</NE>
    - 8153 80697 81086 81108 82631
- <NE>w1</NE</NE> → <NE>w1</NE>
    - 22548 80856 118267
- <NE>w1/NE></NE> → <NE>w1</NE>
    - 31526 79952 80137
- <NE>w1<w2</NE> → <NE>w1w2</NE>
    - 13049 45835
- AB>w1</AB> → <AB>w1</AB>
    - 54419
- <NE>w1></NE> → <NE>w1</NE>
    - 56893 91142 91144 91145
- <NE>w1</NE>w2</NE> → <NE>w1w2</NE>
    - 80145
- <NE>AB>w1w2</NE> → <NE><AB>w1</AB>w2</NE>
    - 82274 84065 89645
- <NE>w1</NE</NE>> → <NE>w1</NE>
    - 95647
- <NEw1</NE> → <NE>w1</NE>
    - 132798
- <NE>MERGE>w1</NE> → <NE>w1</NE>
    - 144226
