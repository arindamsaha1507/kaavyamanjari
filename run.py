"""Main module for analysis of a text"""

import sys
import os
import kaavyamanjari.kaavyamanjari as km

km.create_reference('sandarbha.yml', 'reference.csv')

TEXT = 'niitishataka.txt'

anuchchhedas = km.create_anuchchheda_list(TEXT)

with open('logger.txt', 'w', encoding='utf-8') as logger:
    sys.stdout = logger
    for anuchchheda in anuchchhedas:
        print(anuchchheda)
