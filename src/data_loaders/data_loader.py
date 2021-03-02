import sys

import constants


class DataLoader(object):
    def __init__(self):
        pass

    def load_data(self, path, data_format):
        if data_format == 'txt':
            data = self.load_txt_data(path)

        else:
            print('Error: invalid data format: {}'.format(data_format),
                  file=sys.stderr)
            sys.exit()

        return data

    def load_txt_data(self, path):
        data = []
        with open(path, 'rt', encoding='utf8') as f:
            for line in f:
                line = line.strip(constants.L_DELIM)
                data.append(line)
        return data
