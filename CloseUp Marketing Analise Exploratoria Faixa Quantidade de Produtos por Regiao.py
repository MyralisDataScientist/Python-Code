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

job = client.get_job('bquxjob_11cb001d_1862c3b33a2') # Job ID inserted based on the query results selected to explore
print(job.query)

# Running this code will read results from your previous job
job = client.get_job('bquxjob_11cb001d_1862c3b33a2') # Job ID inserted based on the query results selected to explore
results = job.to_dataframe()

results.head(10)

binsdata = results.copy()

binsdata.columns = ['regiao','qtde_produtos']

min(binsdata['qtde_produtos']), max(binsdata['qtde_produtos'])

bins = 10

edges = np.linspace(min(binsdata['qtde_produtos']), max(binsdata['qtde_produtos']), bins+1).astype(int)

labels = [f'({edges[i]}, {edges[i+1]}]' for i in range(bins)]

binsdata['bins'] = pd.cut(binsdata['qtde_produtos'], bins=bins, labels=labels)

binsdata.sort_values(by='qtde_produtos', ascending = True, inplace = True)

binsdata

df_bins = binsdata[['regiao','bins']]



fig, ax = plt.subplots(figsize=(40, 8))
ax.plot(df_bins['regiao'], df_bins['bins'])
ax.set_title('CloseUp Target - Faixas (frequências) das Quantidades Produtos por Região', fontsize = 20, color = 'blue')
plt.xticks(rotation = 90, fontsize = 10, ha='left') ## , color = 'white' 

plt.yticks(fontsize = 12) ## , color = 'white' 

plt.xlabel('Quantidades de Marcas')
plt.ylabel("Faixa de Quantidade de Produtos por Região")

plt.margins(0.02)

fig.tight_layout() ###--- evita que o texto das labels dos ticks sejam comidos pela margem

plt.savefig('Closeup Marketing Faixa de Quantidade de Produtos por Regiao.jpg', dpi = 300, format='jpg', transparent = False)

files.download('Closeup Marketing Faixa de Quantidade de Produtos por Regiao.jpg') 

plt.show()