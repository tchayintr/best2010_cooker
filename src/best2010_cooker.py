import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
'''
    Script for cooking BEST2010 corpus
        - NE
        - Abbreviation
        - word-level
        - characteristics
'''
'''
    Delimiter symbols
        # - \u00a0: NE delimeter (Non-breaking space based on standford nlp)
        - \u2582 (▂): NE delimeter and English white space
        - \u2585 (▄): Context delimiter
'''

# ORCHID delimiters

W_DELIM = '|'  # word delimiter
CT_DELIM = '| |'  # context delimiter
L_DELIM = '\n'  # line delimiter
TAG_PATTERN = '<[\w/]+>'
NE_TAG_PATTERN = '<NE>(.*?)</NE>'
ABBR_TAG_PATTERN = '<AB>(.*?)</AB>'
EMPTY_LINE_PATTERN = '^\s*$'

# for data io

DELIMITERS = {'NE_DELIMITER': '\u2582', 'CONTEXT_DELIMITER': '\u2585'}
SL_TOKEN_DELIM = ' '
SL_ATTR_DELIM = '_'
WL_TOKEN_DELIM = '\n'
WL_ATTR_DELIM = '\t'

SL_FORMAT = 'sl'
WL_FORMAT = 'wl'
NE_DATA_FORMAT = 'ne'
ABBR_DATA_FORMAT = 'abbr'
VOCAB_DATA_FORMAT = 'vocab'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quiet',
                        '-q',
                        action='store_true',
                        help='Do not report on screen')
    parser.add_argument('--input_data',
                        '-i',
                        type=Path,
                        required=True,
                        help='File path to input data')
    parser.add_argument('--output_data',
                        '-o',
                        type=Path,
                        default=None,
                        help='File path to output data')
    parser.add_argument(
        '--input_data_format',
        '-f',
        default='txt',
        help='Choose format of input data among from \'txt\' (Default: txt)')
    parser.add_argument(
        '--output_data_format',
        default='sl',
        help=
        'Choose format of output data among from \'wl\' and \'sl\' (Default: sl)'
    )
    parser.add_argument(
        '--sentence_len_threshold',
        type=int,
        default=1,
        help=
        'Sentence length threshold. Sentences whose length are lower than the threshold are ignored (Default: 1)'
    )
    parser.add_argument('--gen_ne_vocab',
                        action='store_true',
                        help='Specify to generate NE vocabulary')
    parser.add_argument(
        '--gen_abbr_vocab',
        action='store_true',
        help='Specify to generate abbreviation (ABBR) vocabulary')
    args = parser.parse_args()
    return args


def remove_delimiters(line):
    line = line.replace(
        CT_DELIM, SL_TOKEN_DELIM)  # remove context delimiters '| |' -> ' '
    line = line.replace(W_DELIM,
                        SL_TOKEN_DELIM)  # remove word delimiters '|' -> ' '
    line = line.strip()
    return line


def load_data(path, data_format):
    if data_format == 'txt':
        data = load_txt_data(path)

    else:
        print('Error: invalid data format: {}'.format(data_format),
              file=sys.stderr)
        sys.exit()

    return data


def load_txt_data(path):
    data = []
    with open(path, 'rt', encoding='utf8') as f:
        for line in f:
            line = line.strip(L_DELIM)
            data.append(line)
    return data


def gen_gold_data(data, data_format, threshold=1):
    if data_format == SL_FORMAT:
        data = gen_gold_data_SL(data, threshold)

    elif data_format == WL_FORMAT:
        data = gen_gold_data_WL(data, threshold)

    return data


def gen_gold_data_SL(data, threshold=1):
    gs = []  # gold data
    ls = data  # lines
    TAG_PATTERN_RE = re.compile(TAG_PATTERN)
    for l in ls:
        l = re.sub(TAG_PATTERN_RE, '', l)  # remove tags <tag> -> ''
        l = remove_delimiters(l)
        ws = l.split(SL_TOKEN_DELIM)  # words sequence
        if len(ws) < threshold or (len(ws) < 2 and len(
                ws[0]) < 1):  # filter by threshold and ignore empty line
            continue
        wl = SL_TOKEN_DELIM.join(ws)
        gs.append(wl)
    return gs


def gen_gold_data_WL(data, threshold=1):
    gs = []  # gold data
    ls = data  # lines
    TAG_PATTERN_RE = re.compile(TAG_PATTERN)
    for l in ls:
        l = re.sub(TAG_PATTERN_RE, '', l)  # remove tags <tag> -> ''
        l = remove_delimiters(l)
        ws = l.split(SL_TOKEN_DELIM)  # words sequence
        if len(ws) < threshold or (len(ws) < 2 and len(
                ws[0]) < 1):  # filter by threshold and ignore empty line
            continue
        wl = WL_TOKEN_DELIM.join(
            ws) + WL_TOKEN_DELIM  # concat with WL_DELIM for output data
        gs.append(wl)
    return gs


def gen_ne_vocab(data):
    vs = []  # ne vocabs
    ls = data  # lines
    TAG_PATTERN_RE = re.compile(TAG_PATTERN)
    NE_TAG_PATTERN_RE = re.compile(NE_TAG_PATTERN)
    for l in ls:
        l = remove_delimiters(l)
        nes = re.findall(NE_TAG_PATTERN_RE, l)
        nes = [re.sub(TAG_PATTERN_RE, '', ne) for ne in nes]
        nes = list(map(str.strip, nes))
        vs.extend(nes)
    vs = sorted([v for v in set(vs)])
    return vs


def gen_abbr_vocab(data):
    vs = []  # abbr vocabs
    ls = data  # lines
    TAG_PATTERN_RE = re.compile(TAG_PATTERN)
    ABBR_TAG_PATTERN_RE = re.compile(ABBR_TAG_PATTERN)
    for l in ls:
        l = remove_delimiters(l)
        abbrs = re.findall(ABBR_TAG_PATTERN_RE, l)
        abbrs = [re.sub(TAG_PATTERN_RE, '', abbr) for abbr in abbrs]
        abbrs = list(map(str.strip, abbrs))
        vs.extend(abbrs)
    vs = sorted([v for v in set(vs)])
    return vs


def log(message, file=sys.stderr):
    print(message, file=file)


def report(data, gold_data, ne_vocab=None, abbr_vocab=None):
    lines = data
    sents = gold_data

    n_psents = len(lines)
    n_sents = len(sents)

    ss = [s.split() for s in sents]
    ss_str = [''.join(s) for s in ss]
    ws = [w for s in ss for w in s]
    n_words = len(ws)

    cs = [c for w in ws for c in w]
    n_chars = len(cs)

    max_wps = len(max(ss, key=len))
    max_cps = len(max(ss_str, key=len))
    max_cpw = len(max(ws, key=len))

    min_wps = len(min(ss, key=len))
    min_cps = len(min(ss_str, key=len))
    min_cpw = len(min(ws, key=len))

    avg_wps = n_words / n_sents  # words/sentence
    avg_cps = n_chars / n_sents  # chars/sentence
    avg_cpw = n_chars / n_words  # chars/word

    log('### report')
    log('# [PRE] line: {} ...'.format(len(data)))
    log('# [PRE] sent: {} ...'.format(n_psents))
    log('# [POST] sent: {} ...'.format(n_sents))
    log('# [POST] ne: {} ...'.format(len(ne_vocab))) if ne_vocab else None
    log('# [POST] abbreviation: {} ...'.format(
        len(abbr_vocab))) if abbr_vocab else None
    log('# [POST] word: {} ...'.format(n_words))
    log('# [POST] char: {} ...'.format(n_chars))
    log('# [POST] words/sent: min={} max={} avg={}'.format(
        min_wps, max_wps, avg_wps))
    log('# [POST] chars/sent: min={} max={} avg={}'.format(
        min_cps, max_cps, avg_cps))
    log('# [POST] chars/word: min={} max={} avg={}'.format(
        min_cpw, max_cpw, avg_cpw))


def cook(args):
    start_time = datetime.now().strftime('%Y%m%d_%H%M')
    if not args.quiet:
        log('Start time: {}\n'.format(start_time))
        log('### arguments')
        for k, v in args.__dict__.items():
            log('# {}={}'.format(k, v))
        log('')

    data_path = args.input_data
    data = load_data(data_path, data_format=args.input_data_format)
    gold_data = gen_gold_data(data,
                              data_format=args.output_data_format,
                              threshold=args.sentence_len_threshold)

    ne_vocab = None
    abbr_vocab = None
    if args.gen_ne_vocab:
        ne_vocab = gen_ne_vocab(data)
    if args.gen_abbr_vocab:
        abbr_vocab = gen_abbr_vocab(data)

    if args.output_data:
        output_data_path = '{}/cooked_best2010_{}.{}'.format(
            args.output_data, start_time, args.output_data_format)
        with open(output_data_path, 'w', encoding='utf8') as f:
            for gd in gold_data:
                print(gd, file=f)
            if not args.quiet:
                log('save cooked data: {}'.format(output_data_path))
        if args.gen_ne_vocab:
            output_ne_data_path = '{}/cooked_best2010_{}.{}.{}'.format(
                args.output_data, start_time, NE_DATA_FORMAT,
                VOCAB_DATA_FORMAT)
            with open(output_ne_data_path, 'w', encoding='utf8') as f:
                for ne in ne_vocab:
                    print(ne, file=f)
                if not args.quiet:
                    log('save cooked NE data: {}'.format(output_ne_data_path))
        if args.gen_abbr_vocab:
            output_abbr_data_path = '{}/cooked_best2010_{}.{}.{}'.format(
                args.output_data, start_time, ABBR_DATA_FORMAT,
                VOCAB_DATA_FORMAT)
            with open(output_abbr_data_path, 'w', encoding='utf8') as f:
                for abbr in abbr_vocab:
                    print(abbr, file=f)
                if not args.quiet:
                    log('save cooked abbreviation data: {}'.format(
                        output_abbr_data_path))

    if not args.quiet:
        report(data, gold_data, ne_vocab, abbr_vocab)


def main():
    args = parse_args()
    cook(args)


if __name__ == '__main__':
    main()
