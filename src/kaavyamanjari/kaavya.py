"""Handles everything related to kaavya"""

import sys
import Levenshtein
import pandas as pd
import yaml
import varnakaarya as vk
from varna import svara, vyanjana

LAGHU = '।'
GURU = 'ऽ'


def prastaara_to_ganavibhaaga(prastaara: str) -> str:
    """Converts the prastaara of a kaavya to the ganavibhaaga

    Args:
        prastaara (str): prastaara

    Returns:
        str: ganavibhaaga
    """

    prastaara = list(prastaara)
    ganavibhaaga = ''
    i = 0

    while i < len(prastaara):

        if i + 3 > len(prastaara):

            ganavibhaaga += 'ल' if prastaara[i] == LAGHU else 'ग'
            i += 1

        else:

            test = prastaara[i]+prastaara[i+1]+prastaara[i+2]

            if test == LAGHU + GURU + GURU:
                gana = 'य'
            if test == GURU + LAGHU + GURU:
                gana = 'र'
            if test == GURU + GURU + LAGHU:
                gana = 'त'
            if test == GURU + LAGHU + LAGHU:
                gana = 'भ'
            if test == LAGHU + GURU + LAGHU:
                gana = 'ज'
            if test == LAGHU + LAGHU + GURU:
                gana = 'स'
            if test == GURU + GURU + GURU:
                gana = 'म'
            if test == LAGHU + LAGHU + LAGHU:
                gana = 'न'

            ganavibhaaga += gana

            i += 3

    return ganavibhaaga


def ganavibhaaga_to_prastaara(ganavibhaaga: str) -> str:
    """Converts the ganavibhaaga of a kaavya to the prastaara

    Args:
        ganavibhaaga (str): ganavibhaaga

    Returns:
        str: prastaara
    """

    prastaara = ''

    for gana in ganavibhaaga:

        if gana == 'य':
            prastaara += LAGHU + GURU + GURU
        if gana == 'र':
            prastaara += GURU + LAGHU + GURU
        if gana == 'त':
            prastaara += GURU + GURU + LAGHU
        if gana == 'भ':
            prastaara += GURU + LAGHU + LAGHU
        if gana == 'ज':
            prastaara += LAGHU + GURU + LAGHU
        if gana == 'स':
            prastaara += LAGHU + LAGHU + GURU
        if gana == 'म':
            prastaara += GURU + GURU + GURU
        if gana == 'न':
            prastaara += LAGHU + LAGHU + LAGHU
        if gana == 'ग':
            prastaara += GURU
        if gana == 'ल':
            prastaara += LAGHU

    return prastaara


def create_reference(input_file: str, output_file: str):
    """Creates reference for chhaanda types and their lakshana from yaml file and saves in csv file

    Args:
        input_file (str): input filename (.yml)
        output_file (str)): output filename (.csv)
    """

    with open(input_file, 'r', encoding='utf-8') as ref_file:
        ref = yaml.safe_load(ref_file)

    jaati_list = [x.split(' ')[0] for x in list(ref['समवृत्त'].keys())]

    gana = list(list(x.values()) for x in ref['समवृत्त'].values())
    gana = list(x for v in gana for x in v)

    naama = list(list(x.keys()) for x in ref['समवृत्त'].values())
    naama = list(x for v in naama for x in v)

    assert len(naama) == len(gana)

    yati = []
    ganavibhaaga = []
    jaati = []

    for element in gana:
        if ' ' in element:
            ganavibhaaga.append(element.split(' ')[0])
            yati.append(element.split(' ')[1])
        else:
            ganavibhaaga.append(element)
            yati.append('-')

    prastaara = list(ganavibhaaga_to_prastaara(x) for x in ganavibhaaga)

    for element in prastaara:
        if len(element) <= len(jaati_list):
            jaati.append(jaati_list[len(element)-1])
        else:
            jaati.append(jaati_list[-1])

    temp_dd = {}

    temp_dd['naama'] = naama
    temp_dd['jaati'] = jaati
    temp_dd['ganavibhaaga'] = ganavibhaaga
    temp_dd['prastaara'] = prastaara
    temp_dd['yati'] = yati

    temp_df = pd.DataFrame(temp_dd)

    temp_df.to_csv(output_file, index=False)


class Anuchchheda:
    """A class to represent an anuchchheda (paragraph) of the text
    """

    def __init__(self, index, lines, source):
        self.index = index
        self.raw = lines
        self.source = source

    def get_author(self):
        """Returns author of a text

        Returns:
            str: Author of the text
        """

        return self.source['author']

    def get_title(self):
        """Returns title of the text

        Returns:
            str: Title of the text
        """

        return self.source['title']


class Padya(Anuchchheda):
    """A class to represent a padya (verse) paragraph of the text
    """

    def __init__(self, index, lines, source, reference_file='reference.csv'):

        if len(lines) == 2:
            temp_x = vk.get_vinyaasa(lines[0])
            temp_y = vk.get_vinyaasa(lines[1])
            temp_a, temp_b = vk.break_paada(temp_x)
            temp_c, temp_d = vk.break_paada(temp_y)
            temp_a = vk.get_shabda(temp_a).strip() + '\n'
            temp_b = vk.get_shabda(temp_b).strip() + '\n'
            temp_c = vk.get_shabda(temp_c).strip() + '\n'
            temp_d = vk.get_shabda(temp_d).strip() + '\n'
            lines = [temp_a, temp_b, temp_c, temp_d]

        super().__init__(index, lines, source)

        self.paada = [x.rstrip('\n') for x in self.raw]
        self.prastaara = self.get_prastaara()
        self.reference = pd.read_csv(reference_file)

        self.vritta, self.error = self.match_vritta()

        if len(set(self.vritta)) == 1:
            self.vritta = self.vritta[0]
        else:
            self.vritta = ', '.join(self.vritta)

    def __repr__(self):

        raw = ''.join(self.raw)

        if len(set(self.error)) == 1 and str(self.error[0]) == '0':

            string = f'पद्य {vk.get_sankhyaa(self.index)}\n'
            string += f'{self.vritta}\n{self.prastaara}\n\n{raw}'

        else:
            error = [str(x) for x in self.error]
            error = '+'.join(error)
            string = f'पद्य {vk.get_sankhyaa(self.index)}\n'
            string += f'{self.vritta} त्रुटि: {error}\n{self.prastaara}\n\n{raw}'

        return string

    def match_vritta(self):
        """Matches the padya against the known vrittas

        Returns:
            list(str), list(int): Name of the closest vritta and error from ideal for each paada 
        """

        vritta = []
        difference = []

        list_prastaaras = list(self.reference['prastaara'])

        for paada_prastaara in self.prastaara:

            distances = list(Levenshtein.distance(paada_prastaara, yy)
                             for yy in list_prastaaras)
            if 0 not in distances:
                paada_prastaara_trial = paada_prastaara[:-1] + GURU

                distances_trial = list(Levenshtein.distance(
                    paada_prastaara_trial, yy) for yy in list_prastaaras)

                if 0 in distances_trial:
                    distances = distances_trial

            min_index = 0
            min_value = distances[0]

            for index, distance in enumerate(distances):

                if distance < min_value:
                    min_index = index
                    min_value = distance

            vritta.append(list(self.reference['naama'])[min_index])
            difference.append(min_value)

        return vritta, difference

    def get_prastaara(self):
        """Gives the prastaara of the padya

        Returns:
            list(string): Prastaara of each paada
        """

        prastaara = []

        for verse in self.raw:

            verse = vk.get_vinyaasa(verse)
            verse = list(filter(' '.__ne__, verse))

            for index, varna in enumerate(verse):

                if varna not in svara:
                    continue

                if varna not in ['अ', 'इ', 'उ', 'ऋ']:
                    prastaara.append(GURU)

                elif index + 1 < len(verse) and verse[index + 1] in ['ं', 'ः']:
                    prastaara.append(GURU)

                elif (index + 2 < len(verse) and
                      verse[index + 1] in vyanjana and
                      verse[index + 2] in vyanjana):
                    prastaara.append(GURU)

                else:
                    prastaara.append(LAGHU)

            prastaara.append('\n')

        prastaara = ''.join(prastaara)

        prastaara = prastaara.split('\n')[:-1]

        return prastaara


class Gadya(Anuchchheda):
    """A class to represent a padya (verse) paragraph of the text
    """

    def __repr__(self):

        raw = ''.join(self.raw)
        return f'गद्य {vk.get_sankhyaa(self.index)}\n\n{raw}'


def is_padya(lines: list) -> bool:
    """Checks if an anuchchheda is padya or gadya

    Args:
        lines (list): Lines in the anuchchheda

    Returns:
        bool: True if padya and False if gadya
    """

    if len(lines) in [4, 2]:
        return True
    if len(lines) == 1:
        return False
    print("Unknown type of kaavya")
    sys.exit()

def get_source(fname: str) -> dict:
    """Extracts source intormatiion about the text (title, author , etc.)

    Args:
        fname (str): Filename of the text

    Returns:
        dict: Source information
    """

    sourcefile = 'source_' + fname.split('.', maxsplit=1)[0] + '.yml'

    with open(sourcefile, 'r', encoding='utf-8') as file:
        source_dict = yaml.safe_load(file)

    return source_dict


def create_anuchchheda_list(fname: str) -> list:
    """Parses the text file into anuchchhedas of gadya and padya

    Args:
        fname (str): Input text filename

    Returns:
        list: List of gadya and padya anuchchhedas in the text
    """

    anuchchheda_list = []

    with open(fname, 'r', encoding='utf-8') as text_file:
        data = text_file.readlines()

    sources = get_source(fname)

    start = 0
    index = 1
    for i, line in enumerate(data):
        if line == '\n':
            stop = i
            lines = data[start:stop]
            anuchchheda_list.append(Padya(index=index, lines=lines, source=sources) if is_padya(
                lines) else Gadya(index=index, lines=lines, source=sources))
            start = stop + 1
            index += 1

    return anuchchheda_list


if __name__ == '__main__':

    TEXT = 'champuuraamaayana.txt'

    anuchchhedas = create_anuchchheda_list(TEXT)

    with open('logger.txt', 'w', encoding='utf-8') as logger:
        sys.stdout = logger
        for anuchchheda in anuchchhedas:
            print(anuchchheda)
