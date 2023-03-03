import sys
import varnakaarya as vk

sys.stdout = open('logger.txt', 'w')

class Anuchchheda:

    def __init__(self, index, lines):
        self.id = index
        self.raw = lines

        assert isinstance(self.id, int)

class Padya(Anuchchheda):

    def __init__(self, index, lines):

        super().__init__(index, lines)

    def __repr__(self):

        return 'पद्य {}\n\n'.format(vk.get_sankhyaa(self.id)) + ''.join(self.raw)

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