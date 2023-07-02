#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Organizing the data for the file 'bancoesusalltabsrais2019morelatlongcepestab.csv'
#based on what I did on 'bancoesusalltabs_04012020to08052021rais2019.ipynb', but now it's with the data that has lat and long


# In[2]:


#to see how lats and long were found see 'CEPbancoesusalltabsmarch2020tomay2021.ipynb'


# # Organizing the data

# In[3]:


import pandas as pd
import plotly.express as px
import numpy as np


# In[4]:


bancoesusalltabsrais2019morelatlongcepestab = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestab.csv')


# In[5]:


bancoesusalltabsrais2019morelatlongcepestab.shape


# In[6]:


bancoesusalltabsrais2019morelatlongcepestab.dropna().shape


# In[7]:


bancoesusalltabsrais2019morelatlongcepestab.head(3)


# In[8]:


bancoesusalltabsrais2019morelatlongcepestab.drop(['_merge','cepsindex','_merge2'],axis=1,inplace=True)


# In[9]:


bancoesusalltabsrais2019morelatlongcepestab.head(3)


# In[10]:


pd.set_option('display.max_columns',None)


# In[11]:


bancoesusalltabsrais2019morelatlongcepestab.head(3)


# In[12]:


bancoesusalltabsrais2019morelatlongcepestab.info()


# In[13]:


bancoesusalltabsrais2019morelatlongcepestab.memory_usage()


# In[14]:


pd.set_option('display.max_rows',None)


# In[15]:


bancoesusalltabsrais2019morelatlongcepestab.memory_usage()


# In[16]:


bancoesusalltabsrais2019morelatlongcepestab.dtypes


# In[17]:


bancoesusalltabsrais2019morelatlongcepestab['latitude'].dtype


# In[18]:


bancoesusalltabsrais2019morelatlongcepestab.isna().sum().sort_values(ascending=False)


# In[19]:


import missingno as msno


# In[20]:


msno.bar(bancoesusalltabsrais2019morelatlongcepestab);


# In[21]:


list(bancoesusalltabsrais2019morelatlongcepestab.isnull().sum().sort_values(ascending=False).index)


# In[22]:


#dropping columns with more than 100k missing values, except 'condicoes' that are the comorbities that might be related to death


# In[23]:


bancoesusalltabsrais2019morelatlongcepestab.drop(columns=['DATA DE SAÍDA DA HOSPITALIZAÇÃO',
 'TRIMESTRE',
 'DATA DA HOSPITALIZAÇÃO',
 'estrangeiro',
 'OUTRA, QUAL (PROF. SAÚDE)?',
 'OUTRA, QUAL (PROF. SEG)?',
 'OUTRA, QUAL (OCUPAÇÃO)?',
 'LOCAL DA HOSPITALIZAÇÃO',
 'CATEGORIA DA OCUPAÇÃO',
 'CATEGORIA PROF. DE SEG.',
 'CATEGORIA DO PROF. DE SAÚDE',
 'ESFERA DE GESTÃO',
 'etnia',
 'SETOR DO ÓBITO',
 'DATA DA CONFIRMAÇÃO DO ÓBITO',
 'QUAL UNIDADE?',
 'DATA DO ÓBITO',
 'LOCAL DO ÓBITO',
 'OUTRAS MORBIDADES PRÉVIAS (QUAIS)?',
 'resultadoTesteSorologicoTotais',
 'OUTRO LOCAL DE INTERNAMENTO (NA NOTIFICAÇÃO)',
 'OUTRA UNIDADE NOTIFICADORA',
 'GESTANTE',
 'CONTATO PRÓXIMO DE PROF. DE SAÚDE OU DE SEG. PÚBLICA?',
 'OUTRA OCUPAÇÃO',
 'É SERVIÇO PÚBLICO?',
 'DATA DE CONFIRMAÇÂO',
 'ATUALIZAÇÃO (CLASSIF.)',
 'EXAME',
 'UNIDADE COLETORA',
 'TIPO DE MATERIAL COLETADO',
 'LABORATÓRIO',
 'TIPO DE LABORATÓRIO',
 'DATA DO RESULTADO',
 'DATA DE RECEBIMENTO DA AMOSTRA',
 'RESULTADO DO TESTE',
 'STATUS NO GAL',
 'ATUALIZAÇÂO (EVOLUÇÂO)',
 'LOCAL DE INTERNAMENTO (NA NOTIFICAÇÃO)',
 'IDENTIDADE DE GÊNERO',
 'ORIENTAÇÃO SEXUAL',
 'ENDEREÇO COMPLETO',
 'TIPO DA NOTIFICAÇÃO',
 'COLETA DE EXAMES',
 'UNIDADE NOTIFICADORA',
 'INTERNADO',
 'ID',
 'paisOrigem',
 'resultadoTesteSorologicoIgM',
 'resultadoTesteSorologicoIgG',
 'dataTesteSorologico',
 'tipoTesteSorologico',
 'testeSorologico',
 'notificadorCNPJ',
 'telefone',
 'cbo',
 'complemento',
 'cns',
 'nomeMae',
 'outrosSintomas',
 'cnes'], axis = 1, inplace=True)


# In[24]:


list(bancoesusalltabsrais2019morelatlongcepestab.columns)


# In[25]:


bancoesusalltabsrais2019morelatlongcepestab.shape


# In[26]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestab[['condicoes','estado', 'evolucaoCaso', 'dataInicioSintomas', 'cpf', 
                          'nomeCompletoDesnormalizado','dataNascimento','resultadoTeste', 'bairro', 
                          'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao', 'sintomas', 'cep', 'idade', 'racaCor',
                         'profissionalSeguranca','tipoTeste','sexo', 'Resultado Final','Tipo Vínculo','Escolaridade após 2005','Vl Remun Média Nom','Vl Remun Média (SM)',
                          'Tempo Emprego' ,'Qtd Hora Contr','CBO Ocupação 2002','CNAE 2.0 Classe','CNAE 2.0 Subclasse','Qtd Dias Afastamento',
                          'IBGE Subsetor','CEP Estab','Mun Trab','latitude','longitude','latitudestab','longitudestab']]


# In[27]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[28]:


bancoesusalltabsrais2019morelatlongcepestabselected.dropna().shape


# In[29]:


pd.set_option('display.max_rows',10)


# In[30]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[31]:


bancoesusalltabsrais2019morelatlongcepestabselected.describe()


# In[32]:


pd.Timestamp.min


# In[33]:


pd.Timestamp.max


# In[34]:


bancoesusalltabsrais2019morelatlongcepestabselected['dataNascimento'] = pd.to_datetime(bancoesusalltabsrais2019morelatlongcepestabselected['dataNascimento'], errors = 'coerce') #This will force the dates which are outside the bounds to NaT


# In[35]:


bancoesusalltabsrais2019morelatlongcepestabselected['dataNascimento'].isna().sum()


# In[36]:


bancoesusalltabsrais2019morelatlongcepestabselected['cep']


# In[37]:


bancoesusalltabsrais2019morelatlongcepestabselected['cep'].astype(str).replace('\.0','',regex=True)


# In[38]:


bancoesusalltabsrais2019morelatlongcepestabselected['cep']=bancoesusalltabsrais2019morelatlongcepestabselected['cep'].astype(str).replace('\.0','',regex=True)


# In[39]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[40]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes'].unique()


# In[41]:


#pip install kaleido


# to show plotly graphs on github and when opening again the ipynb (it does not load unless the code is run again) 
# [here](https://github.com/plotly/plotly.py/issues/931)
# fig.show(png) or fig.show(svg)
# use svg instead of png, it takes much less memory, [here](https://vecta.io/blog/comparing-svg-and-png-file-sizes)

# In[42]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='condicoes')
fig.show('svg')


# In[43]:


#deal with 'condicoes' column later


# In[44]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='estado')
fig.show('svg')


# In[45]:


bancoesusalltabsrais2019morelatlongcepestabselected['estado'] = bancoesusalltabsrais2019morelatlongcepestabselected['estado'].str.upper()


# In[46]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='estado')
fig.show('svg')


# In[47]:


bancoesusalltabsrais2019morelatlongcepestabselected['evolucaoCaso']


# In[48]:


bancoesusalltabsrais2019morelatlongcepestabselected['evolucaoCaso'].unique()


# In[49]:


bancoesusalltabsrais2019morelatlongcepestabselected.rename({'evolucaoCaso':'disease evolution'}, axis = 1, inplace =True)


# In[50]:


bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'] = bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].replace(
{'Cura':'healed',
'Em tratamento domiciliar': 'in home treatment', 
'RECUPERADO':'recovered',
'INTERNADO LEITO DE ISOLAMENTO':'hospitalized isolation bed',
'ÓBITO':'death',
'ISOLAMENTO DOMICILIAR':'home isolation',
'INTERNADO UTI':'hospitalized ICU'})


# In[51]:


bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].unique()


# In[52]:


bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].dropna().unique()


# In[53]:


bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].value_counts(normalize=True)


# In[54]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='disease evolution')
fig.update_layout(
    title={
        'text':'Disease Evolution',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[55]:


#if dropping nan from the whole data to do the graph, more observations will be lost
#to do the graph, there's only the need to dropna() on the column that you're doing the histogram graph
#although dropping na only from the specific column to do the graph instead of dropping na from all the data
#the graphs will have different counts and different frequency, so each column graph will be disproportional
#because some columns will have more na and other columns will have less na's


# In[56]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[57]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='resultadoTeste')
fig.show('svg')


# In[58]:


bancoesusalltabsrais2019morelatlongcepestabselected['resultadoTeste'].unique()


# In[59]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[60]:


bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['resultadoTeste']!='Inconclusivo ou Indeterminado')].shape


# In[61]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['resultadoTeste']!='Inconclusivo ou Indeterminado')] 


# In[62]:


bancoesusalltabsrais2019morelatlongcepestabselected['resultadoTeste'].unique()


# In[63]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='resultadoTeste')
fig.show('svg')


# In[64]:


#it's better to work with 'Resultado Final', Final result


# In[65]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[66]:


bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude'].unique()


# In[67]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='profissionalSaude')
fig.show('svg')


# In[68]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[69]:


bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude']=='Sim') | (bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude']=='Não')].shape


# In[70]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude']=='Sim') | (bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude']=='Não')]


# In[71]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='profissionalSaude')
fig.show('svg')


# In[72]:


bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude'].unique()


# In[73]:


bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSaude']
bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'].str.replace('Sim', '1')
bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'].str.replace('Não', '0')
bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'].astype(int)


# In[74]:


bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'].unique()


# In[75]:


bancoesusalltabsrais2019morelatlongcepestabselected['Health Professionals'].mean()


# In[76]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='Health Professionals')
fig.update_layout(
    title={
        'text':'Health Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[77]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].unique()


# In[78]:


#deal with 'sintomas' column later


# In[79]:


bancoesusalltabsrais2019morelatlongcepestabselected['idade'].unique()


# In[80]:


bancoesusalltabsrais2019morelatlongcepestabselected['idade']


# In[81]:


#bancoesusalltabsrais2019morelatlongcepestabselected['idade'] = bancoesusalltabsrais2019morelatlongcepestabselected['idade'].astype(str).replace('\.0','',regex=True)
#bancoesusalltabsrais2019morelatlongcepestabselected['idade']


# In[82]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='idade')
fig.show('svg')


# In[83]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['idade'].sort_values(ascending=False))


# In[84]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[85]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['idade']<=112].shape


# In[86]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['idade']<=112]


# In[87]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['idade'].sort_values(ascending=False))


# In[88]:


bancoesusalltabsrais2019morelatlongcepestabselected['idade'].astype(str).str.rstrip('.0').unique()


# In[89]:


bancoesusalltabsrais2019morelatlongcepestabselected['idade'].unique()


# [age groups](https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html) division cdc usa

# In[90]:


'''
0-4 years old
5-17 years old
18-29 years old
30-39 years old
40-49 years old
50-64 years old
65-74 years old
75-84 years old
85+ years old
'''


# In[91]:


bins = [0, 5, 18, 30, 40, 50, 65, 75, 85, np.inf]
names = ['0 - 4','5 - 17', '18 - 29', '30 - 39','40 - 49','50 - 64','65 - 74','75 - 84', '85+']

bancoesusalltabsrais2019morelatlongcepestabselected['agecohort'] = pd.cut(bancoesusalltabsrais2019morelatlongcepestabselected['idade'], bins, labels=names)

print(bancoesusalltabsrais2019morelatlongcepestabselected.dtypes)


# In[92]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[93]:


fig= px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='agecohort')
fig.show('svg')


# In[94]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected['agecohort'].dropna(), x='agecohort',color='agecohort',
                   title='Agecohort',
                   labels={'agecohort':'Agecohort', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Agecohort',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Agecohort')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[95]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[96]:


bancoesusalltabsrais2019morelatlongcepestabselected['racaCor'].unique()


# In[97]:


bancoesusalltabsrais2019morelatlongcepestabselected['racaCor'] = bancoesusalltabsrais2019morelatlongcepestabselected['racaCor'].str.replace('Indígena', 'Indigena')
bancoesusalltabsrais2019morelatlongcepestabselected['racaCor'].unique()


# In[98]:


bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['racaCor']
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Parda', 'Brown')
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Branca', 'White')
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Amarela', 'Yellow')
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Preta', 'Black')
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Indigena', 'Indigenous')
bancoesusalltabsrais2019morelatlongcepestabselected['race'] = bancoesusalltabsrais2019morelatlongcepestabselected['race'].str.replace('Ignorado', 'Ignored')


# In[99]:


bancoesusalltabsrais2019morelatlongcepestabselected['race'].unique()


# In[100]:


bancoesusalltabsrais2019morelatlongcepestabselected['racaCor'].unique()


# In[101]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[102]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected['race'].dropna(), x='race',color='race',
                   title='Race',
                   labels={'race':'Race', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Race',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Race')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[103]:


bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSeguranca'].unique()


# In[104]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='profissionalSeguranca')
fig.show('svg')


# In[105]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[106]:


bancoesusalltabsrais2019morelatlongcepestabselected.dropna(subset=['profissionalSeguranca']).shape


# In[107]:


#bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSeguranca']=='Sim') | (bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSeguranca']=='Não')] 


# In[108]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape 
#either way results in the same amount of rows
#besides, I have to think better if it's worth it to make the 'security professionals' column, losing 8k rows 

#not worth it


# In[109]:


bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['profissionalSeguranca']
bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'].str.replace('Sim', '1')
bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'].str.replace('Não', '0')
#bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'] = bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'].astype(int)
bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'].unique()


# In[110]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected['Security Professionals'].dropna(), names='Security Professionals')
fig.update_layout(
    title={
        'text':'Security Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[111]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[112]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[113]:


bancoesusalltabsrais2019morelatlongcepestabselected['tipoTeste'].unique()


# [Antígeno e Anticorpo Covid](https://www.fleury.com.br/medico/artigos-cientificos/conheca-as-diferencas-entre-os-testes-diagnosticos-para-covid-19)

# In[114]:


#bancoesusalltabsrais2019morelatlongcepestabselected['test type'] = bancoesusalltabsrais2019morelatlongcepestabselected.loc[:,['tipoTeste']]


# In[115]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[116]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[117]:


#bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[(bancoesusalltabsrais2019morelatlongcepestabselected['test type']=='RT-PCR') | (bancoesusalltabsrais2019morelatlongcepestabselected['test type'] =='TESTE RÁPIDO - ANTICORPO') | (bancoesusalltabsrais2019morelatlongcepestabselected['test type'] =='TESTE RÁPIDO - ANTÍGENO')] 


# In[118]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape 
#losing 17K rows, have to think it it's worth it
#not worth it


# In[119]:


#bancoesusalltabsrais2019morelatlongcepestabselected['test type'].replace({'TESTE RÁPIDO - ANTICORPO':'rapid antibody test', 'TESTE RÁPIDO - ANTÍGENO':'rapid antigen test'}, inplace = True)


# In[120]:


#bancoesusalltabsrais2019morelatlongcepestabselected['test type'].unique()


# In[121]:


'''
fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected['test type'].dropna(), x='test type',color='test type',
                   title='Test Type',
                   labels={'test type':'Test Type', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')
'''


# In[122]:


bancoesusalltabsrais2019morelatlongcepestabselected['tipoTeste'].str.split(', ').explode().value_counts()


# In[123]:


#bancoesusalltabsrais2019morelatlongcepestabselected['test type'].str.split(', ').explode().value_counts().head(10)


# In[124]:


data = [['RCT-PCR', 124702],['rapid antibody test', 75974], ['rapid antigen test', 29689]]
df = pd.DataFrame(data, columns = ['test type', 'count'])
df


# In[125]:


fig = px.bar(df, x='test type',y='count', color='test type')
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Frequency',range=[0, 125000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[126]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[127]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[128]:


bancoesusalltabsrais2019morelatlongcepestabselected['sexo'].unique()


# In[129]:


bancoesusalltabsrais2019morelatlongcepestabselected['sexo'].value_counts(normalize=True)


# In[130]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['sexo']!='Indefinido'].shape


# In[131]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['sexo']!='Indefinido']


# In[132]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[133]:


bancoesusalltabsrais2019morelatlongcepestabselected['sexo'].astype(str).replace({'Masculino':'1','Feminino':'0'})


# In[134]:


bancoesusalltabsrais2019morelatlongcepestabselected['sex'] =  bancoesusalltabsrais2019morelatlongcepestabselected['sexo'].astype(str).replace({'Masculino':'1','Feminino':'0'})


# In[135]:


bancoesusalltabsrais2019morelatlongcepestabselected['sex'] = bancoesusalltabsrais2019morelatlongcepestabselected['sex'].astype('int8')


# In[136]:


bancoesusalltabsrais2019morelatlongcepestabselected['sex'].dtype


# In[137]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='sex',color_discrete_sequence=['red','blue'])
fig.update_layout(
    title={
        'text':'Sex',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[138]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[139]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[140]:


bancoesusalltabsrais2019morelatlongcepestabselected['Resultado Final'].unique()


# In[141]:


bancoesusalltabsrais2019morelatlongcepestabselected['Resultado Final'].value_counts(normalize=True)


# In[142]:


bancoesusalltabsrais2019morelatlongcepestabselected['Resultado Final'].value_counts()


# In[143]:


bancoesusalltabsrais2019morelatlongcepestabselected['Resultado Final'].isna().sum()


# In[144]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='Resultado Final')
fig.show('svg')


# In[145]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[146]:


bancoesusalltabsrais2019morelatlongcepestabselected.dropna(subset=['Resultado Final']).shape


# In[147]:


#loses almost 3k obs if dropping na, not going to drop it for now


# In[148]:


#bancoesusalltabsrais2019morelatlongcepestabselected.dropna(subset=['Resultado Final'], inplace = True)


# In[149]:


#bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[150]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'] = bancoesusalltabsrais2019morelatlongcepestabselected.loc[:,'Resultado Final']


# In[151]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'].astype(str).replace({'Positivo':'1', 'Negativo':'0'})


# In[152]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'] = bancoesusalltabsrais2019morelatlongcepestabselected['final result'].astype(str).replace({'Positivo':'positive', 'Negativo':'negative'})


# In[153]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'].unique()


# In[154]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['final result'] != 'Inconclusivo ou indeterminado'].shape


# In[155]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['final result'] != 'Inconclusivo ou indeterminado']


# In[156]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[157]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'].unique()


# In[158]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'].dropna().shape


# In[159]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['final result'] !='nan'].shape


# In[160]:


#bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['final result'] !='nan']

#can't drop the nans here, because it will make 'disease evolution' death, and more disappear

#bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].unique()


# In[161]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected['final result'], names='final result')
fig.update_layout(
        title={
        'text':'Final Result',
        'y':0.95,
        'x':0.45,
        'xanchor':'center',
        'yanchor':'top'})
fig.show('svg')


# For more details with colors in [Plotly](https://plotly.com/python/discrete-color/) and [here](https://plotly.com/python/pie-charts/)

# In[162]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='final result',color_discrete_sequence=['red', 'royalblue', 'lightgreen'])
fig.update_layout(
        title={
        'text':'Final Result',
        'y':0.95,
        'x':0.48,
        'xanchor':'center',
        'yanchor':'top'},
        )
fig.show('svg')


# In[163]:


bancoesusalltabsrais2019morelatlongcepestabselected[['final result']]


# In[164]:


pd.set_option('display.max_rows',None)


# In[165]:


bancoesusalltabsrais2019morelatlongcepestabselected[['final result']]


# In[166]:


bancoesusalltabsrais2019morelatlongcepestabselected['final result'].astype(str).replace({'Null':''})


# In[167]:


#bancoesusalltabsrais2019morelatlongcepestabselected['final result'] = bancoesusalltabsrais2019morelatlongcepestabselected['final result'].astype(str).replace({'Null':''})


# In[168]:


#bancoesusalltabsrais2019morelatlongcepestabselected['final result'].astype('int8')


# In[169]:


#still won't be able to turn the column into int because of the empty cells


# In[170]:


pd.set_option('display.max_rows',10)


# In[171]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[172]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[173]:


bancoesusalltabsrais2019morelatlongcepestabselected['Escolaridade após 2005']


# In[174]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected,names='Escolaridade após 2005')
fig.show('svg')


# In[175]:


'''
ANALFABETO 1
ATE 5.A INC 2
5.A CO FUND 3
6. A 9. FUND 4
FUND COMPL 5
MEDIO INCOMP 6
MEDIO COMPL 7
SUP. INCOMP 8
SUP. COMP 9
MESTRADO 10
DOUTORADO 11
'''
'''
Incomplete primary education 1,2,3,4
Complete primary education 5,6
Complete secondary education 7,8
Complete higher education 9,10,11
'''


# In[176]:


bins = [1, 5, 7, 9, np.inf]
names = ['1-4','5-6','7-8','9-11']

bancoesusalltabsrais2019morelatlongcepestabselected['schooling'] = pd.cut(bancoesusalltabsrais2019morelatlongcepestabselected['Escolaridade após 2005'], bins, labels=names)

print(bancoesusalltabsrais2019morelatlongcepestabselected.dtypes)


# In[177]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[178]:


bancoesusalltabsrais2019morelatlongcepestabselected['schooling'] = bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].str.replace('1-4','Incomplete primary education')
bancoesusalltabsrais2019morelatlongcepestabselected['schooling'] = bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].str.replace('5-6','Complete primary education')
bancoesusalltabsrais2019morelatlongcepestabselected['schooling'] = bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].str.replace('7-8','Complete secondary education')
bancoesusalltabsrais2019morelatlongcepestabselected['schooling'] = bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].str.replace('9-11','Complete higher education')


# In[179]:


bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].isnull().sum()


# In[180]:


bancoesusalltabsrais2019morelatlongcepestabselected['schooling'].isna().sum()


# In[181]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[182]:


bancoesusalltabsrais2019morelatlongcepestabselected.dropna(subset=['schooling']).shape


# In[183]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected.dropna(subset=['schooling'])


# In[184]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected,x='schooling',color='schooling')
fig.update_layout(
        title = {
        'text':'Schooling',
        'y':0.95,
        'x':0.4,
        'xanchor':'center',
        'yanchor':'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.show('svg')


# In[185]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[186]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[187]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média Nom'].unique()


# In[188]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].unique()


# In[189]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].min()


# In[190]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].sort_values


# In[191]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'] = bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].str.lstrip('0')


# In[192]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].head(10)


# In[193]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].sort_values(ascending=False).head(10)


# In[194]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'] = bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].str.replace(',','.')


# In[195]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'] = bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].astype(float)


# In[196]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].head(10)


# In[197]:


bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'].isna().sum()


# [numeric data into bins](https://stackoverflow.com/questions/49382207/how-to-map-numeric-data-into-categories-bins-in-pandas-dataframe)

# In[198]:


'''sem rendimento (0)
até 1/2 salário mínimo
mais de 1/2 a 1 salário mínimo 
mais de 1 a 2 salários mínimos 
mais de 2 a 5 salários mínimos 
mais de 5 a 10 salários mínimos 
mais de 10 a 20 salários mínimos
mais de 20 salários mínimos
'''


# In[199]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.1 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

bancoesusalltabsrais2019morelatlongcepestabselected['meanminimumwage'] = pd.cut(bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'], bins, labels=names)

print(bancoesusalltabsrais2019morelatlongcepestabselected.dtypes)


# In[200]:


bancoesusalltabsrais2019morelatlongcepestabselected['meanminimumwage']


# In[201]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[202]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[203]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected['meanminimumwage'].dropna(), x='meanminimumwage',color='meanminimumwage',
                   title='Minimum Wage',
                   labels={'meanminimumwagerange':'Minimum Wage', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Minimum Wage',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[204]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[205]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002']


# In[206]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].unique()


# In[207]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].nunique()


# [IBGE CONCLA CBO](https://concla.ibge.gov.br/classificacoes/por-tema/ocupacao/classificacao-brasileira-de-ocupacoes)
# 
# [MTECBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf)
# 
# [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#) 

# In[208]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].unique())


# In[209]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].dtype


# In[210]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].astype(str))


# In[211]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].astype(str)


# In[212]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].astype(str).str[:-5]


# In[213]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].str[:-5].unique()


# In[214]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].isna().sum()


# In[215]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].str[:-5]


# In[216]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# The data dictionary below comes from here [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#)

# In[217]:


'''
CODIGO	TITULO
0	MEMBROS DAS FORÇAS ARMADAS, POLICIAIS E BOMBEIROS MILITARES   
    MEMBERS OF THE ARMED FORCES, POLICE AND MILITARY FIREMEN
    
1	MEMBROS SUPERIORES DO PODER PÚBLICO, DIRIGENTES DE ORGANIZAÇÕES DE INTERESSE PÚBLICO E DE EMPRESAS, GERENTES     
    SENIOR MEMBERS OF THE PUBLIC AUTHORITIES, DIRECTORS OF PUBLIC INTEREST ORGANIZATIONS AND COMPANIES, MANAGERS

2	PROFISSIONAIS DAS CIÊNCIAS E DAS ARTES     
    SCIENCE AND ARTS PROFESSIONALS

3	TÉCNICOS DE NIVEL MÉDIO               
    MEDIUM LEVEL TECHNICIANS

4	TRABALHADORES DE SERVIÇOS ADMINISTRATIVOS  
    ADMINISTRATIVE SERVICE WORKERS

5	TRABALHADORES DOS SERVIÇOS, VENDEDORES DO COMÉRCIO EM LOJAS E MERCADOS  
    SERVICE WORKERS, SELLERS IN STORES AND MARKETS

6	TRABALHADORES AGROPECUÁRIOS, FLORESTAIS E DA PESCA  
    AGRICULTURAL, FORESTRY AND FISHERY WORKERS

7	TRABALHADORES DA PRODUÇÃO DE BENS E SERVIÇOS INDUSTRIAIS  
    WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES

8	TRABALHADORES DA PRODUÇÃO DE BENS E SERVIÇOS INDUSTRIAIS  
     WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES

9	TRABALHADORES EM SERVIÇOS DE REPARAÇÃO E MANUTENÇÃO    
    WORKERS IN REPAIR AND MAINTENANCE SERVICES
'''


# In[218]:


#7 and 8 have the same meaning in the original data dictionary from the website mentioned on the link


# In[219]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group 2002'].dtype


# In[220]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group 2002']


# In[221]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group 2002'].astype(str).replace('0','MEMBERS OF THE ARMED FORCES, POLICE AND MILITARY FIREMEN').replace('1','SENIOR MEMBERS OF THE PUBLIC AUTHORITIES, DIRECTORS OF PUBLIC INTEREST ORGANIZATIONS AND COMPANIES, MANAGERS').replace('2','SCIENCE AND ARTS PROFESSIONALS').replace('3','MEDIUM LEVEL TECHNICIANS').replace('4','ADMINISTRATIVE SERVICE WORKERS').replace('5','SERVICE WORKERS, SELLERS IN STORES AND MARKETS').replace('6','AGRICULTURAL, FORESTRY AND FISHERY WORKERS').replace('7','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('8','WORKERS IN THE PRODUCTION OF INDUSTRIAL GOODS AND SERVICES').replace('9','WORKERS IN REPAIR AND MAINTENANCE SERVICES')


# In[222]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'].unique()


# In[223]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'].dropna().unique()


# In[224]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'].replace('','NaN').unique()


# In[225]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'].replace('','NaN')


# In[226]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[227]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'] != 'NaN'].shape


# In[228]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'] != 'NaN']


# In[229]:


#another 5k rows was lost when dropping NaN from 'CBO Broad Group Name 2002' column


# In[230]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Broad Group Name 2002'].unique()


# In[231]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Broad Group Name 2002')
fig.update_layout(
    title={
        'text':'CBO Broad Group Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show('svg')


# In[232]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Broad Group Name 2002')
fig.update_layout(
    title={
        'text':'CBO Broad Group Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show('svg')


# In[233]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Broad Group Name 2002')
fig.update_layout(
    title={
        'text':'CBO Broad Group Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show()


# In[234]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[235]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].astype(str).str[:-4].unique()


# In[236]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Ocupação 2002'].astype(str).str[:-4]


# The data dictionary below comes from here [CBO](http://www.mtecbo.gov.br/cbosite/pages/downloads.jsf#)

# In[237]:


'''
CODIGO	TITULO
CODE -> TITLE

1	MEMBROS DAS FORÇAS ARMADAS         
    MEMBERS OF THE ARMED FORCES

2	POLICIAIS MILITARES          
    MILITARY POLICE

3	BOMBEIROS MILITARES   
    MILITARY FIREMEN

11	MEMBROS SUPERIORES E DIRIGENTES DO PODER PÚBLICO 
    SUPERIOR MEMBERS AND OFFICERS OF THE PUBLIC AUTHORITY


12	DIRIGENTES DE EMPRESAS E ORGANIZAÇÕES (EXCETO DE INTERESSE PÚBLICO)  
    DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)


13	DIRETORES E GERENTES EM EMPRESA DE SERVIÇOS DE SAÚDE, DA EDUCAÇÃO, OU DE SERVIÇOS CULTURAIS, SOCIAIS OU PESSOAIS  
    DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY

14	GERENTES    
    MANAGERS

20	PESQUISADORES E PROFISSIONAIS POLICIENTÍFICOS
    POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS

21	PROFISSIONAIS DAS CIÊNCIAS EXATAS, FÍSICAS E DA ENGENHARIA    
    PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES

22	PROFISSIONAIS DAS CIÊNCIAS BIOLÓGICAS, DA SAÚDE E AFINS   
    PROFESSIONALS IN BIOLOGICAL, HEALTH AND RELATED SCIENCES

23	PROFISSIONAIS DO ENSINO      
    TEACHING PROFESSIONALS

24	PROFISSIONAIS DAS CIÊNCIAS JURÍDICAS      
    PROFESSIONALS OF LEGAL SCIENCES

25	PROFISSIONAIS DAS CIÊNCIAS SOCIAIS E HUMANAS  
    PROFESSIONALS OF SOCIAL AND HUMAN SCIENCES

26	COMUNICADORES, ARTISTAS E RELIGIOSOS  
    COMMUNICATORS, ARTISTS AND RELIGIOUS

27	PROFISSIONAIS EM GASTRONOMIA
    PROFESSIONALS IN GASTRONOMY

30	TÉCNICOS POLIVALENTES    
    POLYVALENT TECHNICIAN 

31	TÉCNICOS DE NÍVEL MÉDIO DAS CIÊNCIAS FÍSICAS, QUÍMICAS, ENGENHARIA E AFINS  
    MIDDLE LEVEL TECHNICIANS IN PHYSICAL, CHEMICAL, ENGINEERING AND RELATED SCIENCES

32	TÉCNICOS DE NÍVEL MÉDIO DAS CIÊNCIAS BIOLÓGICAS, BIOQUÍMICAS, DA SAÚDE E AFINS 
    MIDDLE LEVEL TECHNICIANS IN BIOLOGICAL, BIOCHEMICAL, HEALTH AND RELATED SCIENCES

33	PROFESSORES LEIGOS E DE NÍVEL MÉDIO    
    LAY TEACHERS AND MIDDLE LEVEL

34	TÉCNICOS DE NÍVEL MÉDIO EM SERVIÇOS DE TRANSPORTES   
    MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES

35	TÉCNICOS DE NIVEL MÉDIO NAS CIÊNCIAS ADMINISTRATIVAS  
    MEDIUM-LEVEL TECHNICIANS IN ADMINISTRATIVE SCIENCES

37	TÉCNICOS EM NIVEL MÉDIO DOS SERVIÇOS CULTURAIS, DAS COMUNICAÇÕES E DOS DESPORTOS  
    MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS

39	OUTROS TÉCNICOS DE NÍVEL MÉDIO
    OTHER MIDDLE LEVEL TECHNICIANS

41	ESCRITURÁRIOS    
    CLERK

42	TRABALHADORES DE ATENDIMENTO AO PÚBLICO   
    PUBLIC SERVICE WORKERS

51	TRABALHADORES DOS SERVIÇOS  
    SERVICE WORKERS

52	VENDEDORES E PRESTADORES DE SERVIÇOS DO COMÉRCIO  
    SELLERS AND SERVICE PROVIDERS

61	PRODUTORES NA EXPLORAÇÃO AGROPECUÁRIA 
    PRODUCERS IN CATTLE RANCHING EXPLORATION

62	TRABALHADORES NA EXPLORAÇÃO AGROPECUÁRIA   
    WORKERS IN CATTLE RANCHING EXPLORATION

63	PESCADORES E EXTRATIVISTAS FLORESTAIS    
    FISHERMEN AND FORESTRY EXTRACTORS

64	TRABALHADORES DA MECANIZAÇÃO AGROPECUÁRIA E FLORESTAL 
    CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS

71	TRABALHADORES DA INDÚSTRIA EXTRATIVA E DA CONSTRUÇÃO CIVIL 
    WORKERS IN THE EXTRACTIVE INDUSTRY AND CIVIL CONSTRUCTION

72	TRABALHADORES DA TRANSFORMAÇÃO DE METAIS E DE COMPÓSITOS  
    METAL AND COMPOSITE TRANSFORMATION WORKERS

73	TRABALHADORES DA FABRICAÇÃO E INSTALAÇÃO ELETROELETRÔNICA  
    WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION

74	MONTADORES DE APARELHOS E INSTRUMENTOS DE PRECISÃO E MUSICAIS   
    ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS

75	JOALHEIROS, VIDREIROS, CERAMISTAS E AFINS    
    JEWELERS, GLASSMEN, CERAMISTS AND RELATED

76	TRABALHADORES NAS INDÚSTRIAS TÊXTIL, DO CURTIMENTO, DO VESTÚARIO E DAS ARTES GRÁFICAS   
    WORKERS IN THE TEXTILE, TANNING, CLOTHING AND GRAPHIC ARTS INDUSTRIES

77	TRABALHADORES DAS INDÚSTRIAS DE MADEIRA E DO MOBILIÁRIO 
    WORKERS IN THE WOOD AND FURNITURE INDUSTRIES

78	TRABALHADORES DE FUNÇÕES TRANSVERSAIS 
    CROSS FUNCTIONAL WORKERS

79	TRABALHADORES DO ARTESANATO
    HANDICRAFT WORKERS

81	TRABALHADORES EM INDÚSTRIAS DE PROCESSOS CONTÍNUOS E OUTRAS INDÚSTRIAS      
    WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES

82	TRABALHADORES DE INSTALAÇÕES SIDERÚRGICAS E DE MATERIAIS DE CONSTRUÇÃO 
    WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS

83	TRABALHADORES DE INSTALAÇÕES E MÁQUINAS DE FABRICAÇÃO DE CELULOSE E PAPEL  
    WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES

84	TRABALHADORES DA FABRICAÇÃO DE ALIMENTOS, BEBIDAS E FUMO     
    FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS

86	OPERADORES DE PRODUÇÃO, CAPTAÇÃO, TRATAMENTO E DISTRIBUIÇÃO (ENERGIA, ÁGUA E UTILIDADES)
    OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)

87	OPERADORES DE OUTRAS INSTALAÇÕES INDUSTRIAIS       
    OPERATORS OF OTHER INDUSTRIAL FACILITIES

91	TRABALHADORES EM SERVIÇOS DE REPARAÇÃO E MANUTENÇÃO MECÂNICA   
    WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES

95	POLIMANTENEDORES                                    
    MAINTAINER

99	OUTROS TRABALHADORES DA CONSERVAÇÃO, MANUTENÇÃO E REPARAÇÃO      
    OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS

'''


# In[238]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'].unique()


# In[239]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'] =='00']


# In[240]:


#'00' should not be in the Main SubGroup.'0' is from the Broad Group Name that turns into 1,2 or 3 in the Main SubGroup, and not '00'
#so it needs to be dropped


# In[241]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[242]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'] !='00'].shape


# In[243]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'] !='00']


# In[244]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'].unique()


# In[245]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[246]:


replacers = {'01':'MEMBERS OF THE ARMED FORCES','02':'MILITARY POLICE',
             '03':'MILITARY FIREMEN','11':'SUPERIOR MEMBERS AND OFFICERS OF THE PUBLIC AUTHORITY',
             '12':'DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)', 
             '13':'DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY',
             '14':'MANAGERS','20':'POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS',
             '21':'PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES', 
             '22':'PROFESSIONALS IN BIOLOGICAL, HEALTH AND RELATED SCIENCES',
             '23':'TEACHING PROFESSIONALS', 
             '24':'PROFESSIONALS OF LEGAL SCIENCES','25':'PROFESSIONALS OF SOCIAL AND HUMAN SCIENCES',
             '26':'COMMUNICATORS, ARTISTS AND RELIGIOUS','27':'PROFESSIONALS IN GASTRONOMY',
             '30':'EDUCATION','POLYVALENT TECHNICIAN':'HUMAN HEALTH AND SOCIAL SERVICES',
             '31':'MIDDLE LEVEL TECHNICIANS IN PHYSICAL, CHEMICAL, ENGINEERING AND RELATED SCIENCES',
             '32':'MIDDLE LEVEL TECHNICIANS IN BIOLOGICAL, BIOCHEMICAL, HEALTH AND RELATED SCIENCES',
             '33':'LAY TEACHERS AND MIDDLE LEVEL',
             '34':'MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES',
            '35':'MEDIUM-LEVEL TECHNICIANS IN ADMINISTRATIVE SCIENCES',
            '37':'MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS',
            '39': 'OTHER MIDDLE LEVEL TECHNICIANS',
            '41':'CLERK','42':'PUBLIC SERVICE WORKERS','51':'SERVICE WORKERS',
            '52':'SELLERS AND SERVICE PROVIDERS', '61':'PRODUCERS IN CATTLE RANCHING EXPLORATION',
            '62':'WORKERS IN CATTLE RANCHING EXPLORATION','63':'FISHERMEN AND FORESTRY EXTRACTORS',
            '64':'CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS','71':'WORKERS IN THE EXTRACTIVE INDUSTRY AND CIVIL CONSTRUCTION',
            '72':'METAL AND COMPOSITE TRANSFORMATION WORKERS','73':'WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION',
            '74':'ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS','75':'JEWELERS, GLASSMEN, CERAMISTS AND RELATED',
            '76':'WORKERS IN THE TEXTILE, TANNING, CLOTHING AND GRAPHIC ARTS INDUSTRIES','77':'WORKERS IN THE WOOD AND FURNITURE INDUSTRIES',
            '78':'CROSS FUNCTIONAL WORKERS','79':'HANDICRAFT WORKERS','81':'WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES',
            '82':'WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS','83':'WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES',
            '84':'FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS','86':'OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)',
            '87':'OPERATORS OF OTHER INDUSTRIAL FACILITIES','91':'WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES',
            '95':'MAINTAINER','99':'OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS'} 
bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup 2002'].replace(replacers)


# In[247]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'].unique()


# In[248]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[249]:


#bancoesusalltabsrais2019morelatlongcepestabselected.rename({'CBO Ocupação 2002':'CBO Occupation 2002'},axis=1,inplace=True)


# In[250]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002')
fig.update_layout(
    title={
        'text':'CBO Main SubGroup Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show('svg')


# In[251]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002')
fig.update_layout(
    title={
        'text':'CBO Main SubGroup Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show('svg')


# In[252]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002')
fig.update_layout(
    title={
        'text':'CBO Main SubGroup Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show()


# In[253]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002')
fig.update_layout(
    title={
        'text':'CBO Main SubGroup Name 2002',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show()


# In[254]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[255]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'].value_counts(normalize=True)


# In[256]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'].value_counts()


# In[257]:


bancoesusalltabsrais2019morelatlongcepestabselected.sort_values(by='CBO Main SubGroup Name 2002')


# In[258]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'].value_counts()<2000


# In[259]:


bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'][0:15]


# In[260]:


replacers = {'PROFESSIONALS IN EXACT, PHYSICAL AND ENGINEERING SCIENCES':'OTHERS',                                         
'WORKERS IN CATTLE RANCHING EXPLORATION':'OTHERS',                                                              
'METAL AND COMPOSITE TRANSFORMATION WORKERS':'OTHERS',                                                           
'WORKERS IN MECHANICAL REPAIR AND MAINTENANCE SERVICES':'OTHERS',                                                
'FOOD, BEVERAGE AND SMOKE MANUFACTURING WORKERS':'OTHERS',                                                       
'COMMUNICATORS, ARTISTS AND RELIGIOUS':'OTHERS',                                                                 
'DIRECTORS OF COMPANIES AND ORGANIZATIONS (EXCEPT PUBLIC INTEREST)':'OTHERS',                                   
'PROFESSIONALS OF LEGAL SCIENCES':'OTHERS',                                                                     
'MEDIUM LEVEL TECHNICIANS IN CULTURAL SERVICES, COMMUNICATIONS AND SPORTS':'OTHERS',                             
'WORKERS IN ELECTRO-ELECTRONIC MANUFACTURING AND INSTALLATION':'OTHERS',                                         
'DIRECTORS AND MANAGERS IN A HEALTH, EDUCATION, OR CULTURAL, SOCIAL OR PERSONAL SERVICES COMPANY':'OTHERS',      
'OPERATORS OF PRODUCTION, CAPTURE, TREATMENT AND DISTRIBUTION (ENERGY, WATER AND UTILITIES)':'OTHERS',           
'OTHER MIDDLE LEVEL TECHNICIANS':'OTHERS',                                                                       
'OTHER CONSERVATION, MAINTENANCE AND REPAIR WORKERS':'OTHERS',                                                   
'MEDIUM-LEVEL TECHNICIANS IN TRANSPORTATION SERVICES':'OTHERS',                                                  
'MAINTAINER':'OTHERS',                                                                                           
'WORKERS IN CONTINUOUS PROCESSES AND OTHER INDUSTRIES':'OTHERS',                                                 
'WORKERS IN THE WOOD AND FURNITURE INDUSTRIES':'OTHERS',                                                         
'WORKERS IN STEEL FACILITIES AND CONSTRUCTION MATERIALS':'OTHERS',                                               
'EDUCATION':'OTHERS',                                                                                            
'POLYSCIENTIFIC RESEARCHERS AND PROFESSIONALS':'OTHERS',                                                         
'CATTLE RANCHING AND FORESTRY MECHANIZATION WORKERS':'OTHERS',                                                  
'PROFESSIONALS IN GASTRONOMY':'OTHERS',                                                                          
'JEWELERS, GLASSMEN, CERAMISTS AND RELATED':'OTHERS',                                                            
'WORKERS IN PULP AND PAPER MANUFACTURING FACILITIES AND MACHINES':'OTHERS',                                     
'MILITARY POLICE':'OTHERS',                                                                                     
'ASSEMBLERS OF PRECISION AND MUSICAL APPARATUS AND INSTRUMENTS':'OTHERS',                                       
'FISHERMEN AND FORESTRY EXTRACTORS':'OTHERS',                                                                    
'MEMBERS OF THE ARMED FORCES':'OTHERS',                                                                          
'PRODUCERS IN CATTLE RANCHING EXPLORATION':'OTHERS',                                                             
'MILITARY FIREMEN':'OTHERS',                                                                                    
'HANDICRAFT WORKERS':'OTHERS'} 
bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002 with Others'] = bancoesusalltabsrais2019morelatlongcepestabselected['CBO Main SubGroup Name 2002'].replace(replacers)


# In[261]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002 with Others')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


# In[262]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002 with Others')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'}, showlegend=False)
fig.show('svg')


# In[263]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='CBO Main SubGroup Name 2002 with Others')
fig.update_layout(
    title={
        'text':'CBO 2002 Main SubGroup Name',
        'y':0.9,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'})#, showlegend=False)
fig.show('svg')


# In[264]:


#bancoesusalltabsrais2019morelatlongcepestabselected.rename({'CBO Ocupação 2002':'CBO Occupation 2002'}, axis = 1, inplace = True)


# In[265]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[266]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[267]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Classe']


# [CNAE IBGE CONCLA Divisões](https://cnae.ibge.gov.br/?option=com_cnae&view=estrutura&Itemid=6160&chave=&tipo=cnae&versao_classe=7.0.0&versao_subclasse=9.1.0)

# In[268]:


'''
Seção	Divisões	Denominação
A	01 .. 03	AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA
B	05 .. 09	INDÚSTRIAS EXTRATIVAS
C	10 .. 33	INDÚSTRIAS DE TRANSFORMAÇÃO
D	35 .. 35	ELETRICIDADE E GÁS
E	36 .. 39	ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO
F	41 .. 43	CONSTRUÇÃO
G	45 .. 47	COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
H	49 .. 53	TRANSPORTE, ARMAZENAGEM E CORREIO
I	55 .. 56	ALOJAMENTO E ALIMENTAÇÃO
J	58 .. 63	INFORMAÇÃO E COMUNICAÇÃO
K	64 .. 66	ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS
L	68 .. 68	ATIVIDADES IMOBILIÁRIAS
M	69 .. 75	ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS
N	77 .. 82	ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES
O	84 .. 84	ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
P	85 .. 85	EDUCAÇÃO
Q	86 .. 88	SAÚDE HUMANA E SERVIÇOS SOCIAIS
R	90 .. 93	ARTES, CULTURA, ESPORTE E RECREAÇÃO
S	94 .. 96	OUTRAS ATIVIDADES DE SERVIÇOS
T	97 .. 97	SERVIÇOS DOMÉSTICOS
U	99 .. 99	ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
'''


# In[269]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Classe'].dtype


# In[270]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[271]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Division'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[272]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[273]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Division']


# In[274]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section'].astype(int).replace(1,'A').replace(2,'A').replace(3,'A').replace(5,'B').replace(6,'B').replace(7,'B').replace(8,'B').replace(9,'B').replace(10,'C').replace(11,'C').replace(12,'C').replace(13,'C').replace(14,'C').replace(15,'C').replace(16,'C').replace(17,'C').replace(18,'C').replace(19,'C').replace(20,'C').replace(21,'C').replace(21,'C').replace(22,'C').replace(23,'C').replace(24,'C').replace(25,'C').replace(26,'C').replace(27,'C').replace(28,'C').replace(29,'C').replace(30,'C').replace(31,'C').replace(32,'C').replace(33,'C').replace(35,'D').replace(36,'E').replace(37,'E').replace(38,'E').replace(39,'E').replace(41,'F').replace(42,'F').replace(42,'F').replace(43,'F').replace(45,'G').replace(46,'G').replace(47,'G').replace(49,'H').replace(50,'H').replace(51,'H').replace(52,'H').replace(53,'H').replace(55,'I').replace(56,'I').replace(58,'J').replace(59,'J').replace(60,'J').replace(61,'J').replace(62,'J').replace(63,'J').replace(64,'K').replace(65,'K').replace(66,'K').replace(68,'L').replace(69,'M').replace(70,'M').replace(71,'M').replace(72,'M').replace(73,'M').replace(74,'M').replace(75,'M').replace(77,'N').replace(78,'N').replace(79,'N').replace(80,'N').replace(81,'N').replace(82,'N').replace(84,'O').replace(85,'P').replace(86,'Q').replace(87,'Q').replace(88,'Q').replace(90,'R').replace(91,'R').replace(92,'R').replace(93,'R').replace(94,'S').replace(95,'S').replace(96,'S').replace(97,'T').replace(99,'U')


# In[275]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section']


# In[276]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'].str.replace('A', 'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA').replace('B','INDÚSTRIAS EXTRATIVAS').replace('C','INDÚSTRIAS DE TRANSFORMAÇÃO').replace('D','ELETRICIDADE E GÁS').replace('E','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO').replace('F','CONSTRUÇÃO').replace('G','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS').replace('H','TRANSPORTE, ARMAZENAGEM E CORREIO').replace('I','ALOJAMENTO E ALIMENTAÇÃO').replace('J','INFORMAÇÃO E COMUNICAÇÃO').replace('K','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS').replace('L', 'ATIVIDADES IMOBILIÁRIAS').replace('M','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS').replace('N','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES').replace('O','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL').replace('P','EDUCAÇÃO').replace('Q','SAÚDE HUMANA E SERVIÇOS SOCIAIS').replace('R','ARTES, CULTURA, ESPORTE E RECREAÇÃO').replace('S','OUTRAS ATIVIDADES DE SERVIÇOS').replace('T','SERVIÇOS DOMÉSTICOS').replace('U','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS')


# In[277]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[278]:


bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'].unique()


# In[279]:


'''
'ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL',
       'OUTRAS ATIVIDADES DE SERVIÇOS',
       'COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS',
       'INDÚSTRIAS DE TRANSFORMAÇÃO', 'INDÚSTRIAS EXTRATIVAS',
       'ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES',
       'INFORMAÇÃO E COMUNICAÇÃO',
       'ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS',
       'SAÚDE HUMANA E SERVIÇOS SOCIAIS',
       'ARTES, CULTURA, ESPORTE E RECREAÇÃO',
       'TRANSPORTE, ARMAZENAGEM E CORREIO', 'ALOJAMENTO E ALIMENTAÇÃO',
       'ATIVIDADES IMOBILIÁRIAS',
       'ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS',
       'EDUCAÇÃO', 'CONSTRUÇÃO', 'ELETRICIDADE E GÁS',
       'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
       'SERVIÇOS DOMÉSTICOS',
       'ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO'
'''


# In[280]:


'''
A -> AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA 
  -> AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE
    
B -> INDÚSTRIAS EXTRATIVAS
  -> EXTRACTIVE INDUSTRIES
    
C -> INDÚSTRIAS DE TRANSFORMAÇÃO
  -> PROCESSING INDUSTRIES
    
D -> ELETRICIDADE E GÁS
  -> ELECTRICITY AND GAS

E -> ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO
  -> WATER, SEWAGE, WASTE MANAGEMENT AND DECONTAMINATION ACTIVITIES

F -> CONSTRUÇÃO
  -> CONSTRUCTION
    
G -> COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS
  -> TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES

H -> TRANSPORTE, ARMAZENAGEM E CORREIO
  -> TRANSPORTATION, STORAGE AND MAIL

I -> ALOJAMENTO E ALIMENTAÇÃO
  -> ACCOMMODATION AND FOOD

J -> INFORMAÇÃO E COMUNICAÇÃO
  -> INFORMATION AND COMMUNICATION

K -> ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS
  -> FINANCIAL, INSURANCE AND RELATED SERVICES ACTIVITIES

L -> ATIVIDADES IMOBILIÁRIAS
  -> REAL ESTATE ACTIVITIES

M -> ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS
  -> PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES

N -> ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES
  -> ADMINISTRATIVE ACTIVITIES AND COMPLEMENTARY SERVICES

O -> ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL
  -> PUBLIC ADMINISTRATION, DEFENSE AND SOCIAL SECURITY

P -> EDUCAÇÃO
  -> EDUCATION 

Q -> SAÚDE HUMANA E SERVIÇOS SOCIAIS
  -> HUMAN HEALTH AND SOCIAL SERVICES

R -> ARTES, CULTURA, ESPORTE E RECREAÇÃO
  -> ARTS, CULTURE, SPORTS AND RECREATION

S -> OUTRAS ATIVIDADES DE SERVIÇOS
  -> OTHER SERVICE ACTIVITIES

T -> SERVIÇOS DOMÉSTICOS
  -> DOMESTIC SERVICES

U -> ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
  -> INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS
'''


# In[281]:


replacers = {'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA ':'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE','INDÚSTRIAS EXTRATIVAS':'EXTRACTIVE INDUSTRIES','INDÚSTRIAS DE TRANSFORMAÇÃO':'PROCESSING INDUSTRIES','ELETRICIDADE E GÁS':'ELECTRICITY AND GAS','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO':'WATER, SEWAGE, WASTE MANAGEMENT AND DECONTAMINATION ACTIVITIES', 'CONSTRUÇÃO':'CONSTRUCTION','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS':'TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES','TRANSPORTE, ARMAZENAGEM E CORREIO':'TRANSPORTATION, STORAGE AND MAIL','ALOJAMENTO E ALIMENTAÇÃO':'ACCOMMODATION AND FOOD','INFORMAÇÃO E COMUNICAÇÃO':'INFORMATION AND COMMUNICATION','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS':'FINANCIAL, INSURANCE AND RELATED SERVICES ACTIVITIES','ATIVIDADES IMOBILIÁRIAS':'REAL ESTATE ACTIVITIES','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS':'PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES':'ADMINISTRATIVE ACTIVITIES AND COMPLEMENTARY SERVICES','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL':'PUBLIC ADMINISTRATION, DEFENSE AND SOCIAL SECURITY','EDUCAÇÃO':'EDUCATION','SAÚDE HUMANA E SERVIÇOS SOCIAIS':'HUMAN HEALTH AND SOCIAL SERVICES','ARTES, CULTURA, ESPORTE E RECREAÇÃO':'ARTS, CULTURE, SPORTS AND RECREATION','OUTRAS ATIVIDADES DE SERVIÇOS':'OTHER SERVICE ACTIVITIES','SERVIÇOS DOMÉSTICOS':'DOMESTIC SERVICES','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS':'INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS'} 
bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'] = bancoesusalltabsrais2019morelatlongcepestabselected['CNAE 2.0 Section Name'].replace(replacers)


# In[282]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[283]:


#bancoesusalltabsrais2019morelatlongcepestabselected.rename({'CNAE 2.0 Classe':'CNAE 2.0 Class', 'CNAE 2.0 Subclasse':'CNAE 2.0 Subclass'},axis=1,inplace=True)


# In[284]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[285]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor']


# In[286]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].unique()


# In[287]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].value_counts()


# In[288]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].value_counts(normalize=True)*100


# [IBGE Subclasse](https://concla.ibge.gov.br/busca-online-cnae.html?classe=84124&tipo=cnae&versao=9&view=classe) 
# 
# [IBGE CNAE 2.0 21 Seções](https://cnae.ibge.gov.br/?view=estrutura)
# 
# [CONCLA CNAE IBGE](https://cnae.ibge.gov.br/?view=classe&tipo=cnae&versao=7&classe=01199)

# In[289]:


from IPython.display import Image
Image(filename='25 subsetor ibge.jpg') 


# In[290]:


'''
24 Administração Pública - Public Administration
16 Comércio Varejista - Retail trade
19 Adm Técnica Profissional - Professional Technical Administration
21 Aloj Comunicações - Communication Accommodation
22 - Médicos Odontológico Vet. - doctors, dentist and veterinarians economic sector -> Human health activities
23 - Ensino -> Education
20 - Transporte e comunicação -> Transport and Communication
17 - Comércio Atacadista -> Wholesale 
13 - Alimentos e Bebidas -> Food and Drink
15 - Construção Civil -> Construction
Other activities 


16+17 (Essential wholesale(17) and retail trade (16))
'''


# In[291]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='IBGE Subsetor')
fig.show('svg')


# In[292]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].astype(str)


# In[293]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('24', 'Public Administration')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('16', 'Retail trade')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('19', 'Professional Technical Administration')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('21', 'Communication Accommodation')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('22', 'Human health activities')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('23', 'Education')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('20', 'Transport and Communication')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('17', 'Wholesale')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('13', 'Food and Drink')
bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'] = bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].str.replace('15', 'Construction')


# In[294]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].unique()


# In[295]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].replace({'1': 'Other activities', '14': 'Other activities', '8': 'Other activities',
                                                       '25': 'Other activities', '18':'Other activities', '6':'Other activities',
                                                      '9':'Other activities','3':'Other activities', '5':'Other activities',
                                                      '10':'Other activities','4':'Other activities','7':'Other activities',
                                                      '11':'Other activities','2':'Other activities','12':'Other activities'}, inplace = True)


# In[296]:


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsector'].unique()


# In[297]:


#bancoesusalltabsrais2019morelatlongcepestabselected.rename({'IBGE Subsector':'Economic activities'}, axis = 1, inplace = True)


# In[298]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected, names='IBGE Subsector')
fig.show('svg')


# In[299]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected, x='IBGE Subsector',color='IBGE Subsector',
                   title='IBGE Subsector',
                   labels={'IBGE Subsector':'IBGE Subsector', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'IBGE Subsector',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 90000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[300]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[301]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[302]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[303]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes']


# In[304]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes'].unique()


# In[305]:


#pd.set_option('display.max_rows', None)


# In[306]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes'].str.split(', ').explode().value_counts()


# In[307]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes'].str.split(', ').explode().value_counts().plot.bar();


# In[308]:


bancoesusalltabsrais2019morelatlongcepestabselected['condicoes'].str.split(', ').explode().value_counts(normalize=True)*100


# In[309]:


'''
Doenças cardíacas crônicas                                                  10272
Diabetes                                                                     7022
Doenças respiratórias crônicas descompensadas                                3505
Obesidade                                                                    1046
Imunossupressão                                                              1023
Gestante                                                                      962
Doenças Cardíacas ou Vasculares                                               801
4 ou 5)                                                                       373
Doenças renais crônicas em estágio avançado (graus 3                          373
Portador de doenças cromossômicas ou estado de fragilidade imunológica        325
Sobrepeso/Obesidade                                                           218
Doenças Respiratórias Crônicas                                                107
Doenças Renais Cronicas                                                        60
Puérpera (até 45 dias do parto)                                                55
Doença Hepática Crônica                                                        23
Gestante de alto risco                                                          6
Gestação                                                                        3
Portador de Doenças Cromossômicas                                               2
Doenças cardíacas crônicas,Doenças respiratórias crônicas descompensadas        1
'''


# In[310]:


107+60+55+23+6+3+2+1


# In[311]:


data = [['chronic heart disease', 10272], ['diabetes',7022], ['decompensated chronic respiratory diseases',3505],
        ['obesity',1046],['immunosuppression',1023],['pregnant', 962],
        ['chronic kidney disease at an advanced stage (grades 3, 4 or 5)',373],
        ['carrier of chromosomal diseases or state of immunological frailty',325],['overweight/obesity',218],['others',257]]
df = pd.DataFrame(data, columns = ['comorbidity','count'])
df


# In[312]:


fig = px.bar(df, x = 'comorbidity', y = 'count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Comorbidity',
        'y':0.95,
        'x':0.35,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
#fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg') #without the svg this graph looks perfect


# In[313]:


fig = px.bar(df, x = 'comorbidity', y = 'count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Comorbidity',
        'y':0.95,
        'x':0.35,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
#fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[314]:


bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution'].unique()


# In[315]:


bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution']=='death'].shape


# In[316]:


dfcomorbiditydeath = bancoesusalltabsrais2019morelatlongcepestabselected[bancoesusalltabsrais2019morelatlongcepestabselected['disease evolution']=='death']


# In[317]:


dfcomorbiditydeath


# In[318]:


dfcomorbiditydeath = dfcomorbiditydeath.dropna(subset=['condicoes'])


# In[319]:


dfcomorbiditydeath.shape


# In[320]:


dfcomorbiditydeath['condicoes'].str.split(', ').explode().value_counts()


# In[321]:


data = [['heart or vascular diseases',147],['diabetes',113],['overweight/obesity',53], ['chronic kidney disease',21],
        ['immunosuppression',14],['chronic respiratory diseases', 14],['chronic liver disease',7],]
df = pd.DataFrame(data, columns = ['comorbidity','death count'])
df


# In[322]:


fig = px.bar(df, x = 'comorbidity', y = 'death count', color = 'comorbidity')
fig.update_layout(
    title={
        'text': 'Death and Comorbidity',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'},paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
#fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[323]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[324]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[325]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas']


# In[326]:


'''
Coriza -> coryza
Vômito -> vomiting
Diarreia -> diarrhea
Mialgia -> myalgia 
Dor de Cabeça -> headache
Cefaleia - > headache
Dor de Garganta -> sore throat
Saturação O2 < 95% -> saturation < 95%
Dispneia -> dyspnea 
Febre -> fever 
Tosse -> cough

Coriza / Congestão Nasal -> Coryza / nasal congestion
Cansaço/fadiga -> tiredness/fatigue
Desconforto respiratório / aperto torácico -> respiratory distress / chest tightness


Alteração/perda de olfato e/ou paladar - change/loss of smell and/or taste

Distúrbios Olfativos -> olfactory dysfunction
Distúrbios Gustativos -> taste dysfunction
outros -> other
assintomático -> asymptomatic

there are other wordsattached to each other example VômitoFebre, DiarreiaTosse, and many others

what symptoms are mild and what symptoms are severe? there's no critiria
how will I organize the column? word count


Epidemiological and clinical characteristics of the first 557 successive
patients with COVID-19 in Pernambuco state, Northeast Brazil

Jurandy Júnior Ferraz de Magalhães et al.

"We then compared the viral load of
severe cases (patients that were admitted to ICU and the ones that have
died) with mild cases at different days since symptoms onset (Fig. 4B).
There was no statistically significant difference in viral load at the time
of diagnosis of patients with mild or severe COVID-19 up to 14 days of
symptoms onset. However, patients with severe disease diagnosed after
14 days of symptoms onset had higher viral load than patients with mild
disease (p = 0.0218)"


https://www.cdc.gov/coronavirus/2019-ncov/symptoms-testing/symptoms.html
https://www.webmd.com/lung/covid-19-symptoms#1

see the notes from meeting if michele said what is a severe and mild symptom
talk to emile to see how she separated these symptoms and how she handled the data

Dispneia é o termo médico usado para o que chamamos comumente de falta de ar ou de dificuldade de respirar. 
Quando um paciente tem dispneia, sua respiração torna-se irregular ou dificultosa, 
sendo que ele pode respirar de forma acelerada.

Mialgia é o termo médico para dor muscular. 

Cefaleia é o termo médico utilizado para designar aquilo que conhecemos como “dor de cabeça"


hospital ward -> enfermaria (caso precise para outra coluna)
'''


# In[327]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].astype(str).unique().sum()


# In[328]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts()


# In[329]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts().plot.bar();


# In[330]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts()>20000


# In[331]:


'''
replacers = {'Tosse':'cough','Outros':'others','Dor de garganta':'sore throat','Febre':'fever','Dor de Cabeça':'headache', 
             'Assintomático':'asymptomatic','Coriza':'coryza','Distúrbios Gustativos':'taste dysfunction',
             'Distúrbios Olfativos':'olfactory dysfunction','Dispneia':'dyspneia',
             'Saturação O2 < 95':'others',
             'Desconforto respiratório / aperto torácico':'others',                                                              
             'Cefaleia':'others',                                                           
             'Mialgia':'others',                                                
             'Cansaço/fadiga':'others',                                                       
             'Diarreia':'others',                                                                 
             'Alteração/perda de olfato e/ou paladar ':'others',                                   
             'Coriza / Congestão Nasal ':'others',                                                                     
             'Vômito':'others',                             
             'Náusea':'others',                                         
             'Tiragem Intercostal':'others',      
             'Distúrbios Gustativos,Distúrbios Olfativos':'others',           
             'Cianose':'others',                                                                       
             'Febre,Tosse,Distúrbios Gustativos,Distúrbios Olfativos ':'others',                                                   
             'Febre,Tosse  ':'others',                                                  
             'Erupções cutâneas':'others',                                                                                           
             'Edema mãos/pés':'others',                                                 
             'Febre,Dor de Garganta':'others',                                                         
             'Tosse,Distúrbios Gustativos,Distúrbios Olfativos':'others',  
             'Batimento Asa de Nariz':'others',                                           
             'Dor de Cabeça,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Tosse,Distúrbios Olfativos':'others',
             'Tosse,Dispneia,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Febre,Tosse,Dispneia':'others',
             'Febre,Distúrbios Olfativos':'others',
             'Dispneia,Distúrbios Gustativos,Distúrbios Olfativos':'others',
             'Tosse,Dor de Garganta,Dor de Cabeça,Coriza':'others',
             'Febre,Tosse,Dor de Garganta':'others',
             'Febre,Dor de Garganta,Dor de Cabeça':'others'}                    
bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'] = bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].astype(str).replace(replacers)
'''


# In[332]:


#this above does not work because the string has to be exactly the same as it shows on the data column


# In[333]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].unique()


# In[334]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].unique())


# In[335]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts()


# In[336]:


list(bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts())


# In[337]:


1632+1257+626+580+569+382+362+358+168+143+21+18+13+12+8+8+7+7+6+5+5+3+2+2+1+1+1+1+1+1+1+1+1+1+1+1


# In[338]:


#others = 6206 
#Outros = 90150

#other = 6206+90150


# In[339]:


6206+90150


# In[340]:


97435+90150+76398+76026+70217+49555+44139+27536+26272+25941


# In[341]:


583669 + 6206


# In[342]:


bancoesusalltabsrais2019morelatlongcepestabselected['sintomas'].str.split(', ').explode().value_counts().sum()


# In[343]:


'''
Tosse                                                        97435
Outros                                                       90150 (+6206 others = 96356)
Dor de Garganta                                              76398
Febre                                                        76026
Dor de Cabeça                                                70217
Assintomático                                                49555
Coriza                                                       44139
Dispneia                                                     27536
Distúrbios Gustativos                                        26272
Distúrbios Olfativos                                         25941
'''


# In[344]:


data = [['cough', 97435], ['others', 96356], ['sore throat', 76398], ['fever',76026], ['headache', 70217], ['asymptomatic',49555], ['coryza',44139],['dyspnea',27536],['taste dysfunction',26272],['olfactory dysfunction',25941]]
df = pd.DataFrame(data, columns = ['symptoms', 'count'])
df


# In[345]:


fig = px.bar(df, x = 'symptoms', y = 'count', color = 'symptoms')
fig.update_layout(
    title={
        'text': 'Symptoms',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[346]:


bancoesusalltabsrais2019morelatlongcepestabselected.shape


# In[347]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[348]:


bancoesusalltabsrais2019morelatlongcepestabselected.head(3)


# In[349]:


bancoesusalltabsrais2019morelatlongcepestabselected.rename({'CBO Ocupação 2002':'CBO Occupation 2002','CNAE 2.0 Classe':'CNAE 2.0 Class', 'CNAE 2.0 Subclasse':'CNAE 2.0 Subclass'}, axis=1,inplace=True)


# In[350]:


bancoesusalltabsrais2019morelatlongcepestabselected.columns


# In[351]:


bancoesusalltabsrais2019morelatlongcepestabselected[['estado','condicoes','disease evolution', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr','Qtd Dias Afastamento', 'Mun Trab', 'Health Professionals', 'Security Professionals',
        'sex', 'race','schooling', 'meanminimumwage', 'agecohort', 'CBO Occupation 2002', 'CBO Broad Group 2002', 
        'CBO Broad Group Name 2002','CBO Main SubGroup 2002', 'CBO Main SubGroup Name 2002',
       'CBO Main SubGroup Name 2002 with Others','IBGE Subsetor','IBGE Subsector','CNAE 2.0 Section','CNAE 2.0 Division','CNAE 2.0 Class',
       'CNAE 2.0 Subclass','CNAE 2.0 Section Name','cep','latitude','longitude','CEP Estab','latitudestab','longitudestab']]


# In[352]:


bancoesusalltabsrais2019morelatlongcepestabselected = bancoesusalltabsrais2019morelatlongcepestabselected[['estado','condicoes','disease evolution', 'dataInicioSintomas', 'cpf',
       'nomeCompletoDesnormalizado', 'dataNascimento', 'resultadoTeste',
       'bairro', 'municipio', 'GERES', 'profissionalSaude', 'dataNotificacao',
       'sintomas', 'idade', 'racaCor', 'profissionalSeguranca',
       'tipoTeste', 'sexo', 'Resultado Final', 'Tipo Vínculo',
       'Escolaridade após 2005', 'Vl Remun Média Nom', 'Vl Remun Média (SM)',
       'Tempo Emprego', 'Qtd Hora Contr','Qtd Dias Afastamento', 'Mun Trab', 'Health Professionals', 'Security Professionals',
        'sex', 'race','schooling', 'meanminimumwage', 'agecohort', 'CBO Occupation 2002', 'CBO Broad Group 2002', 
        'CBO Broad Group Name 2002','CBO Main SubGroup 2002', 'CBO Main SubGroup Name 2002',
       'CBO Main SubGroup Name 2002 with Others','IBGE Subsetor','IBGE Subsector','CNAE 2.0 Section','CNAE 2.0 Division','CNAE 2.0 Class',
       'CNAE 2.0 Subclass','CNAE 2.0 Section Name','cep','latitude','longitude','CEP Estab','latitudestab','longitudestab']]


# In[353]:


bancoesusalltabsrais2019morelatlongcepestabselected.to_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part1.csv',sep=',',index=False)


# ['_xsrf'](https://stackoverflow.com/questions/55014094/jupyter-notebook-not-saving-xsrf-argument-missing-from-post) argument missing from post

# In[ ]:





# ### continues on bancoesusalltabsrais2019morelatlongcepestabselected_part2.ipynb

# In[ ]:




