import sys
import Levenshtein
import pandas as pd
import yaml
import varnakaarya as vk
from varna import svara, vyanjana

sys.stdout = open('logger.txt', 'w', encoding='utf-8')

LAGHU = '।'
GURU = 'ऽ'

def prastaara_to_ganavibhaaga(prastaara):

    prastaara = list(prastaara)
    s = ''
    i = 0

    while i < len(prastaara):

        if i + 3 > len(prastaara):

            s += 'ल' if prastaara[i] == LAGHU else 'ग'
            i += 1

        else:

            test = prastaara[i]+prastaara[i+1]+prastaara[i+2]

            if test == LAGHU + GURU + GURU:
                cc = 'य'
            if test == GURU + LAGHU + GURU:
                cc = 'र'
            if test == GURU + GURU + LAGHU:
                cc = 'त'
            if test == GURU + LAGHU + LAGHU:
                cc = 'भ'
            if test == LAGHU + GURU + LAGHU:
                cc = 'ज'
            if test == LAGHU + LAGHU + GURU:
                cc = 'स'
            if test == GURU + GURU + GURU:
                cc = 'म'
            if test == LAGHU + LAGHU + LAGHU:
                cc = 'न'

            s += cc

            i += 3

    return s

def ganavibhaaga_to_prastaara(ganavibhaaga):

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

def create_reference(input_file, output_file):

    with open(input_file, 'r', encoding='utf-8') as f:
        ref = yaml.safe_load(f)

    jaati_list = [x.split(' ')[0] for x in list(ref['समवृत्त'].keys())]

    gana = list(list(x.values()) for x in ref['समवृत्त'].values())
    gana = list(x for v in gana for x in v)

    naama = list(list(x.keys()) for x in ref['समवृत्त'].values())
    naama = list(x for v in naama for x in v)

    assert len(naama) == len(gana)

    yati = []
    ganavibhaaga = []
    jaati = []

    for x in gana:
        if ' ' in x:
            ganavibhaaga.append(x.split(' ')[0])
            yati.append(x.split(' ')[1])
        else:
            ganavibhaaga.append(x)
            yati.append('-')

    prastaara = list(ganavibhaaga_to_prastaara(x) for x in ganavibhaaga)

    for x in prastaara:
        if len(x) <= len(jaati_list):
            jaati.append(jaati_list[len(x)-1])
        else:
            jaati.append(jaati_list[-1])

    dd = {}

    dd['naama'] = naama
    dd['jaati'] = jaati
    dd['ganavibhaaga'] = ganavibhaaga
    dd['prastaara'] = prastaara
    dd['yati'] = yati

    df = pd.DataFrame(dd)

    df.to_csv(output_file, index=False)



class Anuchchheda:

    def __init__(self, index, lines):
        self.id = index
        self.raw = lines

        assert isinstance(self.id, int)

class Padya(Anuchchheda):

    def __init__(self, index, lines, reference_file='reference.csv'):

        if len(lines) == 2:
            x = vk.get_vinyaasa(lines[0])
            y = vk.get_vinyaasa(lines[1])
            a, b = vk.break_paada(x)
            c, d = vk.break_paada(y)
            a = vk.get_shabda(a).strip() + '\n'
            b = vk.get_shabda(b).strip() + '\n'
            c = vk.get_shabda(c).strip() + '\n'
            d = vk.get_shabda(d).strip() + '\n'
            lines = [a, b, c, d]

        super().__init__(index, lines)

        self.paada = [x.rstrip('\n') for x in self.raw]
        self.prastaara = self.get_prastaara()
        self.reference = pd.read_csv(reference_file)

        self.vritta, self.error = self.match_vritta()

        if len(set(self.vritta)) == 1:
            self.vritta = self.vritta[0]
        else:
            self.vritta = ', '.join(self.vritta)

    def __repr__(self):

        if len(set(self.error)) == 1 and self.error[0] == '0':
            return 'पद्य {}\n{}\n{}\n\n'.format(vk.get_sankhyaa(self.id), self.vritta, self.prastaara) + ''.join(self.raw)
        else:
            return 'पद्य {}\n{} त्रुटि: {}\n{}\n\n'.format(vk.get_sankhyaa(self.id), self.vritta, '+'.join(self.error), self.prastaara) + ''.join(self.raw)

    
    def match_vritta(self):

        vritta = []
        difference = []

        pp = list(self.reference['prastaara'])
        
        for xx in self.prastaara:

            distances = list(Levenshtein.distance(xx, yy) for yy in pp)
            if 0 not in distances:
                xx_trial = xx[:-1] + GURU
                distances_trial = list(Levenshtein.distance(xx_trial, yy) for yy in pp)
                if 0 in distances_trial:
                    distances = distances_trial

            min_index = 0
            min_value = distances[0]

            for ii in range(len(distances)):

                if distances[ii] < min_value:
                    min_index = ii
                    min_value = distances[ii]

            vritta.append(list(self.reference['naama'])[min_index])
            difference.append(str(min_value))

        return vritta, difference

    
    def get_prastaara(self):

        prastaara = []

        for verse in self.raw:

            verse = vk.get_vinyaasa(verse)
            verse = list(filter(' '.__ne__, verse))

            for i in range(len(verse)):

                x = verse[i]

                if x not in svara:
                    continue

                if x not in ['अ', 'इ', 'उ', 'ऋ']:
                    prastaara.append(GURU)

                elif i + 1 < len(verse) and verse[i+1] in ['ं', 'ः']:
                    prastaara.append(GURU)

                elif i + 2 < len(verse) and verse[i+1] in vyanjana and verse[i+2] in vyanjana:
                    prastaara.append(GURU)

                else:
                    prastaara.append(LAGHU)

            prastaara.append('\n')

        prastaara = ''.join(prastaara)

        prastaara = prastaara.split('\n')[:-1]

        return prastaara

class Gadya(Anuchchheda):

    def __init__(self, index, lines):

        super().__init__(index, lines)

    def __repr__(self):

        return 'गद्य {}\n\n'.format(vk.get_sankhyaa(self.id)) + ''.join(self.raw)

def is_padya(lines):
    if len(lines) in [4, 2]:
        return True
    elif len(lines) == 1:
        return False
    else:
        print("Unknown type of kaavya")
        sys.exit()

def create_anuchchheda_list(fname):

    anuchchheda_list = []

    with open(fname, 'r', encoding='utf-8') as f:
        data = f.readlines()

    start = 0
    index = 1
    for i in range(len(data)):
        if data[i] == '\n':
            stop = i
            lines = data[start:stop]
            anuchchheda_list.append(Padya(index=index, lines=lines) if is_padya(lines) else Gadya(index=index, lines=lines))
            start = stop + 1
            index += 1

    return anuchchheda_list

if __name__ == '__main__':

    # create_reference('sandarbha.yml', 'reference.csv')

    # anuchchheda_list = create_anuchchheda_list('gita_moola.txt')
    anuchchhedas = create_anuchchheda_list('champuuraamaayana.txt')

    for anuchchheda in anuchchhedas:
        print(anuchchheda)