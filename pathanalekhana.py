import varnakaarya as vk
import kaavyakaarya as kk

def vivechanaa(fname='pratidarsha.txt'):

    with open(fname) as f:
        raw = f.readlines()

    with open('gita_output.csv', 'w') as f:

        f.write('श्लोक,पाद १,पाद २,पाद ३,पाद ४,\n')

        shloka_counter = 1
        f.write('{},'.format(shloka_counter))

        for i in range(len(raw)):

            paada = raw[i]

            if len(paada) == 1:
                shloka_counter += 1
                f.write('\n{}'.format(shloka_counter))

            vinyaasa = vk.get_vinyaasa(paada)

            if vk.count_svaras(vinyaasa) == 16:

                bhaaga = vk.break_paada(vinyaasa)

                prastaara = kk.get_prastaara(bhaaga[0])
                ganavibhaaga = kk.prastaara_to_ganavibhaaga(prastaara)

                f.write("{},".format(ganavibhaaga))

                prastaara = kk.get_prastaara(bhaaga[1])
                ganavibhaaga = kk.prastaara_to_ganavibhaaga(prastaara)

                f.write("{},".format(ganavibhaaga))

            else:
                prastaara = kk.get_prastaara(vinyaasa)
                ganavibhaaga = kk.prastaara_to_ganavibhaaga(prastaara)

                if len(prastaara) not in [0, 11, 16]:
                    f.write("*{},".format(ganavibhaaga))
                else:
                    f.write("{},".format(ganavibhaaga))

        print(shloka_counter)