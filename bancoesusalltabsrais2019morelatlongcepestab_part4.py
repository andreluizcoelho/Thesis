#!/usr/bin/env python
# coding: utf-8

# ## article 2 

# In[1085]:


#logit ( or multivariate regression) with the probability of catching covid 
#or some causality method, catching covid by sector, days not working, wage interval, education, distance to cdb, etc


# In[1086]:


#do some tables from the articles


# In[1087]:


#use a logistic method, whether or not an individual catches covid, based on all other variables cited above and more


# In[1088]:


#search causal inference and covid on google for ideas


# In[1089]:


#see the paper 

#'Socioeconomic factors and the probability of
#death by Covid-19 in Brazil'

#try to replicate it using logistic equation


# ## plotting map with covidcases per municipality

# In[1090]:


import pandas as pd
import plotly.express as px
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[1091]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part1.csv')


# In[1092]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1093]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1094]:


#bancoesusalltabsrais2019morelatlongcepestabselected1.info()


# In[1095]:


#bancoesusalltabsrais2019morelatlongcepestabselected1.memory_usage()


# In[1096]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[1097]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].value_counts(normalize=True)


# In[1098]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].value_counts()


# In[1099]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].unique()


# In[1100]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.title()


# In[1101]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].astype(str)


# In[1102]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1103]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[1104]:


#fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected1, names='municipio')
#fig.show('svg')


# In[1105]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/PE_Municipios_2020/PE_Municipios_2020.shp')


# In[1106]:


gdf.head(3)


# In[1107]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.title()


# In[1108]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')


# In[1109]:


gdf['NM_MUN']


# In[1110]:


gdf.plot();


# In[1111]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='NM_MUN', right_on='municipio', how='inner', indicator=True)


# In[1112]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[1113]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.head(3)


# In[1114]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.columns


# In[1115]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].unique()


# In[1116]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isnull().sum()


# In[1117]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result']


# In[1118]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].value_counts()


# In[1119]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].unique()


# In[1120]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isnull().sum()


# In[1121]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.dropna(subset=['finalresultdummy'],inplace=True) 


# In[1122]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isnull().sum()


# In[1123]:


#null can not be replaced by 0, this would be a big bias, cause 0 means the test came out negative, null is a response from 
#the system where the data was collected for whatever reason 


# In[1124]:


#bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].replace({'Null':'nan','negative':'0','positive':'1'},inplace=True)


# In[1125]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[1126]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge[(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy']=='negative')| (bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy']=='positive')]


# In[1127]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge[(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy']=='negative')| (bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy']=='positive')]


# In[1128]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[1129]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[1130]:


#bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.dropna(subset=['finalresultdummy'],inplace=True) 


# In[1131]:


#bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[1132]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].replace({'negative':'0','positive':'1'},inplace=True)


# In[1133]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[1134]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].astype(int)


# In[1135]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[1136]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.groupby(by='NM_MUN').sum()


# In[1137]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.groupby(by='NM_MUN').sum()


# In[1138]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum


# In[1139]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.reset_index(level=0,inplace=True)


# In[1140]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.loc[:,['NM_MUN','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[1141]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.shape


# In[1142]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.head(3)


# In[1143]:


gdf


# In[1144]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases, on='NM_MUN', how='inner', indicator=True)


# In[1145]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[1146]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[1147]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[1148]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop('_merge',axis=1,inplace=True)


# In[1149]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[1150]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot();


# In[1151]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(cmap='gist_gray', column='NM_MUN', figsize=(10,10),legend=True);


# In[1152]:


pd.set_option('display.max_rows',None)


# In[1153]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge


# In[1154]:


#dropping Fernando de Noronha because it's messing up the map, 
#Fernando de Noronha has 32 covid positive cases by the way


# In[1155]:


pd.set_option('display.max_rows',10)


# In[1156]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.loc[bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['NM_MUN']=='Fernando De Noronha'].index, inplace = True)


# In[1157]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[1158]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[1159]:


f, ax = plt.subplots(1, figsize=(15, 15))
bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(ax=ax, column='finalresultdummy', legend=True, scheme = 'Quantiles', legend_kwds={'fmt':'{:.0f}'}, 
         cmap='binary', edgecolor='k')#, linewidth = 0.1)
ax.set_axis_off()
ax.set_title('Covid Cases PE March 2020 until May 8th 2021 N=63618', fontsize = 15)
plt.axis('equal')
plt.subplots_adjust(left=0.105, bottom=0.68, right=0.92, top=0.9, wspace=0.02, hspace=0.01) #default (left=0.125 [the left side of the subplots of the figure], bottom=0.1 [the bottom of the subplots of the figure], right=0.9 [the right side of the subplots of the figure], top=0.9[the top of the subplots of the figure], wspace=0.2[the amount of width reserved for blank space between subplots], hspace=0.2[the amount of height reserved for white space between subplots])
#plt.xlim(-41.5, -34.5)
#plt.ylim(-10,-4.5)
plt.show()


# ## plotting map covid cases per bairro

# In[1160]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1161]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[1162]:


bairrosgeojson


# In[1163]:


bairrosgeojson.plot();


# In[1164]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1165]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1166]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.title()


# In[1167]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[1168]:


bairrosgeojson['bairro_nome_ca'] = bairrosgeojson['bairro_nome_ca'].str.title()


# In[1169]:


bairrosgeojson


# In[1170]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge = bairrosgeojson.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='bairro_nome_ca', right_on='bairro',how='inner',indicator=True)


# In[1171]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.shape


# In[1172]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.head(3)


# In[1173]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['final result']


# In[1174]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].unique()


# In[1175]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].value_counts()


# In[1176]:


#null can not be replaced by 0, because null is a result from the system the data was collected for whatever reason 
#and 0 means the result came out negative


# In[1177]:


#bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].replace({'negative':'0','Null':'0','positive':'1'},inplace=True)


# In[1178]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge[(bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy']=='negative')|(bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy']=='positive')]


# In[1179]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge[(bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy']=='negative')|(bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy']=='positive')]


# In[1180]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.shape


# In[1181]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].unique()


# In[1182]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].replace({'negative':'0','positive':'1'},inplace=True)


# In[1183]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].value_counts()


# In[1184]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].astype(int)


# In[1185]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.groupby(by='bairro').sum()


# In[1186]:


bairrocovidsum = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.groupby(by='bairro').sum()


# In[1187]:


bairrocovidsum.reset_index(level=0,inplace=True)


# In[1188]:


bairrocovidsum.loc[:,['bairro','Health Professionals', 'Security Professionals','sex','finalresultdummy']]


# In[1189]:


bairroscovidsumsomecols = bairrocovidsum.loc[:,['bairro','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[1190]:


bairroscovidsumsomecols 


# In[1191]:


bairrosgeojson


# In[1192]:


bairromergesumcovidmerge=bairrosgeojson.merge(bairroscovidsumsomecols, left_on='bairro_nome_ca',right_on='bairro',how='inner',indicator=True)


# In[1193]:


bairromergesumcovidmerge.shape


# In[1194]:


bairromergesumcovidmerge.head(3)


# In[1195]:


bairromergesumcovidmerge.drop(['_merge'],axis=1,inplace=True)


# In[1196]:


bairromergesumcovidmerge.shape


# In[1197]:


bairromergesumcovidmerge.head(3)


# In[1198]:


bairromergesumcovidmerge.plot();


# In[1199]:


bairromergesumcovidmerge.plot(cmap='gist_gray', column='bairro', figsize=(10,10),legend=True);


# In[1200]:


bairromergesumcovidmerge['finalresultdummy'].sum()


# In[1201]:


f, ax = plt.subplots(1, figsize=(20, 20))
bairromergesumcovidmerge.plot(ax=ax, column='finalresultdummy', legend=True, scheme = 'Quantiles', legend_kwds={'fmt':'{:.0f}'}, 
         cmap='binary', edgecolor='k')#, linewidth = 0.1)
ax.set_axis_off()
ax.set_title('Covid Cases Recife March 2020 until May 8th 2021 N=21321', fontsize = 15)
plt.axis('equal')
plt.subplots_adjust(left=0.100, bottom=0.66, right=0.6, top=0.9, wspace=0.02, hspace=0.01) #default (left=0.125 [the left side of the subplots of the figure], bottom=0.1 [the bottom of the subplots of the figure], right=0.9 [the right side of the subplots of the figure], top=0.9[the top of the subplots of the figure], wspace=0.2[the amount of width reserved for blank space between subplots], hspace=0.2[the amount of height reserved for white space between subplots])
#plt.xlim(-41.5, -34.5)
#plt.ylim(-10,-4.5)
plt.show()


# ## just checking positive covid cases and deaths for the whole data 

# In[1202]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1203]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[1204]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].value_counts()


# In[1205]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].value_counts(normalize=True)


# In[1206]:


(361/241695) *100          #0.14% death from the data


# In[1207]:


'''
healed                        172093
recovered                       1252
in home treatment               1028
hospitalized isolation bed       962
death                            361
home isolation                   102
hospitalized ICU                  91
'''


# In[1208]:


172093+1252+1028+962+102+91


# In[1209]:


(175528/241695) *100 #72% did not die, 0.14% died, the rest is missing data, a model with death involved would not be good, 
#because very few people died in the data


# In[1210]:


bancoesusalltabsrais2019morelatlongcepestabselected1['final result'].value_counts()


# In[1211]:


bancoesusalltabsrais2019morelatlongcepestabselected1['final result'].value_counts(normalize=True)


# In[1212]:


(63650/241695) *100  #26.33% tested positive for covid 55.37% tested negative, about twice the number of positive cases,
#unlike doing a model for death which would not be good, doing a model for positive and negative cases might be ok
#maybe not even having the need to balance the data por negative and positive test results to be 50-50 


# ## getting rid of latitude and longitude outside PE and Recife

# In[1213]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import mapclassify


# In[1214]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1215]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1216]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']


# In[1217]:


bancoesusalltabsrais2019morelatlongcepestabselected1['longitude']


# In[1218]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] =='-'].shape


# In[1219]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] !='-'].shape


# In[1220]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] !='-']


# In[1221]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'] =='-'].shape


# In[1222]:


bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['latitude']).shape


# In[1223]:


(bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']=='').sum()


# In[1224]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].isnull().sum()


# In[1225]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].isna().sum()


# In[1226]:


bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['latitude'],inplace=True)


# In[1227]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1228]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']


# In[1229]:


bancoesusalltabsrais2019morelatlongcepestabselected1['longitude']


# In[1230]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] = bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].astype(float)
bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'] = bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'].astype(float)


# In[1231]:


crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'], bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'])]
geometry[:5]


# In[1232]:


geodataframe = gpd.GeoDataFrame(bancoesusalltabsrais2019morelatlongcepestabselected1, crs = crs, geometry = geometry)
geodataframe.head()


# In[1233]:


geodataframe.rename({'final result':'finalresult'},axis=1,inplace=True)


# In[1234]:


geodataframe.shape


# In[1235]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/PE_Municipios_2020/PE_Municipios_2020.shp')


# In[1236]:


gdf.shape


# In[1237]:


gdf.head(3)


# In[1238]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.title()


# In[1239]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')


# In[1240]:


gdf['NM_MUN']


# In[1241]:


gdf['NM_MUN'].nunique()


# In[1242]:


geodataframe['municipio'].nunique()


# In[1243]:


#They should have the same number of municipalities, but they don't, something is not right


# In[1244]:


gdf['NM_MUN'].sort_values().unique()


# In[1245]:


geodataframe['municipio'].sort_values().unique() 


# In[1246]:


#some municipalities had very similiar but different names, that's why there was a diffence in the number of municipalities
#Belem De Sao Francisco should be Belem Do Sao Francisco (1), Iguaraci should be Iguaracy (2), Lagoa Do Itaenga should be Lagoa De Itaenga(3)


# In[1247]:


geodataframe['municipio'] = geodataframe['municipio'].replace({'Belem De Sao Francisco':'Belem Do Sao Francisco','Iguaraci':'Iguaracy','Lagoa Do Itaenga':'Lagoa De Itaenga'})


# In[1248]:


geodataframe['municipio'].nunique()


# In[1249]:


#now it's the same 


# In[1250]:


gdf['NM_MUN'].nunique()


# In[1251]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
geodataframe.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE', fontsize = 18,pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[1252]:


#as we can see many coordinates are outside the shapefile


# In[1253]:


gdf.shape


# In[1254]:


geodataframe.shape


# In[1255]:


#there's a very simple command that will fix this


# In[1256]:


gpd.sjoin(geodataframe, gdf, op='within')


# In[1257]:


latlonginsidepe = gpd.sjoin(geodataframe, gdf, op='within')


# In[1258]:


latlonginsidepe.shape


# In[1259]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsidepe.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE',fontsize=18, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[1260]:


#nice huh? Now all lat and long are inside the shape file


# In[1261]:


#the x and y lim is very important, if it is way off, the map won't even show, so it's important to know the x and y limits 
#of the shapefile, to set the limit right


# In[1262]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[1263]:


bairrosgeojson.shape


# In[1264]:


bairrosgeojson.head(3)


# In[1265]:


#bairrosgeojson['bairro_nome_ca'] = bairrosgeojson['bairro_nome_ca'].str.title()


# In[1266]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
geodataframe.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=16,pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# In[1267]:


#we do same thing for Recife Shapefile, the capital of the state of Pernambuco in Brazil


# In[1268]:


gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[1269]:


bairrosgeojson.shape


# In[1270]:


geodataframe.shape


# In[1271]:


#so you don't get lost, there are 94 bairros in Recife, the geodataframe with all the data has 227872 rows
#since we are keeping the lats and longs inside the shape file only for the bairros inside Recife 
#the rows drops to 86914, because there are lat and long outside the shapefile of the city, which are scattered in the state


# In[1272]:


latlonginsiderecife = gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[1273]:


latlonginsiderecife.shape


# In[1274]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsiderecife.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=14, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# In[1275]:


#dejavu, there you go, all latitudes and longitudes are inside the shapefile, inside the city of Recife


# ## Calculating distance to CBD (Central Business District)

# In[1276]:


#the CBD in my case is marco zero, which the coordinates are (-8.0617353,-34.8706873)


# In[1277]:


#the radius of planet Earth is 6371km


# In[1278]:


#and to calculate the distance from latitude and longitude to the CBD I'll use haversine formula, which you can look up 
#for more details


# In Medium [Here’s How To Calculate Distance Between 2 Geolocations in Python](https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4)

# The [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) determines the great-circle distance between two points on a sphere given their longitudes and latitudes

# ![](https://miro.medium.com/max/1266/1*HPzoryv8InMFwWIYTWEkbw.png)

# In[1279]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)


# In[1280]:


start_lat, start_lon = -8.0617353, -34.8706873


# In[1281]:


distances_km=[]
for row in latlonginsiderecife.itertuples(index=False):
    distances_km.append(
    haversine_distance(start_lat,start_lon,row.latitude,row.longitude)
    ) 


# In[1282]:


latlonginsiderecife['distancefrommarcozero']=distances_km


# In[1283]:


latlonginsiderecife.head(3)


# In[1284]:


latlonginsiderecife.shape


# In[1285]:


latlonginsiderecife['distancefrommarcozero'].describe()


# In[1286]:


latlonginsiderecife.to_csv('organizeddatawithinRecifeshapefileborder.csv',index=False)


# In[1287]:


#calculating the distance from lat and long in Recife to the CBD makes sense for some analysis or model
#but what if I want to calculate that distance for the whole data


# In[1288]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1289]:


latlonginsidepe.shape #there's less data because the lats and long now are inside the shapefile


# In[1290]:


#it dropped from 241k rows to 227k rows because the missing lats and longs were dropped, and it dropped to 220k because 
#lat and longs inside the shapefile PE were kept


# In[1291]:


latlonginsidepe.head(3)


# In[1292]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)


# In[1293]:


start_lat, start_lon = -8.0617353, -34.8706873


# In[1294]:


distances_km=[]
for row in latlonginsidepe.itertuples(index=False):
    distances_km.append(
    haversine_distance(start_lat,start_lon,row.latitude,row.longitude)
    ) 


# In[1295]:


latlonginsidepe['distancefrommarcozero']=distances_km


# In[1296]:


latlonginsidepe.shape


# In[1297]:


latlonginsidepe.head(3)


# In[1298]:


latlonginsidepe['distancefrommarcozero'].describe()


# In[1299]:


#now the whole data for the whole state has the distance to cbd


# In[1300]:


#on part_2 ipynb there are some graphs with covid positive cases and death cases


# ## Creating the column Days without working 

# In[1301]:


latlonginsidepe.columns


# In[1302]:


latlonginsidepe['Qtd Dias Afastamento'].unique()


# In[1303]:


latlonginsidepe['Qtd Dias Afastamento'].describe()


# In[1304]:


latlonginsidepe['Qtd Dias Afastamento'].value_counts()


# In[1305]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

latlonginsidepe['Days Not Working'] = pd.cut(latlonginsidepe['Qtd Dias Afastamento'], bins, labels=names)

print(latlonginsidepe.dtypes)


# In[1306]:


latlonginsidepe.head(3)


# In[1307]:


latlonginsidepe['Days Not Working'].unique()


# In[1308]:


latlonginsidepe['Days Not Working'].value_counts()


# In[1309]:


latlonginsidepe['Days Not Working'].isna().sum() #same number of 0s


# In[1310]:


latlonginsidepe['Qtd Dias Afastamento'].isna().sum() #no NaN in the original column


# In[1311]:


latlonginsidepe['Days Not Working'].astype(str).replace('nan','0')


# In[1312]:


latlonginsidepe['Days Not Working'] = latlonginsidepe['Days Not Working'].astype(str).replace('nan','0')


# In[1313]:


latlonginsidepe['Days Not Working'].dtype


# In[1314]:


latlonginsidepe['Days Not Working'] = latlonginsidepe['Days Not Working'].astype('category')


# In[1315]:


latlonginsidepe['Days Not Working'].dtype


# In[1316]:


latlonginsidepe.head(3)


# In[1317]:


latlonginsidepe['Days Not Working'].value_counts()


# In[1318]:


#there were 172174 nan that should be 0s
#there are now 173437 0s, it might have been because over 1k NaN were transformed to 0s
#it comes from the 0s actually 
#latlonginsidepe['Days Not Working'].value_counts()
'''
20 - 29      18480
10 - 19       7596
30 - 39       5399
50 - 99       4398
1 - 9         4309
300+          2303
40 - 49       1895
100 - 149     1424
0             1263
150 - 199      608
200 - 249      341
250 - 299      227
'''
#1263 0s are not turning into NaN somehow
#but there is no NaN though in the original column


# In[1319]:


latlonginsidepe['Qtd Dias Afastamento'].value_counts()


# In[1320]:


latlonginsidepe['Days Not Working'].isna().sum() 


# In[1321]:


latlonginsidepe['Qtd Dias Afastamento'].isna().sum()


# In[1322]:


latlonginsidepe['Days Not Working'].value_counts()


# In[1323]:


latlonginsidepe.shape


# In[1324]:


latlonginsidepe.to_csv('organizeddatawithinPEshapefileborder.csv',index=False)


# ## Logit Model

# In[1325]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt


# In[1326]:


organizeddataPE = pd.read_csv('organizeddatawithinPEshapefileborder.csv')


# In[1327]:


organizeddataPE.shape


# In[1328]:


organizeddataPE.head(3)


# In[1329]:


organizeddataPE['Security Professionals']


# In[1330]:


organizeddataPE['Security Professionals'].dtype


# In[1331]:


organizeddataPE['Security Professionals'].unique()


# In[1332]:


organizeddataPE['Security Professionals'].value_counts()


# In[1333]:


#organizeddataPE = organizeddataPE.dropna(subset=['Security Professionals'])

#I dropped it before to convert to int type, because with nan, it can not be converted to int, and I wanted to convert to 
#int because the results had always .0 and the results from Health Professinals didn't, but in the end, making the last row 
#Total with agg containing sum and mean, Health Professionals and Security Professionals, ended up having .0
#So I didn't drop na for security professinals later in order not to lose more 5krows


# In[1334]:


organizeddataPE.shape


# In[1335]:


#220k rows dropped to 214k rows because Security Professionals were dropped in order to change dtype from float to int


# In[1336]:


#organizeddataPE['Security Professionals'] = organizeddataPE['Security Professionals'].astype(int)


# In[1337]:


organizeddataPE['finalresult']


# In[1338]:


organizeddataPE['finalresult'].unique()


# In[1339]:


organizeddataPE['finalresult'].value_counts()


# In[1340]:


organizeddataPE['finalresult'].isna().sum()


# In[1341]:


organizeddataPE[(organizeddataPE['finalresult']=='negative')|(organizeddataPE['finalresult']=='positive')].shape


# In[1342]:


organizeddataPE = organizeddataPE[(organizeddataPE['finalresult']=='negative')|(organizeddataPE['finalresult']=='positive')]


# In[1343]:


organizeddataPE.shape


# In[1344]:


#unfortunately 40k rows were lost to keep finalresult positive or negative, there was no other way


# In[1345]:


organizeddataPE.head(3)


# In[1346]:


organizeddataPE['finalresult'].unique()


# In[1347]:


organizeddataPE['finalresult'] = organizeddataPE['finalresult'].str.replace('positive','1').replace('negative','0')


# In[1348]:


organizeddataPE['finalresult'] = organizeddataPE['finalresult'].astype(int)


# In[1349]:


organizeddataPE['finalresult'].unique()


# In[1350]:


organizeddataPE['finalresult'].value_counts()


# In[1351]:


organizeddataPE['finalresult'].value_counts(normalize=True)


# In[1352]:


organizeddataPE.columns


# In[1353]:


organizeddataPE.rename({'Escolaridade após 2005':'School Years', 'Vl Remun Média (SM)':'Minimum Wage','Qtd Dias Afastamento':'No Working Days','sex':'Sex','finalresult':'Final Result','distancefrommarcozero':'Distance to CBD'}, axis = 1, inplace = True)


# In[1354]:


#testing an example for the logit model


# In[1355]:


X = organizeddataPE[['Sex','Distance to CBD']]


# In[1356]:


#categorical variables can not be in the X, like meanminimumwage etc
#there's the need to organize what exact variables will be in X


# In[1357]:


y = organizeddataPE['Final Result']


# In[1358]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)


# In[1359]:


logistic_regression= LogisticRegression()
logistic_regression.fit(X_train,y_train)
y_pred=logistic_regression.predict(X_test)


# In[1360]:


confusion_matrix = pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
sn.heatmap(confusion_matrix, annot=True)


# In[1361]:


print('Accuracy: ',metrics.accuracy_score(y_test, y_pred))
plt.show()


# In[1362]:


#pdf SOCIOECONOMIC FACTORS AND THE PROBABILITY OF DEATH BY COVID-19 IN BRAZIL


# In[1363]:


#Table 1 from the article 
#I can do one table for mean, then one for sum, then groupby minimum wage, race, and scholing, since I made them all categorical


# In[1364]:


organizeddataPE.groupby(by='agecohort').mean()


# In[1365]:


organizeddataPE_agecohortmean = organizeddataPE.groupby(by='agecohort').mean()


# In[1366]:


organizeddataPE_agecohortmean = organizeddataPE_agecohortmean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1367]:


organizeddataPE_agecohortmean 


# In[1368]:


organizeddataPE_agecohortmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[1369]:


#organizeddataPE_agecohortmean.sort_index(ascending = False)


# In[1370]:


#organizeddataPE.groupby(by='agecohort').agg('sum','mean')


# In[1371]:


organizeddataPE_agecohortsum = organizeddataPE.groupby(by='agecohort').sum()


# In[1372]:


organizeddataPE_agecohortsum


# In[1373]:


organizeddataPE_agecohortsum = organizeddataPE_agecohortsum.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1374]:


organizeddataPE_agecohortsum


# In[1375]:


organizeddataPE_agecohortsum.loc[:,{'Health Professionals','Security Professionals','Sex','Final Result'}]


# In[1376]:


organizeddataPE_summean = organizeddataPE.groupby('agecohort').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1377]:


organizeddataPE_summean


# In[1378]:


organizeddataPEagecohort_summean = organizeddataPE_summean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1379]:


organizeddataPE_summean


# In[1380]:


organizeddataPEagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1381]:


organizeddataPEagecohort_summean.loc['Total'] = organizeddataPEagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1382]:


organizeddataPEagecohort_summean


# In[1383]:


organizeddataPE.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1384]:


organizeddataPEmeanminimumwage_summean = organizeddataPE.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1385]:


organizeddataPEmeanminimumwage_summean


# In[1386]:


organizeddataPEmeanminimumwage_summean = organizeddataPEmeanminimumwage_summean.reindex(['0.1 - 1/2', '1/2 - 1', '1 - 2','2 - 5','5 - 10', '10 - 20', '20+'])


# In[1387]:


organizeddataPEmeanminimumwage_summean


# In[1388]:


organizeddataPEmeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1389]:


organizeddataPEmeanminimumwage_summean.loc['Total'] = organizeddataPEmeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1390]:


organizeddataPEmeanminimumwage_summean


# In[1391]:


organizeddataPE.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1392]:


organizeddataPE_racesummean = organizeddataPE.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1393]:


organizeddataPE_racesummean


# In[1394]:


organizeddataPE_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1395]:


organizeddataPE_racesummean.loc['Total'] = organizeddataPE_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1396]:


organizeddataPE_racesummean


# In[1397]:


organizeddataPEschooling_summean = organizeddataPE.groupby('schooling').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2) 


# In[1398]:


organizeddataPEschooling_summean 


# In[1399]:


organizeddataPEschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1400]:


organizeddataPEschooling_summean.loc['Total'] = organizeddataPEschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1401]:


organizeddataPEschooling_summean


# In[1402]:


organizeddataPEdaysnotworing_summean = organizeddataPE.groupby('Days Not Working').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1403]:


pd.set_option('display.max_rows',15)


# In[1404]:


organizeddataPEdaysnotworing_summean


# In[1405]:


organizeddataPEdaysnotworing_summean = organizeddataPEdaysnotworing_summean.reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+'])


# In[1406]:


organizeddataPEdaysnotworing_summean


# In[1407]:


#add a total row


# In[1408]:


organizeddataPEdaysnotworing_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1409]:


organizeddataPEdaysnotworing_summean.loc['Total'] = organizeddataPEdaysnotworing_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1410]:


organizeddataPEdaysnotworing_summean


# In[1411]:


#prepare the variables for the logit model, dummies, see pdf and the medium article


# In[1412]:


organizeddataPE.shape


# In[1413]:


organizeddataPE.head(3)


# In[1414]:


pd.set_option('display.max_columns',None)


# In[1415]:


organizeddataPE.head(3)


# In[1416]:


#reading the article 


# In[1417]:


'''-> means adapting to my case

These models use the following logistic equation:              -> Use the same Logit Model 
g(π) = α + βxi , where:
(i) g(π) = Pr(Y = 1 | x), Y being the dummy variable
indicating death due to Covid-19;
(ii) α is the intercept;
(iii) xi is the vector of explanatory variables and;
(iv) β are the estimated coefficients.

The explanatory variables are:
(a) age and age squared;                                       -> age (leave it as it is, think more about age squared)

"In all models, age is statistically
significant with the expected sign. Furthermore, the growth
rate of this probability decreases as age increases, which is
represented by the negative sign in age squared."

(b) man;                                                       -> man (the column has already 1s for man and 0s for women)

as for the articles results, men die 

(c) race/ethnicity: dummy variable identifying non-white       -> dummy for non-white (make this dummy)   
people and another identifying those whose race/ethnicity
has not been declared in the RAIS;

(d) Education: dummy variables for individuals with complete    -> dummy for complete primary, secondary and high education
primary, secondary and higher education;      

OBS:the same as my categorical values except incomplete primary education, leave incomplete or get rid of it
Leaving incomplete primary education or not, there's the need to make the dummy


(e)Metropolitan region: dummy for establishments located        -> dummy for establishments in RMR (see about that)
in the Metropolitan Region of Rio de Janeiro;

OBS: A dummy could be made for establishments in Recife somehow
or maybe I could use the distance to CBD as a variable



(f) the logarithm of the average annual labor earnings of       -> I could use Vl Remun Média Nom
the individual in 2018;


(g) dummies for different types of occupation;

OBS: the article needs to especify these occupations



(h) dummy indicating vulnerable occupations: health, protective -> I have a column already for health and security professionals
and transport workers;



(i) dummies for economic activity of the company/organization
where the individual works;

OBS: the artcile needs to especify these economic activities



(j) dummy for essential activities: human health, public            -> Find the essential activies in CNAE activities
order and safety, freight transport, courier and support activities
for transportation, passenger transport, essential wholesale
and retail trade, and other essential services (Food and
beverage, banks, cleaning, funeral and others).


The economic activity and occupations variables were used
interchangeably in different models’ specifications, especially
due to the high correlation between some occupations and
certain economic activities.

The individual’s occupation was obtained from the Brazilian
Classification of Occupations (CBO), present in the RAIS
database, based on the International Standard Classification of
Occupations (ISCO-88), and aggregated into 19 groups.

The essential economic activities were defined according to        -> See the essentail economic activies by PE'rules and its division groups in cnae
theGovernment of Rio de Janeiro state’s rules. The economic
activities were divided into 13 groups of essential activities
and three groups of non-essential activities, organized
based on the Brazilian National Classification of Economic
Activities revision 2.0 (CNAE 2.0), which is based on
the International Standard Industrial Classification (ISIC,
rev. 4).



They used Monte-Carlo for rare events, like in the article 
King and Zeng because death would be a rara event
In my case is much worse, I will do for catching covid 
Then Monte Carlo might not be need

Model 1, 2, 3, 4 and 5 differ in occupation and economic activity variables not especified by the article

Model 1 -> in addition to the basic variables, the
individual occupation was included as an explanatory variable

Model 2 -> there is a dummy variable for essential
economic activities in addition to occupation.

Model 3 and 4 -> occupation variables were replaced by economic activities 

Model 4 -> a dummy was added
for vulnerable occupations.


The choice to use either occupation or
activity is because many occupations are concentrated in a few
activities, generating a very high correlation between these two
sets of variables.

Model 5 -> creates a
new aggregation of economic activities, based on the previous
one, but where health professionals in the public administration
were incorporated into the Human health activities, and protective workers in the public administration were shifted
to the public order safety activities.


In my case maybe do a separate model with Economic activities
On the article model 1 and 2 used occupations model 3,4 and 5 used economic activities

See Fig.1 on the article 
Search how to do odds ration in Python

'''


# In[1418]:


#Health Professionals and Security Professionals came from RAIS or BANCO ESUS DATA?
#It is from Banco Esus Data
#'Diferentes planilhas do Banco esus e Rais.xlsx' has the columns from all the data


# In[1419]:


#organize the dummies as next step, test the medium article, find odds ration in python, see essential activities rules from
#the state of PE, divide the economic activities into essential groups, etc
#see pdf and medium article


# In[1420]:


#dummies 


# In[1421]:


organizeddataPE.shape


# In[1422]:


organizeddataPE.columns


# ## articles explanatory variables 

# In[1423]:


#age and age squared


# In[1424]:


organizeddataPE['idade']


# In[1425]:


organizeddataPE.rename({'idade':'age'}, axis=1, inplace=True)


# In[1426]:


organizeddataPE['age']


# In[1427]:


organizeddataPE['age']**2


# In[1428]:


organizeddataPE['Age 2'] = organizeddataPE['age']**2


# In[1429]:


organizeddataPE.head(3)


# In[1430]:


#man 

#the sex column is already a dummy by itself, 1 means man, 0 means woman


# In[1431]:


organizeddataPE['Sex'].unique()


# In[1432]:


organizeddataPE['Sex'].value_counts()


# In[1433]:


organizeddataPE['Sex'].value_counts(normalize=True)


# In[1434]:


organizeddataPE.rename({'Sex':'Men'},axis=1, inplace=True)


# In[1435]:


#44.58 % man 55.42% woman


# In[1436]:


#dummy for non-white and ignored race


# In[1437]:


organizeddataPE['race'].unique()


# In[1438]:


organizeddataPE['race'].value_counts()


# In[1439]:


organizeddataPE['race'].value_counts(normalize=True)


# In[1440]:


organizeddataPE['race'].isna().sum()


# In[1441]:


organizeddataPE = organizeddataPE.dropna(subset=['race'])


# In[1442]:


organizeddataPE.shape


# In[1443]:


organizeddataPE['race'].unique()


# In[1444]:


organizeddataPE['Non-White/Ignored'] = organizeddataPE['race']


# In[1445]:


#non-white 1 white 0

#every variable has a dummy value of 1 on table 2 from the article


# In[1446]:


organizeddataPE['Non-White/Ignored'] = organizeddataPE['Non-White/Ignored'].replace('Brown','Non-white').replace('Yellow','Non-white').replace('Black','Non-white').replace('Indigenous','Non-white').replace('Ignored','Uninformed race')


# In[1447]:


organizeddataPE['Non-White/Ignored'].unique()


# In[1448]:


organizeddataPE['Non-White/Ignored'].value_counts(normalize=True)


# In[1449]:


organizeddataPE['Non-White/Ignored'].value_counts()


# In[1450]:


#organizeddataPE = pd.get_dummies(organizeddataPE, columns=['Non-White/Ignored'])


# In[1451]:


organizeddataPE = pd.concat([organizeddataPE, pd.get_dummies(organizeddataPE['Non-White/Ignored'])], axis=1)


# In[1452]:


organizeddataPE.head(3)


# In[1453]:


organizeddataPE.rename({'Non-White/Ignored_Non-white':'Non-white', 'Non-White/Ignored_Uninformed race':'Uninformed race'},axis=1, inplace=True)


# In[1454]:


organizeddataPE.head(3)


# In[1455]:


#dummy for complete primary, secondary and high education


# In[1456]:


organizeddataPE['schooling'].unique()


# In[1457]:


organizeddataPE['schooling'].value_counts()


# In[1458]:


organizeddataPE['schooling'].value_counts(normalize=True)


# In[1459]:


#pd.get_dummies(organizeddataPE, columns=['schooling'])


# In[1460]:


organizeddataPE = pd.concat([organizeddataPE, pd.get_dummies(organizeddataPE['schooling'])], axis=1)


# In[1461]:


organizeddataPE.head(3)


# In[1462]:


#dummy for establishments in RMR (see about that), dummy for Recife for now, RMR can be done 

#Metropolitan region


# [IPEA Municípios da RMR](https://www.ipea.gov.br/redeipea/images/pdfs/governanca_metropolitana/150717_relatorio_arranjos_reecife.pdf)

# In[1463]:


'''
Araçoiaba, Igarassu, Itapissuma, Ilha de Itamaracá,
Abreu e Lima, Paulista, Olinda, Camaragibe, Recife, Jaboatão dos Guararapes, São
Lourenço da Mata, Moreno, Cabo de Santo Agostinho e Ipojuca
'''


# In[1464]:


'''
Aracoiaba, Igarassu, Itapissuma, Ilha de Itamaraca,
Abreu e Lima, Paulista, Olinda, Camaragibe, Recife, Jaboatao dos Guararapes, Sao
Lourenco da Mata, Moreno, Cabo de Santo Agostinho e Ipojuca
'''


# In[1465]:


organizeddataPE['municipio'].unique()


# In[1466]:


organizeddataPE['municipio'].value_counts()


# In[1467]:


#Igarassu
#Recife
#Aracoiaba
#Cabo de Santo Agostinho
#Camaragibe
#Ilha de Itamaraca
#Paulista
#Abreu e Lima
#Ipojuca
#Olinda
#Moreno
#Itapissuma
#Sao Lourenco da Mata
#Jaboatao dos Guararapes


# In[1468]:


replacers = {'Frei Miguelinho':'0', 'Santa Maria Do Cambuca':'0', 'Surubim':'0', 'Caruaru':'0',
       'Jatauba':'0', 'Altinho':'0', 'Araripina':'0', 'Toritama':'0', 'Bonito':'0',
       'Vertentes':'0', 'Jurema':'0', 'Taquaritinga Do Norte':'0', 'Sao Caitano':'0',
       'Gravata':'0', 'Cha Grande':'0', 'Brejo Da Madre De Deus':'0', 'Ibirajuba':'0',
       'Bezerros':'0', 'Riacho Das Almas':'0', 'Agrestina':'0', 'Igarassu':'1', 'Cumaru':'0',
       'Jaboatao Dos Guararapes':'1', 'Pesqueira':'0', 'Recife':'1', 'Camaragibe':'1',
       'Santa Cruz Do Capibaribe':'0', 'Barra De Guabiraba':'0',
       'Camocim De Sao Felix':'0', 'Feira Nova':'0', 'Paulista':'1', 'Palmares':'0',
       'Carpina':'0', 'Panelas':'0', 'Tabira':'0', 'Abreu E Lima':'1', 'Belem De Maria':'0',
       'Cupira':'0', 'Catende':'0', 'Sao Bento Do Una':'0', 'Garanhuns':'0', 'Goiana':'0',
       'Sao Joaquim Do Monte':'0', 'Lajedo':'0', 'Ipojuca':'1', 'Escada':'0', 'Limoeiro':'0',
       'Cachoeirinha':'0', 'Pombos':'0', 'Vitoria De Santo Antao':'0', 'Belo Jardim':'0',
       'Cabo De Santo Agostinho':'1', 'Sao Lourenco Da Mata':'1', 'Casinhas':'0',
       'Lagoa De Itaenga':'0', 'Olinda':'1', 'Belem Do Sao Francisco':'0', 'Condado':'0',
       'Petrolina':'0', 'Iguaracy':'0', 'Itaquitinga':'0', 'Serra Talhada':'0', 'Triunfo':'0',
       'Nazare Da Mata':'0', 'Moreno':'1', 'Flores':'0', 'Ilha De Itamaraca':'1',
       'Arcoverde':'0', 'Pocao':'0', 'Joao Alfredo':'0', 'Ouricuri':'0',
       'Afogados Da Ingazeira':'0', 'Salgueiro':'0', 'Passira':'0', 'Saire':'0',
       'Sao Joao':'0', 'Itapissuma':'1', 'Ribeirao':'0', 'Vicencia':'0', 'Brejinho':'0',
       'Paudalho':'0', 'Lagoa Do Carro':'0', 'Macaparana':'0', 'Alianca':'0',
       'Bom Jardim':'0', 'Gloria Do Goita':'0', 'Cha De Alegria':'0', 'Aracoiaba':'1',
       'Jaqueira':'0', 'Sanharo':'0', 'Sao Jose Da Coroa Grande':'0', 'Timbauba':'0',
       'Orobo':'0', 'Camutanga':'0', 'Cabrobo':'0', 'Amaraji':'0', 'Tamandare':'0',
       'Salgadinho':'0', 'Gameleira':'0', 'Angelim':'0', 'Itapetim':'0', 'Oroco':'0',
       'Lagoa Grande':'0', 'Exu':'0', 'Petrolandia':'0', 'Machados':'0', 'Caetes':'0',
       'Cortes':'0', 'Bom Conselho':'0', 'Venturosa':'0', 'Canhotinho':'0', 'Jupi':'0',
       'Jucati':'0', 'Sao Jose Do Egito':'0', 'Saloa':'0', 'Solidao':'0', 'Carnaiba':'0',
       'Tuparetama':'0', 'Santa Cruz Da Baixa Verde':'0', 'Ingazeira':'0',
       'Terezinha':'0', 'Lagoa Dos Gatos':'0', 'Tracunhaem':'0', 'Sao Vicente Ferrer':'0',
       'Correntes':'0', 'Itambe':'0', 'Paranatama':'0', 'Brejao':'0', 'Itaiba':'0', 'Buique':'0',
       'Alagoinha':'0', 'Rio Formoso':'0', 'Sao Jose Do Belmonte':'0', 'Floresta':'0',
       'Santa Cruz':'0', 'Calumbi':'0', 'Mirandiba':'0', 'Afranio':'0', 'Capoeiras':'0',
       'Sertania':'0', 'Betania':'0', 'Terra Nova':'0', 'Ibimirim':'0', 'Custodia':'0',
       'Carnaubeira Da Penha':'0', 'Tupanatinga':'0', 'Pedra':'0', 'Tacaimbo':'0',
       'Santa Terezinha':'0', 'Sao Benedito Do Sul':'0', 'Vertente Do Lerio':'0',
       'Aguas Belas':'0', 'Agua Preta':'0', 'Barreiros':'0', 'Xexeu':'0',
       'Joaquim Nabuco':'0', 'Primavera':'0', 'Fernando De Noronha':'0',
       'Buenos Aires':'0', 'Ferreiros':'0', 'Sirinhaem':'0', 'Trindade':'0',
       'Santa Maria Da Boa Vista':'0', 'Dormentes':'0', 'Serrita':'0', 'Verdejante':'0',
       'Parnamirim':'0', 'Bodoco':'0', 'Ipubi':'0', 'Jatoba':'0', 'Tacaratu':'0',
       'Santa Filomena':'0', 'Quixaba':'0', 'Inaja':'0', 'Maraial':'0', 'Manari':'0',
       'Quipapa':'0', 'Itacuruba':'0', 'Iati':'0', 'Moreilandia':'0', 'Calcado':'0',
       'Lagoa Do Ouro':'0', 'Palmeirina':'0', 'Granito':'0'} 
organizeddataPE['Metropolitan region'] = organizeddataPE['municipio'].replace(replacers)


# In[1469]:


organizeddataPE['Metropolitan region'].unique()


# In[1470]:


organizeddataPE['Metropolitan region'].value_counts()


# In[1471]:


organizeddataPE.head(3)


# In[1472]:


#(f) the logarithm of the average annual labor earnings of       -> I could use Vl Remun Média Nom (Minimum Wage)
#the individual in 2018;


# In[1473]:


organizeddataPE['Minimum Wage'].value_counts()


# In[1474]:


#dummies for different types of occupations, essential activities, health and security professinals (unfortunately for this last one, nan will have to be dropped if used)


# In[1475]:


organizeddataPE.head(3)


# In[1476]:


organizeddataPE.rename({'age':'Age'},axis=1,inplace=True)


# In[1477]:


organizeddataPE.dtypes


# In[1478]:


organizeddataPE['Metropolitan region'] = organizeddataPE['Metropolitan region'].astype('uint8')
organizeddataPE['Men'] = organizeddataPE['Men'].astype('uint8')


# In[1479]:


organizeddataPE['Qtd Hora Contr'].unique()


# In[1480]:


organizeddataPE['Qtd Hora Contr'].value_counts()


# In[1481]:


organizeddataPE.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[1482]:


organizeddataPE['Tempo Emprego'].unique()


# In[1483]:


organizeddataPE['Tempo Emprego'].describe()


# In[1484]:


organizeddataPE['Tempo Emprego'] = organizeddataPE['Tempo Emprego'].str.replace(',','.')


# In[1485]:


organizeddataPE['Tempo Emprego'] = organizeddataPE['Tempo Emprego'].str.lstrip('0')


# In[1486]:


organizeddataPE.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[1487]:


organizeddataPE['Job tenure'] = organizeddataPE['Job tenure'].astype(float)


# In[1488]:


organizeddataPE['Job tenure'].unique()


# In[1489]:


organizeddataPE['Job tenure'].describe()


# In[1490]:


#The column IBGE Subsector comes from RAIS


# In[1491]:


#run 3 models 1 with IBGE Subsector 1 with CBO occupations 1 with CNAE


# In[1492]:


organizeddataPE['IBGE Subsector'].unique()


# In[1493]:


pd.Series(organizeddataPE['IBGE Subsector'].unique()).sort_values()


# In[1494]:


print(sorted(organizeddataPE['IBGE Subsector'].unique()))


# In[1495]:


organizeddataPE['IBGE Subsector'].value_counts()


# In[1496]:


organizeddataPEIBGE = pd.concat([organizeddataPE, pd.get_dummies(organizeddataPE['IBGE Subsector'])], axis=1)


# In[1497]:


organizeddataPE.head(3)


# In[1498]:


organizeddataPEIBGE.shape


# In[1499]:


organizeddataPE['CBO Broad Group Name 2002'].unique()


# In[1500]:


organizeddataPE['CBO Main SubGroup Name 2002'].unique()


# In[1501]:


organizeddataPE['CBO Main SubGroup Name 2002 with Others'].unique()


# In[1502]:


pd.set_option('display.max_rows',20)


# In[1503]:


organizeddataPE['CBO Main SubGroup Name 2002 with Others'].value_counts()


# In[1504]:


organizeddataPE['CBO Main SubGroup Name 2002 with Others'].str.title().value_counts()


# In[1505]:


organizeddataPE['CBO Main SubGroup Name 2002 with Others'] = organizeddataPE['CBO Main SubGroup Name 2002 with Others'].str.title()


# In[1506]:


#and, in, of, the


# In[1507]:


organizeddataPECBO = pd.concat([organizeddataPE, pd.get_dummies(organizeddataPE['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[1508]:


organizeddataPECBO.shape


# In[1509]:


organizeddataPECBO.head(3)


# In[1510]:


organizeddataPE['CNAE 2.0 Section Name'].unique()


# In[1511]:


organizeddataPE['CNAE 2.0 Section Name'].value_counts()


# In[1512]:


organizeddataPE['CNAE 2.0 Section Name'] = organizeddataPE['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[1513]:


organizeddataPE['CNAE 2.0 Section Name'].value_counts()


# In[1514]:


organizeddataPE['CNAE 2.0 Section Name'] = organizeddataPE['CNAE 2.0 Section Name'].str.title()


# In[1515]:


organizeddataPECNAE = pd.concat([organizeddataPE, pd.get_dummies(organizeddataPE['CNAE 2.0 Section Name'])], axis = 1)


# In[1516]:


pd.Series(sorted(organizeddataPECNAE['CNAE 2.0 Section Name'].unique()))


# In[1517]:


organizeddataPECNAE.head(3)


# In[1518]:


'''
The essential economic activities were defined according to        -> See the essentail economic activies by PE'rules and its division groups in cnae
theGovernment of Rio de Janeiro state’s rules. The economic
activities were divided into 13 groups of essential activities
and three groups of non-essential activities, organized
based on the Brazilian National Classification of Economic
Activities revision 2.0 (CNAE 2.0), which is based on
the International Standard Industrial Classification (ISIC,
rev. 4).
'''
#what are these essential activities, according to Rio de Janeiro state's rules and PE state's rules?


# [atividades essenciais estado do Rio de Janeiro](http://www.rj.gov.br/secretaria/NoticiaDetalhe.aspx?id_noticia=5656&pl=altera%C3%A7%C3%A3o-na-resolu%C3%A7%C3%A3o-sobre-transportes-intermunicipais-para-os-setores-definidos-como-%27essenciais%27)

# In[1519]:


'''Confira a íntegra da lista de atividades consideradas essenciais:
I - servidores públicos em serviço, inclusive aqueles relacionados às forças armadas, bombeiro militar, 
e agentes de segurança pública;

II - profissionais do setor de saúde em geral, inclusive individuais que prestem serviços de atendimento domiciliar, 
excetuando-se os serviços de natureza estética;

III - profissionais do setor de comércio relacionados aos gêneros alimentícios, tais quais mercados, supermercados, 
 armazéns, hortifrútis, padarias e congêneres, farmácias drogarias e pet shops, revendedores de água e gás;

IV - profissionais do setor de serviços tais quais transporte e logística em geral, como transportadoras, 
portos e aeroportos, motoristas de transporte público, correios, e congêneres, serviços de entregas, distribuidoras, 
fornecimento de catering, bufê e outros serviços de comida preparada, asseio e conservação, manutenção predial, 
empregados em edifícios e condomínios, vigilância e segurança privada, lavanderias hospitalares, veterinárias, 
funerárias, imprensa, serviços de telecomunicação, postos de gasolina, bancário, internet, call center e serviços 
relacionados à tecnologia da informação e de processamento de dados (data center) para suporte de outras atividades 
previstas nesta Resolução, advogados e serviços de advocacia;

V - profissionais do setor industrial que exerçam atividades nas indústrias de alimentos, bebidas, farmacêutica, 
material hospitalar, material médico, produtos de higiene, produtos de limpeza, ração animal, óleo e gás, serviços 
de apoio às operações offshore, refino, coleta de lixo, limpeza urbana e destinação de resíduos, distribuidoras de 
gás e energia elétrica e companhias de saneamento.

VI -  pacientes em tratamento de saúde, com até 1 (um) acompanhante, desde que munidos de atestado médico, 
agendamento ou outro documento comprobatório da condição médica.

VII - profissionais cuidadores de idosos sem comprovação empregatícia, devidamente munidos de documento 
pessoal acompanhado de declaração assinada, conforme modelo oficial disponibilizado no sítio eletrônico 
oficial do Governo do Estado, criado para o enfrentamento da pandemia de coronavírus: https://coronavirus.rj.gov.br/
'''


# [ANEXO I Atividade essenciais RJ](https://www.legisweb.com.br/legislacao/?id=412129)

# In[1520]:


'''
ANEXO I Atividade essenciais:

Unidades de Saúde em Geral;

Clínicas e consultórios médicos e odontológicos; Laboratórios e unidades farmacêuticas;

Clínicas veterinárias;

Postos de Combustíveis e suas lojas de conveniências; Comércio de produtos farmacêuticos;

Atividades de comercialização de panificados e de produção gráfica;

Serviços de limpeza urbana;

Comércio da Construção Civil, ferragens, madeireiras, serralheiras, pinturas e afins Comércio atacadista;

Atividades industriais;

Atividades industriais automotivas;

Serviços Industriais de Utilidade Pública;

Indústria de alimentos e bebidas;

Comércio de autopeças e acessórios para veículos automotores e bicicletas, incluindo-se os serviços de mecânica e borracharia;

Serviços de lavanderia;

Serviços de limpeza, manutenção e zeladoria;
'''


# [atividades essenciais e não essenciais RJ](https://prefeitura.rio/wp-content/uploads/2021/03/DO_22_03_2021_-2a-EDICAO.pdf)

# In[1521]:


'''Art. 3º Fica suspenso:
I - o atendimento presencial, de qualquer natureza, em:
a) bares, lanchonetes, restaurantes e congêneres, exceto para as
modalidades de drive thru, take away e entrega em domicílio (delivery),
vedado, em qualquer hipótese, o consumo no local;
b) boates, danceterias, salões de dança e casas de festa;
c) museus, galerias, bibliotecas, cinemas, teatros, casas de espetáculo,
salas de apresentação, salas de concerto, salões de jogos, circos,
recreação infantil, parques de diversões, temáticos e aquáticos, pistas de
patinação, atividades de entretenimento, visitações turísticas, exposições
de arte, aquários, jardim zoológico;
d) salões de cabeleireiro, barbearias, institutos de beleza, estética e
congêneres;
e) clubes sociais e esportivos e serviços de lazer;
f) quiosques em geral, incluindo-se os da orla marítima, exceto na
modalidade de entrega em domicílio (delivery) e take away ;
g) demais estabelecimentos comerciais e de prestação de serviços não
especificados no art. 2º deste Decreto;
II - o exercício de demais atividades econômicas nas areias das praias
e nos logradouros, incluindo-se o comércio ambulante fixo e itinerante,
o comércio de alimentos, bebidas e produtos por meio de veículos
automotores, rebocáveis ou movidos à propulsão humana, o comércio
exercido em feiras especiais, feiras de ambulantes, feiras de antiquários
e feirartes;
III - a permanência de indivíduos:...'''


# [atividades essenciais PE](https://www.pecontracoronavirus.pe.gov.br/anexo-i-atividades-essenciais/)

# In[1522]:


'''
ANEXO I – Atividades essenciais
ATENÇÃO: No dia 14/05/2020 o decreto Nº 49.017 foi substituído pelo Nº 49.024. Por isso clique aqui para consultar as atividades essenciais válidas.

ANEXO I
ATIVIDADES ESSENCIAIS

I – os serviços públicos referidos no §3º do art. 2º e no art. 3º do Decreto nº 48.835, de 22 de
março de 2020, e alterações posteriores;
II – supermercados, padarias, mercados, lojas de conveniência, feiras livres e demais
estabelecimentos voltados ao abastecimento alimentar da população;
III – lojas de defensivos e insumos agrícolas;
IV – farmácias e estabelecimentos de venda de produtos médico-hospitalares;
V – lojas de produtos de higiene e limpeza;
VI – postos de gasolina;
VII – casas de ração animal;
VIII – depósitos de gás e demais combustíveis;
IX – lojas de material de construção e prevenção de incêndio para aquisição de produtos
necessários à execução de serviços urgentes, por meio de entrega em domicílio e/ou como ponto
de coleta;
X – serviços essenciais à saúde, como médicos, clínicas, hospitais, laboratórios e demais
estabelecimentos relacionados à prestação de serviços na área de saúde;
XI – serviços de abastecimento de água, gás, saneamento, coleta de lixo, energia,
telecomunicações e internet;
XII – clínicas e os hospitais veterinários e assistência a animais;
XIII – lavanderias;
XIV – bancos e serviços financeiros, inclusive lotérica;
XV – serviços de segurança, limpeza, higienização, vigilância e funerários;
XVI – hotéis e pousadas, com atendimento restrito aos hóspedes;
XVII – serviços de manutenção predial e prevenção de incêndio;
XVIII – serviços de transporte, armazenamento de mercadorias e centrais de distribuição, para
assegurar a regular atividade dos estabelecimentos cujo funcionamento não esteja suspenso;
XIX – estabelecimentos industriais e logísticos, bem como os serviços de transporte,
armazenamento e distribuição de seus insumos, equipamentos e produtos;
GOVERNO DO ESTADO DE PERNAMBUCO
F:\Decretos\2020\Procuradoria Geral do Estado – PGE\Proc_1991-DEF.doc
XX – oficinas de manutenção e conserto de máquinas e equipamentos para indústrias e atividades
essenciais previstas neste Decreto, veículos leves e pesados, e, em relação a estes, a
comercialização e serviços associados de peças e pneumáticos;
XXI – em relação à construção civil:
a) atividades urgentes, assim consideradas aquelas que tenham de ser executadas imediatamente,
sob pena de risco grave e imediato ou de difícil reparação;
b) atividades decorrentes de contratos de obras particulares que estejam relacionadas a atividades
essenciais previstas neste Decreto;
c) atividades decorrentes de contratos de obras públicas; e
d) atividades prestadas por concessionários de serviços públicos;
XXII – em relação ao transporte intermunicipal de passageiros:
a) transporte mediante fretamento de funcionários e colaboradores relacionados às indústrias e
atividades essenciais previstas neste Decreto, e o transporte de saída de hóspedes dos meios de
hospedagem para o aeroporto e terminais rodoviários;
b) transporte complementar de passageiros, autorizado em caráter excepcional pela autoridade
municipal competente, mediante formulário específico disponibilizado no site da Empresa
Pernambucana de Transporte Intermunicipal – EPTI, vedada a circulação na Região Metropolitana
do Recife; e
c) transporte regular de passageiros, restrito aos servidores públicos e aos funcionários e
colaboradores relacionados às indústrias e atividades essenciais previstas neste Decreto,
utilizando-se para essa finalidade até 10% (dez por cento) da frota, podendo esse percentual ser
alterado por ato específico do Diretor Presidente da EPTI;
XXIII – serviços urgentes de advocacia;
XXIV – restaurantes para atendimento exclusivo a caminhoneiros, sem aglomeração;
XXV – lojas de material de informática, por meio de entrega em domicílio e/ou como ponto de
coleta;
XXVI – serviço de assistência técnica de eletrodomésticos e equipamentos de informática;
XXVII – preparação, gravação e transmissão de aulas pela internet ou por TV aberta, e o
planejamento de atividades pedagógicas, em estabelecimentos de ensino;
XXVIII – processamento de dados ligados a serviços essenciais;
XXIX – serviços de cuidado e atenção a idosos, pessoas com deficiência e/ou dificuldade de
locomoção e do grupo de risco, realizados em domicílio ou em instituições destinadas a esse fim;
GOVERNO DO ESTADO DE PERNAMBUCO
F:\Decretos\2020\Procuradoria Geral do Estado – PGE\Proc_1991-DEF.doc
XXX – serviços de limpeza, portaria e de zeladoria em condomínios, estabelecimentos comerciais,
entidades associativas e similares;
XXXI – serviços de entrega em domicílio;
XXXII – imprensa; e
XXXIII – estabelecimentos de aviamentos e de tecidos, exclusivamente para o fornecimento dos
insumos necessários à fabricação de máscaras e outros Equipamentos de Proteção Individual –
EPI`s relacionados ao enfrentamento do coronavírus.
'''


# In[1523]:


#serviçõs essenciais
#https://www.folhape.com.br/noticias/decreto-estabelece-as-atividades-essenciais-em-pernambuco-confira/174526/
#https://www.diariodepernambuco.com.br/noticia/economia/2021/03/confira-a-lista-de-servicos-essenciais-que-funcionarao-nos-finais-de-s.html
#https://radiojornal.ne10.uol.com.br/noticia/2021/02/26/servicos-essenciais-o-que-pode-e-o-que-nao-pode-abrir-entre-22h-e-5h-em-pernambuco-a-partir-deste-sabado-27-204858
#https://jc.ne10.uol.com.br/pernambuco/2021/05/12127658-novo-decreto-amplia-lista-de-servicos-essenciais-em-pernambuco-confira.html


# In[1524]:


#https://radiojornal.ne10.uol.com.br/noticia/2021/02/26/servicos-essenciais-o-que-pode-e-o-que-nao-pode-abrir-entre-22h-e-5h-em-pernambuco-a-partir-deste-sabado-27-204858


# In[1525]:


'''
ATIVIDADES ESSENCIAIS

I – serviços públicos municipais, estaduais e federais, inclusive os outorgados ou delegados, 
realizados necessariamente de forma presencial, nos âmbitos dos Poderes Executivo, Legislativo e Judiciário, 
dos Ministérios Públicos e dos Tribunais de Contas; 

X – serviços essenciais à saúde, como médicos, clínicas, hospitais, 
laboratórios e demais estabelecimentos relacionados à prestação de serviços na área de saúde, 
observados os termos da Portaria SES nº 107, de 23 de março de 2020, podendo ainda serem disciplinados 
em outras normas regulamentares editadas pelo Secretário Estadual de Saúde; 

XV – serviços funerários; 

XVI – hotéis e pousadas, incluídos os restaurantes, e afins localizados em suas dependências, 
com atendimento restrito aos hóspedes; 

XXIX – serviços de auxílio, cuidado e atenção a idosos, pessoas com deficiência e/ou dificuldade de 
locomoção e do grupo de risco, realizados em domicílio ou em instituições destinadas a esse fim; 

XXX – serviços de segurança, limpeza, vigilância, portaria e zeladoria em estabelecimentos públicos e privados, 
condomínios, entidades associativas e similares; 

XXXI – serviços de entrega em domicílio de qualquer mercadoria ou produto; 

XXXIV – restaurantes, lanchonetes e similares localizados em unidades hospitalares e de atendimento à saúde e no aeroporto, 
desde que destinados exclusivamente ao atendimento de profissionais da saúde, pacientes e acompanhantes, e passageiros, 
respectivamente; 

XXXV – restaurantes, lanchonetes e similares em geral, exclusivamente como ponto de coleta e entrega em domicílio; 

XXXVI – serviços de assistência social e atendimento à população em estado de vulnerabilidade; 

XXXVII – atividades de preparação, gravação e transmissão de missas, cultos e demais celebrações religiosas 
pela internet ou por outros meios de comunicação, realizadas em igrejas, templos ou outros locais apropriados;

XXXVIII – serviços de auxílio e cuidados prestados a crianças filhas de profissionais de saúde e segurança pública, 
que necessitam se ausentar de casa para trabalhar.” 
'''


# ## Preparing the variables  

# In[1526]:


organizeddataPE.shape


# In[1527]:


organizeddataPEIBGE.shape


# In[1528]:


organizeddataPECBO.shape


# In[1529]:


organizeddataPECNAE.shape


# In[1530]:


organizeddataPE.head(3)


# In[1531]:


organizeddataPE['Age']


# In[1532]:


organizeddataPE['Age 2']


# In[1533]:


organizeddataPE['Men']


# In[1534]:


organizeddataPE['Non-white']


# In[1535]:


organizeddataPE['Uninformed race']


# In[1536]:


organizeddataPE['Complete primary education']


# In[1537]:


organizeddataPE['Complete secondary education']


# In[1538]:


organizeddataPE['Complete higher education']


# In[1539]:


organizeddataPE['Metropolitan region']


# In[1540]:


organizeddataPE['Minimum Wage']


# In[1541]:


organizeddataPE['Final Result']


# In[1542]:


'''
Y = Final Result
Xs For all 3 models 

Age
Age 2
Men
Non-white
Uninformed race
Complete primary education
Complete secondary education
Complete higher education
Metropolitan region
Minimum Wage
'''


# ## Model 1 IBGE Subsector

# In[1543]:


'''
Y = Final Result
Xs For all 3 models 

Age
Age 2
Men
Non-white
Uninformed race
Complete primary education
Complete secondary education
Complete higher education
Metropolitan region
Minimum Wage
'''


# In[1544]:


organizeddataPE.shape


# In[1545]:


organizeddataPE.head(3)


# In[1546]:


organizeddataPE['IBGE Subsector'].unique()


# In[1547]:


list(organizeddataPE['IBGE Subsector'].unique())


# In[1548]:


'''
Y = Final Result
Xs For all 3 models 

Age
Age 2
Men
Non-white
Uninformed race
Complete primary education
Complete secondary education
Complete higher education
Metropolitan region
Minimum Wage

For model 1 aditional Xs
'Public Administration',
 'Communication Accommodation',
 'Retail trade',
 'Other activities',
 'Human health activities',
 'Professional Technical Administration',
 'Construction',
 'Wholesale',
 'Food and Drink',
 'Education',
 'Transport and Communication'

'''


# In[1549]:


#see medium article to run the model


# In[1550]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)


# In[1551]:


organizeddataPE.shape


# In[1552]:


organizeddataPE.head(3)


# In[1553]:


organizeddataPE['Final Result'].value_counts()


# In[1554]:


organizeddataPE['Final Result'].value_counts(normalize=True)


# In[1555]:


organizeddataPE.groupby('Final Result').mean()


# In[1556]:


organizeddataPE.groupby('agecohort').mean()


# In[1557]:


get_ipython().run_line_magic('matplotlib', 'inline')
pd.crosstab(organizeddataPE['agecohort'],organizeddataPE['Final Result']).plot(kind='bar')
plt.title('Covid Cases Frequency for Age Cohort')
plt.xlabel('Age Cohort')
plt.ylabel('Frequency of Covid Cases')
#plt.savefig('purchase_fre_job');


# In[1558]:


table=pd.crosstab(organizeddataPE['schooling'],organizeddataPE['Final Result'])
table.div(table.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.title('Stacked Bar Chart of Schooling vs Covid Cases')
plt.xlabel('Schooling')
plt.ylabel('Proportion of Covid Cases')
plt.margins(0.5)
#plt.savefig('mariral_vs_pur_stack');


# In[1559]:


#if the bars in the graph are very even it might not becase a good predictor of the outcome, otherwise, it might


# In[1560]:


organizeddataPE['agecohort']


# In[1561]:


organizeddataPE['agecohort'].hist()
plt.title('Histogram of Age')
plt.xlabel('Age Cohort')
plt.ylabel('Frequency')
#plt.savefig('hist_age')


# In[1562]:


organizeddataPE[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage']]


# In[1563]:


organizeddataPE['Men'].unique()


# In[1564]:


organizeddataPE['Metropolitan region'].unique()


# In[1565]:


organizeddataPE[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage']].dtypes


# In[1566]:


#pip install imblearn


# In[1567]:


organizeddataPE['Final Result']


# In[1568]:


#organizeddataPE.rename({'Final Result':'Covid'},axis=1,inplace=True)


# In[1569]:


#organizeddataPE.rename({'Covid':'y'},axis=1,inplace=True)


# In[1570]:


organizeddataPE.head(3)


# In[1571]:


#organizeddataPE['Other activities']


# In[1572]:


organizeddataPE.shape


# ## organizeddataPEIBGE data

# In[1573]:


organizeddataPEIBGE.shape


# In[1574]:


organizeddataPEIBGE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[1575]:


organizeddataPEIBGE['y']


# In[1576]:


organizeddataPEIBGE.head(3)


# In[1577]:


organizeddataPEIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]


# In[1578]:


pd.set_option('display.max_rows',23)


# In[1579]:


organizeddataPEIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']].dtypes


# In[1580]:


#os_data_X,os_data_y=os.fit_resample(X_train.values, y_train.ravel())     this line is different from the article, 
#actually I did not need to use the line above after the column with same name as 'Education' and 'Construction' was fixed
#instead of keeping the same data I used 3 different data IBGE, CBO, CNAE

#in order for it to work, after many errors


# In[1581]:


X = organizeddataPEIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]
y = organizeddataPEIBGE['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1582]:


#https://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.RFE.html


# In[1583]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1584]:


#the false should be removed according to Recursive Feature Elimination (RFE) and the order of the columns are in X


# In[1585]:


X


# In[1586]:


organizeddataPEIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]


# In[1587]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']


# In[1588]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1589]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1590]:


#19,5% almost 20%, see another variable, if the variable increase the pseudo R for this case, it might be good to alter the 
#other cases

#adding White it went to 22.5%, which is a good fit


# In[1591]:


'''
What is a good pseudo R-squared in logistic regression?
For example, values of 0.2 to 0.4 for ρ2 represent EXCELLENT fit." So basically, 
ρ2 can be interpreted like R2, but don't expect it to be as big. And values from 0.2-0.4 indicate
(in McFadden's words) excellent model fit.
'''


# In[1592]:


#https://stats.stackexchange.com/questions/82105/mcfaddens-pseudo-r2-interpretation


# In[1593]:


#https://eml.berkeley.edu/~mcfadden/travel.html


# ## Model 2 CBO Main SubGroup Name 2002 with Others

# In[1594]:


organizeddataPECBO.shape


# In[1595]:


organizeddataPEIBGE.head(3)


# In[1596]:


organizeddataPECBO.rename({'Final Result':'y'},axis=1,inplace=True)


# In[1597]:


organizeddataPECBO['y']


# In[1598]:


organizeddataPECBO.head(3)


# In[1599]:


organizeddataPECBO.rename({'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Middle Level Technicians in Biological, Biochemical, Health And Related Scis','Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences':'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis'},axis=1,inplace=True)


# In[1600]:


organizeddataPECBO.columns


# In[1601]:


organizeddataPECBO[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]


# In[1602]:


pd.set_option('display.max_rows',27)


# In[1603]:


organizeddataPECBO[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']].dtypes


# In[1604]:


organizeddataPECBO.columns


# In[1605]:


X = organizeddataPECBO[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]



y = organizeddataPECBO['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1606]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1607]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']


# In[1608]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1609]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1610]:


#25,4% good fit for pseudo R2 according to McFaden


# ## Model 3 CNAE 2.0 Section Name

# In[1611]:


organizeddataPECNAE.shape


# In[1612]:


organizeddataPECNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[1613]:


organizeddataPECNAE.columns


# In[1614]:


organizeddataPECNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]


# In[1615]:


#pd.set_option('display.max_rows',None)


# In[1616]:


organizeddataPECNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']].dtypes


# In[1617]:


#For the Xs 
#I did not include
#'Arts, Culture, Sports And Recreation'
#'Real Estate Activities'
#'Financial, Insurance And Related Services Activities'
#'Domestic Services'


# In[1618]:


#'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial', 'Insurance And Related Services Activities','Domestic Services'


# In[1619]:


#I got rid of Age 2 to see if the model gets better, I should try to add other variables that might incluence y to increase 
#pseudo R squared, removing Age 2 it got worse


# In[1620]:


'''
I removed Domestic Services because it had a non significant p value
'''


# In[1621]:


organizeddataPECNAE.head(3)


# In[1622]:


#I added White


# In[1623]:


#I added Incomplete primary education, then I removed


# In[1624]:


organizeddataPECNAE['condicoes'].unique()


# In[1625]:


X = organizeddataPECNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]
y = organizeddataPECNAE['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1626]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1627]:


#I will get rid of the falses column to see what happens, if done, pseudo R squared gets worse
#what fixed it was this 
#y = y.astype('int64')


# In[1628]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction',
       'Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
     'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
     'No Working Days','Working hours','Job tenure','Distance to CBD']


# In[1629]:


#I did not include
#'Arts, Culture, Sports And Recreation'
#'Real Estate Activities'
#'Financial, Insurance And Related Services Activities'
#'Domestic Services'


# In[1630]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1631]:


y = y.astype('int64') #for this cases the astype of uint8 or int64 won't alter the pseudo R 2


# In[1632]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1633]:


#the results are not very good, redo and see how it behaves, maybe with only very few occupations, activities, essencial activities


# In[1634]:


#increasing No Working Days and Distance to CBD inscreased pseudo R2 to 12%, over 20% is ok according to mcfaden, see article
#citation

#putting back all CNAE divisions besides Domestic Services, increased the pseudo R squared to 14,4%


# In[1635]:


#see some variable to get it over 20%, according to McFadden above 20% is a good fit, between 20%-40%


# In[1636]:


#adding white it increased to 16,8% almost there
#I add Incomplete primary education it increased to 17,5%


# In[1637]:


#adding working hours it's 19,8% almost
#adding job tenure (tempo emprego, how long you stay at a job) it's 23,4% nice


# In[1638]:


#do the same for cbo and ibge sector as I did the alterations for CNAE, see what can be done to death data


# ## Doing for death just to check what happens although it's extremely uneven 300 deaths out of 200k rows

# In[1639]:


organizeddataPE.shape


# In[1640]:


organizeddataPE.head(3)


# In[1641]:


organizeddataPE['disease evolution'].unique()


# In[1642]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1643]:


pd.set_option('display.max_rows',10)


# In[1644]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']


# In[1645]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].unique()


# In[1646]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].value_counts()


# In[1647]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1648]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].isna().sum()


# In[1649]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['disease evolution'])


# In[1650]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1651]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].isna().sum()


# In[1652]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].value_counts()


# In[1653]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'] = bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']


# In[1654]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'] = bancoesusalltabsrais2019morelatlongcepestabselected1['death'].replace('healed','0').replace('recovered','0').replace('in home treatment','0').replace('hospitalized isolation bed','0').replace('death','1').replace('home isolation','0').replace('hospitalized ICU','0')


# In[1655]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'].unique()


# In[1656]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'] = bancoesusalltabsrais2019morelatlongcepestabselected1['death'].astype('uint8')


# In[1657]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'].dtype


# In[1658]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1659]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'].value_counts()


# In[1660]:


bancoesusalltabsrais2019morelatlongcepestabselected1['death'].value_counts(normalize=True)


# In[1661]:


#0.2%


# In[1662]:


bancoesusalltabsrais2019morelatlongcepestabselected1.rename({'Escolaridade após 2005':'School Years', 'Vl Remun Média (SM)':'Minimum Wage','Qtd Dias Afastamento':'No Working Days','sex':'Sex'}, axis = 1, inplace = True)


# In[1663]:


bancoesusalltabsrais2019morelatlongcepestabselected1['No Working Days']


# In[1664]:


bancoesusalltabsrais2019morelatlongcepestabselected1['idade']


# In[1665]:


bancoesusalltabsrais2019morelatlongcepestabselected1.rename({'idade':'age'}, axis=1, inplace=True)


# In[1666]:


bancoesusalltabsrais2019morelatlongcepestabselected1['age']


# In[1667]:


bancoesusalltabsrais2019morelatlongcepestabselected1['age']**2


# In[1668]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Age 2'] = bancoesusalltabsrais2019morelatlongcepestabselected1['age']**2


# In[1669]:


bancoesusalltabsrais2019morelatlongcepestabselected1.rename({'age':'Age'}, axis=1, inplace=True)


# In[1670]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1671]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[1672]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Sex'].unique()


# In[1673]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Sex'].value_counts()


# In[1674]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Sex'].value_counts(normalize=True)


# In[1675]:


bancoesusalltabsrais2019morelatlongcepestabselected1.rename({'Sex':'Men'},axis=1, inplace = True)


# In[1676]:


bancoesusalltabsrais2019morelatlongcepestabselected1['race']


# In[1677]:


bancoesusalltabsrais2019morelatlongcepestabselected1['race'].value_counts()


# In[1678]:


bancoesusalltabsrais2019morelatlongcepestabselected1['race'].value_counts(normalize=True)


# In[1679]:


bancoesusalltabsrais2019morelatlongcepestabselected1['race'].isna().sum()


# In[1680]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['race'])


# In[1681]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'] = bancoesusalltabsrais2019morelatlongcepestabselected1['race']


# In[1682]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored']  = bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'] .replace('Brown','Non-white').replace('Yellow','Non-white').replace('Black','Non-white').replace('Indigenous','Non-white').replace('Ignored','Uninformed race')


# In[1683]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'].unique()


# In[1684]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'].value_counts()


# In[1685]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'].value_counts(normalize=True)


# In[1686]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.concat([bancoesusalltabsrais2019morelatlongcepestabselected1, pd.get_dummies(bancoesusalltabsrais2019morelatlongcepestabselected1['Non-white/Ignored'])],axis=1)


# In[1687]:


bancoesusalltabsrais2019morelatlongcepestabselected1.rename({'Non-White/Ignored_Non-white':'Non-white', 'Non-White/Ignored_Uninformed race':'Uninformed race'},axis=1, inplace=True)


# In[1688]:


bancoesusalltabsrais2019morelatlongcepestabselected1['schooling'].unique()


# In[1689]:


bancoesusalltabsrais2019morelatlongcepestabselected1['schooling'].value_counts()


# In[1690]:


bancoesusalltabsrais2019morelatlongcepestabselected1['schooling'].value_counts(normalize=True)


# In[1691]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.concat([bancoesusalltabsrais2019morelatlongcepestabselected1, pd.get_dummies(bancoesusalltabsrais2019morelatlongcepestabselected1['schooling'])],axis=1)


# In[1692]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1693]:


#RMR
'''
Aracoiaba, Igarassu, Itapissuma, Ilha de Itamaraca,
Abreu e Lima, Paulista, Olinda, Camaragibe, Recife, Jaboatao dos Guararapes, Sao
Lourenco da Mata, Moreno, Cabo de Santo Agostinho e Ipojuca
'''


# In[1694]:


replacers = {'Frei Miguelinho':'0', 'Santa Maria Do Cambuca':'0', 'Surubim':'0', 'Caruaru':'0',
       'Jatauba':'0', 'Altinho':'0', 'Araripina':'0', 'Toritama':'0', 'Bonito':'0',
       'Vertentes':'0', 'Jurema':'0', 'Taquaritinga Do Norte':'0', 'Sao Caitano':'0',
       'Gravata':'0', 'Cha Grande':'0', 'Brejo Da Madre De Deus':'0', 'Ibirajuba':'0',
       'Bezerros':'0', 'Riacho Das Almas':'0', 'Agrestina':'0', 'Igarassu':'1', 'Cumaru':'0',
       'Jaboatao Dos Guararapes':'1', 'Pesqueira':'0', 'Recife':'1', 'Camaragibe':'1',
       'Santa Cruz Do Capibaribe':'0', 'Barra De Guabiraba':'0',
       'Camocim De Sao Felix':'0', 'Feira Nova':'0', 'Paulista':'1', 'Palmares':'0',
       'Carpina':'0', 'Panelas':'0', 'Tabira':'0', 'Abreu E Lima':'1', 'Belem De Maria':'0',
       'Cupira':'0', 'Catende':'0', 'Sao Bento Do Una':'0', 'Garanhuns':'0', 'Goiana':'0',
       'Sao Joaquim Do Monte':'0', 'Lajedo':'0', 'Ipojuca':'1', 'Escada':'0', 'Limoeiro':'0',
       'Cachoeirinha':'0', 'Pombos':'0', 'Vitoria De Santo Antao':'0', 'Belo Jardim':'0',
       'Cabo De Santo Agostinho':'1', 'Sao Lourenco Da Mata':'1', 'Casinhas':'0',
       'Lagoa De Itaenga':'0', 'Olinda':'1', 'Belem Do Sao Francisco':'0', 'Condado':'0',
       'Petrolina':'0', 'Iguaracy':'0', 'Itaquitinga':'0', 'Serra Talhada':'0', 'Triunfo':'0',
       'Nazare Da Mata':'0', 'Moreno':'1', 'Flores':'0', 'Ilha De Itamaraca':'1',
       'Arcoverde':'0', 'Pocao':'0', 'Joao Alfredo':'0', 'Ouricuri':'0',
       'Afogados Da Ingazeira':'0', 'Salgueiro':'0', 'Passira':'0', 'Saire':'0',
       'Sao Joao':'0', 'Itapissuma':'1', 'Ribeirao':'0', 'Vicencia':'0', 'Brejinho':'0',
       'Paudalho':'0', 'Lagoa Do Carro':'0', 'Macaparana':'0', 'Alianca':'0',
       'Bom Jardim':'0', 'Gloria Do Goita':'0', 'Cha De Alegria':'0', 'Aracoiaba':'1',
       'Jaqueira':'0', 'Sanharo':'0', 'Sao Jose Da Coroa Grande':'0', 'Timbauba':'0',
       'Orobo':'0', 'Camutanga':'0', 'Cabrobo':'0', 'Amaraji':'0', 'Tamandare':'0',
       'Salgadinho':'0', 'Gameleira':'0', 'Angelim':'0', 'Itapetim':'0', 'Oroco':'0',
       'Lagoa Grande':'0', 'Exu':'0', 'Petrolandia':'0', 'Machados':'0', 'Caetes':'0',
       'Cortes':'0', 'Bom Conselho':'0', 'Venturosa':'0', 'Canhotinho':'0', 'Jupi':'0',
       'Jucati':'0', 'Sao Jose Do Egito':'0', 'Saloa':'0', 'Solidao':'0', 'Carnaiba':'0',
       'Tuparetama':'0', 'Santa Cruz Da Baixa Verde':'0', 'Ingazeira':'0',
       'Terezinha':'0', 'Lagoa Dos Gatos':'0', 'Tracunhaem':'0', 'Sao Vicente Ferrer':'0',
       'Correntes':'0', 'Itambe':'0', 'Paranatama':'0', 'Brejao':'0', 'Itaiba':'0', 'Buique':'0',
       'Alagoinha':'0', 'Rio Formoso':'0', 'Sao Jose Do Belmonte':'0', 'Floresta':'0',
       'Santa Cruz':'0', 'Calumbi':'0', 'Mirandiba':'0', 'Afranio':'0', 'Capoeiras':'0',
       'Sertania':'0', 'Betania':'0', 'Terra Nova':'0', 'Ibimirim':'0', 'Custodia':'0',
       'Carnaubeira Da Penha':'0', 'Tupanatinga':'0', 'Pedra':'0', 'Tacaimbo':'0',
       'Santa Terezinha':'0', 'Sao Benedito Do Sul':'0', 'Vertente Do Lerio':'0',
       'Aguas Belas':'0', 'Agua Preta':'0', 'Barreiros':'0', 'Xexeu':'0',
       'Joaquim Nabuco':'0', 'Primavera':'0', 'Fernando De Noronha':'0',
       'Buenos Aires':'0', 'Ferreiros':'0', 'Sirinhaem':'0', 'Trindade':'0',
       'Santa Maria Da Boa Vista':'0', 'Dormentes':'0', 'Serrita':'0', 'Verdejante':'0',
       'Parnamirim':'0', 'Bodoco':'0', 'Ipubi':'0', 'Jatoba':'0', 'Tacaratu':'0',
       'Santa Filomena':'0', 'Quixaba':'0', 'Inaja':'0', 'Maraial':'0', 'Manari':'0',
       'Quipapa':'0', 'Itacuruba':'0', 'Iati':'0', 'Moreilandia':'0', 'Calcado':'0',
       'Lagoa Do Ouro':'0', 'Palmeirina':'0', 'Granito':'0'} 
bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].replace(replacers)


# In[1695]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].unique()


# In[1696]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].replace('Cedro','0')


# In[1697]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].unique()


# In[1698]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].value_counts()


# In[1699]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].value_counts(normalize=True)


# In[1700]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1701]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Minimum Wage']


# In[1702]:


bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Metropolitan region'].astype('uint8')
bancoesusalltabsrais2019morelatlongcepestabselected1['Men'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Men'].astype('uint8')


# In[1703]:


#all lats and long are outside the shapefile, do that again


# In[1704]:


#checking gdf and geodataframe again


# In[1705]:


gdf['NM_MUN'].nunique()


# In[1706]:


geodataframe['municipio'].nunique()


# In[1707]:


crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'], bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'])]
geometry[:5]


# In[1708]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[1709]:


geodataframe = gpd.GeoDataFrame(bancoesusalltabsrais2019morelatlongcepestabselected1, crs = crs, geometry = geometry)
geodataframe.head()


# In[1710]:


geodataframe.shape


# In[1711]:


gdf.shape


# In[1712]:


gpd.sjoin(geodataframe, gdf, op='within')


# In[1713]:


latlonginsidepewithdummies = gpd.sjoin(geodataframe, gdf, op='within')


# In[1714]:


latlonginsidepewithdummies.shape


# In[1715]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsidepewithdummies.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE', fontsize = 18,pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[1716]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)


# In[1717]:


start_lat, start_lon = -8.0617353, -34.8706873


# In[1718]:


distances_km=[]
for row in latlonginsidepewithdummies.itertuples(index=False):
    distances_km.append(
    haversine_distance(start_lat,start_lon,row.latitude,row.longitude)
    ) 


# In[1719]:


latlonginsidepewithdummies['distancefrommarcozero']=distances_km


# In[1720]:


latlonginsidepewithdummies.head(3)


# In[1721]:


latlonginsidepewithdummies.shape


# In[1722]:


latlonginsidepewithdummies['distancefrommarcozero'].describe()


# In[1723]:


latlonginsidepewithdummies.rename({'distancefrommarcozero':'Distance to CBD'},axis=1,inplace=True)


# In[1724]:


latlonginsidepewithdummies.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[1725]:


latlonginsidepewithdummies['Tempo Emprego'].unique()


# In[1726]:


latlonginsidepewithdummies['Tempo Emprego'].describe()


# In[1727]:


latlonginsidepewithdummies['Tempo Emprego'] = latlonginsidepewithdummies['Tempo Emprego'].str.replace(',','.')


# In[1728]:


latlonginsidepewithdummies['Tempo Emprego'] = latlonginsidepewithdummies['Tempo Emprego'].str.lstrip('0')


# In[1729]:


latlonginsidepewithdummies.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[1730]:


latlonginsidepewithdummies['Job tenure'] = latlonginsidepewithdummies['Job tenure'].astype(float)


# In[1731]:


latlonginsidepewithdummies['Job tenure'].unique()


# In[1732]:


latlonginsidepewithdummies['Job tenure'].describe()


# ## latlonginsidepewithdummiesIBGE

# In[1733]:


latlonginsidepewithdummiesIBGEdeath = pd.concat([latlonginsidepewithdummies, pd.get_dummies(latlonginsidepewithdummies['IBGE Subsector'])],axis=1)


# In[1734]:


#latlonginsidepewithdummies was already with death, but to make sure I remember that, Inamed the below and other variables with death


# In[1735]:


latlonginsidepewithdummiesIBGEdeath.head(3)


# In[1736]:


latlonginsidepewithdummiesIBGEdeath.shape


# In[1737]:


latlonginsidepewithdummiesIBGEdeath.rename({'death':'y'},axis=1,inplace=True)


# In[1738]:


latlonginsidepewithdummiesIBGEdeath['y']


# In[1739]:


#I removed Age 2 because the logit model had problems, the inf is not that I added again


# In[1740]:


latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].dtypes


# In[1741]:


'''
latlonginsidepewithdummies['Men'] = latlonginsidepewithdummies['Men'].astype('int64')
latlonginsidepewithdummies['Non-white'] = latlonginsidepewithdummies['Non-white'].astype('int64')
latlonginsidepewithdummies['Uninformed race'] = latlonginsidepewithdummies['Uninformed race'].astype('int64')
latlonginsidepewithdummies['Complete primary education'] = latlonginsidepewithdummies['Complete primary education'].astype('int64')
latlonginsidepewithdummies['Complete secondary education'] = latlonginsidepewithdummies['Complete secondary education'].astype('int64')
latlonginsidepewithdummies['Complete higher education'] = latlonginsidepewithdummies['Complete higher education'].astype('int64')
latlonginsidepewithdummies['Metropolitan region'] = latlonginsidepewithdummies['Metropolitan region'].astype('int64')
latlonginsidepewithdummies['Public Administration'] = latlonginsidepewithdummies['Public Administration'].astype('int64')
latlonginsidepewithdummies['Communication Accommodation'] = latlonginsidepewithdummies['Communication Accommodation'].astype('int64')
latlonginsidepewithdummies['Retail trade'] = latlonginsidepewithdummies['Retail trade'].astype('int64')
latlonginsidepewithdummies['Other activities'] = latlonginsidepewithdummies['Other activities'].astype('int64')
latlonginsidepewithdummies['Human health activities'] = latlonginsidepewithdummies['Human health activities'].astype('int64')
latlonginsidepewithdummies['Professional Technical Administration'] = latlonginsidepewithdummies['Professional Technical Administration'].astype('int64')
latlonginsidepewithdummies['Construction'] = latlonginsidepewithdummies['Construction'].astype('int64')
latlonginsidepewithdummies['Wholesale'] = latlonginsidepewithdummies['Wholesale'].astype('int64')
latlonginsidepewithdummies['Food and Drink'] = latlonginsidepewithdummies['Food and Drink'].astype('int64')
latlonginsidepewithdummies['Education'] = latlonginsidepewithdummies['Education'].astype('int64')
latlonginsidepewithdummies['Transport and Communication'] = latlonginsidepewithdummies['Transport and Communication'].astype('int64')
'''
#changing dtype to int64 did not fix the inf in the logit regression


# In[1742]:


latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].corr()


# In[1743]:


latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].describe()


# In[1744]:


#removing complete higher education to see the the maximum likelihood converges
#before, Age 2 was removed (because of singular matrix error) and put back  (to see what would happen), 
#the results and notes after the model are below


# In[1745]:


latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education'
      ,'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']]


# In[1746]:


X = latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education'
      ,'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']]
y = latlonginsidepewithdummiesIBGEdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1747]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1748]:


#removing complete higher education to see the the maximum likelihood converges


# In[1749]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education'
      ,'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']


# In[1750]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1751]:


y = y.astype('int64')
#the y had dtype changed to int64, because the error can not divide by zero, etc


# In[1752]:


y.unique()


# In[1753]:


y


# In[1754]:


pd.set_option('display.max_rows',22)


# In[1755]:


latlonginsidepewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].dtypes


# In[1756]:


'''
bancoesusalltabsrais2019morelatlongcepestabselected1['Age'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Age'].astype(np.float128)
bancoesusalltabsrais2019morelatlongcepestabselected1['Age 2'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Age'].astype(np.float128)
bancoesusalltabsrais2019morelatlongcepestabselected1['Minimum Wage'] = bancoesusalltabsrais2019morelatlongcepestabselected1['Minimum Wage'].astype(np.float128)
'''


# In[1757]:


latlonginsidepewithdummiesIBGEdeath.columns


# In[1758]:


latlonginsidepewithdummiesIBGEdeath['disease evolution'].unique()


# In[1759]:


latlonginsidepewithdummiesIBGEdeath[latlonginsidepewithdummies['disease evolution']=='death'].shape


# In[1760]:


latlonginsidepewithdummies.shape


# In[1761]:


(230/158211)
#0,14%


# In[1762]:


latlonginsidepewithdummiesIBGEdeath.shape


# In[1763]:


#from scipy.special import expit, logit


# In[1764]:


#old_settings = np.seterr(all='print')
#np.geterr()


# In[1765]:


# use result=logit_model.fit_regularized()
# use result=logit_model.fit(method='bfgs')
#result=logit_model.fit(method='lbfgs')
#result=logit_model.fit(method='newton')
#result=logit_model.fit(method='nm')
#result=logit_model.fit_regularized(method='l1')
#logit_model=sm.Logit(endog=y,exog=X)


# In[1766]:


X.shape


# In[1767]:


X.head(3)


# In[1768]:


pd.set_option('display.max_rows',26)


# In[1769]:


X.corr()


# In[1770]:


X.describe()


# In[1771]:


pd.set_option('display.max_rows',30)


# In[1772]:


corr = X.corr() 
c1 = corr.unstack()
c1.sort_values(ascending = False)


# In[1773]:


corr = X.corr()
kot = corr[corr>=.9]
plt.figure(figsize=(12,8))
sns.heatmap(kot, cmap='Reds')
plt.title('Variables with Correlation > .9');


# In[1774]:


y.shape


# In[1775]:


y.head(3)


# In[1776]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X, REML = True)
result=logit_model.fit()
print(result.summary2())


# In[1777]:


#see error "Maximum Likelihood optimization failed to ", also the pseudo R2 is too high, this error was before the singular matrix
#before I turned y into int64


# In[1778]:


#put Singular matrix python on google

#it means that the matrix can not be inverted
#the determinant is zero

#see a way to deal with it

##this might happen because two columns might have perfect correlation = 1
#remove Age 2 might work because it's perfect correlated with Age, the Singular matrix error disappeared

#But why it only ran removing Age 2 this time, the other models that Age 2, and the same correlation problem, 
#but the error singular matrix did not disappeared

#but it now shows "Maximum likelihood optimization failed to"


# In[1779]:


#pseudo R-squared is high 79.6% 
#Complete higher education had very high p-value Metropolitan region
#remove it to see what happens


# In[1780]:


#search more about "Maximum Likelihood optimization failed to "


# the y values having a very high percentage of one category is making it difficult to converge, but the page talks about it as if was one of the X variables [here](https://stackoverflow.com/questions/32926299/how-to-fix-statsmodel-warning-maximum-no-of-iterations-has-exceeded)
# After I removed complete higher education to see if the maximum likelihood converges, it did converge. But the pseudo R2 is 
# very high 79.2%

# In[1781]:


#I put back Age 2, after having removed completed higher education, and it converged, although pseudo R2 went up to 81.4% 


# In[1782]:


#I'll put back Complete higher education just to make sure and remove it, again it resulted in singular matrix
#If Age 2 is removed it won't result into singular matrix, but there will be a maximum likelihood optimization failed to error
#if Age 2 is kept and Complete higher education is removed it converges without error, although the pseudo R2 is 81.4%
#without Age 2 and Complete higher education the pseudo R2 is 79.2%


# In[1783]:


#since this model has a very high pseudo R2, something else needs to be done, like not consider this model with death 


# ## latlonginsidepewithdummiesCBO

# In[1784]:


latlonginsidepewithdummies.columns


# In[1785]:


latlonginsidepewithdummies.head(3)


# In[1786]:


latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'].unique()


# In[1787]:


latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'].str.title().value_counts()


# In[1788]:


latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'] = latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'].str.title()


# In[1789]:


latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others']


# In[1790]:


pd.concat([latlonginsidepewithdummies,pd.get_dummies(latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[1791]:


latlonginsidepewithdummiesCBOdeath = pd.concat([latlonginsidepewithdummies,pd.get_dummies(latlonginsidepewithdummies['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[1792]:


latlonginsidepewithdummiesCBOdeath.rename({'death':'y'},axis=1,inplace=True)


# In[1793]:


latlonginsidepewithdummiesCBOdeath['y']


# In[1794]:


latlonginsidepewithdummiesCBOdeath.head(3)


# In[1795]:


latlonginsidepewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries']]


# In[1796]:


pd.set_option('display.max_rows',27)


# In[1797]:


latlonginsidepewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries']].dtypes


# In[1798]:


latlonginsidepewithdummiesCBOdeath.rename({'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Middle Level Technicians in Biological, Biochemical, Health And Rel Scis','Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences':'Middle Level Technicians In Physical, Chemical, Engineering And Rel Scis'},axis=1,inplace=True)


# In[1799]:


#latlonginsidepewithdummiesCBOdeath.rename({'Middle Level Technicians in Biological, Biochemical, Health And Related Scis':'Middle Level Technicians in Biological, Biochemical, Health And Rel Scis','Middle Level Technicians In Physical, Chemical, Engineering And Related Scis':'Middle Level Technicians In Physical, Chemical, Engineering And Rel Scis'},axis=1,inplace=True)


# In[1800]:


latlonginsidepewithdummiesCBOdeath.columns


# In[1801]:


latlonginsidepewithdummiesCBOdeath.shape


# In[1802]:


#Complete higher education was avoiding the model to converge, huge standard error, it was removed

#same thing for Workers In The Textile, Tanning, Clothing And Graphic Arts Industries


# In[1803]:


latlonginsidepewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Rel Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]


# In[1804]:


X = latlonginsidepewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Rel Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]



y = latlonginsidepewithdummiesCBOdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1805]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1806]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Rel Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']


# In[1807]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1808]:


y = y.astype('int64')


# In[1809]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1810]:


#pseudo R2 very big 84.2%, according to McFadden, it should be between 20% and 40%


# ## latlonginsidepewithdummiesCNAE

# In[1811]:


latlonginsidepewithdummies['CNAE 2.0 Section Name'].unique()


# In[1812]:


latlonginsidepewithdummies['CNAE 2.0 Section Name'].value_counts()


# In[1813]:


latlonginsidepewithdummies['CNAE 2.0 Section Name'] = latlonginsidepewithdummies['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[1814]:


latlonginsidepewithdummies['CNAE 2.0 Section Name'].value_counts()


# In[1815]:


latlonginsidepewithdummies['CNAE 2.0 Section Name'] = latlonginsidepewithdummies['CNAE 2.0 Section Name'].str.title()


# In[1816]:


latlonginsidepewithdummiesCNAEdeath = pd.concat([latlonginsidepewithdummies, pd.get_dummies(latlonginsidepewithdummies['CNAE 2.0 Section Name'])], axis = 1)


# In[1817]:


pd.Series(sorted(latlonginsidepewithdummiesCNAEdeath['CNAE 2.0 Section Name'].unique()))


# In[1818]:


latlonginsidepewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]


# In[1819]:


latlonginsidepewithdummiesCNAEdeath.rename({'death':'y'},axis=1,inplace=True)


# In[1820]:


latlonginsidepewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']].dtypes


# In[1821]:


#'Complete higher education' removing it because it had a singular matrix problem

#Real Estate Activities removing it because the standard error was huge and avoinding the model to converge

#Same thing for Extractive Industries


# In[1822]:


latlonginsidepewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]


# In[1823]:


X = latlonginsidepewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]
y = latlonginsidepewithdummiesCNAEdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[1824]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[1825]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction',
       'Education', 'Electricity And Gas','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
     'Arts, Culture, Sports And Recreation','Financial, Insurance And Related Services Activities',
     'No Working Days','Working hours','Job tenure','Distance to CBD']


# In[1826]:


X=os_data_X[cols]
y=os_data_y['y']


# In[1827]:


y = y.astype('int64')


# In[1828]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1829]:


#it converged but the pseudo R2 is very high 82.2%


# In[1830]:


#analysing death didn't even give a pseudo R-squared, with the positive cases I could add variables to see if
#the pseudo R-squared gets higher than 0.026 to 0.2-0.4


# In[1831]:


#fix the HessianInversionWarning: Inverting hessian failed, no bse or cov_params available
  #warnings.warn('Inverting hessian failed, no bse or cov_params '
    #with the death data


# In[1832]:


#run the models with unbalanced data, it's worse


# In[1833]:


#add variable that influences the models, need to see that


# ### Just testing with an example 

# In[1834]:


organizeddataPECNAE['No Working Days'].unique()


# In[1835]:


organizeddataPECNAE['Distance to CBD']


# In[1836]:


organizeddataPECNAE.head(3)


# In[1837]:


X = organizeddataPECNAE[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','No Working Days', 'Distance to CBD']]
y = organizeddataPECNAE['y']


# In[1838]:


X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.25,random_state=0)


# In[1839]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[1840]:


#add the other variables for death and see what happens

#https://stackoverflow.com/questions/40726490/overflow-error-in-pythons-numpy-exp-function
#https://stackoverflow.com/questions/46173061/statsmodels-throws-overflow-in-exp-and-divide-by-zero-in-log-warnings-and-ps


# In[1841]:


#try later to fix the inf on the pseudo R wit the death variable 
#maybe see Monte Carlo simulation for the death cases 
#myabe try to apply King and Zeng1 studied problems related to the statistical estimation of rare events on python


# ## All logit models for Recife

# In[1842]:


organizeddataRecife = pd.read_csv('organizeddatawithinRecifeshapefileborder.csv')


# In[1843]:


organizeddataRecife.shape


# In[1844]:


pd.set_option('display.max_columns',None)


# In[1845]:


organizeddataRecife.head(3)


# In[1846]:


organizeddataRecife.columns


# In[1847]:


organizeddataRecife['Qtd Dias Afastamento'].unique()


# In[1848]:


organizeddataRecife['Qtd Dias Afastamento'].describe()


# In[1849]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

organizeddataRecife['Days Not Working'] = pd.cut(organizeddataRecife['Qtd Dias Afastamento'], bins, labels=names)

print(organizeddataRecife.dtypes)


# In[1850]:


organizeddataRecife['Days Not Working'].unique()


# In[1851]:


organizeddataRecife['Days Not Working'].value_counts()


# In[1852]:


organizeddataRecife['Days Not Working'].isna().sum() 


# In[1853]:


organizeddataRecife['Qtd Dias Afastamento'].isna().sum()


# In[1854]:


organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[1855]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[1856]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype('category')


# In[1857]:


organizeddataRecife['Days Not Working'].dtype


# In[1858]:


organizeddataRecife.head(3)


# In[1859]:


organizeddataRecife['Days Not Working'].value_counts()


# In[1860]:


organizeddataRecife['Days Not Working'].isna().sum()


# ### Logit Model for Recife 

# In[1861]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt


# In[1862]:


organizeddataRecife['finalresult'].unique()


# In[1863]:


organizeddataRecife['finalresult'].value_counts()


# In[1864]:


organizeddataRecife['finalresult'].isna().sum()


# In[1865]:


organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[1866]:


organizeddataRecife = organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[1867]:


organizeddataRecife.shape


# In[1868]:


organizeddataRecife['finalresult'].unique()


# In[1869]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].replace('negative','0').replace('positive','1')


# In[1870]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].astype('uint8')


# In[1871]:


organizeddataRecife['finalresult'].value_counts()


# In[1872]:


organizeddataRecife['finalresult'].value_counts(normalize=True)


# In[1873]:


organizeddataRecife.columns


# In[1874]:


organizeddataRecife.rename({'Escolaridade após 2005':'School Years', 'Vl Remun Média (SM)':'Minimum Wage','Qtd Dias Afastamento':'No Working Days','sex':'Sex','finalresult':'Final Result','distancefrommarcozero':'Distance to CBD'}, axis = 1, inplace = True)


# In[1875]:


organizeddataRecife.groupby(by='agecohort').mean()


# In[1876]:


organizeddataRecife_agecohortmean = organizeddataRecife.groupby(by='agecohort').mean()


# In[1877]:


organizeddataRecife_agecohortmean = organizeddataRecife_agecohortmean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1878]:


organizeddataRecife_agecohortmean


# In[1879]:


organizeddataRecife_agecohortmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[1880]:


organizeddataRecife_agecohortsum = organizeddataRecife.groupby(by='agecohort').sum()


# In[1881]:


organizeddataRecife_agecohortsum


# In[1882]:


organizeddataRecife_agecohortsum = organizeddataRecife_agecohortsum.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1883]:


organizeddataRecife_agecohortsum


# In[1884]:


organizeddataRecife_agecohortsum.loc[:,{'Health Professionals','Security Professionals','Sex','Final Result'}]


# In[1885]:


organizeddataRecife_summean = organizeddataRecife.groupby('agecohort').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1886]:


organizeddataRecife_summean


# In[1887]:


organizeddataRecifeagecohort_summean = organizeddataRecife_summean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[1888]:


organizeddataRecifeagecohort_summean


# In[1889]:


organizeddataRecifeagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1890]:


organizeddataRecifeagecohort_summean.loc['Total'] = organizeddataRecifeagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1891]:


organizeddataRecifeagecohort_summean


# In[1892]:


organizeddataRecife.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1893]:


organizeddataRecifemeanminimumwage_summean = organizeddataRecife.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1894]:


organizeddataRecifemeanminimumwage_summean


# In[1895]:


organizeddataRecifemeanminimumwage_summean = organizeddataRecifemeanminimumwage_summean.reindex(['0.1 - 1/2', '1/2 - 1', '1 - 2','2 - 5','5 - 10', '10 - 20', '20+'])


# In[1896]:


organizeddataRecifemeanminimumwage_summean


# In[1897]:


organizeddataRecifemeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1898]:


organizeddataRecifemeanminimumwage_summean.loc['Total'] = organizeddataRecifemeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1899]:


organizeddataRecifemeanminimumwage_summean


# In[1900]:


organizeddataRecife.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1901]:


organizeddataRecife_racesummean = organizeddataRecife.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1902]:


organizeddataRecife_racesummean


# In[1903]:


organizeddataRecife_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1904]:


organizeddataRecife_racesummean.loc['Total'] = organizeddataRecife_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1905]:


organizeddataRecife_racesummean


# In[1906]:


organizeddataRecifeschooling_summean = organizeddataRecife.groupby('schooling').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2) 


# In[1907]:


organizeddataRecifeschooling_summean


# In[1908]:


organizeddataRecifeschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1909]:


organizeddataRecifeschooling_summean.loc['Total'] = organizeddataRecifeschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1910]:


organizeddataRecifeschooling_summean


# In[1911]:


organizeddataRecifedaysnotworing_summean = organizeddataRecife.groupby('Days Not Working').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1912]:


organizeddataRecifedaysnotworing_summean


# In[1913]:


organizeddataRecifedaysnotworing_summean = organizeddataRecifedaysnotworing_summean.reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+'])


# In[1914]:


organizeddataRecifedaysnotworing_summean


# In[1915]:


organizeddataRecifedaysnotworing_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1916]:


organizeddataRecifedaysnotworing_summean.loc['Total'] = organizeddataRecifedaysnotworing_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[1917]:


organizeddataRecifedaysnotworing_summean


# In[1918]:


organizeddataRecife.shape


# In[1919]:


organizeddataRecife.head(3)


# In[1920]:


#from the article


# In[1921]:


'''-> means adapting to my case

These models use the following logistic equation:              -> Use the same Logit Model 
g(π) = α + βxi , where:
(i) g(π) = Pr(Y = 1 | x), Y being the dummy variable
indicating death due to Covid-19;
(ii) α is the intercept;
(iii) xi is the vector of explanatory variables and;
(iv) β are the estimated coefficients.

The explanatory variables are:
(a) age and age squared;                                       -> age (leave it as it is, think more about age squared)

"In all models, age is statistically
significant with the expected sign. Furthermore, the growth
rate of this probability decreases as age increases, which is
represented by the negative sign in age squared."

(b) man;                                                       -> man (the column has already 1s for man and 0s for women)

as for the articles results, men die 

(c) race/ethnicity: dummy variable identifying non-white       -> dummy for non-white (make this dummy)   
people and another identifying those whose race/ethnicity
has not been declared in the RAIS;

(d) Education: dummy variables for individuals with complete    -> dummy for complete primary, secondary and high education
primary, secondary and higher education;      

OBS:the same as my categorical values except incomplete primary education, leave incomplete or get rid of it
Leaving incomplete primary education or not, there's the need to make the dummy


(e)Metropolitan region: dummy for establishments located        -> dummy for establishments in RMR (see about that)
in the Metropolitan Region of Rio de Janeiro;

OBS: A dummy could be made for establishments in Recife somehow
or maybe I could use the distance to CBD as a variable



(f) the logarithm of the average annual labor earnings of       -> I could use Vl Remun Média Nom
the individual in 2018;


(g) dummies for different types of occupation;

OBS: the article needs to especify these occupations



(h) dummy indicating vulnerable occupations: health, protective -> I have a column already for health and security professionals
and transport workers;



(i) dummies for economic activity of the company/organization
where the individual works;

OBS: the artcile needs to especify these economic activities



(j) dummy for essential activities: human health, public            -> Find the essential activies in CNAE activities
order and safety, freight transport, courier and support activities
for transportation, passenger transport, essential wholesale
and retail trade, and other essential services (Food and
beverage, banks, cleaning, funeral and others).


The economic activity and occupations variables were used
interchangeably in different models’ specifications, especially
due to the high correlation between some occupations and
certain economic activities.

The individual’s occupation was obtained from the Brazilian
Classification of Occupations (CBO), present in the RAIS
database, based on the International Standard Classification of
Occupations (ISCO-88), and aggregated into 19 groups.

The essential economic activities were defined according to        -> See the essentail economic activies by PE'rules and its division groups in cnae
theGovernment of Rio de Janeiro state’s rules. The economic
activities were divided into 13 groups of essential activities
and three groups of non-essential activities, organized
based on the Brazilian National Classification of Economic
Activities revision 2.0 (CNAE 2.0), which is based on
the International Standard Industrial Classification (ISIC,
rev. 4).



They used Monte-Carlo for rare events, like in the article 
King and Zeng because death would be a rara event
In my case is much worse, I will do for catching covid 
Then Monte Carlo might not be need

Model 1, 2, 3, 4 and 5 differ in occupation and economic activity variables not especified by the article

Model 1 -> in addition to the basic variables, the
individual occupation was included as an explanatory variable

Model 2 -> there is a dummy variable for essential
economic activities in addition to occupation.

Model 3 and 4 -> occupation variables were replaced by economic activities 

Model 4 -> a dummy was added
for vulnerable occupations.


The choice to use either occupation or
activity is because many occupations are concentrated in a few
activities, generating a very high correlation between these two
sets of variables.

Model 5 -> creates a
new aggregation of economic activities, based on the previous
one, but where health professionals in the public administration
were incorporated into the Human health activities, and protective workers in the public administration were shifted
to the public order safety activities.


In my case maybe do a separate model with Economic activities
On the article model 1 and 2 used occupations model 3,4 and 5 used economic activities

See Fig.1 on the article 
Search how to do odds ration in Python

'''


# ### articles explanatory variables now for Recife

# In[1922]:


#Age and Age 2


# In[1923]:


organizeddataRecife['idade']


# In[1924]:


organizeddataRecife.rename({'idade':'Age'}, axis=1, inplace=True)


# In[1925]:


organizeddataRecife['Age']


# In[1926]:


organizeddataRecife['Age']**2


# In[1927]:


organizeddataRecife['Age 2'] = organizeddataRecife['Age']**2


# In[1928]:


organizeddataRecife.head(3)


# In[1929]:


#Men


# In[1930]:


organizeddataRecife['Sex'].unique()


# In[1931]:


organizeddataRecife['Sex'].value_counts()


# In[1932]:


organizeddataRecife['Sex'].value_counts(normalize=True)


# In[1933]:


organizeddataRecife.rename({'Sex':'Men'},axis=1, inplace=True)


# In[1934]:


organizeddataRecife['Men'].dtype


# In[1935]:


organizeddataRecife['Men'] = organizeddataRecife['Men'].astype('uint8')


# In[1936]:


organizeddataRecife['Men'].dtype


# In[1937]:


#Non-white and Uninformed race


# In[1938]:


organizeddataRecife['race'].unique()


# In[1939]:


organizeddataRecife['race'].value_counts()


# In[1940]:


organizeddataRecife['race'].value_counts(normalize=True)


# In[1941]:


organizeddataRecife['race'].isna().sum()


# In[1942]:


organizeddataRecife = organizeddataRecife.dropna(subset=['race'])


# In[1943]:


organizeddataRecife.shape


# In[1944]:


organizeddataRecife['race'].unique()


# In[1945]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['race']


# In[1946]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['Non-White/Ignored'].replace('Brown','Non-white').replace('Yellow','Non-white').replace('Black','Non-white').replace('Indigenous','Non-white').replace('Ignored','Uninformed race')


# In[1947]:


organizeddataRecife['Non-White/Ignored'].unique()


# In[1948]:


organizeddataRecife['Non-White/Ignored'].value_counts()


# In[1949]:


organizeddataRecife['Non-White/Ignored'].value_counts(normalize=True)


# In[1950]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['Non-White/Ignored'])], axis=1)


# In[1951]:


organizeddataRecife.head(3)


# In[1952]:


organizeddataRecife.rename({'Non-White/Ignored_Non-white':'Non-white', 'Non-White/Ignored_Uninformed race':'Uninformed race'},axis=1, inplace=True)


# In[1953]:


organizeddataRecife.head(3)


# In[1954]:


# dummies for complete primary, secondary and high education


# In[1955]:


organizeddataRecife['schooling'].unique()


# In[1956]:


organizeddataRecife['schooling'].value_counts()


# In[1957]:


organizeddataRecife['schooling'].value_counts(normalize=True)


# In[1958]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['schooling'])], axis=1)


# In[1959]:


organizeddataRecife.head(3)


# In[1960]:


#wage


# In[1961]:


organizeddataRecife['Minimum Wage'].value_counts()


# In[1962]:


organizeddataRecife['Qtd Hora Contr'].unique()


# In[1963]:


organizeddataRecife['Qtd Hora Contr'].value_counts()


# In[1964]:


organizeddataRecife.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[1965]:


organizeddataRecife['Tempo Emprego'].unique()


# In[1966]:


organizeddataRecife['Tempo Emprego'].describe()


# In[1967]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.replace(',','.')


# In[1968]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.lstrip('0')


# In[1969]:


organizeddataRecife.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[1970]:


organizeddataRecife['Job tenure'] = organizeddataRecife['Job tenure'].astype(float)


# In[1971]:


organizeddataRecife['Job tenure'].unique()


# In[1972]:


organizeddataRecife['Job tenure'].describe()


# In[1973]:


organizeddataRecife['IBGE Subsector'].unique()


# In[1974]:


organizeddataRecife['IBGE Subsector'].value_counts()


# In[1975]:


organizeddataRecifeIBGE = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['IBGE Subsector'])], axis=1)


# In[1976]:


organizeddataRecifeIBGE.shape


# In[1977]:


organizeddataRecife['CBO Broad Group Name 2002'].unique()


# In[1978]:


organizeddataRecife['CBO Main SubGroup Name 2002'].unique()


# In[1979]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].unique()


# In[1980]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].value_counts()


# In[1981]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].str.title().value_counts()


# In[1982]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'] = organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].str.title()


# In[1983]:


organizeddataRecifeCBO = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[1984]:


organizeddataRecifeCBO.shape


# In[1985]:


organizeddataRecifeCBO.head(3)


# In[1986]:


organizeddataRecife['CNAE 2.0 Section Name'].unique()


# In[1987]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[1988]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[1989]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[1990]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].str.title()


# In[1991]:


organizeddataRecifeCNAE = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['CNAE 2.0 Section Name'])], axis = 1)


# In[1992]:


pd.Series(sorted(organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()))


# In[1993]:


organizeddataRecifeCNAE.head(3)


# ### preparing the variables for the logit model Recife

# In[1994]:


organizeddataRecife.shape


# In[1995]:


organizeddataRecifeIBGE.shape


# In[1996]:


organizeddataRecifeCBO.shape


# In[1997]:


organizeddataPECNAE.shape


# In[1998]:


organizeddataRecife.head(3)


# ### model 1 IBGE Subsector

# In[1999]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)


# In[2000]:


organizeddataRecifeIBGE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[2001]:


organizeddataRecifeIBGE['y']


# In[2002]:


#removed No Working Days because it was not significant


# In[2003]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]


# In[2004]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']].dtypes


# In[2005]:


X = organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]
y = organizeddataRecifeIBGE['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2006]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2007]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']


# In[2008]:


os_data_y['y']=os_data_y['y'].astype('int64')


# In[2009]:


#I saw somewhere before that might be the dtypes the reason for getting these errors in the logit model
#"Divide by zero encountered in log" when not dividing by zero 
#inverting hessian failed, no bse or cov_params

#Chaning the y dtype from uint8 to int64 worked!!!


# In[2010]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2011]:


y.dtype


# In[2012]:


# use result=logit_model.fit_regularized()
# use result=logit_model.fit(method='bfgs')
#result=logit_model.fit(method='lbfgs')
#result=logit_model.fit(method='newton')
#result=logit_model.fit(method='nm')
#result=logit_model.fit_regularized(method='l1')
#logit_model=sm.Logit(endog=y,exog=X)
#result=logit_model.fit_regularized(start_params=None, method='l1', maxiter='defined_by_method', full_output=1, disp=1, callback=None, alpha=0)

#result=logit_model.fit(method='powell')
#result=logit_model.fit(method='cg')
#result=logit_model.fit(method='ncg')
#result=logit_model.fit(method='basinhopping')
#result=logit_model.fit(method='minimize')


# All StatsModels Discrete Model Logit Method to [try](https://www.statsmodels.org/devel/generated/statsmodels.discrete.discrete_model.Logit.fit.html)

# In[2013]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[2014]:


#Pseudo R-squared inf


# ### model 2 CBO for Recife 

# In[2015]:


organizeddataRecifeCBO.shape


# In[2016]:


organizeddataRecifeCBO.rename({'Final Result':'y'},axis=1,inplace=True)


# In[2017]:


organizeddataRecifeCBO.rename({'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Middle Level Technicians in Biological, Biochemical, Health And Related Scis','Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences':'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis'},axis=1,inplace=True)


# In[2018]:


organizeddataRecifeCBO[['Age','Age 2','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','Working hours','Job tenure',
                       'Distance to CBD']]


# In[2019]:


#removing No Working Days because it was not significant 
#removing Men because it was also not significant


# In[2020]:


X = organizeddataRecifeCBO[['Age','Age 2','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','Working hours','Job tenure',
                       'Distance to CBD']]



y = organizeddataRecifeCBO['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2021]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2022]:


cols=['Age','Age 2','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Complete higher education',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians in Biological, Biochemical, Health And Related Scis',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries','Working hours','Job tenure',
                       'Distance to CBD']


# In[2023]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2024]:


y = y.astype('int64')


# In[2025]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[2026]:


#pseudo R 2 inf again


# ### model 3 CNAE 2.0 Section Name for Recife

# In[2027]:


organizeddataRecifeCNAE.shape


# In[2028]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[2029]:


organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD']]


# In[2030]:


#removing No Working Days because it was not significant


# In[2031]:


X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD']]
y = organizeddataRecifeCNAE['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2032]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2033]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction',
       'Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
     'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities','Working hours','Job tenure','Distance to CBD']


# In[2034]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2035]:


y = y.astype('int64')


# In[2036]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[2037]:


#fix the pseudo R2 inf for all 3 models in Recife, and for the death model in PE


# In[2038]:


#as for the death model there's no Distance to CBD, and some lat and long are off, and it's still inf for the pseudo R 2


# In[2039]:


#bancoesusalltabsrais2019morelatlongcepestabselected1 this data was used for the death model and it is not fixed for 
#lat and long inside the shape file, will the inf disappear if it's fixed for lat and long inside the shapefile
#I put the lats and long inside the shapefile and it did not fix it


# In[2040]:


#see more the error 'Inverting hessian failed, no bse or cov_params '
#search about logit model for rare events python


# ## all three models doing death for Recife

# In[2041]:


#all models for PE were between 0.2-0.4 which is good, the death models for pe were above 0.8, which is not good
#all models for Recife were between 0.2-0.4 which is good, now see what happens with the death models for Recife


# In[2042]:


organizeddataRecife


# In[2043]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsiderecife.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=14, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# In[2044]:


#check what I did for PE death 


# In[2045]:


#cell 636


# In[2046]:


latlonginsidepewithdummies.shape


# In[2047]:


bairrosgeojson.shape


# In[2048]:


bairrosgeojson.head(3)


# In[2049]:


latlonginsidepewithdummies.head(3)


# In[2050]:


'''
ValueError: 'index_left' and 'index_right' cannot be names in the frames being joined
So I removed them'''


# In[2051]:


latlonginsidepewithdummies = latlonginsidepewithdummies.drop(columns=['index_right'],axis=1)


# In[2052]:


gpd.sjoin(latlonginsidepewithdummies, bairrosgeojson, op='within')


# In[2053]:


geodataframe.shape


# In[2054]:


gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[2055]:


#same results in number of rows


# In[2056]:


latlonginsideRecifewithdummies = gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[2057]:


latlonginsideRecifewithdummies.shape


# In[2058]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsideRecifewithdummies.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=14, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# In[2059]:


latlonginsideRecifewithdummies.head(3)


# In[2060]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)


# In[2061]:


start_lat, start_lon = -8.0617353, -34.8706873


# In[2062]:


distances_km=[]
for row in latlonginsideRecifewithdummies.itertuples(index=False):
    distances_km.append(
    haversine_distance(start_lat,start_lon,row.latitude,row.longitude)
    ) 


# In[2063]:


latlonginsideRecifewithdummies['distancefrommarcozero']=distances_km


# In[2064]:


latlonginsideRecifewithdummies.head(3)


# In[2065]:


latlonginsideRecifewithdummies.shape


# In[2066]:


latlonginsideRecifewithdummies['distancefrommarcozero'].describe()


# In[2067]:


latlonginsideRecifewithdummies.rename({'distancefrommarcozero':'Distance to CBD'},axis=1,inplace=True)


# In[2068]:


latlonginsideRecifewithdummies.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[2069]:


latlonginsideRecifewithdummies['Tempo Emprego'].unique()


# In[2070]:


latlonginsideRecifewithdummies['Tempo Emprego'].describe()


# In[2071]:


latlonginsideRecifewithdummies['Tempo Emprego'] = latlonginsideRecifewithdummies['Tempo Emprego'].str.replace(',','.')


# In[2072]:


latlonginsideRecifewithdummies['Tempo Emprego'] = latlonginsideRecifewithdummies['Tempo Emprego'].str.lstrip('0')


# In[2073]:


latlonginsideRecifewithdummies.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[2074]:


latlonginsideRecifewithdummies['Job tenure'] = latlonginsideRecifewithdummies['Job tenure'].astype(float)


# In[2075]:


latlonginsideRecifewithdummies['Job tenure'].unique()


# In[2076]:


latlonginsideRecifewithdummies['Job tenure'].describe()


# ## latloninsdeRecifewithdummiesIBGE 

# In[2077]:


latlonginsideRecifewithdummiesIBGEdeath = pd.concat([latlonginsideRecifewithdummies, pd.get_dummies(latlonginsideRecifewithdummies['IBGE Subsector'])],axis=1)


# In[2078]:


latlonginsideRecifewithdummiesIBGEdeath.head(3)


# In[2079]:


latlonginsideRecifewithdummiesIBGEdeath.shape


# In[2080]:


latlonginsideRecifewithdummiesIBGEdeath.rename({'death':'y'},axis=1,inplace=True)


# In[2081]:


latlonginsideRecifewithdummiesIBGEdeath['y']


# In[2082]:


latlonginsideRecifewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].dtypes


# In[2083]:


latlonginsideRecifewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].describe()


# In[2084]:


latlonginsideRecifewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']].corr()


# In[2085]:


#I could think of a variable similar to being inside Metropolitan region, like if the bairro is within 2km from CBD


# In[2086]:


X = latlonginsideRecifewithdummiesIBGEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race',
                                             'Complete primary education','Complete secondary education'
      ,'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure',
                                             'Distance to CBD']]
y = latlonginsideRecifewithdummiesIBGEdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2087]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2088]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education'
      ,'Metropolitan region','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','No Working Days', 'Working hours', 'Job tenure','Distance to CBD']


# In[2089]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2090]:


y = y.astype('int64')


# In[2091]:


y.unique()


# In[2092]:


latlonginsideRecifewithdummiesIBGEdeath['disease evolution'].unique()


# In[2093]:


latlonginsideRecifewithdummiesIBGEdeath[latlonginsideRecifewithdummiesIBGEdeath['disease evolution']=='death'].shape


# In[2094]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X, REML = True)
result=logit_model.fit()
print(result.summary2())


# In[2095]:


#it did not converge, if removing these variables with very high standard error and p-values it will converge
#but the pseudo R2 is very high 85.0%


# ## latlonginsidRecifewithdummiesCBO

# In[2096]:


latlonginsideRecifewithdummies.columns


# In[2097]:


latlonginsideRecifewithdummies.shape


# In[2098]:


latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'].unique()


# In[2099]:


latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'].str.title().value_counts()


# In[2100]:


latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'] = latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'].str.title()


# In[2101]:


latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others']


# In[2102]:


pd.concat([latlonginsideRecifewithdummies,pd.get_dummies(latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[2103]:


latlonginsideRecifewithdummiesCBOdeath = pd.concat([latlonginsideRecifewithdummies,pd.get_dummies(latlonginsideRecifewithdummies['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[2104]:


latlonginsideRecifewithdummiesCBOdeath.rename({'death':'y'},axis=1,inplace=True)


# In[2105]:


latlonginsideRecifewithdummiesCBOdeath['y']


# In[2106]:


latlonginsideRecifewithdummiesCBOdeath.head(3)


# In[2107]:


latlonginsideRecifewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries']]


# In[2108]:


latlonginsideRecifewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries']].dtypes


# In[2109]:


latlonginsideRecifewithdummiesCBOdeath.rename({'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Middle Level Techns in Biol, Biochemical, Health And Rel Scis','Middle Level Technicians In Phys, Chemical, Engineering And Related Sciences':'Middle Level Techns In Physical, Chemical, Engineering And Rel Scis'},axis=1,inplace=True)


# In[2166]:


latlonginsideRecifewithdummiesCBOdeath.rename({'Middle Level Techns in Biological, Biochemical, Health And Rel Scis':'Middle Level Techns in Biol, Biochemical, Health And Rel Scis','Middle Level Techns In Physical, Chemical, Engineering And Rel Scis':'Middle Level Techns In Phys, Chemical, Engineering And Rel Scis'},axis=1,inplace=True)


# In[2167]:


latlonginsideRecifewithdummiesCBOdeath.columns


# In[2168]:


latlonginsideRecifewithdummiesCBOdeath.shape


# In[2175]:


#removing Middle Level Techns In Phys, Chemical, Engineering And Rel Scis cause the p-value was huge and the model did not 
#converge


# In[2177]:


latlonginsideRecifewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Techns in Biol, Biochemical, Health And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]


# In[2176]:


X = latlonginsideRecifewithdummiesCBOdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Techns in Biol, Biochemical, Health And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']]



y = latlonginsideRecifewithdummiesCBOdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2178]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2179]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
                        'Complete secondary education','Metropolitan region',
                        'Minimum Wage','Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Techns in Biol, Biochemical, Health And Rel Scis',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals',
       'Workers In The Extractive Industry And Civil Construction','No Working Days','Working hours','Job tenure',
                       'Distance to CBD']


# In[2180]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2181]:


y = y.astype('int64')


# In[2182]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[2118]:


#very high pseudo R2 89.2%, if the variables with very high standar errors and p-values are removed, the maximum likelihood 
#optimization will converge


# ## latlonginsideRecifewithdummiesCNAE

# In[2119]:


latlonginsideRecifewithdummies['CNAE 2.0 Section Name'].unique()


# In[2120]:


latlonginsideRecifewithdummies['CNAE 2.0 Section Name'].value_counts()


# In[2121]:


latlonginsideRecifewithdummies['CNAE 2.0 Section Name'] = latlonginsideRecifewithdummies['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[2122]:


latlonginsideRecifewithdummies['CNAE 2.0 Section Name'].value_counts()


# In[2123]:


latlonginsideRecifewithdummies['CNAE 2.0 Section Name'] = latlonginsideRecifewithdummies['CNAE 2.0 Section Name'].str.title()


# In[2124]:


latlonginsideRecifewithdummiesCNAEdeath = pd.concat([latlonginsideRecifewithdummies, pd.get_dummies(latlonginsideRecifewithdummies['CNAE 2.0 Section Name'])], axis = 1)


# In[2125]:


pd.Series(sorted(latlonginsideRecifewithdummiesCNAEdeath['CNAE 2.0 Section Name'].unique()))


# In[2126]:


latlonginsideRecifewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]


# In[2127]:


latlonginsideRecifewithdummiesCNAEdeath.rename({'death':'y'},axis=1,inplace=True)


# In[2128]:


latlonginsideRecifewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']].dtypes


# In[2183]:


#removing  'Electricity And Gas' cause the p-value was huge and the model would not converge


# In[2184]:


X = latlonginsideRecifewithdummiesCNAEdeath[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Financial, Insurance And Related Services Activities',
                        'No Working Days','Working hours','Job tenure','Distance to CBD']]
y = latlonginsideRecifewithdummiesCNAEdeath['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[2185]:


data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[2186]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education','Metropolitan region','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction',
       'Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
     'Arts, Culture, Sports And Recreation','Financial, Insurance And Related Services Activities',
     'No Working Days','Working hours','Job tenure','Distance to CBD']


# In[2187]:


X=os_data_X[cols]
y=os_data_y['y']


# In[2188]:


y = y.astype('int64')


# In[2189]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[2190]:


#very high pseudo R2, if the variables with very high standard errors and high p-values are removed the ML optimization will converge


# In[ ]:




