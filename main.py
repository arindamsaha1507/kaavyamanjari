import pandas as pd
import plotly.express as px
import pathanalekhana as pl
import kaavyakaarya as kk

import Levenshtein

pl.vivechanaa('gita_moola.txt')

df = pd.read_csv('gita_output.csv')
print(df.columns)
df = df[['श्लोक','पाद १','पाद २','पाद ३','पाद ४']]

droplist = []

for i in range(len(df)):
    if df.iloc[i,1][0] == '*' or df.iloc[i,2][0] == '*' or df.iloc[i,3][0] == '*' or df.iloc[i,4][0] == '*':
        droplist.append(i)

print(df)

counter = {}

for i in range(2**8):

    code = "{0:b}".format(i).zfill(8)

    code = code.replace('0', '।')
    code = code.replace('1', 'ऽ')

    code = kk.prastaara_to_ganavibhaaga(code)

    counter[code] = [0, 0, 0, 0]


for i in range(len(df)):

    for j in range(4):
        if df.iloc[i,j+1] in counter.keys():
            counter[df.iloc[i,j+1]][j] += 1

# print(counter)

dd = pd.DataFrame.from_dict(counter, orient='index', columns=['पाद १','पाद २','पाद ३','पाद ४'])

print(dd)

fig = px.bar(dd)
fig.show()

# print(dd.sort_values(by='पाद १'))
# print(dd.sort_values(by='पाद २'))
# print(dd.sort_values(by='पाद ३'))
# print(dd.sort_values(by='पाद ४'))

mat = [[0 for _ in range(2**8)] for _ in range(2**8)]

for i in range(2**8):
    
    x = "{0:b}".format(i).zfill(8)

    x = x.replace('0', '।')
    x = x.replace('1', 'ऽ')

    # x = kk.prastaara_to_ganavibhaaga(x)

    for j in range(2**8):

        y = "{0:b}".format(j).zfill(8)

        y = y.replace('0', '।')
        y = y.replace('1', 'ऽ')

        # y = kk.prastaara_to_ganavibhaaga(y)

        print(i, j, Levenshtein.distance(x,y))
        mat[i][j] = Levenshtein.distance(x,y)
        # print(mat[i][j])

print(mat)

fig = px.imshow(mat)
fig.show()

print(len(df[df['पाद १'] == df['पाद २']]))
print(len(df[df['पाद १'] == df['पाद ३']]))
print(len(df[df['पाद १'] == df['पाद ४']]))
print(len(df[df['पाद २'] == df['पाद ३']]))
print(len(df[df['पाद २'] == df['पाद ४']]))
print(len(df[df['पाद ३'] == df['पाद ४']]))