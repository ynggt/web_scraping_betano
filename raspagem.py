import re
from collections import defaultdict
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
import numpy as np
add_printer(1)

def obter_dataframe(query='*'):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=True,
        )
    return df
driver = Driver(uc=True)
driver.get("https://br.betano.com/sport/futebol/brasil/brasileirao-serie-a/10016/")

df=obter_dataframe(query='section')
texto=df.loc[df.aa_className.str.contains('grid__column',regex=False,na=False)].aa_innerText.iloc[0]

df=pd.DataFrame(texto.splitlines())
df=df.loc[df.loc[df.loc[0].str.contains(r'Brasileirão\s+-\s+Série\s+A',regex=True, na=False)].index[-1]+1:].reset_index(drop=True)

df[0]=df[0].str.strip()
allbets=np.array_split(df, df.loc[df[0].str.contains(r"^\d+\d+/\d+\d+$")].index)

d=defaultdict(list)
for bet in allbets:
    d[len(bet)].append(bet)

df=pd.concat([q.reset_index(drop=True) for q in d[sorted(d)[-1]]],axis=1, ignore_index=True)


df=df.loc[np.setdiff1d(df.index,df.applymap(lambda x:re.match('resultado',x,flags=re.I)).dropna(how='all').index)].reset_index(drop=True)
df=df.T
df = df.drop(df.columns[[4, 5]], axis=1)
df.columns = ['data', 'hora', 'time1', 'time2', 'vitoria_time1', 'empate', 'vitoria_time2']
df=df.astype({'vitoria_time1':'Float64', 'empate':'Float64', 'vitoria_time2':'Float64'})
soma = (1/df[['vitoria_time1', 'empate', 'vitoria_time2']]).sum(axis=1)
valor = (soma-1)*100
print(round(valor,4))