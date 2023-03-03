import sys
import varnakaarya as vk

from varna import *

laghu = '।'
guru = 'ऽ'


sys.stdout = open('logger.txt', 'w')

class Anuchchheda:

    def __init__(self, index, lines):
        self.id = index
        self.raw = lines

        assert isinstance(self.id, int)

class Padya(Anuchchheda):

    def __init__(self, index, lines):

        super().__init__(index, lines)

        self.prastaara = self.get_prastaara()

    def __repr__(self):

        return 'पद्य {}\n{}\n'.format(vk.get_sankhyaa(self.id), self.prastaara) + ''.join(self.raw)
    
    def get_prastaara(self):

        prastaara = []

        for verse in self.raw:

            verse = vk.get_vinyaasa(verse)

            for i in range(len(verse)):

                x = verse[i]

                if x not in svara:
                    continue

                if x not in ['अ', 'इ', 'उ']:
                    prastaara.append(guru)

                elif i + 1 < len(verse) and verse[i+1] in ['ं', 'ः']:
                    prastaara.append(guru)

                elif i + 2 < len(verse) and verse[i+1] in vyanjana and verse[i+2] in vyanjana:
                    prastaara.append(guru)

                else:
                    prastaara.append(laghu)

            prastaara.append('\n')

        prastaara = ''.join(prastaara)

        return prastaara

class Gadya(Anuchchheda):

    def __init__(self, index, lines):

        super().__init__(index, lines)

    def __repr__(self):

        return 'गद्य {}\n\n'.format(vk.get_sankhyaa(self.id)) + ''.join(self.raw)


def is_padya(lines):
    if len(lines) == 4:
        return True
    elif len(lines) == 1:
        return False
    else:
        print("Unknown type of kaavya")
        sys.exit()

def create_anuchchheda_list(fname):

    anuchchheda_list = []

    with open(fname, 'r') as f:
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

    anuchchheda_list = create_anuchchheda_list('champuuraamaayana.txt')

    for anuchchheda in anuchchheda_list:
        print(anuchchheda)