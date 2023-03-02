from varna import *

laghu = '।'
guru = 'ऽ'

def get_prastaara(verse):

    prastaara = []

    # print(verse)

    for i in range(len(verse)):

        x = verse[i]

        if x not in svara:
            # print(x)
            continue

        # print("Test", x)

        if x not in ['अ', 'इ', 'उ']:
            prastaara.append(guru)

        elif i + 1 < len(verse) and verse[i+1] in ['ं', 'ः']:
            prastaara.append(guru)

        elif i + 2 < len(verse) and verse[i+1] in vyanjana and verse[i+2] in vyanjana:
            prastaara.append(guru)

        else:
            prastaara.append(laghu)

    prastaara = ''.join(prastaara)

    return prastaara

def prastaara_to_ganavibhaaga(prastaara):

    prastaara = list(prastaara)
    s = ''
    i = 0

    while i < len(prastaara):

        if i + 3 > len(prastaara):

            s += 'ल' if prastaara[i] == laghu else 'ग'
            i += 1

        else:

            test = prastaara[i]+prastaara[i+1]+prastaara[i+2]

            if test == laghu + guru + guru:
                cc = 'य'
            if test == guru + laghu + guru:
                cc = 'र'
            if test == guru + guru + laghu:
                cc = 'त'
            if test == guru + laghu + laghu:
                cc = 'भ'
            if test == laghu + guru + laghu:
                cc = 'ज'
            if test == laghu + laghu + guru:
                cc = 'स'
            if test == guru + guru + guru:
                cc = 'म'
            if test == laghu + laghu + laghu:
                cc = 'न'

            s += cc

            i += 3

    return s

def ganavibhaaga_to_prastaara(ganavibhaaga):

    prastaara = ''

    for gana in ganavibhaaga:

        if gana == 'य':
            prastaara += laghu + guru + guru
        if gana == 'र':
            prastaara += guru + laghu + guru
        if gana == 'त':
            prastaara += guru + guru + laghu
        if gana == 'भ':
            prastaara += guru + laghu + laghu
        if gana == 'ज':
            prastaara += laghu + guru + laghu
        if gana == 'स':
            prastaara += laghu + laghu + guru
        if gana == 'म':
            prastaara += guru + guru + guru
        if gana == 'न':
            prastaara += laghu + laghu + laghu
        if gana == 'ग':
            prastaara += guru
        if gana == 'ल':
            prastaara += laghu

    return prastaara