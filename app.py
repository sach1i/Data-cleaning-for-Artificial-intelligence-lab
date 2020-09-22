from os import listdir
from os.path import isfile, join
import pathlib
from string import ascii_letters
import operator
import string


#  removes all characters but spaces, newline and normal alphabet letters
def remove_chars(line):
    line = line.lower()
    allowed = set(ascii_letters + ' ' + '\n')
    nochars = ''.join(l for l in line if l in allowed)
    return nochars


# deletes header, calls remove chars
def format_data(cat,copies):
    for c in cat:
        onlyfiles = [f for f in listdir(c) if isfile(join(c, f))]
        for file in onlyfiles:
            f = open(c + file, 'r')
            keep = 0
            content = f.readlines()
            for line in content:
                if len(line) == 1:
                    keep = content.index(line) + 1
                    break
            content = content[keep:]
            name = copies + copycats[cat.index(c)] + '\\' + str(onlyfiles.index(file))
            new = open(name, 'w+')
            for line in content:
                new.writelines(remove_chars(line))





#  takes file, appends all words from file to global string (string of all words from all files), calls 'add_to_dictionary'
def add_to_global(file):
    new = open(file, 'r')
    strings = new.readlines()
    glob_string = ''
    for s in strings:
        glob_string += s
    word_list = glob_string.split()
    for w in word_list:
        add_to_dictionary(w, (word_list.count(w)))


#  adds word to dictionary of all words across all documents with its frequency
def add_to_dictionary(word, word_count):
    if word in dictionary:
        dictionary[word] += word_count
    else:
        dictionary[word] = word_count


def set_attributes(file,d):
    for key in d:
        file.writelines(f'@ATTRIBUTE {key} NUMERIC\n')



def set_data(file, d, cat):
    new = open(file,'r')
    words = new.read()
    vector = []
    for key in d:
        if key in words:
            vector.append(1)
        else:
            vector.append(0)
    vector.append(cat)
    vector = str(vector)
    convert = vector.replace('[','').replace(']','\n').replace('\'','')
    convert = convert.replace(', ',',')
    return convert




if __name__ == '__main__':
    top_words = {}
    dictionary = {}
    amount_of_files = 10000
    counter = 0
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                  "you'd",
                  'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
                  'hers',
                  'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what',
                  'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were',
                  'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
                  'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
                  'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
                  'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                  'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
                  'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
                  'can',
                  'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
                  'ain',
                  'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
                  'hasn',
                  "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
                  "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                  "won't",
                  'wouldn', "wouldn't", 'would', 'could', 'should', 'im', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'ix',
                  'xx']
    stop_words.extend(list(string.ascii_lowercase))

    directory = (pathlib.Path(__file__).parent.absolute())
    copies = str(directory) + '\\copies\\'
    atheism = str(directory) + '\\.atheism\\'
    windows = str(directory) + '\\comp.windows.x\\'
    autos = str(directory) + '\\rec.autos\\'
    med = str(directory) + '\\sci.med\\'
    guns = str(directory) + '\\talk.politics.guns\\'

    cat = [atheism, autos, guns, med, windows]
    copycats = ['atheism', 'autos', 'guns', 'med', 'windows']
    format_data(cat, copies)
    for category in copycats:
        for i in range(1000):
            name = copies + category + '\\' + str(i)
            add_to_global(name)

    while counter < amount_of_files:
        key = max(dictionary.items(), key=operator.itemgetter(1))[0]
        value = dictionary[key]
        del dictionary[key]
        if (key not in stop_words) and (len(key) < 12):
            top_words[key] = value
            counter += 1

    arff = open('result.arff','w+')
    arff.writelines('@RELATION iris\n\n')
    set_attributes(arff, top_words)
    arff.writelines('@ATTRIBUTE document_category {atheism,autos,guns,med,windows}\n')
    arff.writelines('@DATA\n')

    for category in copycats:
        for i in range(1000):
            file_name = copies + category + '\\'+str(i)
            arff.write(set_data(file_name,top_words,category))
