from varna import *

def maarjaka(word):
    word = word.rstrip('\n')
    # word = word.replace(" ", "")

    return word    

def count_svaras(vinyaasa):

    return sum([1 for x in vinyaasa if x in svara])

def break_paada(vinyaasa):

    i = 0

    while count_svaras(vinyaasa[0:i]) < count_svaras(vinyaasa)/2.0:
        i += 1

    return [vinyaasa[0:i], vinyaasa[i:]]

def add_akaara(shabda, index, vinyaasa):

    if index+1 < len(shabda):
        if shabda[index+1] in vyanjana_with_akaara or shabda[index+1] in avasaana or shabda[index+1] in ['ः', 'ं']:
            vinyaasa.append('अ')
        if shabda[index+1] in ['ँ']:
            vinyaasa.append('अँ')
    else:
        vinyaasa.append('अ')

    return vinyaasa

def get_vinyaasa(shabda):

    shabda = maarjaka(shabda)

    # print(shabda)

    vinyaasa = []

    for i in range(len(shabda)):
        x = shabda[i]
        if x in svara:
            vinyaasa.append(x)
        elif x in vyanjana_with_akaara:
            vinyaasa.append(x+'्')
            vinyaasa = add_akaara(shabda, i, vinyaasa)
        elif x in maatraa:
            if i+1 < len(shabda):
                if shabda[i+1] in ['ँ']:
                    vinyaasa.append(maatraa_to_svara[x]+'ँ')
                else:
                    vinyaasa.append(maatraa_to_svara[x])
            else:
                vinyaasa.append(maatraa_to_svara[x])
        elif x in ['्', 'ँ']:
            pass
        else:
            vinyaasa.append(x)
    
    return vinyaasa