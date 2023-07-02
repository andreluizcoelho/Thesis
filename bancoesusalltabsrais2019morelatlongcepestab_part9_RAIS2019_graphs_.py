#!/usr/bin/env python
# coding: utf-8

# ## RAIS2019 before the merge to compare with the organized merged data
# ### do the CNAE division as done before in the merge

# In[96]:


## this was typed in the anaconda prompt before opening this page, otherise the file wouldn't open
## the text file opened but never showed the print
## jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10


# In[97]:


#file = open('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.txt', 'r')
#dados = file.read()
#print(dados)


# In[98]:


#f = open('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.txt',  200000000)
#text = f.read()
#f.close()


# In[99]:


#print(f)


# In[100]:


#with open ('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.txt', 'r') as f:
#    text = f.read()


# In[101]:


#print(text)


# In[102]:


### File: readline-example-3.py
#file = open('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.txt')
#while 1:
#    lines = file.readlines(100000)
#    if not lines:
#        break
#    for line in lines:
#        pass ### do something**strong text*


# In[103]:


#print(file)


# In[104]:


#with open ('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.txt', 'r') as f:
#    text = f.read()


# In[105]:


#print(text)


# In[106]:


#text


# ## RAIS 2019, run from RAIS 2019 Only RECIFE

# In[1]:


import pandas as pd


# In[ ]:


rais2019 = pd.read_csv('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/RAIS_VINC_ID_NORDESTE/RAIS_VINC_ID_PE/RAIS_VINC_ID_PE.csv', sep=';', header=0)


# In[3]:


rais2019.shape


# In[4]:


rais2019.head(4)


# In[5]:


rais2019['CPF'].duplicated().sum()


# In[6]:


rais2019['Município'].astype(str).str[:-4]


# In[7]:


rais2019[rais2019['Município'].astype(str).str[:-4]=='26'] #2132196 all the data is already on PE


# ## Recife

# In[8]:


rais2019[rais2019['Município']==261160] # 830030 rows


# In[43]:


rais2019Recife = rais2019[rais2019['Município']==261160]


# In[44]:


rais2019Recife.to_csv('rais2019Recife.csv', index=False)


# # Start here

# # RAIS 2019 Only RECIFE

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px


# In[2]:


rais2019Recife = pd.read_csv('rais2019Recife.csv')


# In[3]:


#rais2019=rais2019.rename(columns=rais2019.iloc[0]).drop(rais2019.index[0])


# In[4]:


pd.set_option('display.max_columns', None)


# In[5]:


rais2019Recife.shape


# In[6]:


rais2019Recife.head(4)


# In[7]:


rais2019Recife['CPF'].duplicated().sum()


# In[8]:


rais2019Recife[['Escolaridade após 2005','Sexo Trabalhador','Raça Cor','Vl Remun Média Nom','Vl Remun Média (SM)','Tempo Emprego','CNAE 2.0 Classe','Qtd Dias Afastamento','Idade']]


# In[9]:


rais2019Recife = rais2019Recife[['Sexo Trabalhador','Raça Cor','Idade','Escolaridade após 2005','Vl Remun Média (SM)','Vl Remun Média Nom','CNAE 2.0 Classe','Tempo Emprego','Qtd Dias Afastamento']]


# In[10]:


rais2019Recife


# In[11]:


rais2019Recife.isna().sum()


# ## Remember to remove the Na's after the bins are created 

# In[12]:


rais2019Recife['Sexo Trabalhador']


# In[13]:


rais2019Recife['Sexo Trabalhador'].value_counts()


# In[14]:


rais2019Recife['Sexo Trabalhador'].replace(2,0)


# In[15]:


rais2019Recife.isna().sum()


# In[16]:


rais2019Recife['Men'] = rais2019Recife['Sexo Trabalhador'].replace(2,0)


# ## Figure 21 Proportion of Men RAIS 2019

# In[17]:


fig = px.pie(rais2019Recife,names='Men')
fig.update_traces(textinfo='percent+value')
fig.update_layout(
        title={
        'text':'Proportion of Men',
        'y':0.95,
        'x':0.5,
        'xanchor':'center',
        'yanchor':'top'},showlegend=False)
fig.show()


# In[18]:


rais2019Recife['Raça Cor']


# In[19]:


'''
from 
RAIS_vinculos_layoutmicrodados.xls

INDIGENA	1
BRANCA	2
PRETA	4
AMARELA	6
PARDA	8
NAO IDENT	9
IGNORADO	{ñ class}
'''


# In[20]:


rais2019Recife['Raça Cor'].unique()


# In[21]:


rais2019Recife['Raça Cor'].value_counts()


# In[22]:


rais2019Recife['Raça Cor'].replace(1,'Indigenous').replace(2,'White').replace(4,'Black').replace(6,'Yellow').replace(8,'Brown').replace(9,'Ignored').replace(99,'Ignored')


# In[23]:


rais2019Recife['Raça Cor'] = rais2019Recife['Raça Cor'].replace(1,'Indigenous').replace(2,'White').replace(4,'Black').replace(6,'Yellow').replace(8,'Brown').replace(9,'Ignored').replace(99,'Ignored')


# In[24]:


rais2019Recife['Raça Cor'].unique()


# In[25]:


rais2019Recife.rename({'Raça Cor':'Race'},axis=1,inplace=True)


# In[26]:


'''fig = px.pie(rais2019Recife, names='Race')
fig.show('svg')'''


# # Figure 22 Proportion of RACE RAIS 2019

# In[27]:


fig = px.histogram(rais2019Recife['Race'], x='Race',color='Race',text_auto=True)#,
                   #title='Race')#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
#fig  = go.Figure()
#fig.add_trace(go.Histogram(x='Race',name='Race',texttemplate='%{x}', textfont_size=12))
fig.update_layout(
    title={
        'text': 'Race',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',bargap=0.1, showlegend=False)
#fig.update_traces(showlegend=True,text='Race')
fig.update_yaxes(title=' ',range=[0, 400000])
fig.update_xaxes(title=' ')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[28]:


# [age groups](https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html)


# In[29]:


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

bins = [0, 5, 18, 30, 40, 50, 65, 75, 85, np.inf]
names = ['0 - 4','5 - 17', '18 - 29', '30 - 39','40 - 49','50 - 64','65 - 74','75 - 84', '85+']

rais2019Recife['Age Cohort'] = pd.cut(rais2019Recife['Idade'], bins, labels=names)

print(rais2019Recife.dtypes)


# In[30]:


rais2019Recife['Age Cohort'].isna().sum()


# In[31]:


rais2019Recife.dropna(subset=['Age Cohort'])


# In[32]:


rais2019Recife['Age Cohort'].replace('Nan',0).astype(str).replace('nan','0').astype('category')


# In[33]:


rais2019Recife.shape


# In[34]:


rais2019Recife = rais2019Recife.dropna(subset=['Age Cohort'])


# In[35]:


rais2019Recife.shape


# In[36]:


rais2019Recife['Age Cohort'].isna().sum()


# In[37]:


#rais2019Recife['Age Cohort'] = rais2019Recife['Age Cohort'].astype(str).replace('nan','0').astype('category')
#replacing nan by 0 doesn't really makes sense


# In[38]:


#rais2019Recife['Age Cohort'].isna().sum()


# # Figure 23 Proportion of Age Cohort RAIS 2019

# In[39]:


fig = px.histogram(rais2019Recife['Age Cohort'], x='Age Cohort',color='Age Cohort',
                   title='Age Cohort',text_auto=True)#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
fig.update_layout(
    title={
        'text': 'Age Cohort',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',showlegend=False)
fig.update_yaxes(title=' ',range=[0, 300000])#,showgrid=True,ticks='outside')#.update_yaxes(categoryorder='total descending')
fig.update_xaxes(title=' ',categoryorder='array', categoryarray= ['0', '0 - 4', '5 - 17', '18 - 29', '30 - 39', '40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])#.update_xaxes(categoryorder='total ascending')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[40]:


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


# In[41]:


bins = [1, 5, 7, 9, np.inf]
names = ['1-4','5-6','7-8','9-11']

rais2019Recife['Educational Attainment'] = pd.cut(rais2019Recife['Escolaridade após 2005'], bins, labels=names)

print(rais2019Recife.dtypes)


# In[42]:


rais2019Recife['Educational Attainment'].isna().sum()


# In[43]:


rais2019Recife['Escolaridade após 2005']


# In[44]:


rais2019Recife['Escolaridade após 2005'].value_counts()


# In[45]:


rais2019Recife['Escolaridade após 2005'].isna().sum()


# In[46]:


fig = px.pie(rais2019Recife['Escolaridade após 2005'],names='Escolaridade após 2005')
fig.show('svg')


# In[47]:


rais2019Recife['Educational Attainment'] = rais2019Recife['Educational Attainment'].str.replace('1-4','Incomplete primary education')
rais2019Recife['Educational Attainment'] = rais2019Recife['Educational Attainment'].str.replace('5-6','Complete primary education')
rais2019Recife['Educational Attainment'] = rais2019Recife['Educational Attainment'].str.replace('7-8','Complete secondary education')
rais2019Recife['Educational Attainment'] = rais2019Recife['Educational Attainment'].str.replace('9-11','Complete higher education')


# In[48]:


fig = px.pie(rais2019Recife['Educational Attainment'],names='Educational Attainment')
fig.show('svg')


# # Figure 24 Educational Attainment RAIS 2019 

# In[49]:


fig = px.histogram(rais2019Recife['Educational Attainment'].dropna(), x='Educational Attainment',color='Educational Attainment',
                   title='Educational Attainment',text_auto=True)#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
fig.update_layout(
    title={
        'text': 'Educational Attainment',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',showlegend=False)#,separators =',.')#,yaxis_visible=False, yaxis_showticklabels=False)
fig.update_yaxes(title=' ',range=[0, 500000])
fig.update_xaxes(title=' ',categoryorder='array',categoryarray=['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education'])#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(name='count',texttemplate="%{x}", textfont_size=20)
#fig.update_traces(organizeddataRecifeforgraphsselected='%{text:.2s}', textposition='outside')
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside', textfont_size=14) #%{y:.1s},%{y:.2s},%{y:.3s}
#fig.update_traces(marker=dict(color='grey'))
#fig.update_traces(textsrc='outside')
fig.show()


# In[50]:


#sem rendimento (0), até 1/2 salário mínimo, mais de 1/2 a 1 salário mínimo, mais de 1 a 2 salários mínimos 
#mais de 2 a 5 salários mínimos, mais de 5 a 10 salários mínimos, mais de 10 a 20 salários mínimos, mais de 20 salários mínimos


# In[51]:


rais2019Recife['Vl Remun Média (SM)'].str.lstrip('0')


# In[52]:


rais2019Recife['Vl Remun Média (SM)'] = rais2019Recife['Vl Remun Média (SM)'].str.lstrip('0')


# In[53]:


rais2019Recife['Vl Remun Média (SM)'] = rais2019Recife['Vl Remun Média (SM)'].str.replace(',','.')


# In[54]:


rais2019Recife['Vl Remun Média (SM)'] = rais2019Recife['Vl Remun Média (SM)'].astype(float)


# In[55]:


rais2019Recife['Vl Remun Média (SM)'].sort_values(ascending=False).head(10)


# In[56]:


rais2019Recife['Vl Remun Média (SM)'].describe()


# In[57]:


rais2019Recife['Vl Remun Média (SM)'].max #Minimum Wage


# In[58]:


rais2019Recife['Vl Remun Média (SM)'].isna().sum()


# In[59]:


'''fig = px.pie(rais2019Recife['Vl Remun Média (SM)'], names='Vl Remun Média (SM)')
fig.show('svg')'''
#it did not work well


# In[60]:


rais2019Recife.columns


# In[61]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.1 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

rais2019Recife['Minimum Wage Range'] = pd.cut(rais2019Recife['Vl Remun Média (SM)'], bins, labels=names)

print(rais2019Recife.dtypes)


# In[62]:


rais2019Recife['Vl Remun Média (SM)'].isna().sum()


# In[63]:


rais2019Recife['Minimum Wage Range'].isna().sum()


# In[64]:


rais2019Recife['Minimum Wage Range'].astype(str).replace('nan','0').astype('category')


# In[65]:


rais2019Recife['Minimum Wage Range'] = rais2019Recife['Minimum Wage Range'].astype(str).replace('nan','0').astype('category')


# # Figure 25 Minimum Wage Range RAIS 2019 

# In[66]:


fig = px.histogram(rais2019Recife['Minimum Wage Range'], x='Minimum Wage Range',color='Minimum Wage Range',
                   title='Minimum Wage Range',text_auto=True)#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
fig.update_layout(
    title={
        'text': 'Minimum Wage Range',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',showlegend=False)
fig.update_yaxes(title=' ',range=[0, 500000])
fig.update_xaxes(title=' ',categoryorder='array', categoryarray= ['0', '0.1 - 1/2', '1/2 - 1', '1 - 2', '2 - 5', '5 - 10', '10 - 20', '20+'])#.update_xaxes(categoryorder='total ascending')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside', textfont_size=14) 
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[67]:


#rais2019Recife[rais2019Recife['Vl Remun Média (SM)'] <0.4]


# In[68]:


rais2019Recife['Vl Remun Média Nom'] = rais2019Recife['Vl Remun Média Nom'].str.lstrip('0')


# In[69]:


rais2019Recife['Vl Remun Média Nom'] = rais2019Recife['Vl Remun Média Nom'].str.replace(',','.')


# In[70]:


rais2019Recife['Vl Remun Média Nom'] = rais2019Recife['Vl Remun Média Nom'].astype(float)


# In[71]:


rais2019Recife['Vl Remun Média Nom'].sort_values(ascending=False).head(10)


# In[72]:


rais2019Recife['Vl Remun Média Nom'].value_counts()


# In[73]:


rais2019Recife['Vl Remun Média Nom'].describe()


# In[74]:


'''fig = px.pie(rais2019, names='Vl Remun Média Nom')
fig.show('svg')
'''


# In[75]:


rais2019Recife.head(3)


# In[76]:


# [numeric data into bins](https://stackoverflow.com/questions/49382207/how-to-map-numeric-data-into-categories-bins-in-pandas-dataframe)


# In[77]:


'''sem rendimento (0)
até 1/2 salário mínimo
mais de 1/2 a 1 salário mínimo 
mais de 1 a 2 salários mínimos 
mais de 2 a 5 salários mínimos 
mais de 5 a 10 salários mínimos 
mais de 10 a 20 salários mínimos
mais de 20 salários mínimos
'''


# In[78]:


rais2019Recife['Vl Remun Média Nom'].value_counts()


# In[79]:


bins = [0, 1, 499, 998, 1996, 4990, 9980, 19960, np.inf]
names = ['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+']

rais2019Recife['Nominal Wage Range'] = pd.cut(rais2019Recife['Vl Remun Média Nom'], bins, labels=names)

print(rais2019Recife.dtypes)


# In[80]:


rais2019Recife['Nominal Wage Range'].value_counts()


# In[81]:


rais2019Recife['Vl Remun Média Nom'].value_counts()


# In[82]:


rais2019Recife['Vl Remun Média Nom'].isna().sum()


# In[83]:


rais2019Recife['Nominal Wage Range'].isna().sum()


# In[84]:


rais2019Recife['Nominal Wage Range'].astype(str).replace('nan','0').astype('category')


# In[85]:


rais2019Recife['Nominal Wage Range'] = rais2019Recife['Nominal Wage Range'].astype(str).replace('nan','0').astype('category')


# In[86]:


fig = px.pie(rais2019Recife['Nominal Wage Range'], names='Nominal Wage Range')
fig.show('svg')


# # Figure 25 (repetive) do not include Nominal Wage Range RAIS 2019 

# In[87]:


fig = px.histogram(rais2019Recife['Nominal Wage Range'], x='Nominal Wage Range',color='Nominal Wage Range',
                   title='Nominal Wage Range',text_auto=True)#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
fig.update_layout(
    title={
        'text': 'Nominal Wage Range',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)', showlegend=False)
fig.update_yaxes(title=' ',range=[0, 500000])
fig.update_xaxes(title=' ',categoryorder='array', categoryarray =['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# ### the transition for CNAE is on part1 ipynb 

# In[132]:


rais2019Recife['CNAE 2.0 Classe']


# In[133]:


#[CNAE IBGE CONCLA Divisões](https://cnae.ibge.gov.br/?option=com_cnae&view=estrutura&Itemid=6160&chave=&tipo=cnae&versao_classe=7.0.0&versao_subclasse=9.1.0)


# In[134]:


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


# In[135]:


rais2019Recife['CNAE 2.0 Classe'].dtype


# In[136]:


rais2019Recife['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[137]:


rais2019Recife['CNAE 2.0 Division'] = rais2019Recife['CNAE 2.0 Classe'].astype(str).str[:-3]


# In[138]:


rais2019Recife['CNAE 2.0 Division']


# In[139]:


rais2019Recife['CNAE 2.0 Section'] = rais2019Recife['CNAE 2.0 Division'].astype(int).replace(1,'A').replace(2,'A').replace(3,'A').replace(5,'B').replace(6,'B').replace(7,'B').replace(8,'B').replace(9,'B').replace(10,'C').replace(11,'C').replace(12,'C').replace(13,'C').replace(14,'C').replace(15,'C').replace(16,'C').replace(17,'C').replace(18,'C').replace(19,'C').replace(20,'C').replace(21,'C').replace(21,'C').replace(22,'C').replace(23,'C').replace(24,'C').replace(25,'C').replace(26,'C').replace(27,'C').replace(28,'C').replace(29,'C').replace(30,'C').replace(31,'C').replace(32,'C').replace(33,'C').replace(35,'D').replace(36,'E').replace(37,'E').replace(38,'E').replace(39,'E').replace(41,'F').replace(42,'F').replace(42,'F').replace(43,'F').replace(45,'G').replace(46,'G').replace(47,'G').replace(49,'H').replace(50,'H').replace(51,'H').replace(52,'H').replace(53,'H').replace(55,'I').replace(56,'I').replace(58,'J').replace(59,'J').replace(60,'J').replace(61,'J').replace(62,'J').replace(63,'J').replace(64,'K').replace(65,'K').replace(66,'K').replace(68,'L').replace(69,'M').replace(70,'M').replace(71,'M').replace(72,'M').replace(73,'M').replace(74,'M').replace(75,'M').replace(77,'N').replace(78,'N').replace(79,'N').replace(80,'N').replace(81,'N').replace(82,'N').replace(84,'O').replace(85,'P').replace(86,'Q').replace(87,'Q').replace(88,'Q').replace(90,'R').replace(91,'R').replace(92,'R').replace(93,'R').replace(94,'S').replace(95,'S').replace(96,'S').replace(97,'T').replace(99,'U')


# In[140]:


rais2019Recife['CNAE 2.0 Section Name'] = rais2019Recife['CNAE 2.0 Section'].str.replace('A', 'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA').replace('B','INDÚSTRIAS EXTRATIVAS').replace('C','INDÚSTRIAS DE TRANSFORMAÇÃO').replace('D','ELETRICIDADE E GÁS').replace('E','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO').replace('F','CONSTRUÇÃO').replace('G','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS').replace('H','TRANSPORTE, ARMAZENAGEM E CORREIO').replace('I','ALOJAMENTO E ALIMENTAÇÃO').replace('J','INFORMAÇÃO E COMUNICAÇÃO').replace('K','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS').replace('L', 'ATIVIDADES IMOBILIÁRIAS').replace('M','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS').replace('N','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES').replace('O','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL').replace('P','EDUCAÇÃO').replace('Q','SAÚDE HUMANA E SERVIÇOS SOCIAIS').replace('R','ARTES, CULTURA, ESPORTE E RECREAÇÃO').replace('S','OUTRAS ATIVIDADES DE SERVIÇOS').replace('T','SERVIÇOS DOMÉSTICOS').replace('U','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS')


# In[141]:


rais2019Recife.head(3)


# In[142]:


rais2019Recife['CNAE 2.0 Section Name'].unique()


# In[143]:


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


# In[144]:


replacers = {'AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA':'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE','INDÚSTRIAS EXTRATIVAS':'EXTRACTIVE INDUSTRIES','INDÚSTRIAS DE TRANSFORMAÇÃO':'PROCESSING INDUSTRIES','ELETRICIDADE E GÁS':'ELECTRICITY AND GAS','ÁGUA, ESGOTO, ATIVIDADES DE GESTÃO DE RESÍDUOS E DESCONTAMINAÇÃO':'WATER, SEWAGE, WASTE MANAGEMENT AND DECONTAMINATION ACTIVITIES', 'CONSTRUÇÃO':'CONSTRUCTION','COMÉRCIO; REPARAÇÃO DE VEÍCULOS AUTOMOTORES E MOTOCICLETAS':'TRADE; REPAIR OF MOTOR VEHICLES AND MOTORCYCLES','TRANSPORTE, ARMAZENAGEM E CORREIO':'TRANSPORTATION, STORAGE AND MAIL','ALOJAMENTO E ALIMENTAÇÃO':'ACCOMMODATION AND FOOD','INFORMAÇÃO E COMUNICAÇÃO':'INFORMATION AND COMMUNICATION','ATIVIDADES FINANCEIRAS, DE SEGUROS E SERVIÇOS RELACIONADOS':'FINANCIAL, INSURANCE AND RELATED SERVICES ACTIVITIES','ATIVIDADES IMOBILIÁRIAS':'REAL ESTATE ACTIVITIES','ATIVIDADES PROFISSIONAIS, CIENTÍFICAS E TÉCNICAS':'PROFESSIONAL, SCIENTIFIC AND TECHNICAL ACTIVITIES','ATIVIDADES ADMINISTRATIVAS E SERVIÇOS COMPLEMENTARES':'ADMINISTRATIVE ACTIVITIES AND COMPLEMENTARY SERVICES','ADMINISTRAÇÃO PÚBLICA, DEFESA E SEGURIDADE SOCIAL':'PUBLIC ADMINISTRATION, DEFENSE AND SOCIAL SECURITY','EDUCAÇÃO':'EDUCATION','SAÚDE HUMANA E SERVIÇOS SOCIAIS':'HUMAN HEALTH AND SOCIAL SERVICES','ARTES, CULTURA, ESPORTE E RECREAÇÃO':'ARTS, CULTURE, SPORTS AND RECREATION','OUTRAS ATIVIDADES DE SERVIÇOS':'OTHER SERVICE ACTIVITIES','SERVIÇOS DOMÉSTICOS':'DOMESTIC SERVICES','ORGANISMOS INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS':'INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS'} 
rais2019Recife['CNAE 2.0 Section Name'] = rais2019Recife['CNAE 2.0 Section Name'].replace(replacers)


# In[145]:


rais2019Recife.head(3)


# In[146]:


rais2019Recife['CNAE 2.0 Section Name'].unique()


# In[147]:


rais2019Recife['CNAE 2.0 Section Name'].isna().sum()


# In[148]:


rais2019Recife['CNAE 2.0 Section Name'].unique()


# In[149]:


fig = px.pie(rais2019Recife['CNAE 2.0 Section Name'],names='CNAE 2.0 Section Name')
fig.show('svg')


# In[150]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show('svg')


# In[151]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.95,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show('svg')


# # Figure 26 CNAE 2.0 Economy Sectors % RAIS 2019

# In[154]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.275,
        'xanchor': 'center',
        'yanchor': 'top'})#,showlegend=False)
fig.show()


# In[109]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# # Figure 27 CNAE 2.0 Economy Sectors Values RAIS 2019

# In[157]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.275,
        'xanchor': 'center',
        'yanchor': 'top'})#,showlegend=False)
fig.show()


# In[111]:


fig = px.pie(rais2019Recife, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.47,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# In[112]:


rais2019Recife['CNAE 2.0 Section Name'].value_counts()


# In[113]:


rais2019Recife['CNAE 2.0 Section Name'].value_counts(ascending=True)


# In[114]:


len(rais2019Recife['CNAE 2.0 Section Name'].unique())
#len(organizeddataRecifeforgraphsselected['CNAE 2.0 Section Name'].unique()) had 19 because 
#DOMESTIC SERVICES (12)  and INTERNATIONAL BODIES AND OTHER EXTRATERRITORIAL INSTITUTIONS (19)  was not on there


# In[115]:


rais2019Recife


# In[116]:


rais2019Recife['Tempo Emprego']


# In[117]:


rais2019Recife['Tempo Emprego'] = rais2019Recife['Tempo Emprego'].str.replace(',','.')


# In[118]:


rais2019Recife['Tempo Emprego']


# In[119]:


rais2019Recife['Tempo Emprego'].str.lstrip('0')


# In[120]:


rais2019Recife['Tempo Emprego'] = rais2019Recife['Tempo Emprego'].str.lstrip('0')


# In[121]:


rais2019Recife['Tempo Emprego'].value_counts()


# In[122]:


rais2019Recife


# In[123]:


rais2019Recife['Qtd Dias Afastamento']


# In[124]:


rais2019Recife['Qtd Dias Afastamento'].value_counts()


# # Stop here!

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Merge bancoesus and rais2019, see it later, this is not the merge, this is not the merge kept for the whole thesis

# In[58]:


bancoesus27022021 = pd.read_excel('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/BASE ESUS 27.02.2021.xlsx')


# In[59]:


bancoesus27022021.shape


# In[9]:


bancoesus27022021.head(5)


# In[12]:


bancoesus27022021['cpf'].str.replace('-','')


# In[9]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('-','')


# In[10]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('.','')


# In[13]:


bancoesus27022021['cpf']


# In[12]:


bancoesus27022021.head(5)


# In[21]:


rais2019['CPF'].dtypes


# In[25]:


rais2019['CPF'].astype(object)


# In[28]:


rais2019['CPF']


# In[27]:


rais2019['CPF'].dtypes


# In[31]:


rais2019['CPF'].astype(object)


# In[15]:


rais2019['CPF'] = rais2019['CPF'].astype(object)


# In[16]:


rais2019['CPF'].dtypes


# In[23]:


bancoesus27022021['cpf'].dtypes


# In[30]:


# bancoesus27022021['cpf'].astype(int)   error: Python int too large to convert to C long


# In[17]:


rais2019bancoesus2722021 = rais2019.merge(bancoesus27022021, how='inner', left_on='CPF', right_on='cpf', indicator=True)


# In[18]:


rais2019bancoesus2722021.shape


# In[36]:


rais2019bancoesus2722021.head(3)


# In[29]:


rais2019sortedCPF = rais2019.sort_values(by = 'CPF', ascending = False)


# In[30]:


rais2019sortedCPF.head(3)


# In[31]:


bancoesus27022021sortedcpf = bancoesus27022021.sort_values(by = 'cpf', ascending = False)


# In[32]:


bancoesus27022021sortedcpf.head(3)


# In[33]:


rais2019sortedCPFbancoesus27022021sortedcpf = rais2019sortedCPF.merge(bancoesus27022021sortedcpf, how='inner', left_on='CPF', right_on='cpf', indicator = True)


# In[34]:


rais2019sortedCPFbancoesus27022021sortedcpf


# In[36]:


bancoesus27022021.cpf


# In[39]:


bancoesus27022021 = bancoesus27022021.dropna(subset = ['cpf'])


# In[40]:


bancoesus27022021sortedcpf.cpf


# In[42]:


bancoesus27022021sortedcpfnonan = bancoesus27022021sortedcpf.dropna(subset = ['cpf'])


# In[43]:


rais2019sortedCPFbancoesus27022021sortedcpfnonan = rais2019sortedCPF.merge(bancoesus27022021sortedcpfnonan, how='inner', left_on='CPF', right_on='cpf', indicator=True)


# In[44]:


rais2019sortedCPFbancoesus27022021sortedcpfnonan.shape


# In[45]:


bancoesus27022021sortedcpfnonan.shape


# In[46]:


#the merge is not happening because NaN was removed nor because the values were sorted, would it be because 
#I changed in the case below, the astype to str?


# In[48]:


bancoesus27022021sortedcpfnonan['cpf'].astype(str)


# In[50]:


rais2019sortedCPF['CPF'].astype(str)


# In[51]:


bancoesus27022021sortedcpfnonan['cpf'] = bancoesus27022021sortedcpfnonan['cpf'].astype(str)


# In[52]:


rais2019sortedCPF['CPF'] = rais2019sortedCPF['CPF'].astype(str)


# In[53]:


rais2019sortedCPFbancoesus27022021sortedcpfnonan = rais2019sortedCPF.merge(bancoesus27022021sortedcpfnonan, how='inner', left_on='CPF', right_on='cpf', indicator=True)


# In[54]:


rais2019sortedCPFbancoesus27022021sortedcpfnonan.shape


# In[55]:


#it worked!!!, the merge happened not because of removing the NaN on the column chosen for the merge nor because the values 
#were sorted, the merge happened because it was changed to string
#although after changing all values on the columns to be merged were stored as dtype:object


# In[ ]:





# In[56]:


#As a final check, I will merge from the orginal database, without removing the NaN nor sorting the values, but just changing 
#dtype to string, although it'll be stored as object, just to make sure I'll get the same results on the merge


# In[60]:


bancoesus27022021.head(3)


# In[66]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('-','')


# In[67]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('.','')


# In[69]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].astype(str)


# In[73]:


rais2019['CPF'] = rais2019['CPF'].astype(str)


# In[74]:


rais2019.head(3)


# In[75]:


rais2019bancoesus27022021 = rais2019.merge(bancoesus27022021, how='inner', left_on='CPF',right_on='cpf', indicator = True)


# In[76]:


rais2019bancoesus27022021.shape


# In[78]:


#it worked!!!, changing both columns on the merge to astype(str), although its stored as dtype object after changing it to string
#another important thing noticed, there's no need to sort the values, nor remove the NaN before the merge, what made the difference, 
#was to change the chosen columns' dtypes to string


# In[ ]:





# In[1]:


#####


# In[ ]:





# In[37]:


rais2019['CPF'] = rais2019['CPF'].astype(str)


# In[38]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].astype(str)


# In[39]:


rais2019['CPF'].dtypes


# In[40]:


bancoesus27022021['cpf'].dtypes


# In[41]:


#it doesn't work to turn object into a string when there is NaN values in the column 


# In[ ]:


rais2019['CPF']


# In[43]:


bancoesus27022021.dropna(subset = ['cpf']).head(3)


# In[45]:


bancoesus27022021[bancoesus27022021['cpf'].notna()].head(3)


# In[46]:


bancoesus27022021['cpf']


# In[47]:


#no idea why NaN turned into nan, but whatever 


# In[49]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('nan','NaN')


# In[54]:


bancoesus27022021[bancoesus27022021['cpf'].notna()]


# In[51]:


bancoesus27022021.dropna(subset = ['cpf']).head(3)


# In[53]:


bancoesus27022021['cpf'].dtypes


# In[55]:


#NaN is not dropping in any way


# In[57]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].str.replace('NaN','')


# In[58]:


bancoesus27022021['cpf']


# In[59]:


bancoesus27022021.dropna(subset = ['cpf'])


# In[61]:


bancoesus27022021['cpf'] = bancoesus27022021['cpf'].replace('', float('NaN'))


# In[63]:


bancoesus27022021nonancpf = bancoesus27022021.dropna(subset = ['cpf']) #there you go geez, no nan on cpf column now 


# In[64]:


bancoesus27022021nonancpf.shape


# In[65]:


bancoesus27022021.shape


# In[66]:


bancoesus27022021nonancpf.head(3)


# In[67]:


rais2019['CPF'].isna().sum()


# In[70]:


rais2019.CPF.isnull().sum() # no nan values for cpf on 2 million rows!!!


# In[71]:


rais2019['CPF']


# In[75]:


rais2019['CPF'].isin([0]).sum()


# In[76]:


rais2019['Ind Trab Parcial'].isin([0]).sum()


# In[77]:


#no nan for banco esus to transform to string and see if the merge gets better
#rais2019 has no NaN on cpf column nor 0s for the same column, for over 2 million rows!!!


# In[80]:


bancoesus27022021['cpf'].astype(str) # it did not turn into string because of the NaN values 'dtype: object'


# In[81]:


bancoesus27022021nonancpf['cpf'].astype(str)


# In[83]:


bancoesus27022021nonancpf['cpf'].str


# In[84]:


bancoesus27022021nonancpf['cpf']


# In[85]:


bancoesus27022021nonancpf['cpf'].astype('str')


# In[88]:


bancoesus27022021nonancpf['cpf'].astype(str)


# In[89]:


bancoesus27022021nonancpf['cpf'].dtypes


# In[90]:


bancoesus27022021nonancpf['cpf'].map(str)


# In[95]:


bancoesus27022021nonancpf['cpf'].astype(str)


# In[96]:


rais2019['CPF'].astype(str)


# In[99]:


rais2019 = rais2019.sort_values(by='CPF', ascending = False)


# In[100]:


rais2019.head(3)


# In[101]:


bancoesus27022021nonancpf.sort_values(by = 'cpf', ascending = False)


# In[102]:


bancoesus27022021nonancpf = bancoesus27022021nonancpf.sort_values(by = 'cpf', ascending = False)


# In[104]:


bancoesus27022021nonancpf.head(5)


# In[105]:


rais2019bancoesus27022021nonancpf = rais2019.merge(bancoesus27022021nonancpf, left_on='CPF', right_on='cpf', how='inner', indicator=True)


# In[111]:


rais2019bancoesus27022021nonancpf.shape #after dropping nan values and sorting value from the column to do the merge, it worked,
#so it's better to sort values and drop nan in the column that will merge, before merging? it seems it is


# In[112]:


rais2019bancoesus27022021nonancpf.to_excel('mergerais2019bancoesus27022021.xlsx', index = False)


# ### Merged Data Rais2019 and BancoEsus27022021

# In[10]:


import pandas as pd
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib
import matplotlib.pyplot as pl
import seaborn as sns
import plotly.express as px


# In[2]:


rais2019esus27022021 = pd.read_excel('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/mergerais2019bancoesus27022021.xlsx')


# In[3]:


rais2019esus27022021.shape


# In[25]:


rais2019esus27022021.dropna()


# In[9]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[10]:


rais2019esus27022021.head(3)


# In[11]:


rais2019esus27022021.describe()


# In[14]:


rais2019esus27022021.corr()


# In[15]:


corr = rais2019esus27022021.corr()
corr.style.background_gradient(cmap='coolwarm').set_precision(2)


# In[16]:


corr = rais2019esus27022021.corr() 
c1 = corr.unstack()
c1.sort_values(ascending = False)


# In[28]:


dfCorr = rais2019esus27022021.corr()
filteredDf = dfCorr[((dfCorr >= .5) | (dfCorr <= -.5)) & (dfCorr !=1.000)]
plt.figure(figsize=(30,25))
sns.heatmap(filteredDf, annot=True, cmap='coolwarm')
plt.title('Variables with Correlation > .5 or <.-5 and not equal to 1',
          size=20, verticalalignment='bottom')
plt.show()


# In[30]:


corr = rais2019esus27022021.corr()
kot = corr[corr>=.9]
plt.figure(figsize=(20,20))
sns.heatmap(kot, cmap='Reds')
plt.title('Variables with Correlation > .9');


# In[27]:


pd.set_option('display.max_columns', None)


# In[28]:


rais2019esus27022021.columns


# In[30]:


rais2019esus27022021.columns.tolist()


# In[29]:


print(rais2019esus27022021.columns.tolist())


# In[32]:


rais2019esus27022021['CBO 94 Ocupação']


# In[33]:


rais2019esus27022021['CNAE 2.0 Classe']


# In[38]:


rais2019esus27022021['Sexo Trabalhador'].value_counts


# In[42]:


rais2019esus27022021['Sexo Trabalhador'].value_counts()


# In[39]:


rais2019esus27022021['Sexo Trabalhador'].value_counts(normalize=True) * 100 #1-masculino 2-feminino


# In[43]:


rais2019esus27022021['Raça Cor'].value_counts(normalize=True) * 100


# In[49]:


rais2019esus27022021.head(3)


# In[44]:


'''INDIGENA	1
BRANCA	2
PRETA	4
AMARELA	6
PARDA	8
NAO IDENT	9
IGNORADO	{ñ class}'''


# In[48]:


rais2019esus27022021['Raça Cor'].rename(index={'8': 'Parda'})


# In[50]:


#print(rais2019esus27022021['Raça Cor'].set_axis(['Row_1', 'Row_2', 'Row_3'], axis='index'))


# In[45]:


rais2019esus27022021['racaCor'].value_counts(normalize=True) * 100 #a bit different percentages from rais 2019


# In[46]:


rais2019esus27022021['sexo'].value_counts(normalize=True) * 100 #almost the same as from rais 2019 


# In[14]:


fig = px.pie(rais2019esus27022021, values='Sexo Trabalhador', names='Raça Cor')
fig.show()


# In[17]:


fig = px.pie(rais2019esus27022021, values='Sexo Trabalhador', names='racaCor')
fig.show()


# In[ ]:




