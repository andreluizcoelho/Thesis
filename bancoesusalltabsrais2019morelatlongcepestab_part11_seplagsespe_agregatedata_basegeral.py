#!/usr/bin/env python
# coding: utf-8

# In[1071]:


import pandas as pd
import plotly.express as px


# the files were downloaded 31/05/2022 from seplag PE COVID-19 em [Dados](https://dados.seplag.pe.gov.br/apps/corona_dados.html)

# In[1072]:


from PIL import Image
myImage = Image.open('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/Organizing-Writing Thesis/dados agregados covid/PE Contra Covid 31052022.png');
myImage


# # Covid-19 em Dados(1).csv

# In[1073]:


Covid19emdados = pd.read_csv('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/Organizing-Writing Thesis/dados agregados covid/COVID-19 em Dados (1).csv')


# In[1074]:


# dt_referencia year-month-day


# In[1075]:


Covid19emdados


# In[1076]:


Covid19emdados.shape


# In[1077]:


Covid19emdados.tail()


# In[1078]:


#filter for the same dates as for the merge data 


# In[1079]:


Covid19emdados.sort_values('dt_referencia')


# In[1080]:


Covid19emdados = Covid19emdados.sort_values('dt_referencia')


# In[1081]:


Covid19emdados.head(3)


# In[1082]:


Covid19emdados[Covid19emdados['dt_referencia']<='2021-05-08']


# In[1083]:


Covid19emdadosuntilMay8th2021 = Covid19emdados[Covid19emdados['dt_referencia']<='2021-05-08']


# In[1084]:


Covid19emdadosuntilMay8th2021.shape


# In[1085]:


Covid19emdadosuntilMay8th2021.head(3)


# In[1086]:


Covid19emdadosuntilMay8th2021.tail()


# # basemapa.csv

# In[1087]:


basemapa = pd.read_csv('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/Organizing-Writing Thesis/dados agregados covid/basemapa.csv', sep=';', header=0)


# In[1088]:


#why is there a confirmed case in 04-01-2020 if the first case was in March 12 2020?


# In[1089]:


basemapa.head(29)


# In[1090]:


basemapa.shape


# In[1091]:


basemapa['X.U.FEFF.municipio_nm'].unique()


# In[1092]:


basemapa[basemapa['X.U.FEFF.municipio_nm']=='RECIFE']


# In[1093]:


basemapa['casos'].sum() #1,865,638 number of cases bigger than 936k, PE Contra o COVID


# In[1094]:


#filter by the same data on the merged data


# In[1095]:


basemapa[basemapa['dt_notificacao']<='08/05/2021']


# In[1096]:


basemapa['dt_notificacao'].sort_values(ascending=True)


# In[1097]:


pd.to_datetime(basemapa['dt_notificacao'])


# In[1098]:


basemapa['dt_notificacao_datetime'] =pd.to_datetime(basemapa['dt_notificacao'])


# In[1099]:


basemapa


# In[1100]:


basemapa[(basemapa['dt_notificacao_datetime']<='2021-05-08') & (basemapa['X.U.FEFF.municipio_nm']=='RECIFE')] #& and | or


# In[1101]:


basemapaRecifeuntilMay8th2021 = basemapa[(basemapa['dt_notificacao_datetime']<='2021-05-08') & (basemapa['X.U.FEFF.municipio_nm']=='RECIFE')] 


# In[1102]:


basemapaRecifeuntilMay8th2021.shape


# In[1103]:


basemapaRecifeuntilMay8th2021.head(3)


# In[1104]:


basemapaRecifeuntilMay8th2021.sort_values('dt_notificacao_datetime')


# In[1105]:


basemapaRecifeuntilMay8th2021 = basemapaRecifeuntilMay8th2021.sort_values('dt_notificacao_datetime')


# In[1106]:


basemapaRecifeuntilMay8th2021['casos'].sum()


# In[1107]:


basemapaRecifeuntilMay8th2021['óbito'].sum()


# # basegeral(1).csv

# In[1108]:


basegeral = pd.read_csv('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/rais2019/Organizing-Writing Thesis/dados agregados covid/basegeral (1).csv',sep=';',header=0)


# In[1109]:


#why does the data start in 23 April 2020 and not March 12 2020 which is the first case in PE, Recife 


# In[1110]:


basegeral


# In[1111]:


basegeral.head()


# In[1112]:


basegeral.sort_values('dt_notificacao')


# In[1113]:


basegeral[(basegeral['dt_notificacao']<='2021-05-08') & (basegeral['Resultado']=='POSITIVO')]


# In[1114]:


basegeral['evolucao'].unique()


# In[1115]:


basegeral[(basegeral['dt_notificacao']<='2021-05-08') & (basegeral['Resultado']=='POSITIVO')].shape #positive cases


# In[1116]:


basegeral[(basegeral['evolucao']=='OBITO') & (basegeral['dt_notificacao']<='2021-05-08')]


# In[1117]:


basegeral[(basegeral['evolucao']=='OBITO') & (basegeral['dt_notificacao']<='2021-05-08')].shape #death cases


# In[1118]:


(22982/385535)*100
#death rate


# In[1119]:


basegeral[(basegeral['dt_notificacao']<='2021-05-08') & (basegeral['Resultado']=='POSITIVO') & (basegeral['evolucao']=='OBITO')].shape


# # Only Recife first

# In[1120]:


basegeral[basegeral['municipio']=='RECIFE']


# In[1121]:


basegeralRecife = basegeral[basegeral['municipio']=='RECIFE']


# In[1122]:


basegeralRecife.shape


# In[1123]:


basegeralRecife.head(3)


# In[1124]:


basegeralRecife['Resultado'].unique()


# # 2020-03-12 March 12th 2020 until 2021-05-08 May 8th 2021

# In[1125]:


basegeralRecife[basegeralRecife['dt_notificacao']<='2021-05-08']


# In[1126]:


basegeralRecifeuntilMay8th2021 = basegeralRecife[basegeralRecife['dt_notificacao']<='2021-05-08']


# In[1127]:


basegeralRecifeuntilMay8th2021.shape


# In[1128]:


basegeralRecifeuntilMay8th2021.head(3)


# In[1129]:


basegeralRecifeuntilMay8th2021.sort_values('dt_notificacao')


# In[1130]:


basegeralRecifeuntilMay8th2021 = basegeralRecifeuntilMay8th2021.sort_values('dt_notificacao')


# In[1131]:


basegeralRecifeuntilMay8th2021


# In[1132]:


basegeralRecifeuntilMay8th2021.reset_index(drop=True, inplace=True)


# In[1133]:


basegeralRecifeuntilMay8th2021


# In[1134]:


basegeralRecifeuntilMay8th2021['dt_obito'].unique()


# In[1135]:


basegeralRecifeuntilMay8th2021[basegeralRecifeuntilMay8th2021['dt_obito']!='NaN']


# In[1136]:


basegeralRecifeuntilMay8th2021['dt_obito'].isna().sum()


# In[1137]:


basegeralRecifeuntilMay8th2021.shape


# In[1138]:


371604-365398


# In[1139]:


(6206/371604)*100 #1,67% of death, 6206 died out of 365398


# # compare with the merge data and do graphs

# In[1140]:


basegeralRecifeuntilMay8th2021


# In[1141]:


basegeralRecifeuntilMay8th2021['Resultado']


# In[1142]:


basegeralRecifeuntilMay8th2021['Resultado'].unique()


# In[1143]:


basegeralRecifeuntilMay8th2021.columns


# In[1144]:


basegeralRecifeuntilMay8th2021.head(3)


# In[1145]:


basegeralRecifeuntilMay8th2021['sintomas']


# In[1146]:


basegeralRecifeuntilMay8th2021['sintomas'].unique()


# In[1147]:


basegeralRecifeuntilMay8th2021['comorbidades'].unique()


# In[1148]:


basegeralRecifeuntilMay8th2021['tipo']


# In[1149]:


basegeralRecifeuntilMay8th2021['tipo'].unique()


# In[1150]:


basegeralRecifeuntilMay8th2021['tipo'].value_counts()


# In[1151]:


basegeralRecifeuntilMay8th2021[['Sexo','raca','prof_saude','faixa_etaria']]


# In[1152]:


basegeralRecifeuntilMay8th2021['Sexo'].value_counts()


# In[1153]:


basegeralRecifeuntilMay8th2021['Sexo'].replace('MASCULINO',1).replace('Masculino',1).replace('FEMININO',0).replace('Feminino',0)


# In[1154]:


basegeralRecifeuntilMay8th2021['Sexo'] = basegeralRecifeuntilMay8th2021['Sexo'].replace('MASCULINO',1).replace('Masculino',1).replace('FEMININO',0).replace('Feminino',0)


# In[1155]:


basegeralRecifeuntilMay8th2021['Sexo'].value_counts()


# In[1156]:


basegeralRecifeuntilMay8th2021[(basegeralRecifeuntilMay8th2021['Sexo']==1) | (basegeralRecifeuntilMay8th2021['Sexo']==0)]


# In[1157]:


basegeralRecifeuntilMay8th2021 =basegeralRecifeuntilMay8th2021[(basegeralRecifeuntilMay8th2021['Sexo']==1) | (basegeralRecifeuntilMay8th2021['Sexo']==0)]


# In[1158]:


basegeralRecifeuntilMay8th2021


# In[1159]:


basegeralRecifeuntilMay8th2021['Sexo'].value_counts()


# In[1160]:


basegeralRecifeuntilMay8th2021['raca'].unique()


# In[1161]:


basegeralRecifeuntilMay8th2021['raca'].value_counts()


# In[1162]:


basegeralRecifeuntilMay8th2021['raca'].replace('PARDA','Brown').replace('IGNORADO','Ignored').replace('BRANCA','White').replace('PRETA','Black').replace('AMARELA','Yellow').replace('INDIGENA','Indigenous')


# In[1163]:


basegeralRecifeuntilMay8th2021['raca'] = basegeralRecifeuntilMay8th2021['raca'].replace('PARDA','Brown').replace('IGNORADO','Ignored').replace('BRANCA','White').replace('PRETA','Black').replace('AMARELA','Yellow').replace('INDIGENA','Indigenous')


# In[1164]:


basegeralRecifeuntilMay8th2021['raca'].value_counts()


# In[1165]:


basegeralRecifeuntilMay8th2021['prof_saude']


# In[1166]:


basegeralRecifeuntilMay8th2021['prof_saude'].unique()


# In[1167]:


basegeralRecifeuntilMay8th2021['prof_saude'].isna().sum()


# In[1168]:


basegeralRecifeuntilMay8th2021['prof_saude'].replace('NÃ£o',0).replace('NÃƒO',0).replace('Sim',1).replace('SIM',1)


# In[1169]:


basegeralRecifeuntilMay8th2021['prof_saude'] = basegeralRecifeuntilMay8th2021['prof_saude'].replace('NÃ£o','0').replace('NÃƒO','0').replace('Sim','1').replace('SIM','1')


# In[1170]:


basegeralRecifeuntilMay8th2021['prof_saude'].unique()


# In[1171]:


basegeralRecifeuntilMay8th2021['prof_saude'].isna().sum()


# In[1172]:


basegeralRecifeuntilMay8th2021.head()


# In[1173]:


basegeralRecifeuntilMay8th2021.dropna(subset=['prof_saude'],inplace=True)


# In[1174]:


basegeralRecifeuntilMay8th2021


# In[1175]:


basegeralRecifeuntilMay8th2021['prof_saude'].isna().sum()


# In[1176]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].unique()


# In[1177]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].isna().sum()


# In[1178]:


basegeralRecifeuntilMay8th2021.dropna(subset=['faixa_etaria'],inplace=True)


# In[1179]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].isna().sum()


# In[1180]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].unique()


# In[1181]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].replace('0-9 anos','0 - 9').replace('10-19 anos','10-19').replace('10-19 anos','10-19').replace('20-29 anos','20-29').replace('30-39 anos','30-39').replace('40-49 anos','40-49').replace('50-59 anos','50-59').replace('60-69 anos','60-69').replace('70-79 anos','70-79').replace('80+ anos','80+')


# In[1182]:


basegeralRecifeuntilMay8th2021['faixa_etaria'] = basegeralRecifeuntilMay8th2021['faixa_etaria'].replace('0-9 anos','0 - 9').replace('10-19 anos','10 - 19').replace('20-29 anos','20 - 29').replace('30-39 anos','30 - 39').replace('40-49 anos','40 - 49').replace('50-59 anos','50 - 59').replace('60-69 anos','60 - 69').replace('70-79 anos','70 - 79').replace('80+ anos','80+')


# In[1183]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].unique()


# In[1184]:


basegeralRecifeuntilMay8th2021['faixa_etaria'].isna().sum()


# In[1185]:


basegeralRecifeuntilMay8th2021.head(3)


# In[1186]:


basegeralRecifeuntilMay8th2021[['Sexo','raca','prof_saude','faixa_etaria']]


# In[1187]:


basegeralRecifeuntilMay8th2021.rename({'Sexo':'Men','raca':'Race','prof_saude':'Health Professionals','faixa_etaria':'Age Cohort'},axis=1,inplace=True)


# In[1188]:


basegeralRecifeuntilMay8th2021


# In[1189]:


basegeralRecifeuntilMay8th2021[['Men','Health Professionals','Age Cohort','Race']]


# In[1190]:


basegeralRecifeuntilMay8th2021['Race'].unique()


# In[1191]:


basegeralRecifeuntilMay8th2021['Race'].isna().sum()


# In[1192]:


basegeralRecifeuntilMay8th2021.dropna(subset=['Race'],inplace=True)


# In[1193]:


basegeralRecifeuntilMay8th2021


# In[1194]:


basegeralRecifeuntilMay8th2021['evolucao'].unique()


# In[1195]:


basegeralRecifeuntilMay8th2021['evolucao'].value_counts()


# In[1196]:


(3908/352634)*100


# In[1197]:


basegeralRecifeuntilMay8th2021[basegeralRecifeuntilMay8th2021['Resultado']=='POSITIVO']


# ## 3908 dead out of 91425 positive cases, 4,27% death rate for Recife

# In[1198]:


(3908/91425)*100


# In[1199]:


basegeralRecifeuntilMay8th2021selected = basegeralRecifeuntilMay8th2021[['Men','Health Professionals','Age Cohort','Race']]


# In[1200]:


basegeralRecifeuntilMay8th2021selected.isna().sum()


# In[1201]:


(48816/352634)*100


# In[1202]:


basegeralRecifeuntilMay8th2021selected.shape


# In[ ]:





# In[1203]:


basegeralRecifeuntilMay8th2021selected.head()


# In[1204]:


fig = px.pie(basegeralRecifeuntilMay8th2021selected, names='Men')
fig.update_traces(textinfo='percent+value')
fig.update_layout(
        title={
        'text':'Proportion of Men',
        'y':0.95,
        'x':0.5,
        'xanchor':'center',
        'yanchor':'top'},showlegend=False)
fig.show()


# In[1205]:


fig = px.pie(basegeralRecifeuntilMay8th2021selected, names='Health Professionals',color='Health Professionals',
            color_discrete_map={0:'darkred',1:'darkblue'})
fig.update_traces(textinfo='percent+value')
fig.update_layout(
        title={
        'text':'Proportion of Health Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor':'center',
        'yanchor':'top'},showlegend=False)
fig.show()


# In[1206]:


basegeralRecifeuntilMay8th2021selected['Age Cohort'].unique()


# In[1207]:


fig = px.histogram(basegeralRecifeuntilMay8th2021selected, x='Age Cohort', color='Age Cohort',text_auto=True)#,
                   #title='Race')#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
#fig  = go.Figure()
#fig.add_trace(go.Histogram(x='Race',name='Race',texttemplate='%{x}', textfont_size=12))
fig.update_layout(
    title={
        'text': 'Age Cohort',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',bargap=0.1, showlegend=False)
#fig.update_traces(showlegend=True,text='Race')
fig.update_yaxes(title=' ',range=[0, 100000])
fig.update_xaxes(title=' ',categoryorder='array', categoryarray= ['0 - 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69', '70 - 79', '80+'])#.update_xaxes(categoryorder='total ascending')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[1208]:


fig = px.histogram(basegeralRecifeuntilMay8th2021selected, x='Race', color='Race',text_auto=True)#,
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
fig.update_yaxes(title=' ',range=[0, 150000])
fig.update_xaxes(title=' ')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:,.0f}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[1209]:


basegeralRecifeuntilMay8th2021selected.shape


# In[1210]:


basegeralRecifeuntilMay8th2021selected


# In[1211]:


basegeralRecifeuntilMay8th2021selected.dtypes


# In[1212]:


basegeralRecifeuntilMay8th2021selected['Men'] = basegeralRecifeuntilMay8th2021selected['Men'].astype(int)
basegeralRecifeuntilMay8th2021selected['Health Professionals'] = basegeralRecifeuntilMay8th2021selected['Health Professionals'].astype(int)


# In[1213]:


basegeralRecifeuntilMay8th2021selected.groupby('Age Cohort').mean().round(2)


# In[1214]:


basegeralRecifeuntilMay8th2021selected_agecohort_mean = basegeralRecifeuntilMay8th2021selected.groupby('Age Cohort').mean().round(2)


# In[1215]:


basegeralRecifeuntilMay8th2021selected_agecohort_mean.loc['Total'] = basegeralRecifeuntilMay8th2021selected_agecohort_mean.agg({'Men':'mean','Health Professionals':'mean'}).round(2)


# In[1216]:


basegeralRecifeuntilMay8th2021selected_agecohort_mean


# In[1217]:


basegeralRecifeuntilMay8th2021selected_race_mean = basegeralRecifeuntilMay8th2021selected.groupby('Race').mean().round(2)


# In[1218]:


basegeralRecifeuntilMay8th2021selected_race_mean.loc['Total'] = basegeralRecifeuntilMay8th2021selected_race_mean.agg({'Men':'mean','Health Professionals':'mean'}).round(2)


# In[1219]:


basegeralRecifeuntilMay8th2021selected_race_mean


# In[1220]:


basegeralRecifeuntilMay8th2021selected_race_mean['Men']*100


# In[1221]:


(basegeralRecifeuntilMay8th2021selected_race_mean['Men']*100).astype(int)


# In[1234]:


basegeralRecifeuntilMay8th2021selected_race_mean.reindex(['White','Yellow','Brown','Black','Indigenous','Ignored','Total']).round(2)


# Formatting pandas DataFrame columns [stackoverflow](https://stackoverflow.com/questions/23981601/format-certain-floating-dataframe-columns-into-percentage-in-pandas)

# In[1223]:


'''output = df.to_string(formatters={
    'var1': '{:,.2f}'.format,
    'var2': '{:,.2f}'.format,
    'var3': '{:,.2%}'.format
})
print(output)'''


# In[1224]:


basegeralRecifeuntilMay8th2021selected_race_mean.style.format({'Men': '{:,.0%}'})


# In[1225]:


basegeralRecifeuntilMay8th2021selected_race_mean.style.format({'Health Professionals': '{:,.0%}'})


# In[1226]:


#basegeralRecifeuntilMay8th2021selected_race_mean[['Men','Health Professionals']].apply(lambda x: map(lambda x:'{:.2f}%'.format(x),x),axis=1)


# In[1227]:


#df[['var1','var2']] = df[['var1','var2']].applymap("{0:.2f}".format)
#df['var3'] = df['var3'].applymap(lambda x: "{0:.2f}%".format(x*100))


# In[1228]:


basegeralRecifeuntilMay8th2021selected_race_mean[['Men','Health Professionals']].applymap('{:.0%}'.format)


# In[1229]:


basegeralRecifeuntilMay8th2021selected_race_mean = basegeralRecifeuntilMay8th2021selected_race_mean[['Men','Health Professionals']].applymap('{:.0%}'.format)


# In[1230]:


basegeralRecifeuntilMay8th2021selected_race_mean


# In[ ]:





# In[ ]:





# In[ ]:





# # Why is the first case 4th january 2020 from Frei Miguelinho PE positive, if the media says the first case is from Recife PE March 12th 2020?

# In[1231]:


#https://www.seplag.pe.gov.br/contato I sent an e-mail asking Maria Fernanda Ribeiro 20:37 01/06/2022
# meanwhile she responds or not lets get the cases from 2020-03-12 March 12th 2020 until 2021-05-08 May 8th 2021

# I have noticed that it is because some people are positive for other tests like influenza


# In[1232]:


basegeral.shape


# In[1233]:


#filter by the same data on the merged data


# # the merged data begins 04 12 2020 until 08 05 2021
# # the first case in Pernambuco was actually 12 03 2020 in Recife

# In[ ]:




