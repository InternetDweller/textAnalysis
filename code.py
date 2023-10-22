# -*- coding: utf-8 -*-

from prettytable import PrettyTable

#####################################################################
#####################################################################
##########################  НАТАША  #################################
#####################################################################
#####################################################################

# Судя по всему, вторая цифра в head_id это слово, которое имеет связь с данным словом

from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    
    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)

#####################################################################
#####################################################################
#########################  ГЛОБАЛЬНЫЕ  ##############################
#####################################################################
#####################################################################

greatArr = [['Требования']] #для складирования информации в таблицу

#####################################################################
#####################################################################
##########################  ФУНКЦИИ  ################################
#####################################################################
#####################################################################

def checkWord(word1, word2):
    if word1.pos == 'PUNCT':
        return False
    if word2.pos == 'PUNCT':
        return False
    if word1.pos == 'CCONJ':
        return False
    if word2.pos == 'CCONJ':
        return False
    if word1.pos == 'PRON':
        return False
    if word2.pos == 'PRON':
        return False
    if word1.pos == 'ADP':
        return False
    if word2.pos == 'ADP':
        return False
    if word1.pos == 'NUM':
        return False
    if word2.pos == 'NUM':
        return False
    if word1.id != word2.head_id:
        return False
    return True

# Функция выполняет весь набор действий по процессингу исходного текста
def syntaxise(text):
    parsedText = Doc(text)
    parsedText.segment(segmenter)
    parsedText.tag_morph(morph_tagger)
    for token in parsedText.tokens:
        token.lemmatize(morph_vocab)
    parsedText.parse_syntax(syntax_parser)
    return parsedText

# Функция читает файл, имя которого туда передали
def readFile(fileName):
    f = open(fileName, "r", encoding='utf8')
    return f.read()

# Функция сравнивает наборы пар и возвращает количество совпадений
# set1 - требования пользователя, set2 - возможности программы
def comparePairs(set1, set2, fNum):
    matches = 0
    for item in set1:
        item_count = set2.count(item)
        if item_count > 0:
            matches += 1
            greatArr[fNum].append('x' * item_count)
        else:
            greatArr[fNum].append('-')
    return matches

# Функция преобразует пары слов в массив строк для дальнейшего сравнения
def toList(syntaxed):
    myList = []
    for token in syntaxed.tokens:
        for ids in syntaxed.tokens:
            if (checkWord(token, ids) == True):
                myList.append(f"{token.lemma} {ids.lemma}")
    return myList

# Функция переделывает текст принимаемого файла в список пар
def bigProcess(file):
    newFile = readFile(file)
    fileText = syntaxise(newFile)
    newList = toList(fileText)
    return newList

# Функция разделяет исходный файл на массив строк и закидывает его в большой массив для вывода
def reqsForTable(file):
    newFile = readFile(file)
    lines = newFile.split('\n')
    for line in lines:
        greatArr[0].append(line)

# Функция принимает файл с требованиями и файлы документации, сравнивает их и выводит процент совпадения
def getResults(userReqs, files):
    fNum = 0
    userReqsForComp = bigProcess(userReqs)
    reqsForTable(userReqs)
    for file in files:
        greatArr.append([file])
        fNum = fNum + 1
        res = comparePairs(userReqsForComp, bigProcess(file), fNum)
        resPerc = res * 100 / len(userReqsForComp)
        print(f"{file}: {round(resPerc)}% ({res} из {len(userReqsForComp)})")

#Функция транспонирует массив с выходными данными для нормального построчного вывода
def transposeArr(arr):
    transpArr = []
    for i in range(len(arr[0])):
        temp = []
        for j in range(len(arr)):
            temp.append(arr[j][i])
        transpArr.append(temp)
    return transpArr

#Функция выводит таблицу с результатами при помощи библиотеки
def printPretty(arr):
    prettyArr = transposeArr(arr)
    mytable = PrettyTable()
    mytable.field_names = prettyArr[0]

    for i in range(1, len(prettyArr)):
        mytable.add_rows([prettyArr[i]])

    table = mytable.get_string()
    print(table)

#####################################################################
#####################################################################
######################## ОСНОВНОЙ КОД  ##############################
#####################################################################
#####################################################################

requirements = input('Имя файла с пользовательскими требованиями: ')
filenum = input('Количество файлов документации: ')

docfiles = []
for i in range(1, int(filenum) + 1):
    newdoc = input(f'Имя файла документации {i}: ')
    docfiles.append(newdoc)

print('\nРезультаты:')
getResults(requirements, docfiles)
printPretty(greatArr)