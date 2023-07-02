#!/usr/bin/env python
# coding: utf-8

# # Spatial Econometrics_article 1

# In[1]:


import pandas as pd
import plotly.express as px
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[2]:


import esda
from geopandas import GeoDataFrame
import libpysal as lps
from libpysal.weights import KNN
from shapely.geometry import Point
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


from libpysal.weights.contiguity import Queen
from libpysal import examples
import os
import splot


# In[4]:


#bancoesusalltabsrais2019morelatlongcepestabselected2 = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part2.csv')


# In[5]:


#PE with Moran, LISA and IDHM


# In[6]:


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part1.csv')


# In[7]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[8]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[9]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.title()


# In[10]:


bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'] = bancoesusalltabsrais2019morelatlongcepestabselected1['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[11]:


gdf = gpd.read_file('C:/Users/andre/Documents/Thesis/Thesis Project/Novas planilhas até 22-12-2020/cruzamento/PE_Municipios_2020/PE_Municipios_2020.shp')


# In[12]:


gdf.head(3)


# In[13]:


gdf['NM_MUN'] = gdf['NM_MUN'].str.title()
gdf['NM_MUN'] = gdf['NM_MUN'].str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8')


# In[14]:


gdf['NM_MUN']


# In[15]:


gdf.plot();


# In[16]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='NM_MUN', right_on='municipio', how='inner', indicator=True)


# In[17]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[18]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.head(3)


# In[19]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].unique()


# In[20]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result'].isnull().sum()


# In[21]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['final result']


# In[22]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.dropna(subset=['finalresultdummy'],inplace=True) 


# In[23]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].replace({'Null':'0','negative':'0','positive':'1'},inplace=True)


# In[24]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].unique()


# In[25]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge['finalresultdummy'].astype(int)


# In[26]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.shape


# In[27]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmerge.groupby(by='NM_MUN').sum()


# In[28]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum


# In[29]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.reset_index(level=0,inplace=True)


# In[30]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergesum.loc[:,['NM_MUN','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[31]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.shape


# In[32]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases.head(3)


# In[33]:


gdf


# In[34]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge = gdf.merge(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcases, on='NM_MUN', how='inner', indicator=True)


# In[35]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[36]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[37]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[38]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop('_merge',axis=1,inplace=True)


# In[39]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.head(3)


# In[40]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot();


# In[41]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.plot(cmap='gist_gray', column='NM_MUN', figsize=(10,10),legend=True);


# In[42]:


#dropping Fernando de Noronha because it's messing up the map, 
#Fernando de Noronha has 32 covid positive cases by the way


# In[43]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.drop(bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.loc[bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['NM_MUN']=='Fernando De Noronha'].index, inplace = True)


# In[44]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[45]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge['finalresultdummy'].sum()


# In[46]:


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


# In[47]:


bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.shape


# In[48]:


idhm_pe = pd.read_csv('IDHM PE.csv')


# In[49]:


idhm_pe.head(3)


# In[50]:


idhm_pe


# In[51]:


idhm_pe = idhm_pe.loc[:,['Territorialidade','IDHM']]


# In[52]:


idhm_pe.rename({'Territorialidade':'municipio'}, axis = 1, inplace=True)


# In[53]:


idhm_pe = idhm_pe.sort_values('municipio')


# In[54]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8').unique()


# In[55]:


idhm_pe = idhm_pe.sort_values('municipio').reset_index(drop=True)


# In[56]:


idhm_pe['municipio'] = idhm_pe['municipio'].astype(str).str[:-4]


# In[57]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.strip()


# In[58]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.title()


# In[59]:


idhm_pe['municipio'] = idhm_pe['municipio'].str.replace('Belem De Sao Francisco','Belem Do Sao Francisco').str.replace('Iguaraci','Iguaracy').str.replace('Lagoa Do Itaenga','Lagoa De Itaenga')


# In[60]:


idhm_pe.shape


# In[61]:


idhm_pe.head(3)


# In[62]:


idhm_pe_merge = bancoesusalltabsrais2019morelatlongcepestabselected1_gdfmergecovidtotalcasesmerge.merge(idhm_pe, how = 'inner',left_on = 'NM_MUN', right_on='municipio',indicator=True)


# In[63]:


idhm_pe_merge.shape


# In[64]:


idhm_pe_merge.head(3)


# In[65]:


idhm_pe_merge.drop(['municipio','_merge'],axis=1,inplace=True)


# In[66]:


idhm_pe_merge.head(3)


# In[67]:


idhm_pe_merge.plot(column='finalresultdummy');


# In[68]:


idhm_pe_merge.plot(column='IDHM');


# In[69]:


#estimatedpop2019datasusmunPE = pd.read_excel('populaçãoestimadamun2019datasusPE.xlsx')


# In[70]:


#estimatedpop2019datasusmunPE.to_csv('populaçãoestimadamun2019datasusPE_1.csv',index=False)


# In[71]:


estimatedpop2019datasusmunPE = pd.read_csv('populaçãoestimadamun2019datasusPE_1.csv')


# In[72]:


estimatedpop2019datasusmunPE.head(3)


# In[73]:


estimatedpop2019datasusmunPE.shape


# In[74]:


estimatedpop2019datasusmunPE


# In[75]:


estimatedpop2019datasusmunPE.tail(3)


# In[76]:


idhm_pe_merge.head(3)


# In[77]:


#cod_mun would've been nice, but it's different


# In[78]:


estimatedpop2019datasusmunPE['Município'] = estimatedpop2019datasusmunPE['Município'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[79]:


estimatedpop2019datasusmunPE['Município'] = estimatedpop2019datasusmunPE['Município'].str.title()


# In[80]:


idhm_pe_merge_pop = idhm_pe_merge.merge(estimatedpop2019datasusmunPE, how = 'inner', left_on='NM_MUN', right_on='Município', indicator=True)


# In[81]:


idhm_pe_merge_pop.shape


# In[82]:


idhm_pe_merge_pop.head(3)


# In[83]:


idhm_pe_merge_pop.drop(['cod_mun','Município','_merge'],axis=1,inplace=True)


# In[84]:


idhm_pe_merge_pop.rename({'População_estimada':'estimatedpop'},axis=1, inplace=True)


# In[85]:


idhm_pe_merge_pop.head(3)


# In[86]:


idhm_pe_merge_pop['covidrateper100kinhabitants'] = (idhm_pe_merge_pop['finalresultdummy'] / idhm_pe_merge_pop['estimatedpop'])*100000


# In[87]:


idhm_pe_merge_pop.head(3)


# In[88]:


idhm_pe_merge_pop.rename({'covidrateper100kinhabitants':'covidincidence'},axis=1,inplace=True)


# In[89]:


idhm_pe_merge_pop


# [Bivariate LISA](http://pysal.org/notebooks/viz/splot/esda_morans_viz.html)

# ## 1) Moran and LISA 

# ## 1.1) y = idhm_pe_merge_pop['finalresultdummy']
# 
# ## 1.2) y = idhm_pe_merge_pop['IDHM']
# 
# ## 1.3) y = idhm_pe_merge_pop['covidincidence']

# In[90]:


#I have to find all notebooks in pysal.org, it might have all spatial models


# In[91]:


#run one of the letters


# In[92]:


#a)


# ## 1.1) y = idhm_pe_merge_pop['finalresultdummy']

# In[93]:


y = idhm_pe_merge_pop['finalresultdummy'].values
w = Queen.from_dataframe(idhm_pe_merge_pop)
w.transform = 'r'


# In[94]:


from esda.moran import Moran

w = Queen.from_dataframe(idhm_pe_merge_pop)
moran = Moran(y, w)
moran.I


# In[95]:


from splot.esda import moran_scatterplot


# In[96]:


fig, ax = moran_scatterplot(moran, aspect_equal=True)
plt.show()


# In[97]:


from splot.esda import plot_moran

plot_moran(moran, zstandard=True, figsize=(10,4))
plt.show()


# In[98]:


moran.p_sim


# In[99]:


from splot.esda import moran_scatterplot
from esda.moran import Moran_Local

# calculate Moran_Local and plot
moran_loc = Moran_Local(y, w)
fig, ax = moran_scatterplot(moran_loc)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[100]:


fig, ax = moran_scatterplot(moran_loc, p=0.05)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[101]:


from splot.esda import lisa_cluster

lisa_cluster(moran_loc, idhm_pe_merge, p=0.05, figsize = (12,12))
plt.title('LISA Covid Cases')
'''font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}
plt.rc('font', **font)
'''
#plt.rcParams.update({'font.size': 16})
plt.margins(0.22)
plt.show()


# In[102]:


from splot.esda import plot_local_autocorrelation
plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'finalresultdummy')
plt.rcParams.update({'font.size': 9})
plt.show()


# In[103]:


plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'finalresultdummy', quadrant=1)
plt.show()


# # 1.2) y = idhm_pe_merge_pop['IDHM']

# In[164]:


y = idhm_pe_merge_pop['IDHM'].values
w = Queen.from_dataframe(idhm_pe_merge_pop)
w.transform = 'r'


# In[165]:


from esda.moran import Moran

w = Queen.from_dataframe(idhm_pe_merge_pop)
moran = Moran(y, w)
moran.I


# In[166]:


from splot.esda import moran_scatterplot


# In[167]:


fig, ax = moran_scatterplot(moran, aspect_equal=True)
plt.show()


# In[168]:


from splot.esda import plot_moran

plot_moran(moran, zstandard=True, figsize=(10,4))
plt.show()


# In[169]:


moran.p_sim


# In[170]:


from splot.esda import moran_scatterplot
from esda.moran import Moran_Local

# calculate Moran_Local and plot
moran_loc = Moran_Local(y, w)
fig, ax = moran_scatterplot(moran_loc)
ax.set_xlabel('IDHM')
ax.set_ylabel('Spatial Lag of IDHM')
plt.show()


# In[171]:


fig, ax = moran_scatterplot(moran_loc, p=0.05)
ax.set_xlabel('IDHM')
ax.set_ylabel('Spatial Lag of IDHM')
plt.show()


# In[172]:


from splot.esda import lisa_cluster

lisa_cluster(moran_loc, idhm_pe_merge, p=0.05, figsize = (12,12))
plt.title('LISA IDHM')
'''font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}
plt.rc('font', **font)
'''
#plt.rcParams.update({'font.size': 16})
plt.margins(0.22)
plt.show()


# In[173]:


from splot.esda import plot_local_autocorrelation
plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'IDHM')
plt.rcParams.update({'font.size': 9})
plt.show()


# In[174]:


plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'IDHM', quadrant=1)
plt.show()


# ## 1.3) y = idhm_pe_merge_pop['covidincidence']

# In[189]:


y = idhm_pe_merge_pop['covidincidence'].values
w = Queen.from_dataframe(idhm_pe_merge_pop)
w.transform = 'r'


# In[190]:


from esda.moran import Moran

w = Queen.from_dataframe(idhm_pe_merge_pop)
moran = Moran(y, w)
moran.I


# In[191]:


from splot.esda import moran_scatterplot


# In[192]:


fig, ax = moran_scatterplot(moran, aspect_equal=True)
plt.show()


# In[193]:


from splot.esda import plot_moran

plot_moran(moran, zstandard=True, figsize=(10,4))
plt.show()


# In[194]:


moran.p_sim


# In[195]:


from splot.esda import moran_scatterplot
from esda.moran import Moran_Local

# calculate Moran_Local and plot
moran_loc = Moran_Local(y, w)
fig, ax = moran_scatterplot(moran_loc)
ax.set_xlabel('Covid Incidence')
ax.set_ylabel('Spatial Lag of Covid Incidence')
plt.show()


# In[196]:


fig, ax = moran_scatterplot(moran_loc, p=0.05)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Incidence')
plt.show()


# In[197]:


from splot.esda import lisa_cluster

lisa_cluster(moran_loc, idhm_pe_merge, p=0.05, figsize = (12,12))
plt.title('LISA Covid Incidence')
'''font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}
plt.rc('font', **font)
'''
plt.rcParams.update({'font.size': 12})
plt.margins(0.22)
plt.show()


# In[198]:


from splot.esda import plot_local_autocorrelation
plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'covidincidence')
plt.show()


# In[199]:


plot_local_autocorrelation(moran_loc, idhm_pe_merge_pop, 'covidincidence', quadrant=1)
plt.show()


# ## 2) Bivariate LISA 
# ## 2.1) y=finalresultdummy x=IDHM
# ## 2.2) y=covidincidence x=IDHM

# In[ ]:





# ## 2.1) y=finalresultdummy x=IDHM

# In[213]:


y = idhm_pe_merge_pop['covid cases'].values
w = Queen.from_dataframe(idhm_pe_merge_pop)
w.transform = 'r'


# In[214]:


from esda.moran import Moran

w = Queen.from_dataframe(idhm_pe_merge_pop)
moran = Moran(y, w)
moran.I


# In[215]:


from esda.moran import Moran_BV, Moran_Local_BV
from splot.esda import plot_moran_bv_simulation, plot_moran_bv


# In[216]:


x = idhm_pe_merge_pop['IDHM'].values


# In[217]:


moran = Moran(y,w)
moran_bv = Moran_BV(y, x, w)
moran_loc = Moran_Local(y, w)
moran_loc_bv = Moran_Local_BV(y, x, w)


# In[218]:


fig, axs = plt.subplots(2, 2, figsize=(15,10),
                        subplot_kw={'aspect': 'equal'})

moran_scatterplot(moran, ax=axs[0,0])
moran_scatterplot(moran_loc, p=0.05, ax=axs[1,0])
moran_scatterplot(moran_bv, ax=axs[0,1])
moran_scatterplot(moran_loc_bv, p=0.05, ax=axs[1,1])
plt.show()


# In[219]:


plot_moran_bv(moran_bv)
plt.show()


# In[220]:


from esda.moran import Moran_Local_BV


# In[221]:


moran_loc_bv = Moran_Local_BV(x, y, w)
fig, ax = moran_scatterplot(moran_loc_bv, p=0.05)
ax.set_xlabel('IDHM')
ax.set_ylabel('Spatial lag of Covid Cases')
plt.show()


# In[222]:


plot_local_autocorrelation(moran_loc_bv, idhm_pe_merge_pop, 'covidincidence')
plt.show()


# ## 2.2) y=covidincidence x=IDHM

# In[223]:


y = idhm_pe_merge_pop['covidincidence'].values
w = Queen.from_dataframe(idhm_pe_merge_pop)
w.transform = 'r'


# In[224]:


from esda.moran import Moran

w = Queen.from_dataframe(idhm_pe_merge_pop)
moran = Moran(y, w)
moran.I


# In[225]:


from esda.moran import Moran_BV, Moran_Local_BV
from splot.esda import plot_moran_bv_simulation, plot_moran_bv


# In[226]:


x = idhm_pe_merge_pop['IDHM'].values


# In[227]:


moran = Moran(y,w)
moran_bv = Moran_BV(y, x, w)
moran_loc = Moran_Local(y, w)
moran_loc_bv = Moran_Local_BV(y, x, w)


# In[228]:


fig, axs = plt.subplots(2, 2, figsize=(15,10),
                        subplot_kw={'aspect': 'equal'})

moran_scatterplot(moran, ax=axs[0,0])
moran_scatterplot(moran_loc, p=0.05, ax=axs[1,0])
moran_scatterplot(moran_bv, ax=axs[0,1])
moran_scatterplot(moran_loc_bv, p=0.05, ax=axs[1,1])
plt.show()


# In[229]:


plot_moran_bv(moran_bv)
plt.show()


# In[230]:


from esda.moran import Moran_Local_BV


# In[231]:


moran_loc_bv = Moran_Local_BV(x, y, w)
fig, ax = moran_scatterplot(moran_loc_bv, p=0.05)
ax.set_xlabel('IDHM')
ax.set_ylabel('Spatial lag of Covid Incidence')
plt.show()


# In[232]:


plot_local_autocorrelation(moran_loc_bv, idhm_pe_merge_pop, 'IDHM')
plt.show()


# ### 3) Spatial Regressions OLS, SEM, SAR 
# ### 3.1) x=IDHM y=covid cases
# ### 3.2) x=IDHM y=covidincidence

# In[233]:


# Load libraries
import numpy as np
import pandas as pd
import seaborn as sns

#sns.set_style('darkgrid')
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


# In[234]:


idhm_pe_merge_pop.crs


# In[235]:


#W = weights.KNN.from_dataframe(idhm_pe_merge, k=8)
#W = weights.KNN.from_dataframe(gdf, k=6)
#W = weights.KNN.from_dataframe(gdf, k=4)


W = weights.Queen.from_dataframe(idhm_pe_merge)
#W = weights.Rook.from_dataframe(gdf)

# Compute inverse distance squared based on maximum nearest neighbor distance between the n observations 
#maxMin = weights.min_threshold_dist_from_shapefile("map.shp")
#W = weights.DistanceBand.from_dataframe(gdf, threshold = maxMin, binary=False, alpha=-2)

# Row-standardize W
W.transform = 'r'


# In[236]:


plot_spatial_weights(W, idhm_pe_merge_pop)
plt.title('Spatial Queen Matrix For Centroid Neighbors')
plt.rcParams.update({'font.size': 10});


# In[237]:


W.neighbors


# In[238]:


W.min_neighbors


# In[239]:


W.mean_neighbors


# In[240]:


W.max_neighbors


# In[241]:


W.histogram


# In[242]:


idhm_pe_merge_pop.rename({'finalresultdummy':'covid cases'},axis=1,inplace=True)


# ### 3.1) x=IDHM y=covid cases

# In[243]:


y = idhm_pe_merge_pop['covid cases'].values
y_name = 'covid cases'


# In[244]:


x = np.array([idhm_pe_merge_pop.IDHM]).T
x_name = 'IDHM'


# In[245]:


ols = OLS(y = y, x = x, w = W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop', 
          white_test=True, spat_diag=True, moran=True)
print(ols.summary)


# In[247]:


sem = ML_Error(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop')
print(sem.summary)


# In[248]:


sar = ML_Lag(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop')
print(sar.summary)


# # 3.2) x=IDHM y=covid incidence

# In[250]:


y = idhm_pe_merge_pop['covidincidence'].values
y_name = 'covidincidence'


# In[251]:


x = np.array([idhm_pe_merge_pop.IDHM]).T
x_name = 'IDHM'


# In[252]:


ols = OLS(y = y, x = x, w = W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop', 
          white_test=True, spat_diag=True, moran=True)
print(ols.summary)


# In[253]:


sem = ML_Error(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop')
print(sem.summary)


# In[254]:


sar = ML_Lag(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='idhm_pe_merge_pop')
print(sar.summary)


# In[ ]:





# In[255]:


idhm_pe_merge_pop.head(3)


# In[256]:


idhm_pe_merge_pop = idhm_pe_merge_pop.loc[:,['NM_MUN','covid cases','IDHM','estimatedpop','covidincidence']]


# In[257]:


idhm_pe_merge_pop.head(3)


# In[258]:


idhm_pe_merge_pop.rename({'NM_MUN':'Municipality','covid cases':'Covid Cases','estimatedpop':'Estimated Population','covidincidence':'Covid Incidence'},axis=1,inplace=True)


# In[259]:


idhm_pe_merge_pop


# In[261]:


pd.set_option('display.max_rows',None)


# In[262]:


idhm_pe_merge_pop['Covid Incidence'] = idhm_pe_merge_pop['Covid Incidence'].round(2) 


# In[263]:


idhm_pe_merge_pop


# In[264]:


(32/3061)*1000


# In[265]:


#Municipality: Fernando De Noronha, Covid Cases: 32, IDHM: 0.788, Estimated Population: 3061 , Covid Incidence: 10.45


# In[266]:


idhm_pe_merge_pop = idhm_pe_merge_pop.append({'Municipality':'Fernando De Noronha', 'Covid Cases':'32','IDHM':'0.788','Estimated Population':'3061','Covid Incidence':'10.45'},ignore_index=True)


# In[267]:


idhm_pe_merge_pop


# In[268]:


idhm_pe_merge_pop = idhm_pe_merge_pop.sort_values('Municipality').reset_index(drop=True)


# In[269]:


idhm_pe_merge_pop


# In[270]:


#idhm_pe_merge_pop.loc['184'] = idhm_pe_merge_pop({'Municipality':'Fernando De Noronha', 'Covid Cases':'32','IDHM':'0.788','Estimated Population':'3061','Covid Incidence':'10.45'})


# In[271]:


'''
Como variável independente, foi utilizado o desenvolvimento social, sendo a variável
IDHM estimada para cada município no ano de 2010, conforme disponível no PNUD.
O IDHM pode ser classificado em muito baixo (0 a 0,499), baixo (0,500 a 0,599), médio (0,600
a 0,699), alto (0,700 a 0,799) e muito alto (0,800 a 1). O IDHM sintetiza em uma média de
três subíndices, calculados na base de poucos indicadores facilmente coletados nas diversas
nações, três dimensões básicas e universais da vida, que são as condições para que as escolhas
e oportunidades dos indivíduos possam ser ampliadas: o acesso ao conhecimento (educação),
o direito a uma vida longa e saudável (longevidade) e o direito a um padrão de vida
digno (renda).
'''


# In[ ]:




