import argparse
from pathlib import Path


class CookerArgumentLoader(object):
    def __init__(self):
        pass

    def parse_args(self):
        args = self.get_argument_parser().parse_args()
        return args

    def get_argument_parser(self):
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
            help='Choose format of input data among from \'txt\' (Default: txt)'
        )
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
        parser.add_argument(
            '--denoise',
            action='store_true',
            help=
            'Specify to deeply clean the input data (original data denoising) see README.md for more details'
        )
        parser.add_argument('--gen_ne_vocab',
                            action='store_true',
                            help='Specify to generate NE vocabulary')
        parser.add_argument(
            '--gen_ab_vocab',
            action='store_true',
            help='Specify to generate abbreviation (AB) vocabulary')
        parser.add_argument('--exclude_empty_line',
                            action='store_true',
                            help='Specify to exclude empty line')
        parser.add_argument(
            '--gen_div_data',
            action='store_true',
            help=
            'Specify to generate division data (train, valid, test) see README.md for more details'
        )
        return parser
