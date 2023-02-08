###--- google colab - CloseUp Marketing - Quantidade de Marcas por Laboratório - Somente para produtos prescritos

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from google.colab import auth
from google.cloud import bigquery
from google.colab import data_table
from google.colab import files

project = 'myralisdev' # Project ID inserted based on the query results selected to explore
location = 'US' # Location inserted based on the query results selected to explore
client = bigquery.Client(project=project, location=location)
data_table.enable_dataframe_formatter()
auth.authenticate_user()

###--- O código do getjob é da query executada no bigquery
job = client.get_job('bquxjob_1c5178fd_18622443bd0') # Job ID inserted based on the query results selected to explore
print(job.query) ###--- exibe o código sql da query

###--- Running this code will read results from your previous job
job = client.get_job('bquxjob_1c5178fd_18622443bd0') # Job ID inserted based on the query results selected to explore
results = job.to_dataframe() ###--- extrai os dados gerados pela query

###--- copia para outro dataframe os dados do dataframe results
binsdata = results.copy()

###--- renomeia as features
binsdata.columns = ['laboratorio','qtde_marcas']

###--- Qtde de bins
bins = 64

###--- gera os bins INTEIROS de acordo com a quantidade de intervalos (bins) escolhidos
edges = np.linspace(min(binsdata['qtde_marcas']), max(binsdata['qtde_marcas']), bins+1).astype(int)
labels = [f'({edges[i]}, {edges[i+1]}]' for i in range(bins)]
binsdata['bins'] = pd.cut(binsdata['qtde_marcas'], bins=bins, labels=labels)

###--- gera o gráfico das distribuições 
fig, ax = plt.subplots(figsize=(70, 7))
ax.plot(binsdata['laboratorio'], binsdata['bins'])
ax.set_title("CloseUp Target - Faixas (frequências) das Quantidades Marcas por Laboratório", fontsize = 20, color = 'blue')
plt.xticks(rotation = 90, fontsize = 10, ha='left') ## , color = 'white' 

plt.yticks(fontsize = 12) ## , color = 'white' 

plt.margins(0.02)

fig.tight_layout() ###--- evita que o texto das labels dos ticks sejam comidos pela margem

plt.savefig('CloseupMarketing Qtde Marcas Por Laboratorio.jpg', dpi = 300, format='jpg', transparent = False)

files.download('CloseupMarketing Qtde Marcas Por Laboratorio.jpg') 

plt.show()