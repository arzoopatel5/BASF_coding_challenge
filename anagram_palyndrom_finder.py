"""anagram and palindrome finder"""
from itertools import permutations, chain
from html.parser import HTMLParser
import urllib.request
import re
import argparse

#argparse lets you use command line arguments for python
parser = argparse.ArgumentParser(description='parse a website to find anagrams and palindromes')
parser.add_argument('-url', required=False, help='url for the website you want to parse')
args = parser.parse_args()

class StringEditor:
    """StringEditor can append strings, remove substrings, 
        reverse strings, and save and load files"""
    def append(string_1, string_2):
        """returns string_2 appended on to string_1"""
        return string_1 + string_2
    def remove(string_1, string_2):
        """returns string_1 with string_2 removed"""
        return string_1.replace(string_2, '')
    def mirror(string):
        """returns the reversed string"""
        return string[::-1]
    def save(file, string):
        """save a string to a file named "file" """
        with open(file, 'w', encoding="utf-8") as file_2:
            file_2.write(string)
    def load(file):
        """read a file named "file" and return it as a string"""
        with open(file, 'r', encoding="utf-8") as f:
            return f.read()
class Anagram(StringEditor):
    """Anagram can find all anagrams to a string"""
    def anagrams(string):
        """returns all permutations of a string"""
        #get all permutations and remove duplicates
        anagrams = set([''.join(i) for i in permutations(string)])
        #remove original string
        anagrams.remove(string)
        return anagrams
class Palindromes(StringEditor):
    """Palindromes stores only palindromes"""
    def __init__(self):
        """initialize with a set for palindromes"""
        self.palindromes = set()
    def palindrome(self, string):
        """adds string to palindromes if it is a palindrome"""
        if string == StringEditor.mirror(string):
            self.palindromes.add(string)
    def add_palindromes(self, words):
        """adds multiple strings to palindromes if they are palindromes"""
        for string in words:
            self.palindrome(string)
    def get_palindromes(self):
        """returns the palindromes stored in this object"""
        return list(self.palindromes)
class Parser(HTMLParser):
    """Parser is an extention of HTMLParser that can extract text from an HTML file"""
    def __init__(self):
        """initialize with a list for words"""
        HTMLParser.__init__(self)
        self.words = []
    def handle_data(self, data):
        """store words split by space into list"""
        self.words.append(data.split(' '))
    def get_words(self):
        """return words from HTML"""
        return self.words
def anagram_palyndrom_finder(url, filename='text.html'):
    """takes a url and extract the anagrams and palindromes from the webpage"""
    #download the url as HTML
    get_html(url, filename)
    #load the HTML file
    text = StringEditor.load(filename)
    #remove the script and style sections from the file
    text = re.sub('<script.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub('<style.*?</style>', '', text, flags=re.DOTALL)
    #parse the html for words
    parser = Parser()
    parser.feed(text)
    parser.close()
    words = parser.get_words()
    #flatten the list into a 1d list
    words = list(chain.from_iterable(words))
    #remove the characters that are not alphanumeric
    words = [re.sub(r'[\W_]+', '', word, flags=re.UNICODE).lower() for word in words]
    words = [re.sub(r'[0-9]+', '', word, flags=re.UNICODE) for word in words]
    #for the sake of runtime and memory efficiency, remove any words larger than 10 characters 
    #   because permutations take O(n!)
    words = [word for word in words if len(word) < 10]
    #remove duplicates
    words = list(set(words))
    if '' in words:
        words.remove('')
    return get_anagrams_palindromes(words)
#
def get_anagrams_palindromes(words):
    """gets the anagrams and palindromes from a list of words"""
    palindromes = Palindromes()
    palindromes.add_palindromes(words)
    anagrams = set()
    for word in words:
        potential_anagrams = Anagram.anagrams(word)
        for word_2 in words:
            if word_2 in potential_anagrams:
                anagrams.add(word)
                anagrams.add(word_2)
    anagrams.update(palindromes.get_palindromes())
    return list(anagrams)
#
def get_html(url, filename):
    """get the HTML file froma url"""
    try:
        file = urllib.request.urlopen(url)
    except:
        print('something went wrong with getting the website')
    else:
        StringEditor.save(filename, str(file.read().decode('utf-8')))

#uncomment for testing
assert StringEditor.append('a', 'b') == 'ab'
assert StringEditor.append('', 'b') == 'b'
assert StringEditor.append('a', '') == 'a'
assert StringEditor.append('', '') == ''

assert StringEditor.remove('abc', 'a') == 'bc'
assert StringEditor.remove('abc', 'b') == 'ac'
assert StringEditor.remove('abc', 'c') == 'ab'
assert StringEditor.remove('abc', 'd') == 'abc'
assert StringEditor.remove('abc', '') == 'abc'
assert StringEditor.remove('', 'a') == ''

assert StringEditor.mirror('abc') == 'cba'
assert StringEditor.mirror('ab') == 'ba'
assert StringEditor.mirror('a') == 'a'
assert StringEditor.mirror('') == ''

StringEditor.save('test.txt', 'test')
assert StringEditor.load('test.txt') == 'test'
StringEditor.save('test.txt', 'test\ntest')
assert StringEditor.load('test.txt') == 'test\ntest'
StringEditor.save('test.txt', '\n')
assert StringEditor.load('test.txt') == '\n'
StringEditor.save('test.txt', '')
assert StringEditor.load('test.txt') == ''

assert sorted(Anagram.anagrams('abc')) == sorted(['acb', 'bac', 'bca', 'cab', 'cba'])
assert Anagram.anagrams('ab') == set(['ba'])
assert Anagram.anagrams('a') == set()
assert sorted(Anagram.anagrams('aba')) == sorted(['aab', 'baa'])
assert Anagram.anagrams('') == set()

palindromes = Palindromes()
assert palindromes.get_palindromes() == []
palindromes.palindrome('a')
assert palindromes.get_palindromes() == ['a']
palindromes.palindrome('ab')
assert palindromes.get_palindromes() == ['a']
palindromes.palindrome('aba')
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aba'])
palindromes.palindrome('aba')
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aba'])
palindromes.palindrome('')
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aba', ''])
palindromes.add_palindromes(['a','aa','bab','bc'])
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aba', '', 'aa', 'bab'])
palindromes.add_palindromes([])
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aba', '', 'aa', 'bab'])
palindromes = Palindromes()
palindromes.add_palindromes([])
assert palindromes.get_palindromes() == []
palindromes.add_palindromes(['a', 'aa', 'bab', 'bc'])
assert sorted(palindromes.get_palindromes()) == sorted(['a', 'aa', 'bab'])

assert get_anagrams_palindromes(['a']) == ['a']
assert sorted(get_anagrams_palindromes(['a', 'b'])) == sorted(['a', 'b'])
assert sorted(get_anagrams_palindromes(['a', 'b', 'ab'])) == sorted(['a', 'b'])
assert sorted(get_anagrams_palindromes(['a', 'b', 'ab', 'ba'])) == sorted(['a', 'b', 'ab', 'ba'])
assert sorted(get_anagrams_palindromes(['a', 'b', 'ab', 'ba', 'ac',''])) == sorted(['a', 'b', 'ab', 'ba', ''])
assert get_anagrams_palindromes([]) == []

if args.url:
    for word in anagram_palyndrom_finder(args.url):
        print(word, end='\t')
    print('')
