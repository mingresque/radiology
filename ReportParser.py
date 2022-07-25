"""
    This file will check on *.txt documents
    1. Extract all lines (findings and impression).
"""


import re
import json
import os
import requests
import operator
import pyperclip

class Terms:
    linkingverb = ["are", "is", "may"]
    article = ["a", "an", "the"]
    preposition = ["from", "as", "which","in", "its", "of", "there", "to", "and", "at", "also", "on", "with", "around"]
    verb = ["seen", "noted"]
    adjective = ["mild", "minimal"]
    pad = tuple(article + linkingverb + preposition + verb + adjective)
    acronym = {"anterior talofibular ligament": "ATFL",
                "flexor hallucis longus": "FHL",
                "anterior cruciate ligament": "ACL",
                "posterior cruciate ligament": "PCL",
                "lateral collateral ligament": "LCL",
                "medial collateral ligament": "MCL",
                "metatarsophalangeal": "MTP",
                "interphalangeal": "IP",
                "right": "[R]",
                "left": "[L]",
                "bilateral": "[B]",
                "represent": "=",
                "show": "=",
                "suggestive": "="}


class unusedFunc:
    def extractLine(text: str) -> list:
        return [line.strip() for line in
        text.lower().split('\n') if not text.isspace()]


class fileLoads:
    def __init__(self, fileRaw: str, fileJsn: str, fileGit: str) -> None:
        self.fileRaw = fileRaw  # Raw file containing the original report.
        self.fileJsn = fileJsn  # Jsn file containing the normal findings and impression.
        self.fileGit = fileGit  # Git URL containg the final product.
        self.RawA, self.RawB = self.fileRaw_load()
        self.Jsn = self.fileJsn_load()
        self.GitRaw = requests.get(self.fileGit).text
        self.Git = self.fileGit_load()
        self.GitFix = self.fileGit_loadArray()

    def fileRaw_load(self) -> list:
        with open(self.fileRaw) as file: dataList = file.read()
        return self.extractLines(dataList)  # Get lists of lines from raw file.

    def extractLines(self, texts: str) -> tuple[list, list]:
        """ Pass string from textfile, and this function will separate impression and findings.
        """
        nonEmptyLines = [line.strip() for line in texts.split("\n") if line.strip() != ""]
        a, b = 0, 0
        for index, line in enumerate(nonEmptyLines):
            # print(index, line)
            if line.lower().startswith("findings:"):
                a = index
            elif line.lower().startswith("impression:"):
                b = index
                # break
        findings = nonEmptyLines[a + 1: b - 1]
        
        reg = r'([^0-9])\.([^\S\n])'
        for index, i in enumerate(findings):
            if bool(re.search(reg, i)):
                x = re.sub(reg, r'\1.***', i)
                x = x.split("***")
                # print(x)
                findings[index] = x
                # print(f'with DOT: {i}')
            # if isMatch()
        findings = flattenList(findings)
        # print(findings)
        impression = nonEmptyLines[b + 1: -1]
        return findings, impression

        #x = "I am not happy 3.4 x 3.5 x 3.0 with you. This is sad."
        #print(re.sub(r'([^0-9])\.([^0-9])', r'\1(.)***', x))
        # I am not happy 3.4 x 3.5 x 3.0 with you(.)***This is sad.



    def fileJsn_load(self) -> list:
        temp_list = []
        if os.path.exists(self.fileJsn):
            with open(self.fileJsn) as f:
                try:
                    temp_list = json.load(f)
                except json.JSONDecodeError:
                    pass
        return temp_list

    def fileJsn_dump(self) -> None:
        with open(self.fileJsn, "w") as f: json.dump(self.Jsn, f, indent=4)

    def extract(self, rawData: str) -> list[tuple[str, str, str]]:
        ''' Receives a text from Github file with the format
                .tag1 tag 2
                impression1
                -
                finding1
        Returns a tuple of tuples with the following indices:
                [0] tag1
                [1] impression
                [2] findings'''
        ws = '\n\v\f\r\u2028\u2029'
        array = []
        for i in rawData.split('\n.')[1:-1]:
            find = re.findall('^(.*)' f'[{ws}]*' f'([{ws}\w\W]' '{1,})' f'[{ws}]' '^\-' f'[{ws}]*' f'([{ws}\w\W]' '*)', i, re.MULTILINE)
            if len(find[0]) == 3:
                flat = find[0]
                array += [(flat[0], flat[1].strip(), flat[2].strip())]
        return array
    def fileGit_load(self) -> list:
        x = self.extract(self.GitRaw)
        listss = [h for i in x for index, h in enumerate(i) if index == 1]
        return listss

    def fileGit_loadArray(self, text=None) -> tuple[tuple[int, str, tuple[str], tuple[str]]]:
        ''' Receives a text from Github file with the format
                .tag1 tag 2
                impression1
                -
                finding1
            Returns a tuple of tuples with the following indices:
                [0] - int: index number
                [1] - str: tags
                [2] - tuple of impression lines
                [3] - tuple of finding lines'''
        cleanText = lambda x: list(map(lambda line: line.strip(), x))
        if text is None: text = self.GitRaw
        text = text.split("\n")
        array = []
        for index, line in enumerate(cleanText(text)):
            if line == "": continue
            if line.startswith("# "): continue
            if line.startswith("."):
                if array != []: array[-1][3] = tuple(array[-1][3])
                array += [[index + 1, line[1:], [], []]]
                toggle = 2

            elif line.startswith("-"):
                array[-1][2] = tuple(array[-1][2]) 
                #if array[-1][toggle]
                toggle = 3
            else:
                array[-1][toggle].append(line)
        return tuple(tuple(sub) for sub in array)


def extractColumn(col: list[int], array: list) -> list:
    return list(map(operator.itemgetter(*col), array))


def stripWord(phrase: str) -> str:
    display = phrase  # .lower()
    for i in Terms.pad:
        # continue
        display = re.sub(r"[ ]{0,}\b" + i + r"\b[ ]{0,}", " ", display, flags=re.I)

    for i in Terms.acronym:
        if isMatch(display, i):
            display = re.sub(r"\b" + i + r"\b", Terms.acronym[i], display, flags=re.I)
    return display.strip()


def initializeNormal() -> None:
    print(z.RawA)
    print("")
    print(z.RawB)
    for _, line in enumerate(z.RawA):
        if line in z.Jsn: continue

        display = stripWord(line)

        inputs = input(f"\nIs this normal: {display}?\n")
        if inputs == "q": return None
        if inputs != "n": z.Jsn.append(line)
    z.fileJsn_dump()


def sortLines(inputs: str):

    def enumerateFindings(skipIndex: list = None):
        for index, line in enumerate(z.RawA):
            if skipIndex != None:
                if index in skipIndex: continue
            if index in extractColumn([1], userSelect): continue
            identifier = ""
            if line in z.Jsn:
                identifier = "n"
                continue
            temp = stripWord(line) if complete else line[0:y]
            print(f"{index:3} {identifier:2} {temp}")
    userSelect = tuple(tuple(map(int, line.split())) for line in inputs.split("\n") if line.strip() != "")
    print("\nIMPRESSION:")
    for index, line in enumerate(z.RawB):
        if index in extractColumn([0], userSelect): continue
        identifier = "x" if line in z.Git else ""
        temp = stripWord(line) if complete else line[0:y]
        print(f"{index:3} {identifier:2} {temp}")

    print("\nFINDINGS:")
    enumerateFindings()

    if userSelect[0][0] != 999:
        for i in userSelect:
            print(f'\n{i}')
            print(f".{consultant}")
            print(z.RawB[i[0]], end="\n-\n")
            print(z.RawA[i[1]])

    takenIndices = []
    checker = []
    choices = []
    freePass = False
    for index, line in (i for i in enumerate(z.RawB)):
        clean = stripWord(line)
        print(f"\nStatement {index+1} of {len(z.RawB)}: {clean}")
        enumerateFindings(takenIndices + choices)
        print(f"Type [q]uit or FINDINGS indices (separated by space): _", end="")
        while True:
            user2 = input("_ ")
            if user2 == "q": return False
            if user2 == "pass": break
            if re.sub("[^\S\n]", "", user2).isdigit():
                # if index >= 1: checker += [(index, choices)]
                choices = list(map(int, user2.split()))
                for i in choices: print(i, stripWord(z.RawA[i]))
                user3 = input(f'Are these correct? [Y]es/[N]o : _')
                if user3 == "": 
                    takenIndices += choices
                    checker += [(index, choices)]
                    break      
        continue

        while True:
            user3 = input(f'Are these correct? [Y]es/[N]o : _')
            if user3 == "q": return False
            if user3 == "n":
                print("Input another value. _")
            else:
                choices = list(map(int, user2.split()))

                break  # 1 of 2 ways out of this loop.
    strings = ""
    xx = os.linesep
    inputs = input("Part? \n_")
    yy = USER.consultant + " part_" + inputs
    for x, y in checker:
        strings += f"{xx}{xx}.{yy}{xx}{z.RawB[x]}{xx}-{xx}"
        for j in y:
            strings += z.RawA[j] + xx
    pyperclip.copy(strings)
    print(strings)

    return 1


def arrayFromFile(sDir: str) -> tuple[str]:  # import os
    fileList = os.listdir(sDir)  # Get all files from this folder
    texts = []
    for file in fileList:
        with open(sDir + file) as fileOpen:
            note = fileOpen.read()
            texts.append(note)
    return tuple(texts)


def isMatch(testString: str, searchTerms: str) -> bool:
    reg = (f'(?=.*\\b{re.escape(term)})' for term in searchTerms.lower().split(","))
    reg = ''.join(reg)
    return bool(re.search(reg, testString.lower()))


def flattenList(LIST: list) -> list[not list]:
    array = []
    for item in LIST:
        if isinstance(item, list):
            array.extend(item)
        else:
            array.append(item)
    return array

class USER:
    global complete
    consultant = "dr_santos mod_mr"
    initialize = 0
    x = """
        999 1
        """

def main():


    class link:
        Raw = r"D:\PROJECTS\RADIO EDITOR\belarmino\new\santos (105).txt"
        Jsn = r"D:\PROJECTS\RADIO EDITOR\normal.txt"
        Git = "https://raw.githubusercontent.com/mingresque/radiology/main/mr_knee"
        Dir = r"D:\PROJECTS\RADIO EDITOR\belarmino\new"

    global complete, y, consultant


    global z
    z = fileLoads(link.Raw, link.Jsn, link.Git)

    complete = True
    y = 150

    xy = extractColumn([0,1,2], z.fileGit_loadArray())
    for i, j, k in xy:
        print(i, re.sub(".*part_", "", j), "  ", stripWord(k[0]))
    #    if isMatch(yy[0], "degenera,chan"): print(yy)
    return 1
    for file in os.listdir(link.Dir):
        fileL = link.Dir + "\\" + file
        z = fileLoads(fileL, link.Jsn, link.Git)
        if USER.initialize == 1:
            initiializeNormal()
        else:
            print(file)
            if sortLines(USER.x) == False: break


if __name__ == '__main__': main()
