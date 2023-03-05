import sys
import varna as vn

def maarjaka(word):
    word = word.rstrip('\n')
    # word = word.replace(" ", "")

    return word    

def count_svaras(vinyaasa):

    return sum([1 for x in vinyaasa if x in vn.svara])

def break_paada(vinyaasa):

    i = 0

    while count_svaras(vinyaasa[0:i]) < count_svaras(vinyaasa)/2.0:
        i += 1

    if vinyaasa[i] in ['ः', 'ं'] or vinyaasa[i] not in [' ']:
        i += 1

    return [vinyaasa[0:i], vinyaasa[i:]]

def add_akaara(shabda, index, vinyaasa):

    if index+1 < len(shabda):
        if shabda[index+1] in vn.vyanjana_with_akaara or shabda[index+1] in vn.avasaana or shabda[index+1] in ['ः', 'ं']:
            vinyaasa.append('अ')
        if shabda[index+1] in ['ँ']:
            vinyaasa.append('अँ')
    else:
        vinyaasa.append('अ')

    return vinyaasa

def get_vinyaasa(shabda):

    shabda = maarjaka(shabda)
    vinyaasa = []

    for i in range(len(shabda)):
        x = shabda[i]
        if x in vn.svara:
            vinyaasa.append(x)
        elif x in vn.vyanjana_with_akaara:
            vinyaasa.append(x+'्')
            vinyaasa = add_akaara(shabda, i, vinyaasa)
        elif x in vn.maatraa:
            if i+1 < len(shabda):
                if shabda[i+1] in ['ँ']:
                    vinyaasa.append(vn.maatraa_to_svara[x]+'ँ')
                else:
                    vinyaasa.append(vn.maatraa_to_svara[x])
            else:
                vinyaasa.append(vn.maatraa_to_svara[x])
        elif x in ['्', 'ँ']:
            pass
        else:
            vinyaasa.append(x)
    
    return vinyaasa

def get_shabda(vinyaasa):

    shabda = ''

    for ii in range(len(vinyaasa)):

        varna = vinyaasa[ii]

        if ii == 0 and varna in vn.svara:
            jj = varna
        elif varna in vn.svara and (vinyaasa[ii-1] in vn.svara or vinyaasa[ii-1] == ' '):
            jj = varna
        elif varna in vn.vyanjana and ii+1 < len(vinyaasa):
            if vinyaasa[ii+1] in vn.svara or vinyaasa[ii+1] in vn.anunaasika_svara:
                jj = varna[0]
            else:
                jj = varna
        elif varna == 'अ':
            jj = ''
        elif varna in vn.svara:
            jj = vn.svara_to_maatraa[varna]
        elif varna in vn.anunaasika_svara:
            jj = vn.svara_to_maatraa[varna[0]] + 'ँ'
        else:
            jj = varna

        shabda = shabda+jj

    return shabda

def get_sankhyaa(s):

    r = ''
    s = str(s)

    for x in s:
        if x == '.':
            r += x
        elif int(x) < 0 or int(x) > 9:
            print("{} is Not a digit".format(x))
            sys.exit()
        else:
            r += vn.sankhyaa[int(x)]

    return r

def expand_pratyahaara(p):
    
    assert len(p)==3
    assert p[2]=='्'

    start = p[0]
    stop = p[1]+p[2]

    i = vn.maaheshwar_suutra.index(start)
    j = vn.maaheshwar_suutra.index(stop)

    r = vn.maaheshwar_suutra[i:j]

    it = [x for x in r if x in vn.vyanjana]
    for ii in it:
        r.remove(ii)

    rr = [x+'्' if x in vn.vyanjana_with_akaara else x for x in r]

    if 'अ' in rr:
        rr.append('आ')
    if 'इ' in rr:
        rr.append('ई')
    if 'उ' in rr:
        rr.append('ऊ')

    return rr