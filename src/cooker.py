'''
    Script for cooking BEST2010 corpus
        - NE
        - Abbreviation
        - word-level
        - BEST2010 characteristics analysis
        - generate division data
          (train, valid, test)
'''

from collections import Counter
from datetime import datetime
import os
import re
import sys

from arguments import cooker_arguments
import common
import constants
from data_loaders import data_loader
import denoiser
import util


class Cooker(object):
    def __init__(self):
        self.args = self.get_args()
        self.data_loader = data_loader.DataLoader()

    def get_args(self):
        parser = cooker_arguments.CookerArgumentLoader()
        args = parser.parse_args()
        return args

    def denoise(self, data):
        return denoiser.Denoiser.run(data)

    def gen_gold_data(self,
                      data,
                      data_format,
                      threshold=1,
                      exclude_empty_line=False):
        if data_format == constants.SL_FORMAT:
            data = self.gen_gold_data_SL(data, threshold, exclude_empty_line)

        elif data_format == constants.WL_FORMAT:
            data = self.gen_gold_data_WL(data, threshold, exclude_empty_line)

        return data

    def gen_gold_data_SL(self, data, threshold=1, exclude_empty_line=False):
        gs = []  # gold data
        ls = data  # lines
        TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)
        for l in ls:
            l = re.sub(TAG_PATTERN_RE, '', l)  # remove tags <tag> -> ''
            l = common.remove_delimiters(l)
            ws = l.split(constants.SL_TOKEN_DELIM)  # words sequence
            if len(ws) < threshold:  # filter by threshold
                continue
            if exclude_empty_line and (len(ws) < 2 and
                                       len(ws[0]) < 1):  # to ignore empty line
                continue
            wl = constants.SL_TOKEN_DELIM.join(ws)
            gs.append(wl)
        return gs

    def gen_gold_data_WL(self, data, threshold=1, exclude_empty_line=False):
        gs = []  # gold data
        ls = data  # lines
        TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)
        for l in ls:
            l = re.sub(TAG_PATTERN_RE, '', l)  # remove tags <tag> -> ''
            l = common.remove_delimiters(l)
            ws = l.split(constants.SL_TOKEN_DELIM)  # words sequence
            if len(ws) < threshold:  # filter by threshold
                continue
            if exclude_empty_line and (len(ws) < 2 and
                                       len(ws[0]) < 1):  # to ignore empty line
                continue
            wl = constants.WL_TOKEN_DELIM.join(
                ws
            ) + constants.WL_TOKEN_DELIM  # concat with WL_DELIM for output data
            gs.append(wl)
        return gs

    def gen_div_data(self, data):
        train_data = []
        valid_data = []
        test_data = []
        for i, d in enumerate(data):
            data_div_type = common.get_data_div_type(i)
            if data_div_type == constants.BEST2010_TRAIN_DIV:
                train_data.append(d)
            elif data_div_type == constants.BEST2010_VALID_DIV:
                valid_data.append(d)
            elif data_div_type == constants.BEST2010_TEST_DIV:
                test_data.append(d)
        return train_data, valid_data, test_data

    def gen_common_vocab(self, data):
        word_dic = Counter()
        vs = []  # common vocabs
        ls = data  # lines
        for l in ls:
            ws = l.split(constants.SL_TOKEN_DELIM)
            word_dic.update(ws)
        vs = sorted(list(word_dic.keys()))
        return vs

    def gen_ne_vocab(self, data):
        vs = []  # ne vocabs
        ls = data  # lines
        TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)
        NE_TAG_PATTERN_RE = re.compile(constants.NE_TAG_PATTERN)
        for l in ls:
            l = common.remove_delimiters(l)
            nes = re.findall(NE_TAG_PATTERN_RE, l)
            nes = [re.sub(TAG_PATTERN_RE, '', ne) for ne in nes]
            nes = list(map(str.strip, nes))
            vs.extend(nes)
        vs = sorted([v for v in set(vs)])
        return vs

    def gen_ab_vocab(self, data):
        vs = []  # ab vocabs
        ls = data  # lines
        TAG_PATTERN_RE = re.compile(constants.TAG_PATTERN)
        AB_TAG_PATTERN_RE = re.compile(constants.AB_TAG_PATTERN)
        for l in ls:
            l = common.remove_delimiters(l)
            abbrs = re.findall(AB_TAG_PATTERN_RE, l)
            abbrs = [re.sub(TAG_PATTERN_RE, '', abbr) for abbr in abbrs]
            abbrs = list(map(str.strip, abbrs))
            vs.extend(abbrs)
        vs = sorted([v for v in set(vs)])
        return vs

    def log(self, message, file=sys.stderr):
        print(message, file=file)

    def summarize(self,
                  data,
                  gold_data,
                  train_gdata=None,
                  valid_gdata=None,
                  test_gdata=None,
                  train_common_vocab=None,
                  valid_common_vocab=None,
                  test_common_vocab=None,
                  train_ne_vocab=None,
                  valid_ne_vocab=None,
                  test_ne_vocab=None,
                  train_ab_vocab=None,
                  valid_ab_vocab=None,
                  test_ab_vocab=None,
                  common_vocab=None,
                  ne_vocab=None,
                  ab_vocab=None):
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

        self.log('### report')
        self.log('# [PRE] line: {} ...'.format(len(data)))
        self.log('# [PRE] sent: {} ...'.format(n_psents))
        self.log('# [POST] sent: {} ...'.format(n_sents))
        self.log('# [POST] train-div: {} ...'.format(
            len(train_gdata))) if train_gdata else None
        self.log('# [POST] valid-div: {} ...'.format(
            len(valid_gdata))) if valid_gdata else None
        self.log('# [POST] test-div: {} ...'.format(
            len(test_gdata))) if test_gdata else None
        self.log('# [POST] common vocab: {} ...'.format(
            len(common_vocab))) if common_vocab else None
        self.log('# [POST] ne: {} ...'.format(
            len(ne_vocab))) if ne_vocab else None
        self.log('# [POST] abbreviation: {} ...'.format(
            len(ab_vocab))) if ab_vocab else None

        self.log('# [POST] train-vocab: {} ...'.format(
            len(train_common_vocab))) if train_common_vocab else None
        self.log('# [POST] valid-vocab: {} ...'.format(
            len(valid_common_vocab))) if valid_common_vocab else None
        self.log('# [POST] test-vocab: {} ...'.format(
            len(test_common_vocab))) if test_common_vocab else None

        self.log('# [POST] train-ne: {} ...'.format(
            len(train_ne_vocab))) if train_ne_vocab else None
        self.log('# [POST] valid-ne: {} ...'.format(
            len(valid_ne_vocab))) if valid_ne_vocab else None
        self.log('# [POST] test-ne: {} ...'.format(
            len(test_ne_vocab))) if test_ne_vocab else None

        self.log('# [POST] train-ab: {} ...'.format(
            len(train_ab_vocab))) if train_ab_vocab else None
        self.log('# [POST] valid-ab: {} ...'.format(
            len(valid_ab_vocab))) if valid_ab_vocab else None
        self.log('# [POST] test-ab: {} ...'.format(
            len(test_ab_vocab))) if test_ab_vocab else None

        self.log('# [POST] word: {} ...'.format(n_words))
        self.log('# [POST] char: {} ...'.format(n_chars))
        self.log('# [POST] words/sent: min={} max={} avg={}'.format(
            min_wps, max_wps, avg_wps))
        self.log('# [POST] chars/sent: min={} max={} avg={}'.format(
            min_cps, max_cps, avg_cps))
        self.log('# [POST] chars/word: min={} max={} avg={}'.format(
            min_cpw, max_cpw, avg_cpw))

    def cook(self):
        start_time = datetime.now().strftime('%Y%m%d_%H%M')
        if not self.args.quiet:
            timer = util.Timer()
            timer.start()
            self.log('Start time: {}\n'.format(start_time))
            self.log('### arguments')
            for k, v in self.args.__dict__.items():
                self.log('# {}={}'.format(k, v))
            self.log('')

        data_path = self.args.input_data
        data = self.data_loader.load_data(
            data_path, data_format=self.args.input_data_format)

        if self.args.denoise:
            data = self.denoise(data)

        gold_data = self.gen_gold_data(
            data,
            data_format=self.args.output_data_format,
            threshold=self.args.sentence_len_threshold,
            exclude_empty_line=self.args.exclude_empty_line)

        # generate train, valid, test divisions along with their NEs and ABs
        train_gdata = None
        valid_gdata = None
        test_gdata = None

        train_common_vocab = None
        valid_common_vocab = None
        test_common_vocab = None

        train_ne_vocab = None
        valid_ne_vocab = None
        test_ne_vocab = None

        train_ab_vocab = None
        valid_ab_vocab = None
        test_ab_vocab = None
        if self.args.gen_div_data:
            # train_data, valid_data, test_data = self.gen_div_data(gold_data)
            train_data, valid_data, test_data = self.gen_div_data(data)
            train_gdata = self.gen_gold_data(
                train_data,
                data_format=self.args.output_data_format,
                threshold=self.args.sentence_len_threshold,
                exclude_empty_line=self.args.exclude_empty_line)
            valid_gdata = self.gen_gold_data(
                valid_data,
                data_format=self.args.output_data_format,
                threshold=self.args.sentence_len_threshold,
                exclude_empty_line=self.args.exclude_empty_line)
            test_gdata = self.gen_gold_data(
                test_data,
                data_format=self.args.output_data_format,
                threshold=self.args.sentence_len_threshold,
                exclude_empty_line=self.args.exclude_empty_line)
            if self.args.gen_common_vocab:
                train_common_vocab = self.gen_common_vocab(train_gdata)
                valid_common_vocab = self.gen_common_vocab(valid_gdata)
                test_common_vocab = self.gen_common_vocab(test_gdata)
            if self.args.gen_ne_vocab:
                train_ne_vocab = self.gen_ne_vocab(train_data)
                valid_ne_vocab = self.gen_ne_vocab(valid_data)
                test_ne_vocab = self.gen_ne_vocab(test_data)
            if self.gen_ab_vocab:
                train_ab_vocab = self.gen_ab_vocab(train_data)
                valid_ab_vocab = self.gen_ab_vocab(valid_data)
                test_ab_vocab = self.gen_ab_vocab(test_data)

        # generate global common, NE and AB vocabularies
        common_vocab = None
        ne_vocab = None
        ab_vocab = None
        if self.args.gen_common_vocab:
            common_vocab = self.gen_common_vocab(gold_data)
        if self.args.gen_ne_vocab:
            ne_vocab = self.gen_ne_vocab(data)
        if self.args.gen_ab_vocab:
            ab_vocab = self.gen_ab_vocab(data)

        # print to files
        if self.args.output_data:
            output_data_dir = self.args.output_data
            output_data_prefix_dir = '{}'.format(start_time)
            output_data_prefix_path = 'cooked_best2010_{}'.format(start_time)
            # if not os.path.exists(output_data_dir):
            #     os.makedirs(output_data_dir)
            if not os.path.exists(output_data_dir / output_data_prefix_dir):
                os.makedirs(output_data_dir / output_data_prefix_dir)
            output_data_path = '{}/{}/{}.{}'.format(
                output_data_dir, output_data_prefix_dir,
                output_data_prefix_path, self.args.output_data_format)
            with open(output_data_path, 'w', encoding='utf8') as f:
                for gd in gold_data:
                    print(gd, file=f)
                if not self.args.quiet:
                    self.log('save cooked data: {}'.format(output_data_path))

            if self.args.gen_div_data:
                output_train_data_path = '{}/{}/{}.{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.BEST2010_TRAIN_DIV,
                    constants.SL_FORMAT)
                output_valid_data_path = '{}/{}/{}.{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.BEST2010_VALID_DIV,
                    constants.SL_FORMAT)
                output_test_data_path = '{}/{}/{}.{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.BEST2010_TEST_DIV,
                    constants.SL_FORMAT)
                with open(output_train_data_path, 'w', encoding='utf8') as f:
                    for trd in train_gdata:
                        print(trd, file=f)
                    if not self.args.quiet:
                        self.log('save cooked train data: {}'.format(
                            output_train_data_path))
                with open(output_valid_data_path, 'w', encoding='utf8') as f:
                    for vad in valid_gdata:
                        print(vad, file=f)
                    if not self.args.quiet:
                        self.log('save cooked valid data: {}'.format(
                            output_valid_data_path))
                with open(output_test_data_path, 'w', encoding='utf8') as f:
                    for ted in test_gdata:
                        print(ted, file=f)
                    if not self.args.quiet:
                        self.log('save cooked test data: {}'.format(
                            output_test_data_path))

                if self.args.gen_common_vocab:
                    output_train_vocab_data_path = '{}/{}/{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TRAIN_DIV,
                        constants.VOCAB_DATA_FORMAT)
                    output_valid_vocab_data_path = '{}/{}/{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_VALID_DIV,
                        constants.VOCAB_DATA_FORMAT)
                    output_test_vocab_data_path = '{}/{}/{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TEST_DIV,
                        constants.VOCAB_DATA_FORMAT)
                    with open(output_train_vocab_data_path,
                              'w',
                              encoding='utf8') as f:
                        for train_cvocab in train_common_vocab:
                            print(train_cvocab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked train common vocab data: {}'.
                                     format(output_train_vocab_data_path))
                    with open(output_valid_vocab_data_path,
                              'w',
                              encoding='utf8') as f:
                        for valid_cvocab in valid_common_vocab:
                            print(valid_cvocab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked valid common vocab data: {}'.
                                     format(output_valid_vocab_data_path))
                    with open(output_test_vocab_data_path,
                              'w',
                              encoding='utf8') as f:
                        for test_cvocab in test_common_vocab:
                            print(test_cvocab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked test common vocab data: {}'.
                                     format(output_test_vocab_data_path))
                if self.args.gen_ne_vocab:
                    output_train_ne_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TRAIN_DIV,
                        constants.NE_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    output_valid_ne_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_VALID_DIV,
                        constants.NE_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    output_test_ne_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TEST_DIV,
                        constants.NE_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    with open(output_train_ne_data_path, 'w',
                              encoding='utf8') as f:
                        for train_ne in train_ne_vocab:
                            print(train_ne, file=f)
                        if not self.args.quiet:
                            self.log('save cooked train NE data: {}'.format(
                                output_train_ne_data_path))
                    with open(output_valid_ne_data_path, 'w',
                              encoding='utf8') as f:
                        for valid_ne in valid_ne_vocab:
                            print(valid_ne, file=f)
                        if not self.args.quiet:
                            self.log('save cooked valid NE data: {}'.format(
                                output_valid_ne_data_path))
                    with open(output_test_ne_data_path, 'w',
                              encoding='utf8') as f:
                        for test_ne in test_ne_vocab:
                            print(test_ne, file=f)
                        if not self.args.quiet:
                            self.log('save cooked test NE data: {}'.format(
                                output_test_ne_data_path))
                if self.args.gen_ab_vocab:
                    output_train_ab_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TRAIN_DIV,
                        constants.AB_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    output_valid_ab_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_VALID_DIV,
                        constants.AB_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    output_test_ab_data_path = '{}/{}/{}.{}.{}.{}'.format(
                        output_data_dir, output_data_prefix_dir,
                        output_data_prefix_path, constants.BEST2010_TEST_DIV,
                        constants.AB_DATA_FORMAT, constants.VOCAB_DATA_FORMAT)
                    with open(output_train_ab_data_path, 'w',
                              encoding='utf8') as f:
                        for train_ab in train_ab_vocab:
                            print(train_ab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked train AB data: {}'.format(
                                output_train_ab_data_path))
                    with open(output_valid_ab_data_path, 'w',
                              encoding='utf8') as f:
                        for valid_ab in valid_ab_vocab:
                            print(valid_ab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked valid AB  data: {}'.format(
                                output_valid_ab_data_path))
                    with open(output_test_ab_data_path, 'w',
                              encoding='utf8') as f:
                        for test_ab in test_ab_vocab:
                            print(test_ab, file=f)
                        if not self.args.quiet:
                            self.log('save cooked test AB data: {}'.format(
                                output_test_ab_data_path))

            if self.args.gen_common_vocab:
                output_vocab_data_path = '{}/{}/{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.VOCAB_DATA_FORMAT)
                with open(output_vocab_data_path, 'w', encoding='utf8') as f:
                    for vocab in common_vocab:
                        print(vocab, file=f)
                    if not self.args.quiet:
                        self.log('save cooked common vocab data: {}'.format(
                            output_vocab_data_path))
            if self.args.gen_ne_vocab:
                output_ne_data_path = '{}/{}/{}.{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.NE_DATA_FORMAT,
                    constants.VOCAB_DATA_FORMAT)
                with open(output_ne_data_path, 'w', encoding='utf8') as f:
                    for ne in ne_vocab:
                        print(ne, file=f)
                    if not self.args.quiet:
                        self.log('save cooked NE data: {}'.format(
                            output_ne_data_path))
            if self.args.gen_ab_vocab:
                output_ab_data_path = '{}/{}/{}.{}.{}'.format(
                    output_data_dir, output_data_prefix_dir,
                    output_data_prefix_path, constants.AB_DATA_FORMAT,
                    constants.VOCAB_DATA_FORMAT)
                with open(output_ab_data_path, 'w', encoding='utf8') as f:
                    for abbr in ab_vocab:
                        print(abbr, file=f)
                    if not self.args.quiet:
                        self.log('save cooked abbreviation data: {}'.format(
                            output_ab_data_path))

        if not self.args.quiet:
            self.summarize(data, gold_data, train_gdata, valid_gdata,
                           test_gdata, train_common_vocab, valid_common_vocab,
                           test_common_vocab, train_ne_vocab, valid_ne_vocab,
                           test_ne_vocab, train_ab_vocab, valid_ab_vocab,
                           test_ab_vocab, common_vocab, ne_vocab, ab_vocab)
            timer.stop()
            print('Elapsed time: {:6f} sec.'.format(timer.elapsed),
                  file=sys.stderr)


if __name__ == '__main__':
    cooker = Cooker()
    cooker.cook()
