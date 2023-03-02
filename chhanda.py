class Chhanda:

    def __init__(self, index, lines):

        self.id = index
        self.raw = lines

        assert len(self.raw) in [2, 4]
        assert isinstance(self.id, int)

    def __repr__(self):

        return 'Chhanda {}\n'.format(self.id) + ''.join(self.raw) + '\n'


def create_chhandas_list(fname):

    chhandas_list = []

    with open(fname, 'r') as f:
        data = f.readlines()

    start = 0
    index = 1
    for i in range(len(data)):
        if data[i] == '\n':
            stop = i
            chhandas_list.append(Chhanda(index=index, lines=data[start:stop]))
            start = stop + 1
            index += 1

    return chhandas_list

if __name__ == '__main__':

    chhandas_list = create_chhandas_list('gita_moola.txt')

    print(chhandas_list)