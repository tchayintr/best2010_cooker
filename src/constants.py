# BEST2010 delimiters

W_DELIM = '|'  # word delimiter
CT_DELIM = '| |'  # context delimiter
L_DELIM = '\n'  # line delimiter
TAG_PATTERN = '<[\w/]+>'
NE_TAG_PATTERN = '<NE>(.*?)</NE>'
AB_TAG_PATTERN = '<AB>(.*?)</AB>'
EMPTY_LINE_PATTERN = '^\s*$'

NE_DELIM_STANFORD_T = '\u00a0'  # NE delimeter (Non-breaking space based on standford nlp)
NE_DELIM_T = '▂'  # NE delimeter and English white space \u2582
CT_DELIM_T = '▄'  # Context delimiter

# for data io

DELIMITERS = {'NE_DELIMITER': '\u2582', 'CONTEXT_DELIMITER': '\u2585'}
SL_TOKEN_DELIM = ' '
SL_ATTR_DELIM = '_'
WL_TOKEN_DELIM = '\n'
WL_ATTR_DELIM = '\t'

SEG_FORMAT = 'seg'
SL_FORMAT = 'sl'
WL_FORMAT = 'wl'
NE_DATA_FORMAT = 'ne'
AB_DATA_FORMAT = 'ab'
VOCAB_DATA_FORMAT = 'vocab'

BEST2010_TRAIN_DIV = 'train'
BEST2010_VALID_DIV = 'valid'
BEST2010_TEST_DIV = 'test'
