#!/usr/bin/env python
# coding: utf-8

# ## continuing to organize the data, map related

# In[44]:


import pandas as pd
import plotly.express as px
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[45]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part1.csv')


# In[46]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[47]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[48]:


bancoesusalltabsrais2019morelatlongcepestabselected1.info()


# In[49]:


bancoesusalltabsrais2019morelatlongcepestabselected1.memory_usage()


# In[50]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[51]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio']


# In[52]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].value_counts()


# In[53]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].value_counts(normalize=True)


# In[54]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].unique()


# In[55]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.title()


# In[56]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].dtype


# In[57]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].astype(str).replace('á','a').replace('ã','a').replace('â','a').replace('ê','e').replace('é','e').replace('í','i').replace('ô','o').replace('ó','o').replace('ú','u').replace('ç','c')
#it does not work, because when this string replace is used the string to be replaced, has to be the same


# In[58]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].astype(str)


# In[59]:


#bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].astype(str).replace('á','a').replace('ã','a').replace('â','a').replace('ê','e').replace('é','e').replace('í','i').replace('ô','o').replace('ó','o').replace('ú','u').replace('ç','c')
#this does not work


# In[60]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').unique()


# In[61]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[62]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[63]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio']


# In[64]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].value_counts()


# In[65]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected1, names='municipio')
fig.show('svg')


# In[66]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/PE_Municipios_2020/PE_Municipios_2020.shp')


# In[67]:


gdf.head(3)


# In[68]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.title()


# In[69]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')


# In[70]:


gdf['NM_MUN']


# In[71]:


gdf.plot();


# In[72]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='NM_MUN', right_on='municipio', how='inner', indicator=True)


# In[73]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[74]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.head(3)


# In[75]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.columns


# In[76]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].unique()


# In[77]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isnull().sum()


# In[78]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isna().sum()


# In[79]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result']


# In[80]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.dropna(subset=['finalresultdummy'],inplace=True) 


# In[81]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[82]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].replace({'Null':'0','negative':'0','positive':'1'},inplace=True)


# In[83]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[84]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].astype(int)


# In[85]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[86]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.groupby(by='NM_MUN').sum()


# In[87]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.groupby(by='NM_MUN').sum()


# In[88]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum


# In[89]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.reset_index(level=0,inplace=True)


# In[90]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.loc[:,['NM_MUN','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[91]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.shape


# In[92]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.head(3)


# In[93]:


gdf


# In[94]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases, on='NM_MUN', how='inner', indicator=True)


# In[95]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[96]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[97]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[98]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop('_merge',axis=1,inplace=True)


# In[99]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[100]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot();


# In[101]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(cmap='gist_gray', column='NM_MUN', figsize=(10,10),legend=True);


# In[102]:


pd.set_option('display.max_rows',None)


# In[103]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge


# In[104]:


#dropping Fernando de Noronha because it's messing up the map, 
#Fernando de Noronha has 32 covid positive cases by the way


# In[105]:


pd.set_option('display.max_rows',10)


# In[106]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.loc[bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['NM_MUN']=='Fernando De Noronha'].index, inplace = True)


# In[107]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[108]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[109]:


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


# In[110]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[111]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[112]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro']


# In[113]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].unique()


# In[114]:


list(bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'])


# In[115]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[116]:


bairrosgeojson


# In[117]:


bairrosgeojson.plot();


# In[118]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[119]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.title()


# In[120]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[121]:


bairrosgeojson['bairro_nome_ca'] = bairrosgeojson['bairro_nome_ca'].str.title()


# In[122]:


bairrosgeojson


# In[123]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge = bairrosgeojson.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='bairro_nome_ca', right_on='bairro',how='inner',indicator=True)


# In[124]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.shape


# In[125]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.head(3)


# In[126]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['final result']


# In[127]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].unique()


# In[128]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].replace({'negative':'0','Null':'0','positive':'1'},inplace=True)


# In[129]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].value_counts()


# In[130]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].astype(int)


# In[131]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.groupby(by='bairro').sum()


# In[132]:


bairrocovidsum = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.groupby(by='bairro').sum()


# In[133]:


bairrocovidsum.reset_index(level=0,inplace=True)


# In[134]:


bairrocovidsum.loc[:,['bairro','Health Professionals', 'Security Professionals','sex','finalresultdummy']]


# In[135]:


bairroscovidsumsomecols = bairrocovidsum.loc[:,['bairro','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[136]:


bairroscovidsumsomecols 


# In[137]:


bairrosgeojson


# In[138]:


bairromergesumcovidmerge=bairrosgeojson.merge(bairroscovidsumsomecols, left_on='bairro_nome_ca',right_on='bairro',how='inner',indicator=True)


# In[139]:


bairromergesumcovidmerge.shape


# In[140]:


bairromergesumcovidmerge.head(3)


# In[141]:


bairromergesumcovidmerge.plot();


# In[142]:


bairromergesumcovidmerge.plot(cmap='gist_gray', column='bairro', figsize=(10,10),legend=True);


# In[143]:


bairromergesumcovidmerge['finalresultdummy'].sum()


# In[144]:


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


# In[145]:


bairromergesumcovidmerge.drop(['_merge'],axis=1,inplace=True)


# In[146]:


bairromergesumcovidmerge.shape


# In[147]:


bairromergesumcovidmerge.head(3)


# ## latitude and longitude 

# In[148]:


#plot lats and longs over the shapefile, check if the lats and long, latscepest and longcepestab are correct, etc


# In[149]:


import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import mapclassify


# In[150]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[151]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[152]:


bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'].dtype


# In[153]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].dtype


# In[154]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']


# In[155]:


bancoesusalltabsrais2019morelatlongcepestabselected1['longitude']


# In[156]:


#need to transform lat and long from string to float, but there can't be missing cells to transform it to float


# In[157]:


pd.set_option('display.max_rows',None)


# In[158]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']


# In[159]:


pd.set_option('display.max_rows',10)


# In[160]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] =='-'].shape


# In[161]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] !='-'].shape


# In[162]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] !='-']


# In[163]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'] =='-'].shape


# In[164]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'] = bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].astype(float)
bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'] = bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'].astype(float)


# In[165]:


#nan_value=float('NaN')
#bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].str.replace('',nan_value)


# In[166]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].shape


# In[167]:


bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['latitude']).shape


# In[168]:


(bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']=='').sum()


# In[169]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].isnull().sum()


# In[170]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'].isna().sum()


# In[171]:


bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['latitude'],inplace=True)


# In[172]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[173]:


bancoesusalltabsrais2019morelatlongcepestabselected1['latitude']


# In[174]:


bancoesusalltabsrais2019morelatlongcepestabselected1['longitude']


# In[175]:


crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(bancoesusalltabsrais2019morelatlongcepestabselected1['longitude'], bancoesusalltabsrais2019morelatlongcepestabselected1['latitude'])]
geometry[:5]


# In[176]:


geodataframe = gpd.GeoDataFrame(bancoesusalltabsrais2019morelatlongcepestabselected1, crs = crs, geometry = geometry)
geodataframe.head()


# In[177]:


pd.set_option('display.max_columns',None)


# In[178]:


geodataframe.columns


# In[179]:


geodataframe.rename({'final result':'finalresult'},axis=1,inplace=True)


# In[180]:


gdf.shape


# In[181]:


gdf['NM_MUN'].nunique()


# In[182]:


gdf['NM_MUN'].sort_values()


# In[183]:


gdf['NM_MUN'].sort_values().unique()


# In[184]:


geodataframe.shape


# In[185]:


geodataframe['municipio'].nunique() #188? 


# In[186]:


geodataframe['municipio'].sort_values().unique() 


# In[187]:


#Belem De Sao Francisco should be Belem Do Sao Francisco (1), Iguaraci should be Iguaracy (2), Lagoa Do Itaenga should be Lagoa De Itaenga(3) 


# In[188]:


geodataframe['municipio'] = geodataframe['municipio'].replace({'Belem De Sao Francisco':'Belem Do Sao Francisco','Iguaraci':'Iguaracy','Lagoa Do Itaenga':'Lagoa De Itaenga'})


# In[189]:


geodataframe['municipio'].nunique()


# In[190]:


geodataframe['municipio'].isin(gdf['NM_MUN'])


# In[191]:


gdf['NM_MUN'].isin(geodataframe['municipio'])


# In[192]:


geodataframe['finalresult'].unique() #maybe I have to do groupby the map like the other map example


# In[193]:


'''
#plot confirmed cases world map 
#plotting the points from latitude and longitude over a shapefile
fig, ax = plt.subplots(figsize = (15,15))
gdf.plot(ax=ax, alpha = 0.4, color = 'grey')
geodataframe.plot(ax = ax, column='finalresult', scheme="quantiles",
           figsize=(25, 20),
           legend=True,cmap='coolwarm')
plt.title('Confirmed Case Amount in Different Municipalities',fontsize=15)
# add countries names and numbers 
for i in range(0,30):
    plt.text(float(geodataframe.longitude[i]),float(geodataframe.latitude[i]),"{}\n{}".format(geodataframe.municipio[i],geodataframe.finalresult[i]),size=8)
plt.show()



IndexError: boolean index did not match indexed array along dimension 0; dimension is 225115 
but corresponding boolean dimension is 227872
'''


# In[194]:


#check github plotting lat and long over the shapefile 
#check the plotting over the shapefile on nupit article


# In[195]:


'''
fig = px.scatter_geo(geodataframe,
                    lat=geodataframe.latitude,
                    lon=geodataframe.longitude,
                    hover_name='municipio')
fig.update_layout(
    title={
        'text':'Municipio Coordinates',
        'y':0.94,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
'''


# In[196]:


fig = px.scatter_geo(geodataframe,
                    lat=geodataframe.latitude,
                    lon=geodataframe.longitude,
                    hover_name='municipio')
fig.update_layout(
    title={
        'text':'Latitude and Longitude Data Coordinates',
        'y':0.88,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[197]:


#check nupit_susnovo.ipynb in thesis, thesis project, novaplanilhas, cruzamento


# In[198]:


gdf.columns


# In[199]:


gdf['NM_MUN']


# In[200]:


geodataframe.columns


# In[201]:


geodataframe['municipio']


# In[202]:


#different way to adjust the distance between the title and the plot

#fig.suptitle('Lat and Long data over shapefile PE', fontsize=12)
#plt.subplots_adjust(top=0.8) 
#plt.suptitle('Amazing Stats', size=16, y=1.12)


# In[203]:


#choose color maps
#https://matplotlib.org/stable/tutorials/colors/colormaps.html


# In[204]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
geodataframe.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE', fontsize = 18,pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[205]:


#it worked, it was the zoom, the zoom was so far away that the PE map could not be seen


# In[206]:


#it seems the shapefile is not working or something, it looks like it's brasil not PE
#maybe something with the shapefile or with the zoom


# In[207]:


#maybe the points (lats and long) that are of state of PE, needs to be fixed first in order for the map to work
#because some are really off


# In[208]:


geodataframe.head(3)


# In[209]:


gdf


# In[210]:


#gdf.plot()
fig, ax = plt.subplots(figsize=(7,7))
gdf.plot(ax=ax)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34)


# In[211]:


gdf.plot()


# In[212]:


geodataframe.plot();


# In[213]:


#before calculating the distance to marco zero, etc
#let's see where lat and long are inside only Recife, and not PE 


# In[214]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
geodataframe.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=16,pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# https://www.linkedin.com/pulse/geopandas-plotting-data-points-map-using-python-r%C3%A9gis-nisengwe/

# https://stackoverflow.com/questions/45207650/indexerror-boolean-index-did-not-match-indexed-array-along-dimension-0

# https://github.com/andreluizcoelho/mediumarticles/blob/main/twoimportantwaystoplotmaps.ipynb

# In[215]:


#add cbd marco zero, calculate the distance between marco zero and lat long, see latestab and longtestab too


# In[216]:


#make a column with marco zero lat and long 
#maybe not
#but what needs to be done is to calculate the distance from individuals cep and cep estab do cdb (marco zero)


# In[217]:


#https://developers.google.com/maps/documentation/javascript/examples/geocoding-simple


# In[218]:


'''
{
  "results": [
    {
      "address_components": [
        {
          "long_name": "Praça Rio Branco",
          "short_name": "Praça Rio Branco",
          "types": [
            "route"
          ]
        },
        {
          "long_name": "Recife",
          "short_name": "Recife",
          "types": [
            "political",
            "sublocality",
            "sublocality_level_1"
          ]
        },
        {
          "long_name": "Recife",
          "short_name": "Recife",
          "types": [
            "administrative_area_level_2",
            "political"
          ]
        },
        {
          "long_name": "Pernambuco",
          "short_name": "PE",
          "types": [
            "administrative_area_level_1",
            "political"
          ]
        },
        {
          "long_name": "Brazil",
          "short_name": "BR",
          "types": [
            "country",
            "political"
          ]
        },
        {
          "long_name": "50030-150",
          "short_name": "50030-150",
          "types": [
            "postal_code"
          ]
        }
      ],
      "formatted_address": "Praça Rio Branco - Recife, PE, 50030-150, Brazil",
      "geometry": {
        "bounds": {
          "south": -8.0627383,
          "west": -34.8711246,
          "north": -8.0615193,
          "east": -34.8706073
        },
        "location": {
          "lat": -8.0617353,
          "lng": -34.8706873
        },
        "location_type": "GEOMETRIC_CENTER",
        "viewport": {
          "south": -8.063477780291501,
          "west": -34.8722149302915,
          "north": -8.060779819708497,
          "east": -34.8695169697085
        }
      },
      "place_id": "ChIJPRgmj6QYqwcRjfmoe7K_nmo",
      "types": [
        "route"
      ]
    }
  ]
}
'''


# In[219]:


#marco zero  "lat": -8.0617353 "lng": -34.8706873


# In[220]:


#https://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile


# ### fixing the lat and long that are outside the shape file 

# In[221]:


gdf.plot();


# In[222]:


fig, ax = plt.subplots(figsize=(10,10))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
ax.set_title('PE shapefile', pad=18)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-9.5,-7.2)
ax.set_xlim(-41.5,-34.5);


# In[223]:


gdf.head(3)


# In[224]:


geodataframe.head(3)


# In[225]:


#https://stackoverflow.com/questions/7861196/check-if-a-geopoint-with-latitude-and-longitude-is-within-a-shapefile


# In[226]:


#https://stackoverflow.com/questions/43892459/check-if-geo-point-is-inside-or-outside-of-polygon


# In[227]:


#clean lat and long outside shapefile python put that on google 
#set lat and long limit dataframe column


# In[228]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
geodataframe.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE', fontsize = 18, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[229]:


geodataframe.head(3)


# In[230]:


geodataframe.shape


# [unary_union](https://geopandas.org/docs/reference/api/geopandas.GeoSeries.unary_union.html)
# 
# Returns a geometry containing the union of all geometries in the GeoSeries.

# In[231]:


#https://stackoverflow.com/questions/52600811/using-geopandas-how-do-i-select-all-points-not-within-a-polygon


# In[232]:


geodataframe['geometry'].unary_union


# In[233]:


#geodataframe[geodataframe['geometry'].disjoint(geodataframe['geometry'].unary_union)]


# In[234]:


#https://stackoverflow.com/questions/52600811/using-geopandas-how-do-i-select-all-points-not-within-a-polygon


# In[235]:


#https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python


# In[236]:


from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

point = Point(0.5, 0.5)
polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
print(polygon.contains(point))


# In[237]:


import geopandas as gpd


# In[238]:


#https://gis.stackexchange.com/questions/358373/extract-polygon-name-dataframe-if-the-geo-point-is-inside-polygon


# In[239]:


gdf.plot()


# In[240]:


gdf.head(3)


# In[241]:


gpd.sjoin(geodataframe, gdf, op='within')


# In[242]:


latlonginsidepe = gpd.sjoin(geodataframe, gdf, op='within')


# In[243]:


fig = px.scatter_geo(latlonginsidepe,
                    lat=latlonginsidepe.latitude,
                    lon=latlonginsidepe.longitude,
                    hover_name='municipio')
fig.update_layout(
    title={
        'text':'Lat and Long inside PE',
        'y':0.88,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')


# In[244]:


fig, ax = plt.subplots(figsize=(15,15))
gdf.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsidepe.plot(ax=ax, color='red', markersize=5);
ax.set_title('Lat and Long data over shapefile PE',fontsize=18, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-10,-7)
ax.set_xlim(-42,-34);


# In[245]:


#nice, they are all inside the shapefile 


# In[246]:


#on google 'decide if latitude column is inside polygon column python'


# In[247]:


bairrosgeojson.shape


# In[248]:


bairrosgeojson.head(3)


# In[249]:


gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[250]:


latlonginsiderecife = gpd.sjoin(geodataframe, bairrosgeojson, op='within')


# In[251]:


fig, ax = plt.subplots(figsize=(7,7))
bairrosgeojson.plot(ax=ax, facecolor='Grey', edgecolor='k',alpha=1,linewidth=1,cmap='viridis')
#You can use different 'cmaps' such as jet, plasm,magma, infereno,cividis, binary...(I simply chose cividis)
latlonginsiderecife.plot(ax=ax, color='green', markersize=5);
ax.set_title('Lat and Long data over shapefile Recife', fontsize=14, pad=20)
ax.set_ylabel('Longitude', fontsize=10)
ax.set_xlabel('Latitude', fontsize=10)
ax.set_ylim(-8.2,-7.9)
ax.set_xlim(-35.1,-34.8);


# In[252]:


#inside too, it dropped from 247k to 88k rows from lats and long inside recife
#for lat and long inside PE it drops from 247k rows to 240k rows


# In[253]:


#now what? calculate the distance between lat and long and cdb? cdb would be inside recife, and with PE, no cdb, 
#or all municipalities going into recife cdb (marco zero), caruaru, petrolina etc would have another cdb or not?


# In[254]:


#calculation distance between two points, an example


# In[255]:


#pip install haversine


# In[256]:


import haversine as hs


# In[257]:


loc1=(28.426846,77.088834)
loc2=(28.394231,77.050308)
hs.haversine(loc1,loc2)


# In[258]:


from haversine import Unit
#To calculate distance in meters 
hs.haversine(loc1,loc2,unit=Unit.METERS)


# In[259]:


#calculating distances between two points


# Calculate [bearing](https://towardsdatascience.com/calculating-the-bearing-between-two-geospatial-coordinates-66203f57e4b4) between two points)

# In[260]:


#https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/


# In[261]:


latlonginsiderecife.head(3)


# In[262]:


#https://nathanrooy.github.io/posts/2016-09-07/haversine-with-python/
#https://www.movable-type.co.uk/scripts/latlong.html


# In[263]:


#https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4


# In[264]:


#cdbmarcozerocoordinates = (-8.0617353,-34.8706873)


# In[265]:


#loc1=(28.426846,77.088834)
#loc2=(28.394231,77.050308)
#hs.haversine(loc1,loc2)


# In[266]:


'''
distances_km=[]
for row in latlonginsiderecife.itertuples(index=False):
    distances_km.append(
    hs.haversine(cdbmarcozerocoordinates,row.latitude,row.longitude)
    )
'''


# In Medium [Here’s How To Calculate Distance Between 2 Geolocations in Python](https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4)

# The [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula) determines the great-circle distance between two points on a sphere given their longitudes and latitudes

# ![](https://miro.medium.com/max/1266/1*HPzoryv8InMFwWIYTWEkbw.png)

# In[267]:


def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   return np.round(res, 2)


# In[268]:


#cdbmarcozerocoordinates = (-8.0617353,-34.8706873)
#radius of planet Earth 6371km 


# In[269]:


start_lat, start_lon = -8.0617353, -34.8706873


# In[270]:


distances_km=[]
for row in latlonginsiderecife.itertuples(index=False):
    distances_km.append(
    haversine_distance(start_lat,start_lon,row.latitude,row.longitude)
    ) 


# In[271]:


latlonginsiderecife['distancefrommarcozero']=distances_km


# In[272]:


latlonginsiderecife.head(3)


# In[273]:


latlonginsiderecife.shape


# In[274]:


latlonginsiderecife['distancefrommarcozero'].describe()


# In[ ]:





# In[275]:


#replicating some stuff that might be publishble 


# In[276]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[277]:


#death and number of cases by wage difference


# In[278]:


fig = px.histogram(bancoesusalltabsrais2019morelatlongcepestabselected1['meanminimumwage'].dropna(), x='meanminimumwage',color='meanminimumwage',
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


# In[279]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult'], names='finalresult')
fig.update_layout(
        title={
        'text':'Final Result',
        'y':0.95,
        'x':0.45,
        'xanchor':'center',
        'yanchor':'top'})
fig.show('svg')


# In[280]:


fig = px.pie(bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult']=='positive'], names='finalresult')
fig.update_layout(
        title={
        'text':'Final Result',
        'y':0.95,
        'x':0.45,
        'xanchor':'center',
        'yanchor':'top'})
fig.show('svg')


# In[281]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult']=='positive'] #positive for covid


# In[282]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult']=='positive'


# In[283]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult']=='positive']


# In[284]:


covidpositivecases = bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult']=='positive']


# In[285]:


fig = px.bar(bancoesusalltabsrais2019morelatlongcepestabselected1[['meanminimumwage','finalresult']].dropna(), x='meanminimumwage',y='finalresult', color='meanminimumwage')
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'},paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 125000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[286]:


fig = px.bar(covidpositivecases, x='meanminimumwage',y='finalresult', color='finalresult')
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'},paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 125000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[287]:


#it might be grey cause there's positive and negative, when it's only negative, it'll probably be colorful


# In[288]:


covidpositivecases.head(3)


# In[289]:


covidpositivecases['meanminimumwage']


# In[290]:


covidpositivecases['meanminimumwage'].isna().sum()


# In[291]:


covidpositivecases['finalresult'].isna().sum()


# In[292]:


covidpositivecases.dropna(subset=['meanminimumwage'],inplace = True)


# In[293]:


covidpositivecases['meanminimumwage'].isna().sum()


# In[294]:


fig = px.bar(covidpositivecases, x='finalresult',y='meanminimumwage', color='meanminimumwage')
fig.update_layout(
    title={
        'text': 'Test Type',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'},paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 125000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[295]:


fig = px.line(covidpositivecases, x='meanminimumwage', y='finalresult', color='finalresult')
fig.show()


# In[296]:


#that was stupid, it's already positive, all I have to do is make the graph for the mininumwage


# In[297]:


fig = px.histogram(covidpositivecases, x='meanminimumwage',color='meanminimumwage')
fig.update_layout(
    title={
        'text': 'Covid Positive Cases by Minimum Wage',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Cases')#,range=[0, 70000])
fig.update_xaxes(title='minimum wage')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[298]:


#minimum wage and death 


# In[299]:


covidpositivecases.columns


# In[300]:


covidpositivecases['disease evolution'].unique()


# In[301]:


covidpositivecases['estado'].unique()


# In[302]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[303]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].unique()


# In[304]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']=='death']


# In[305]:


coviddeathcases = bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']=='death']


# In[306]:


coviddeathcases['meanminimumwage'].isna().sum()


# In[307]:


coviddeathcases.dropna(subset=['meanminimumwage'], inplace = True)


# In[308]:


fig = px.histogram(coviddeathcases, x='meanminimumwage',color='meanminimumwage')
fig.update_layout(
    title={
        'text': 'Covid Deaths by Minimum Wage',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Deaths')#,range=[0, 70000])
fig.update_xaxes(title='minimum wage')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[309]:


#continue the analysis with covid death and cases by ativities sector
#check how/why deaths by covid are so low, see on t


# In[310]:


covidpositivecases.head(3)


# In[311]:


fig = px.histogram(covidpositivecases, x='IBGE Subsector',color='IBGE Subsector')
fig.update_layout(
    title={
        'text': 'Covid Positive Cases by IBGE Subsector',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Cases')#,range=[0, 70000])
fig.update_xaxes(title='IBGE Subsector')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[312]:


fig = px.histogram(covidpositivecases, x='CNAE 2.0 Section Name',color='CNAE 2.0 Section Name')
fig.update_layout(
    title={
        'text': 'Covid Positive Cases by CNAE 2.0',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Cases')#,range=[0, 70000])
fig.update_xaxes(title='CNAE 2.0')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[313]:


fig = px.histogram(coviddeathcases, x='IBGE Subsector',color='IBGE Subsector')
fig.update_layout(
    title={
        'text': 'Covid Deaths by IBGE Subsector',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Deaths')#,range=[0, 70000])
fig.update_xaxes(title='IBGE Subsector')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[314]:


fig = px.histogram(coviddeathcases, x='CNAE 2.0 Section Name',color='CNAE 2.0 Section Name')
fig.update_layout(
    title={
        'text': 'Covid Deaths by CNAE 2.0',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Deaths')#,range=[0, 70000])
fig.update_xaxes(title='CNAE 2.0')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[315]:


fig = px.bar(coviddeathcases, x = 'CNAE 2.0 Section Name', y = 'meanminimumwage', color = 'meanminimumwage')
fig.update_layout(
    title={
        'text': 'Covid Deaths: Minimum Wage By CNAE 2.0',
        'y':0.95,
        'x':0.35,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')#, showlegend=False)
#fig.update_yaxes(title='count',range=[0, 9000])
#fig.update_xaxes(title='Test Type')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg') #without the svg this graph looks perfect


# In[316]:


fig = px.line(coviddeathcases, x = 'CNAE 2.0 Section Name', y = 'meanminimumwage', color='CNAE 2.0 Section Name')
fig.show('svg')


# In[317]:


#unemployment


# In[318]:


coviddeathcases.columns


# In[319]:


coviddeathcases.head(2)


# In[320]:


coviddeathcases['Qtd Dias Afastamento'].unique()


# In[321]:


coviddeathcases['Qtd Dias Afastamento']==0


# In[322]:


coviddeathcases[coviddeathcases['Qtd Dias Afastamento']==0]


# In[323]:


#see if there's a relation between death and people who are working more, not laid off


# In[324]:


fig = px.histogram(coviddeathcases, x='Qtd Dias Afastamento',color='Qtd Dias Afastamento')
fig.update_layout(
    title={
        'text': 'Covid Deaths by Days Not Working',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Deaths')#,range=[0, 70000])
fig.update_xaxes(title='Days Not Working')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[325]:


coviddeathcases['Qtd Dias Afastamento'].unique()


# In[326]:


'''fig = px.pie(coviddeathcases, names='Qtd Dias Afastamento')
fig.show()
'''


# In[327]:


coviddeathcases['Qtd Dias Afastamento'].value_counts()


# In[328]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

coviddeathcases['Days Not Working'] = pd.cut(coviddeathcases['Qtd Dias Afastamento'], bins, labels=names)

print(coviddeathcases.dtypes)


# In[329]:


coviddeathcases.head(3)


# In[330]:


coviddeathcases['Days Not Working'].unique()


# In[331]:


fig = px.histogram(coviddeathcases['Days Not Working'].dropna(), x='Days Not Working',color='Days Not Working')
fig.update_layout(
    title={
        'text': 'Covid Deaths by Days Not Working',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Deaths')#,range=[0, 70000])
fig.update_xaxes(title='Days Not Working')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[332]:


coviddeathcases['Days Not Working'].value_counts()


# In[333]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

covidpositivecases['Days Not Working'] = pd.cut(covidpositivecases['Qtd Dias Afastamento'], bins, labels=names)

print(covidpositivecases.dtypes)


# In[334]:


covidpositivecases['Days Not Working'].value_counts()


# In[335]:


fig = px.histogram(covidpositivecases['Days Not Working'].dropna(), x='Days Not Working',color='Days Not Working')
fig.update_layout(
    title={
        'text': 'Covid Positive Cases by Days Not Working',
        'y':0.95,
        'x':0.45,
        'xanchor': 'center',
        'yanchor': 'top'},
    paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
fig.update_yaxes(title='Covid Positive Cases')#,range=[0, 70000])
fig.update_xaxes(title='Days Not Working')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[336]:


#make a graph with moving average of 7 days, 14 days. 
#see if the lockdown reduced cases and deaths
#for now do some spatial econometrics of high-high, high-low, etc. Moran Index, LISA, etc


# ## Spatial Econometrics 

# In[337]:


#https://nbviewer.org/github/pysal/esda/blob/master/notebooks/Spatial%20Autocorrelation%20for%20Areal%20Unit%20Data.ipynb


# In[338]:


#pip install pysal taking too long, it didn't work, it's better to work with libpysal


# In[339]:


import esda
import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import libpysal as lps
from libpysal.weights import KNN
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
get_ipython().run_line_magic('matplotlib', 'inline')


# In[340]:


#first doing for recife, then for PE 


# In[341]:


bairromergesumcovidmerge.shape


# In[342]:


bairromergesumcovidmerge.head(3)


# In[343]:


bairromergesumcovidmerge.plot()


# In[344]:


bairromergesumcovidmerge.plot(column='finalresultdummy');


# In[527]:


fig, ax = plt.subplots(figsize=(9,9), subplot_kw={'aspect':'equal'})
bairromergesumcovidmerge.plot(column='finalresultdummy', scheme='Quantiles', k=5, cmap='GnBu', legend=True, ax=ax)
ax.set_axis_off()
plt.margins(0.25);
#ax.set_xlim(150000, 160000)
#ax.set_ylim(208000, 215000)


# In[528]:


#Queen weights matrix 


# In[529]:


df = bairromergesumcovidmerge
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'r'


# In[530]:


#spatial lag


# In[531]:


y = bairromergesumcovidmerge['finalresultdummy']
ylag = lps.weights.lag_spatial(wq, y)


# In[532]:


ylag


# In[533]:


import mapclassify as mc
ylagq5 = mc.Quantiles(ylag, k=5)


# In[534]:


f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True,         k=5, cmap='GnBu', linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('Spatial Lag Covid Positive Cases (Quintiles)')

plt.show()


# In[535]:


df['lag_covid_cases'] = ylag
f,ax = plt.subplots(1,2,figsize=(2.16*4,4))
df.plot(column='finalresultdummy', ax=ax[0], edgecolor='k',
        scheme="quantiles",  k=5, cmap='GnBu')
ax[0].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[0].set_title('Covid Cases')
df.plot(column='lag_covid_cases', ax=ax[1], edgecolor='k',
        scheme='quantiles', cmap='GnBu', k=5)
ax[1].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[1].set_title('Spatial Lag Covid Cases')
ax[0].axis('off')
ax[1].axis('off')
plt.show()


# In[536]:


#what spatial lag means
#A spatial lag is a variable that averages the neighboring values of a location.
#https://libraries.mit.edu/files/gis/regression_presentation_iap2013.pdf


# In[537]:


#global spatial autocorrelation 


# In[538]:


#binary case


# In[539]:


y.median()


# In[540]:


yb = y > y.median()
sum(yb)


# In[541]:


#there are 46 nighborhoods with covid positive cases above the median and 47 (cause there are 93 in total) below the median


# In[542]:


y


# In[543]:


yb = y > y.median()
labels = ['0 Low', '1 High']
yb = [labels[i] for i in 1*yb] 
df['yb'] = yb


# In[544]:


#The spatial distribution of the binary variable immediately raises questions 
#about the juxtaposition of the "black" and "white" areas.


# In[545]:


fig, ax = plt.subplots(figsize=(10,8), subplot_kw={'aspect':'equal'})
df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)


# In[546]:


#join counts


# In[547]:


#Given that we have 46 Black polygons on our map, what is the number of Black Black (BB) joins we 
#could expect if the process were such that the Black polygons were randomly assigned on the map? 
#This is the logic of join count statistics.


# In[548]:


import esda 
yb = 1 * (y > y.median()) # convert back to binary
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'b'
np.random.seed(12345)
jc = esda.join_counts.Join_Counts(yb, wq)


# In[549]:


jc.bb


# In[550]:


jc.ww


# In[551]:


jc.bw


# In[552]:


#Note that the three cases exhaust all possibilities:


# In[553]:


jc.bb + jc.ww + jc.bw


# In[554]:


wq.s0 / 2


# In[555]:


#which is the unique number of joins in the spatial weights object.
#Our object tells us we have observed 89 BB joins:


# In[556]:


jc.bb


# In[557]:


jc.mean_bb


# In[558]:


jc.mean_bb.round(0)


# In[559]:


'''import seaborn as sbn
sbn.kdeplot(jc.sim_bb, shade=True)
plt.vlines(jc.bb, 0, 0.075, color='r')
plt.vlines(jc.mean_bb, 0,0.075)
plt.xlabel('BB Counts')
'''


# In[560]:


jc.p_sim_bb


# In[561]:


#Since this is below conventional significance levels, we would reject the null of complete spatial randomness in 
#favor of spatial autocorrelation in covid positive cases.


# In[562]:


#continuous case


# In[563]:


#First, we transform our weights to be row-standardized, from the current binary state:


# In[564]:


wq.transform = 'r'


# In[565]:


y = df['finalresultdummy']


# In[566]:


#Moran's I is a test for global autocorrelation for a continuous attribute:


# In[567]:


np.random.seed(12345)
mi = esda.moran.Moran(y, wq)
mi.I


# In[568]:


import seaborn as sbn
sbn.kdeplot(mi.sim, shade=True)
plt.vlines(mi.I, 0, 1, color='r')
plt.vlines(mi.EI, 0,1)
plt.xlabel("Moran's I")


# In[569]:


mi.p_sim


# In[570]:


#local autocorrelation: hot spots, cold spots, and Spatial Outliers


# In[571]:


np.random.seed(12345)
import esda


# In[572]:


wq.transform = 'r'
lag_covidcases = lps.weights.lag_spatial(wq, df['finalresultdummy'])


# In[573]:


covidcases = df['finalresultdummy']
b, a = np.polyfit(covidcases, lag_covidcases, 1)
f, ax = plt.subplots(1, figsize=(9, 9))

plt.plot(covidcases, lag_covidcases, '.', color='firebrick')

 # dashed vert at mean of the price
plt.vlines(covidcases.mean(), lag_covidcases.min(), lag_covidcases.max(), linestyle='--')
 # dashed horizontal at mean of lagged price 
plt.hlines(lag_covidcases.mean(), covidcases.min(), covidcases.max(), linestyle='--')

# red line of best fit using global I as slope
plt.plot(covidcases, a + b*covidcases, 'r')
plt.title('Moran Scatterplot')
plt.ylabel('Spatial Lag of Covid Cases')
plt.xlabel('Covid Cases')
plt.show()


# In[574]:


li = esda.moran.Moran_Local(y, wq)


# In[575]:


li.q


# In[576]:


(li.p_sim < 0.05).sum()


# In[577]:


sig = li.p_sim < 0.05
hotspot = sig * li.q==1
coldspot = sig * li.q==3
doughnut = sig * li.q==2
diamond = sig * li.q==4


# In[578]:


spots = ['n.sig.', 'hot spot']
labels = [spots[i] for i in hotspot*1]


# In[579]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['red', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()


# In[580]:


spots = ['n.sig.', 'cold spot']
labels = [spots[i] for i in coldspot*1]


# In[581]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['blue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()


# In[582]:


spots = ['n.sig.', 'doughnut']
labels = [spots[i] for i in doughnut*1]


# In[583]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['lightblue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()


# In[584]:


spots = ['n.sig.', 'diamond']
labels = [spots[i] for i in diamond*1]


# In[585]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['pink', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()


# In[586]:


sig = 1 * (li.p_sim < 0.05)
hotspot = 1 * (sig * li.q==1)
coldspot = 3 * (sig * li.q==3)
doughnut = 2 * (sig * li.q==2)
diamond = 4 * (sig * li.q==4)
spots = hotspot + coldspot + doughnut + diamond
spots


# In[587]:


spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
labels = [spot_labels[i] for i in spots]


# In[588]:


from matplotlib import colors
hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()


# In[589]:


#do the same for PE, see what it all means,
#then do the same for bairros and PE for death cases, 
#run at least SLM, SAR, SEM, SLX


# In[590]:


#PE 


# In[591]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[592]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[593]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(column='finalresultdummy')


# In[594]:


fig, ax = plt.subplots(figsize=(15,12), subplot_kw={'aspect':'equal'})
bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(column='finalresultdummy', scheme='Quantiles', k=5, cmap='GnBu', legend=True, ax=ax)
plt.margins(0.25)
#ax.set_xlim(150000, 160000)
#ax.set_ylim(208000, 215000)


# In[595]:


#spatial autocorrelation


# In[596]:


#spatial similarity


# In[597]:


#queen 


# In[598]:


df = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'r'


# In[599]:


y = df['finalresultdummy']
ylag = lps.weights.lag_spatial(wq, y)


# In[600]:


ylag


# In[601]:


import mapclassify as mc
ylagq5 = mc.Quantiles(ylag, k=5)


# In[602]:


f, ax = plt.subplots(1, figsize=(12, 12))
df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True,         k=5, cmap='GnBu', linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('Spatial Lag Covid Cases (Quintiles)')
plt.margins(0.18)
plt.show()


# In[603]:


df['lag_covidcases'] = ylag
f,ax = plt.subplots(1,2,figsize=(12,12))
df.plot(column='finalresultdummy', ax=ax[0], edgecolor='k',
        scheme="quantiles",  k=5, cmap='GnBu')
ax[0].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[0].set_title('Covid Cases')
df.plot(column='lag_covidcases', ax=ax[1], edgecolor='k',
        scheme='quantiles', cmap='GnBu', k=5)
ax[1].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[1].set_title('Spatial Lag Covid Cases')
ax[0].axis('off')
ax[1].axis('off')
plt.show()


# In[604]:


#Global Spatial Autocorrelation


# In[605]:


#binary case


# In[606]:


y.median()


# In[607]:


yb = y > y.median()
sum(yb)


# In[608]:


#there are 92 neighborhoods with covid cases above the median and 92 below


# In[609]:


y


# In[610]:


yb = y > y.median()
labels = ["0 Low", "1 High"]
yb = [labels[i] for i in 1*yb] 
df['yb'] = yb


# In[611]:


fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)
plt.margins(0.2)


# In[612]:


#join counts


# In[613]:


import esda 
yb = 1 * (y > y.median()) # convert back to binary
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'b'
np.random.seed(12345)
jc = esda.join_counts.Join_Counts(yb, wq)


# In[614]:


jc.bb


# In[615]:


jc.ww


# In[616]:


jc.bw


# In[617]:


jc.bb + jc.ww + jc.bw


# In[618]:


wq.s0 / 2


# In[619]:


jc.bb # we have observed 155 BB joins


# In[620]:


jc.mean_bb


# In[621]:


'''import seaborn as sbn
sbn.kdeplot(jc.sim_bb, shade=True)
plt.vlines(jc.bb, 0, 0.075, color='r')
plt.vlines(jc.mean_bb, 0,0.075)
plt.xlabel('BB Counts')
'''


# In[622]:


jc.p_sim_bb


# In[623]:


#continuous case


# In[624]:


wq.transform = 'r'


# In[625]:


y = df['finalresultdummy']


# In[626]:


np.random.seed(12345)
mi = esda.moran.Moran(y, wq)
mi.I


# In[627]:


import seaborn as sbn
sbn.kdeplot(mi.sim, shade=True)
plt.vlines(mi.I, 0, 1, color='r')
plt.vlines(mi.EI, 0,1)
plt.xlabel("Moran's I")


# In[628]:


mi.p_sim


# In[629]:


#local autocorrelation: hot spots, cold spots, and spatial outliers


# In[630]:


np.random.seed(12345)
import esda


# In[631]:


wq.transform = 'r'
lag_covidcases = lps.weights.lag_spatial(wq, df['finalresultdummy'])


# In[632]:


covidcases = df['finalresultdummy']
b, a = np.polyfit(covidcases, lag_covidcases, 1)
f, ax = plt.subplots(1, figsize=(8, 8))

plt.plot(covidcases, lag_covidcases, '.', color='firebrick')

 # dashed vert at mean of the price
plt.vlines(covidcases.mean(), lag_covidcases.min(), lag_covidcases.max(), linestyle='--')
 # dashed horizontal at mean of lagged price 
plt.hlines(lag_covidcases.mean(), covidcases.min(), covidcases.max(), linestyle='--')

# red line of best fit using global I as slope
plt.plot(covidcases, a + b*covidcases, 'r')
plt.title('Moran Scatterplot')
plt.ylabel('Spatial Lag of Covid Cases')
plt.xlabel('Covid Cases')
plt.show()


# In[633]:


li = esda.moran.Moran_Local(y, wq)


# In[634]:


li.q


# In[635]:


(li.p_sim < 0.05).sum()


# In[636]:


sig = li.p_sim < 0.05
hotspot = sig * li.q==1
coldspot = sig * li.q==3
doughnut = sig * li.q==2
diamond = sig * li.q==4


# In[637]:


spots = ['n.sig.', 'hot spot']
labels = [spots[i] for i in hotspot*1]


# In[638]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['red', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.margins(0.25)
plt.show()


# In[639]:


spots = ['n.sig.', 'cold spot']
labels = [spots[i] for i in coldspot*1]


# In[640]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['blue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.margins(0.25)
plt.show()


# In[641]:


spots = ['n.sig.', 'doughnut']
labels = [spots[i] for i in doughnut*1]


# In[642]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['lightblue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.margins(0.25)
plt.show()


# In[643]:


spots = ['n.sig.', 'diamond']
labels = [spots[i] for i in diamond*1]


# In[644]:


df = df
from matplotlib import colors
hmap = colors.ListedColormap(['pink', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
ax.set_axis_off()
plt.margins(0.35)
plt.show()


# In[645]:


sig = 1 * (li.p_sim < 0.05)
hotspot = 1 * (sig * li.q==1)
coldspot = 3 * (sig * li.q==3)
doughnut = 2 * (sig * li.q==2)
diamond = 4 * (sig * li.q==4)
spots = hotspot + coldspot + doughnut + diamond
spots


# In[646]:


spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
labels = [spot_labels[i] for i in spots]


# In[647]:


from matplotlib import colors
hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
f, ax = plt.subplots(1, figsize=(12, 12))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
plt.margins(0.25)
ax.set_axis_off()
plt.show()


# In[648]:


from matplotlib import colors
hmap = colors.ListedColormap(['lightgrey', 'red', 'lightblue','blue','pink'])
f, ax = plt.subplots(1, figsize=(10, 10))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
plt.subplots_adjust(left=0.2, bottom=0.2, right=1.15, top=1.5, wspace=1.8, hspace=2.5)
plt.margins(0.25)
ax.set_axis_off()
plt.show()


# In[649]:


#fix the legend, do the maps with bairros recife, and PE for death cases
#the lat and long over the shapefile way above were all lats and long and not covid or death cases, maybe do that too


# In[650]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[651]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[652]:


bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution'].unique()


# In[653]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']=='death']


# In[654]:


341/227000


# In[655]:


bancoesusalltabsrais2019morelatlongcepestabselected1[bancoesusalltabsrais2019morelatlongcepestabselected1['disease evolution']=='death'].sort_values('municipio')


# In[656]:


coviddeathcases.shape


# In[657]:


coviddeathcases['municipio'].unique()


# In[658]:


coviddeathcases['bairro'].unique()


# In[659]:


#no deaths by bairro in the dataset
#very few death 307, in the municipalitites only 90 out of 186 municipalities, probably not worth to do LISA analysis,
#there will be too many missing municipalities, and the analysis won't work 


# ### Spatial Models

# In[660]:


from PIL import Image
myImage = Image.open('somespatialmodels.jpg')
myImage


# In[661]:


#SAR and SLX in Python
#http://darribas.org/gds_scipy16/ipynb_md/08_spatial_regression.html


# In[662]:


#Spatial Wage and Education on Covid 


# In[663]:


#wage and education. as well as health indicators need to be a mean, since the info are grouped by to make the map


# In[664]:


#there's the need to calculate the moving average


# In[665]:


covidpositivecases.head(3)


# In[666]:


covidpositivecases.shape


# In[667]:


#SLM


# In[668]:


#check if all X values has to be numerical or if it can be categorical


# In[669]:


#x = covidpositivecases[['idade','racaCor','Escolaridade após 2005','Qtd Dias Afastamento','meanminimumwage']]


# In[670]:


covidpositivecases['finalresult'].unique()


# In[671]:


covidpositivecases['finalresultdummy'] = covidpositivecases['finalresult'].replace('positive','1')


# In[672]:


covidpositivecases['finalresultdummy'] = covidpositivecases['finalresultdummy'].astype('int8')


# In[673]:


covidpositivecases.head(3)


# In[674]:


#https://pysal.org/libpysal/generated/libpysal.weights.KNN.html


# In[675]:


#https://geographicdata.science/book/notebooks/11_regression.html


# In[676]:


import spreg


# In[677]:


covidpositivecases['finalresultdummy'].astype


# In[678]:


covidpositivecases['sex'].astype


# In[679]:


#let's use the other data, because covid positivecases has only positive cases, it won't make sense for the dependent variable


# In[680]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[681]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[682]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1['finalresult'].replace('positive','1').replace('negative','0').replace('Null','0')


# In[683]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[684]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresultdummy'].unique()


# In[685]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresultdummy'].isna().sum()


# In[686]:


bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['finalresultdummy'],inplace=True)


# In[687]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresultdummy'].unique()


# In[688]:


bancoesusalltabsrais2019morelatlongcepestabselected1['schooling'].unique()


# In[689]:


bancoesusalltabsrais2019morelatlongcepestabselected1['agecohort'].unique()


# In[690]:


bancoesusalltabsrais2019morelatlongcepestabselected1['meanminimumwage'].unique()


# In[691]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

bancoesusalltabsrais2019morelatlongcepestabselected1['Days Not Working'] = pd.cut(bancoesusalltabsrais2019morelatlongcepestabselected1['Qtd Dias Afastamento'], bins, labels=names)

print(bancoesusalltabsrais2019morelatlongcepestabselected1.dtypes)


# In[692]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[693]:


'''
getdummy for schooling and race
'''


# In[694]:


pd.get_dummies(bancoesusalltabsrais2019morelatlongcepestabselected1, columns = ['schooling', 'race'])


# In[695]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.get_dummies(bancoesusalltabsrais2019morelatlongcepestabselected1, columns = ['schooling', 'race'])


# In[696]:


bancoesusalltabsrais2019morelatlongcepestabselected1.columns


# In[697]:


bancoesusalltabsrais2019morelatlongcepestabselected1[['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow']] = bancoesusalltabsrais2019morelatlongcepestabselected1[['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow']].astype(int)


# In[698]:


bancoesusalltabsrais2019morelatlongcepestabselected1[['Qtd Dias Afastamento', 'idade']] = bancoesusalltabsrais2019morelatlongcepestabselected1[['Qtd Dias Afastamento', 'idade']].astype(float)


# In[699]:


bancoesusalltabsrais2019morelatlongcepestabselected1[['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow']].head(3)


# In[700]:


bancoesusalltabsrais2019morelatlongcepestabselected1[['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow']].dtypes


# In[701]:


variable_names = ['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow']


# In[702]:


#variable_names = ['sex']


# In[703]:


bancoesusalltabsrais2019morelatlongcepestabselected1[variable_names].isna().sum()


# In[704]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = bancoesusalltabsrais2019morelatlongcepestabselected1.dropna(subset=['sex','Health Professionals','Qtd Dias Afastamento','idade','schooling_Complete higher education',
       'schooling_Complete primary education',
       'schooling_Complete secondary education',
       'schooling_Incomplete primary education', 'race_Black', 'race_Brown',
       'race_Ignored', 'race_Indigenous', 'race_White', 'race_Yellow'])


# In[705]:


bancoesusalltabsrais2019morelatlongcepestabselected1['finalresultdummy'].head(3)


# In[706]:


#drop nans on these columns


# In[707]:


# Fit OLS model
m1 = spreg.OLS(
    # Dependent variable
    bancoesusalltabsrais2019morelatlongcepestabselected1[['finalresultdummy']].values, 
    # Independent variables
     bancoesusalltabsrais2019morelatlongcepestabselected1[variable_names].values,
    # Dependent variable name
    name_y= 'finalresultdummy', 
    # Independent variable name
    name_x=variable_names
)


# In[736]:


print(m1.summary)


# In[737]:


#https://www.yawintutor.com/typeerror-argument-of-type-bool-is-not-iterable/


# In[ ]:





# In[ ]:





# In[738]:


#Example from the website 
#https://geographicdata.science/book/notebooks/11_regression.html


# In[739]:


sandiegoairbnb = gpd.read_file('regression_db.geojson')


# In[740]:


sandiegoairbnb.shape


# In[741]:


sandiegoairbnb.head(3)


# In[742]:


variable_names = [
    'accommodates',    # Number of people it accommodates
    'bathrooms',       # Number of bathrooms
    'bedrooms',        # Number of bedrooms
    'beds',            # Number of beds
    # Below are binary variables, 1 True, 0 False
    'rt_Private_room', # Room type: private room
    'rt_Shared_room',  # Room type: shared room
    'pg_Condominium',  # Property group: condo
    'pg_House',        # Property group: house
    'pg_Other',        # Property group: other
    'pg_Townhouse'     # Property group: townhouse
]


# In[743]:


# Fit OLS model
m1 = spreg.OLS(
    # Dependent variable
    sandiegoairbnb[['log_price']].values, 
    # Independent variables
    sandiegoairbnb[variable_names].values,
    # Dependent variable name
    name_y='log_price', 
    # Independent variable name
    name_x=variable_names
)


# In[744]:


print(m1.summary)


# In[745]:


###https://deepnote.com/@carlos-mendez/PYTHON-Basic-spatial-econometrics-He5bDBGzQI6SAdyUpgmWNQ


# In[746]:


#pip install splot


# In[747]:


# Load libraries
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_style('darkgrid')
#sns.set_style('whitegrid')
#sns.set_style('white')


import geopandas as gpd
import matplotlib.pyplot as plt

import libpysal
from libpysal  import weights
from libpysal.weights import Queen

import esda
from esda.moran import Moran, Moran_Local

import splot
from splot.esda import moran_scatterplot, plot_moran, lisa_cluster, plot_local_autocorrelation
from splot.libpysal import plot_spatial_weights

from giddy.directional import Rose

from spreg import OLS
from spreg import MoranRes
from spreg import ML_Lag
from spreg import ML_Error


# In[748]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(2)


# In[749]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.crs


# In[750]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(2)


# In[751]:


#spatial weights matrix


# In[752]:


W = weights.KNN.from_dataframe(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge, k=8)
#W = weights.KNN.from_dataframe(gdf, k=6)
#W = weights.KNN.from_dataframe(gdf, k=4)


#W = weights.Queen.from_dataframe(gdf)
#W = weights.Rook.from_dataframe(gdf)

# Compute inverse distance squared based on maximum nearest neighbor distance between the n observations 
#maxMin = weights.min_threshold_dist_from_shapefile("map.shp")
#W = weights.DistanceBand.from_dataframe(gdf, threshold = maxMin, binary=False, alpha=-2)

# Row-standardize W
W.transform = 'r'


# In[753]:


plot_spatial_weights(W,gdf);


# In[754]:


W.neighbors


# In[755]:


W.min_neighbors


# In[756]:


W.mean_neighbors


# In[757]:


W.max_neighbors


# In[758]:


W.histogram


# In[759]:


#regression preparations


# In[760]:


y = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].values
y_name='finalresultdummy'


# In[761]:


x = np.array([bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['Health Professionals']]).T
x_name = 'Health Professionals'


# In[762]:


#OLS


# In[763]:


ols = OLS(y = y, x = x, w = W, 
          name_y=y_name, name_x = [x_name], name_w='W', name_ds='bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge', 
          white_test=True, spat_diag=True, moran=True)
print(ols.summary)


# In[764]:


#SEM


# In[765]:


sem = ML_Error(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge')
print(sem.summary)


# In[766]:


#SAR


# In[767]:


sar = ML_Lag(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge')
print(sar.summary)


# In[768]:


#http://andrewgaidus.com/Spatial_Econonometric_Modeling/


# In[769]:


#https://methods.sagepub.com/dataset/howtoguide/spatial-lag-dublin-2018-python


# In[770]:


#https://pysal.org/spreg/notebooks/Panel_FE_example.html


# In[771]:


#https://pysal.org/spreg/notebooks/GM_Lag_example.html


# In[772]:


#https://lost-stats.github.io/Geo-Spatial/spatial_lag_model.html


# [ESDA](https://towardsdatascience.com/exploratory-spatial-data-analysis-esda-spatial-autocorrelation-7592edcbef9a), Moran Index and HH, LH, LL, HL 

# In[773]:


#organize the map PE with variables and IDHM


# In[774]:


import pandas as pd 


# In[775]:


#idhmpe = pd.read_excel('IDHM PE.xlsx')


# In[776]:


#idhmpe.to_csv('IDHM PE.csv', index = False)


# In[899]:


idhm_pe = pd.read_csv('IDHM PE.csv')


# In[900]:


idhm_pe.head(3)


# In[901]:


idhm_pe.loc[:,['Territorialidade','IDHM']]


# In[902]:


idhm_pe = idhm_pe.loc[:,['Territorialidade','IDHM']]


# In[903]:


idhm_pe


# In[904]:


idhm_pe.rename({'Territorialidade':'municipio'}, axis = 1, inplace=True)


# In[905]:


idhm_pe = idhm_pe.sort_values('municipio')


# In[906]:


idhm_pe


# In[907]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').unique()


# In[908]:


idhm_pe = idhm_pe.reset_index(drop=True)


# In[909]:


idhm_pe = idhm_pe.sort_values('municipio').reset_index(drop=True)


# In[910]:


idhm_pe


# In[911]:


idhm_pe['municipio'] = idhm_pe['municipio'].astype(str).str[:-4]


# In[912]:


idhm_pe


# In[913]:


df.head(3)


# In[914]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[915]:


idhm_pe


# In[916]:


idhm_pe.dtypes


# In[917]:


df.dtypes


# In[918]:


df.shape #Fernando de Noronha is not on there


# In[919]:


idhm_pe['municipio'] = idhm_pe['municipio'].astype(str)
df['NM_MUN'] = df['NM_MUN'].astype(str)


# In[920]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.strip()


# In[921]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.title()


# In[922]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.replace('Belem De Sao Francisco','Belem Do Sao Francisco').str.replace('Iguaraci','Iguaracy').str.replace('Lagoa Do Itaenga','Lagoa De Itaenga')


# In[923]:


idhm_pe


# In[924]:


idhm_pe.shape


# In[925]:


idhm_pe_df = df.merge(idhm_pe, how = 'inner',left_on = 'NM_MUN', right_on='municipio',indicator=True)


# In[926]:


idhm_pe_df


# In[927]:


idhm_pe_df.shape


# In[928]:


idhm_pe_df.drop(['municipio','_merge'],axis=1,inplace=True)


# In[929]:


idhm_pe_df


# In[930]:


from matplotlib import colors
hmap = colors.ListedColormap(['lightgrey', 'red', 'lightblue','blue','pink'])
f, ax = plt.subplots(1, figsize=(10, 10))
df.assign(cl=labels).plot(column='cl', categorical=True,         k=2, cmap=hmap, linewidth=0.1, ax=ax,         edgecolor='white', legend=True)
plt.subplots_adjust(left=0.2, bottom=0.2, right=1.15, top=1.5, wspace=1.8, hspace=2.5)
plt.margins(0.25)
ax.set_axis_off()
plt.show()


# In[ ]:




