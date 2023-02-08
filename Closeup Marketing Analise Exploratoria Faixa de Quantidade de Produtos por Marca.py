# @title Setup
from google.colab import auth
from google.cloud import bigquery
from google.colab import data_table
from google.colab import files

project = 'myralisdev' # Project ID inserted based on the query results selected to explore
location = 'US' # Location inserted based on the query results selected to explore
client = bigquery.Client(project=project, location=location)
data_table.enable_dataframe_formatter()
auth.authenticate_user()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

job = client.get_job('bquxjob_7cf4247c_1862d62cbdd') # Job ID inserted based on the query results selected to explore
print(job.query)

job = client.get_job('bquxjob_7cf4247c_1862d62cbdd') # Job ID inserted based on the query results selected to explore
results = job.to_dataframe()

binsdata = results.copy()

binsdata.columns = ['marca','qtde_produtos']

binsdata.shape

min(binsdata['qtde_produtos']), max(binsdata['qtde_produtos'])

bins = 7 ###--- sempre escolher quantidade de bins que não deixem 0 na sequência

edges = np.linspace(min(binsdata['qtde_produtos']), max(binsdata['qtde_produtos']), bins+1).astype(int)

labels = [f'({edges[i]}, {edges[i+1]}]' for i in range(bins)]

binsdata['bins'] = pd.cut(binsdata['qtde_produtos'], bins=bins, labels=labels)

binsdata.sort_values(by='qtde_produtos', ascending = True, inplace = True)

df_bins = binsdata[['marca','bins']]

df_bins = df_bins.groupby(['bins']).aggregate({'marca':'count'})

df_bins.reset_index(drop = False, inplace = True)

df_bins.columns = ['qtde_produtos','qtde_marcas']



fig, ax = plt.subplots(figsize=(20, 5))

ax.plot(df_bins['qtde_marcas'], df_bins['qtde_produtos'])
ax.set_title('CloseUp Target - Faixas (frequências) das Quantidades de Produto por Marcas', fontsize = 20, color = 'blue')
plt.xticks(rotation = 90, fontsize = 10, ha='left') ## , color = 'white' 

plt.yticks(fontsize = 12) ## , color = 'white' 

plt.xlabel('Quantidades de Marcas')
plt.ylabel("Faixa de Quantidade de Produtos por Marca")

plt.margins(0.02)

fig.tight_layout() ###--- evita que o texto das labels dos ticks sejam comidos pela margem

plt.savefig('Closeup Marketing Faixa de Quantidade de Produtos por Marca.jpg', dpi = 300, format='jpg', transparent = False)

files.download('Closeup Marketing Faixa de Quantidade de Produtos por Marca.jpg') 

plt.show()