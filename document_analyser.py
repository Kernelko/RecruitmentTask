"""This program counts words in all .txt documents it can find in a directory,
and sorts them according to their occurrence.
Then, it returns a dictionary with a given word, how many times it occurred,
document names where it occurred and sentences with this word.
User can provide the parameter "number", to specify how many top results
(word,text id, sentences) are needed in output (default is 10).
Optionally, the user can provide a list of words to be excluded from the results,
because prepositions like "the", "a" and others usually don't provide a lot of 
information about the text. 
"""

import glob
from collections import defaultdict
from os.path import basename
import argparse

class LinesNumberException(Exception):
    """Raised when parameter number is not a number"""
    pass
class FilesNotPresentException(Exception):
    """Raised when the there are no files"""
    pass
class FilesEmptyException(Exception):
    """Raised when the files are empty"""
    pass

parser = argparse.ArgumentParser()
parser.add_argument("number",default="10",nargs = '?', help = "Display n amount of data where n is a given value")
parser.add_argument('common', nargs='?', type=argparse.FileType('r'), help='Filename of source of the words to be excluded')
args = parser.parse_args()

if not args.number.isnumeric():
    raise LinesNumberException

if args.common:
            common_words_list = args.common.read().lower().split()
else:
    common_words_list=[]


def get_files():
    """get files and check if there are any"""
    files = glob.glob('*.txt')
    if not files:
        raise FilesNotPresentException
    return files

def get_content():
    """get words from files, check if files are not empty"""
    for filename in get_files():
        document_name = basename(filename)
        with open(filename, encoding='utf8') as file:
            content = file.read().lower()
            for sentence in content.split("."):
                for word in sentence.split():
                    if word in common_words_list:
                        break 
                    else:
                        yield word.strip(','), sentence.strip('\n').strip(), document_name

def count_occurrence():
    """count words occurences"""
    occurrence_dict = defaultdict(WordCount)
    content = get_content()
    if not content:
        raise FilesEmptyException
    for word, sentence, document_name in content:
        occurrence_dict[word].increment(sentence, document_name)
    sorted_occurrence_dict = sorted(occurrence_dict.items(), key=lambda kv: -kv[1].count)
    return sorted_occurrence_dict

class WordCount(object):
    """class with word name, occurence, document membership and sentences where it occurrs"""
    def __init__(self):
        self.count = 0
        self.sentences = set()
        self.document_names = set()

    def increment(self, sentence, document_name):
        """increments the counter, adds sentences and document names"""
        self.count += 1
        self.sentences.add(sentence)
        self.document_names.add(document_name)

def get_result():
    """gets the result of documents analysis"""
    i = 0
    result = count_occurrence()
    while i < int(args.number):
        yield result[i][0], result[i][1].document_names, result[i][1].sentences
try:
    for element in get_result():
        print(element)

except LinesNumberException:
    print("ERROR: result size is not a number, please type numeric value.")
except FilesNotPresentException:
    print("ERROR: No files in directory to process.")
except FilesEmptyException:
    print("ERROR: All your files are empty, nothing to process.")
