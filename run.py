"""Main module for analysis of a text"""

import os
import sys
import src.kaavyamanjari as km

TEXT_PATH = 'src/texts'

km.create_reference('sandarbha.yml', 'reference.csv')

with open('logger.txt', 'w', encoding='utf-8') as logger:

    for text in os.listdir(TEXT_PATH):

        if 'source_' not in text:

            print(f'Reading {text}')

            anuchchhedas = km.create_anuchchheda_list(text)

            sys.stdout = logger
            for anuchchheda in anuchchhedas:
                print(anuchchheda)
            sys.stdout = sys.__stdout__

            print(f'Read {len(anuchchhedas)} paragraphs')
