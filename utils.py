from nltk.tokenize import sent_tokenize
import os
import re
from datetime import datetime

"""
sudo python -m nltk.downloader -d /usr/local/share/nltk_data all
"""


def print_log(txt_log):
    log_file = os.path.join('.', 'log.txt')
    try:
        with open(log_file, 'at') as log:
            log.write("{}   ==>   {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), txt_log))
        print(txt_log)
    except Exception as e:
        print(e)


def tokenize(text):
    sentences = sent_tokenize(text, language='english')
    return sentences


def parse_text(org_file, dst_file):
    try:
        para = []
        with open(org_file, 'rt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                para.append(line)
            para = ' '.join(para)

        new_para = split_sentence(para)
        with open(dst_file, 'wt', encoding='utf-8') as f:
            for line in new_para:
                f.write('{}\n'.format(line))
        return True
    except Exception as e:
        print(e)
        return False


def split_sentence(line):
    delimiters = ". ", "? ", "! "
    regex_pattern = '|'.join(map(re.escape, delimiters))
    texts = re.split(regex_pattern, line)
    return texts