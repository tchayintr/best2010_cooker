import constants
import divs


def get_data_div_type(index):
    for indices in divs.BEST2010_DIVISION['TRAIN']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if index in r:
            return constants.BEST2010_TRAIN_DIV
    for indices in divs.BEST2010_DIVISION['VALID']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if index in r:
            return constants.BEST2010_VALID_DIV
    for indices in divs.BEST2010_DIVISION['TEST']:
        b = indices[0]
        e = indices[1] + 1
        r = range(b, e)
        if index in r:
            return constants.BEST2010_TEST_DIV


def remove_delimiters(line):
    line = line.replace(
        constants.CT_DELIM,
        constants.SL_TOKEN_DELIM)  # remove context delimiters '| |' -> ' '
    line = line.replace(
        constants.W_DELIM,
        constants.SL_TOKEN_DELIM)  # remove word delimiters '|' -> ' '
    line = line.strip()
    return line
