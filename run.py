"""Tester"""

import kaavyamanjari.kaavyamanjari as km


TEXT = 'champuuraamaayana.txt'

anuchchhedas = km.create_anuchchheda_list(TEXT)

with open('logger.txt', 'w', encoding='utf-8') as logger:
    # sys.stdout = logger
    for anuchchheda in anuchchhedas:
        print(anuchchheda)
