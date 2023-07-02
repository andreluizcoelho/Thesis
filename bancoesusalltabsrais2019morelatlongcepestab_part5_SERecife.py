#!/usr/bin/env python
# coding: utf-8

# # Spatial Econometrics_Recife_article3

# API reference Spreg [commands](https://pysal.org/spreg/api.html)

# In[2]:


pip install giddy


# In[1]:


pip install rasterio


# In[1]:


pip install GDAL


# In[2]:


pip install Rtree


# In[1]:


pip install pysal


# In[1]:


import pysal as ps


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


bancoesusalltabsrais2019morelatlongcepestabselected1 = pd.read_csv('bancoesusalltabsrais2019morelatlongcepestabselected_part1.csv')


# In[5]:


bancoesusalltabsrais2019morelatlongcepestabselected1.shape


# In[6]:


bancoesusalltabsrais2019morelatlongcepestabselected1.head(3)


# In[7]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[8]:


bairrosgeojson


# In[9]:


bairrosgeojson.plot();


# In[10]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.title()


# In[11]:


bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'] = bancoesusalltabsrais2019morelatlongcepestabselected1['bairro'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# In[12]:


bairrosgeojson['bairro_nome_ca'] = bairrosgeojson['bairro_nome_ca'].str.title()


# In[13]:


bairrosgeojson


# In[14]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge = bairrosgeojson.merge(bancoesusalltabsrais2019morelatlongcepestabselected1, left_on='bairro_nome_ca', right_on='bairro',how='inner',indicator=True)


# In[15]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.shape


# In[16]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.head(3)


# In[17]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['final result']


# In[18]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].unique()


# In[19]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].replace({'negative':'0','Null':'0','positive':'1'},inplace=True)


# In[20]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].value_counts()


# In[21]:


bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'] = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge['finalresultdummy'].astype(int)


# In[22]:


#to do the same thing as for PE IDHM and estimatedpop per bairro is needed
#either try to get them, or just use finalresultdummy without the two varaibles above


# In[23]:


bairrocovidsum = bancoesusalltabsrais2019morelatlongcepestabselected1recifemerge.groupby(by='bairro').sum()


# In[24]:


bairrocovidsum.head()


# In[25]:


bairrocovidsum.reset_index(level=0,inplace=True)


# In[26]:


bairrocovidsum.head()


# In[27]:


bairrocovidsum.loc[:,['bairro','Health Professionals', 'Security Professionals','sex','finalresultdummy']]


# In[28]:


bairroscovidsumsomecols = bairrocovidsum.loc[:,['bairro','Health Professionals','Security Professionals','sex','finalresultdummy']]


# In[29]:


bairroscovidsumsomecols 


# In[30]:


bairrosgeojson


# In[31]:


bairromergesumcovidmerge=bairrosgeojson.merge(bairroscovidsumsomecols, left_on='bairro_nome_ca',right_on='bairro',how='inner',indicator=True)


# In[32]:


bairromergesumcovidmerge.shape


# In[33]:


bairromergesumcovidmerge.head(3)


# In[34]:


bairromergesumcovidmerge.plot();


# In[35]:


bairromergesumcovidmerge.plot(cmap='gist_gray', column='bairro', figsize=(10,10),legend=True);


# In[36]:


bairromergesumcovidmerge['finalresultdummy'].sum()


# In[37]:


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


# In[38]:


bairromergesumcovidmerge.drop(['_merge'],axis=1,inplace=True)


# In[39]:


bairromergesumcovidmerge.shape


# In[40]:


bairromergesumcovidmerge.head(3)


# ## 1) Moran and Lisa y = bairromergesumcovidmerge[finalresultdummy]

# In[41]:


y = bairromergesumcovidmerge['finalresultdummy'].values
w = Queen.from_dataframe(bairromergesumcovidmerge)
w.transform = 'r'


# In[42]:


from esda.moran import Moran

w = Queen.from_dataframe(bairromergesumcovidmerge)
moran = Moran(y, w)
moran.I


# In[43]:


from splot.esda import moran_scatterplot


# In[44]:


fig, ax = moran_scatterplot(moran, aspect_equal=True)
plt.show()


# In[45]:


from splot.esda import plot_moran

plot_moran(moran, zstandard=True, figsize=(10,4))
plt.show()


# In[46]:


moran.p_sim


# In[47]:


#not significant


# In[48]:


#how many municipalities in PE do not have data if death is used as y value?


# In[49]:


from splot.esda import moran_scatterplot
from esda.moran import Moran_Local

# calculate Moran_Local and plot
moran_loc = Moran_Local(y, w)
fig, ax = moran_scatterplot(moran_loc)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[50]:


fig, ax = moran_scatterplot(moran_loc, p=0.05)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[51]:


from splot.esda import lisa_cluster

lisa_cluster(moran_loc, bairromergesumcovidmerge, p=0.05, figsize = (12,12))
plt.title('LISA Covid Cases')
'''font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}
plt.rc('font', **font)
'''
plt.rcParams.update({'font.size': 12})
plt.margins(0.22)
plt.show()


# In[52]:


from splot.esda import plot_local_autocorrelation
plot_local_autocorrelation(moran_loc, bairromergesumcovidmerge, 'finalresultdummy')
plt.rcParams.update({'font.size': 9})
plt.show()


# # 2) Bivariate LISA  y=finalresultdummy x=sex

# In[53]:


y =bairromergesumcovidmerge['finalresultdummy'].values
w = Queen.from_dataframe(bairromergesumcovidmerge)
w.transform = 'r'


# In[54]:


from esda.moran import Moran

w = Queen.from_dataframe(bairromergesumcovidmerge)
moran = Moran(y, w)
moran.I


# In[55]:


from esda.moran import Moran_BV, Moran_Local_BV
from splot.esda import plot_moran_bv_simulation, plot_moran_bv


# In[56]:


x = bairromergesumcovidmerge['sex'].values


# In[57]:


moran = Moran(y,w)
moran_bv = Moran_BV(y, x, w)
moran_loc = Moran_Local(y, w)
moran_loc_bv = Moran_Local_BV(y, x, w)


# In[58]:


fig, axs = plt.subplots(2, 2, figsize=(15,10),
                        subplot_kw={'aspect': 'equal'})

moran_scatterplot(moran, ax=axs[0,0])
moran_scatterplot(moran_loc, p=0.05, ax=axs[1,0])
moran_scatterplot(moran_bv, ax=axs[0,1])
moran_scatterplot(moran_loc_bv, p=0.05, ax=axs[1,1])
plt.show()


# In[59]:


plot_moran_bv(moran_bv)
plt.show()


# In[60]:


from esda.moran import Moran_Local_BV


# In[61]:


moran_loc_bv = Moran_Local_BV(x, y, w)
fig, ax = moran_scatterplot(moran_loc_bv, p=0.05)
ax.set_xlabel('Sex')
ax.set_ylabel('Spatial lag of Covid Cases')
plt.show()


# In[62]:


plot_local_autocorrelation(moran_loc_bv, bairromergesumcovidmerge, 'finalresultdummy')
plt.show()


# # 3) Spatial Regressions OLS, SEM, SAR 
# ### 3.1) x=sex y=covid cases

# In[63]:


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
from libpysal import weights
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


# In[64]:


bairromergesumcovidmerge.crs


# In[65]:


#W = weights.KNN.from_dataframe(idhm_pe_merge, k=8)
W = weights.KNN.from_dataframe(bairromergesumcovidmerge,k=8)

#W = weights.KNN.from_dataframe(gdf, k=6)
#W = weights.KNN.from_dataframe(gdf, k=4)


'''W = weights.Queen.from_dataframe(bairromergesumcovidmerge)'''
#W = weights.Rook.from_dataframe(gdf)

# Compute inverse distance squared based on maximum nearest neighbor distance between the n observations 
#maxMin = weights.min_threshold_dist_from_shapefile("map.shp")
#W = weights.DistanceBand.from_dataframe(gdf, threshold = maxMin, binary=False, alpha=-2)

# Row-standardize W
W.transform = 'r'


# In[66]:


plot_spatial_weights(W, bairromergesumcovidmerge)
plt.title('Spatial Queen Matrix For Centroid Neighbors')
plt.rcParams.update({'font.size': 10});


# In[67]:


W.neighbors


# In[68]:


W.min_neighbors


# In[69]:


W.mean_neighbors


# In[70]:


W.max_neighbors


# In[71]:


W.histogram


# In[72]:


bairromergesumcovidmerge.rename({'finalresultdummy':'covid cases'},axis=1,inplace=True)


# In[73]:


y = bairromergesumcovidmerge['covid cases'].values
y_name = 'covid cases'


# In[74]:


x = np.array([bairromergesumcovidmerge.sex]).T
x_name = 'sex'


# In[1]:


#ols


# In[75]:


ols = OLS(y = y, x = x, w = W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bairromergesumcovidmerge', 
          white_test=True, spat_diag=True, moran=True)
print(ols.summary)


# In[2]:


#sem


# In[76]:


sem = ML_Error(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bairromergesumcovidmerge')
print(sem.summary)


# In[3]:


#sar


# In[77]:


sar = ML_Lag(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bairromergesumcovidmerge')
print(sar.summary)


# In[78]:


#the results were not significant


# ### SLX with the aggregated data

# [Spatial Regression examples including SLX](https://geographicdata.science/book/notebooks/11_regression.html)

# [Spatial Regression examples darribas](http://darribas.org/gds_scipy16/ipynb_md/08_spatial_regression.html)

# [pysal doc, slides, etc tutorials](https://access.readthedocs.io/en/latest/tutorials.html)

# API reference [Accessibility Class](https://access.readthedocs.io/en/latest/api.html)

# API reference [Spatial Regression Models](https://pysal.org/spreg/api.html)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## Spatial two stage least squares (S2SLS)

# [API reference Spatial Regression Models](https://pysal.org/spreg/api.html)

# [spreg.GM_Lag](https://pysal.org/spreg/generated/spreg.GM_Lag.html)

# Luc Anselin youtube video S2SLS part [1](https://www.youtube.com/watch?v=7HecdApU_x8)

# Luc Anselin youtube video S2SLS part [2](https://www.youtube.com/watch?v=sUa-N273SoA)

# Luc Anselin youtube video S2SLS [1:17:54 video](https://www.youtube.com/watch?v=Y56HymHrQLw)

# In[ ]:


'''
the instruments are uncorrelated with the error term, because the X are exogenous
the instruments should be correlated with the endogenous variables, but not too correlated, otherwise it would be the same as the 
endogenous variables
Assumptions: plim(l/n)Q'Z = Hqz finite and full column rank
requires at least one exogenous xk, other than constant
S2SLS does not work for pure SAR model
identifiability condition precludes H0:B=0
Spatial 2SLS Estimation:
standard result, with instruments 
Q=[X,WX,W^2X,...]
for homoskedastic, uncorrelated errors
consistent, but not most efficient, this is the trade-off of switching from ML estimator
if the assumptions hold the best estimator is the maximumlikehood estimator

instruments kelejian and Prucha (1999)
instruments Q = [X, WX, W2X...]
in practice we use the exogenous variables, the spatial lag, and then move on to the spatial 2 stage least squares
'''


# Spatial Data Science University of [Chicago](https://spatial.uchicago.edu/) 

# Spatial Data Science University of Chicago [Datasets](https://geodacenter.github.io/data-and-lab//)

# University of Chicago [S2SLS pdf](https://spatial.uchicago.edu/sites/spatial.uchicago.edu/files/11_spatial2sls_slides.pdf)

# some latex commands for jupyter notebook [python](https://personal.math.ubc.ca/~pwalls/math-python/jupyter/latex/)

# Spatial 2SLS example in [Python](https://pysal.org/spreg/notebooks/GM_Lag_example.html)

# In[1]:


import numpy as np 
import libpysal
import spreg


# In[2]:


libpysal.examples.explain("baltim")


# In[3]:


# Read Baltimore data
db = libpysal.io.open(libpysal.examples.get_path("baltim.dbf"), "r")
ds_name = "baltim.dbf"

# Read dependent variable
y_name = "PRICE"
y = np.array(db.by_col(y_name)).T
y = y[:, np.newaxis]

# Read exogenous variables
x_names = ["NROOM", "NBATH", "PATIO", "FIREPL", "AC", "GAR", "AGE", "LOTSZ", "SQFT"]
x = np.array([db.by_col(var) for var in x_names]).T


# In[4]:


# Read spatial data
ww = libpysal.io.open(libpysal.examples.get_path("baltim_q.gal"))
w = ww.read()
ww.close()
w_name = "baltim_q.gal"
w.transform = "r"


# Basic Spatial 2SLS
# The model to estimate is: 
#                                     $$y = \rho Wy + X\beta + \epsilon$$
#                                     
# where you use WX as instruments of Wy

# Wy endogenous = simultaneous equation bias
# $$y = Z\theta + u$$
# $$Z = [WyX]$$
# $$\theta = [\rho\beta']'$$

# In[5]:


model = spreg.GM_Lag(
    y,
    x,
    w=w,
    name_y=y_name,
    name_x=x_names,
    name_w="baltim_q",
    name_ds="baltim"
)
print(model.summary)


# Second order spatial lags
# You can also use [WX, W^2X] as instruments of Wy. 

# In[6]:


# using second order spatial lags for the instruments, set w_lags = 2
model2 = spreg.GM_Lag(
    y,
    x,
    w=w,
    w_lags=2,
    name_y=y_name,
    name_x=x_names,
    name_w="baltim_q",
    name_ds="baltim"
)
print(model2.summary)


# Spatial Diagnostics

# In[7]:


model = spreg.GM_Lag(
    y,
    x,
    w=w,
    spat_diag=True,
    name_y=y_name,
    name_x=x_names,
    name_w="baltim_q",
    name_ds="baltim"
)
print(model.summary)


# In[ ]:


#Anselin-Kelejian Test is a test for remaining error autocorrelation in the lag model
#I mean this happens to be a lag model you test is the remaining error correlation there isnt't really evidence of that
#so if there isnst any error atucolletation the correction for the hack versus the correction for the white is not 
#going to make a big difference

#the houseman type test could compare the standard errors for the hac with the white and so but
#intuitivelly you know if you have a serious problem of spatial autocorrelation in addition to heteroscedasticity then 
#the hack correction will make a difference but if there isn't much of a spatial problem then the mais problem is the 
#heteroskedasticity and then the white correction will do the trick basically and since the hack correction is in superset
#of the white correction so it's white plus the spatial part right so if the spatial part doesn't matter very much 
#they're basically going to be the same but if the spatial part does matter this is a way to avoid having to estimate 
#a higher-order model in if you are not particularly interested in the particular coefficient but you just want to have
#the inference correct to standard errors correct this is how you approach. 
#it's easy to stick in the instruments , the estimates does not change much between hac and white standard errors, 
#the standard errors change


# White Standard Errors

# In[8]:


model = spreg.GM_Lag(
    y,
    x,
    w=w,
    robust="white",
    spat_diag=True,
    name_y=y_name,
    name_x=x_names,
    name_w="baltim_q",
    name_ds="baltim"
)
print(model.summary)


# In[17]:


'''
notes from Spatial Two Stage Least Squares video: https://www.youtube.com/watch?v=Y56HymHrQLw

estimates with different spatial lag orders for the instruments OLS, Lag 1, Lag 2, Lag 3, ML
if ML assumptions are satisfied, and if using optiomal instruments, non-normality and heterocedaskicity
if ML and lags 1,2,3 are not similar the assumptions from ML are not satisfied
lag 1,2,3 is more robust when using robust standard errors, works good with heterocedasticity unlike ML

Spatial 2SLS with Additional Endogenous Variables
not onl Wy endogenous but also some of the Z
y = rhoWy + Xbeta + Ygama + u, 
instruments for the other endogenous variables
 instruments and their spatial lags 
the tricky part is which are the instruments and if they are really exogenous

Best and Optimal Estimators
Optimal Instrument Maxis (Lee 2003)
 Q=[X,W(I-rhoW)-1XBeta]
 using consistent estimates for rho and beta from first stage estimation 
 requires inverse of n by n matrix
 yields Best 2SLS
 
Best 2SLS (Keleijan et al 2004)
 avoids inverse matrix
 exploits the usual series expansion
 Q = [X,sums=0rho^sW^s+1Xbeta]
 rho and B from frist stage estimation 
 approximation up to s = r = o(n^1/2)

Optimal GMM (Lee 2006)
 general set of moment conditions
 E[Q'u]=0
 E[u'Pu]=simga^2trP=0
 matrices PindexI with trace 0 and matrices Pindex2 with diagonal zero
 
 the instrument needs to be uncorrelated with the error term
 
Optimal GMM 
 examples of matrix P 
 W: diagonal zero 
 W^2 - [trW^2)/2]ln: trace zero
 optimal GMM is consistent and asymptotically normal 
 for normal error terms OGMM has tsame limiting distribution as MLE
 
HAC (it deals with the endogeneity of the spatial lag dependent variable and also with the heterokedasticity, what you have to 
do in the Maximum Likelihood)
Consistent Covariance Estimate

General Covariance Structure
 y = XB + u, E[uu']=sum(greek letter)
  both heteroskedasticity and autocorrelation
  Var[betaols]= (l/n)(l/nX'X)-1(l/n X'sumX)(l/nX'X)-1
  
Heteroskedastic-Consistent Covariance Estimation (White 1980)
 sum = diag(sigmai^2) different variance for each i
  plim (l/n)X'sumX = l/nsumisigmai^2xixi'
  no separate estimator for each sigmai^2
  
Spatial Lag with Heteroskedasticity 
 White (1980) correction for 2SLS estimation
 coefficient variance for general error covariance structure
 
Temporal Correlation 
 Newey-West (87), Andrews(91)
  too many terms to estimate; average is over n but there are n^2 covariance terms
  
 impose structure
  no temporal correlation beyond a given time
  decay in the correlation as the time lag is larger
 estimate must yield a positive definite covariance matrix
 
Heteroskedastic and Temporal Consistent 

 bartlett weights
 
Spatial HAC
 Spatial Covariance Estimator
  same principle as for temporal correlation 
  average of sample spatial covariances up to a distance cut-off
  zero covariance beyond cut-ff
  
Implementation on a Grid
 Conley (1999)
 observations arranged on M by N grid
 Bartlett window analogue of time series
  a proper choice of Lm and Ln, weights ensures that variance covariance matrix is positive definite
  
Generalization - Kelejian and Pruch (2006)
 error terms u = Repsilon, R unknown
 GMM setup with instrument matrix H
 using Kernel function 
 
Examples of Kernel Functions
Truncated, Uniform
Triangular, Bartlett
Epanechnikov, Quadratic
Quartic, Biweight, Bisquare
Parzen

Gaussian, Normal

Spatial HAC Estimator

White and HAC standard errors

White standard errors is correction for heterokedasticity only 
HAC standard error is correction for both heteroskedasticity and spatial autocorrelation for unknown form

HAC approach is a local spatial autocorrelation
if we have a strong autocorrelation process, it's actually a global spatial autocorrelation structure


'''


# HAC estimator [paper](http://econweb.umd.edu/~prucha/papers/JE140(2007b).pdf)

# ## Applying 2SLS on the data

# Spatial 2SLS [example](https://pysal.org/spreg/notebooks/GM_Lag_example.html)

# ## Trying to make spatial weight matrix for individual data 

# In[1]:


import pandas as pd


# In[2]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[3]:


organizeddataRecifeCNAE


# In[4]:


pd.set_option('display.max_columns',None)


# In[5]:


organizeddataRecifeCNAE.head(3)


# In[6]:


organizeddataRecifeCNAE.columns


# In[7]:


organizeddataRecifeCNAE.dtypes


# In[8]:


organizeddataRecifeCNAE['Final Result']


# In[9]:


organizeddataRecifeCNAE.rename({'Final Result':'y'}, axis = 1, inplace = True)


# In[10]:


organizeddataRecifeCNAE.y


# In[11]:


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
from libpysal import weights
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

import pandas as pd
from shapely.geometry import Point
from geopandas import GeoDataFrame


# In[12]:


organizeddataRecifeCNAE['longitude']


# In[13]:


crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(organizeddataRecifeCNAE['longitude'], organizeddataRecifeCNAE['latitude'])]
geometry[:5]


# In[14]:


organizeddataRecifeCNAEGeoDataFrame = gpd.GeoDataFrame(organizeddataRecifeCNAE, crs = crs, geometry = geometry)
organizeddataRecifeCNAEGeoDataFrame.head()


# In[15]:


organizeddataRecifeCNAEGeoDataFrame.shape


# In[16]:


organizeddataRecifeCNAEGeoDataFrame.plot(cmap='gist_gray', column='bairro_nome', figsize=(10,10),legend=False);
plt.title('Individual Data From Bairros in Recife')


# Pysal [weights](https://pysal.org/notebooks/lib/libpysal/weights.html), nice example

# In[17]:


organizeddataRecifeCNAEGeoDataFrame['y'].values


# Distance Based Statistical Method for Planar Point Patterns, [pysal](https://pysal.org/notebooks/explore/pointpats/distance_statistics.html)

# In[18]:


organizeddataRecifeCNAEGeoDataFrame['geometry'] #x longitude y latitude


# GIS in Python: Intro to Coordinate Reference Systems in [Python](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-vector-data-python/spatial-data-vector-shapefiles/intro-to-coordinate-reference-systems-python/)

# In[19]:


organizeddataRecifeCNAEGeoDataFrame['latitude']


# Pysal weights mexico and rio grande do sul [example](https://pysal.org/notebooks/lib/libpysal/weights.html)

# Spatial weights [pysal](http://darribas.org/gds15/content/labs/lab_05.html), good examples

# libpysal API reference [Spatial Weights](https://pysal.org/libpysal/api.html)

# libpysal.weights.[KNN](https://pysal.org/libpysal/generated/libpysal.weights.KNN.html#libpysal.weights.KNN)

# libpysal.weights.[W](https://pysal.org/libpysal/generated/libpysal.weights.W.html)

# libpysal [inverse distance](https://pysal.org/libpysal/_modules/libpysal/weights/distance.html)

# libpysal inverse distance [example](https://pysal.org/libpysal/generated/libpysal.weights.DistanceBand.html)

# libpysal.weights.[DistanceBand](https://pysal.org/libpysal/generated/libpysal.weights.DistanceBand.html)

# Geographic Data Science with Python [Spatial Weights](https://geographicdata.science/book/notebooks/04_spatial_weights.html)

# darribas [spatial weights](http://darribas.org/gds_scipy16/ipynb_md/03_spatial_weights.html)

# In[20]:


organizeddataRecifeCNAEGeoDataFrame['geometry']


# In[21]:


organizeddataRecifeCNAEGeoDataFrame['geometry'].values


# In[22]:


organizeddataRecifeCNAEGeoDataFrame['geometry'].to_numpy


# In[23]:


organizeddataRecifeCNAEGeoDataFrame['latitude']


# In[24]:


organizeddataRecifeCNAEGeoDataFrame['latitude'].values


# In[25]:


organizeddataRecifeCNAEGeoDataFrame['longitude'].values


# Combine two columns of text in [pandas dataframe](https://stackoverflow.com/questions/19377969/combine-two-columns-of-text-in-pandas-dataframe)

# In[26]:


organizeddataRecifeCNAEGeoDataFrame[['longitude','latitude']].astype(str).agg(','.join,axis=1)


# In[27]:


organizeddataRecifeCNAEGeoDataFrame['points'] = organizeddataRecifeCNAEGeoDataFrame[['longitude','latitude']].astype(str).agg(','.join,axis=1)


# In[28]:


organizeddataRecifeCNAEGeoDataFrame.update('(' + organizeddataRecifeCNAEGeoDataFrame[['points']].astype(str) + '),')


# In[29]:


organizeddataRecifeCNAEGeoDataFrame['points']


# In[30]:


organizeddataRecifeCNAEGeoDataFrame['points'].values


# In[31]:


organizeddataRecifeCNAEGeoDataFrame['points'].to_numpy()


# In[32]:


list(organizeddataRecifeCNAEGeoDataFrame['points'])


# In[33]:


#on anaconda terminal write: jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10


# In[34]:


#pd.set_option('display.max_rows',None)


# In[38]:


print(organizeddataRecifeCNAEGeoDataFrame['points'])    


# In[36]:


#organizeddataRecifeCNAEGeoDataFrame['points'].to_string         the one below is better


# In[37]:


print(organizeddataRecifeCNAEGeoDataFrame['points'].to_string(index=False))    #takes forever to copy


# print a list with integers without the brackets, command and no quotes, [stackoverflow](https://stackoverflow.com/questions/17757450/how-to-print-a-list-with-integers-without-the-brackets-commas-and-no-quotes/17757544)

# In[39]:


print(''.join(map(str,organizeddataRecifeCNAEGeoDataFrame['points'].to_list())))


# In[36]:


#copy all points 


# In[40]:


import libpysal 


# In[41]:


#w=libpysal.weights.DistanceBand(points,threshold=1,binary=False) #inverse distance weights

#MemoryError: bad allocation


# In[45]:


organizeddataRecifeCNAEGeoDataFrame['points'].dtype


# In[46]:


organizeddataRecifeCNAEGeoDataFrame.head(3)


# In[60]:


w=libpysal.weights.KNN(organizeddataRecifeCNAEGeoDataFrame['points'],k=20, p=2)


# In[52]:


#are all bairros correct and inside the border?


# In[55]:


list(organizeddataRecifeCNAEGeoDataFrame['bairro'].unique())


# In[61]:


list(organizeddataRecifeCNAEGeoDataFrame['bairro_nome'].unique())


# In[63]:


organizeddataRecifeCNAEGeoDataFrame[organizeddataRecifeCNAEGeoDataFrame['bairro_nome']=='Peixinhos']


# In[67]:


organizeddataRecifeCNAEGeoDataFrame['municipio'].value_counts()


# In[69]:


organizeddataRecifeCNAEGeoDataFrame['municipio'].value_counts(normalize=True)*100


# In[70]:


organizeddataRecifeCNAEGeoDataFrame[organizeddataRecifeCNAEGeoDataFrame['municipio']=='Recife']


# In[71]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife=organizeddataRecifeCNAEGeoDataFrame[organizeddataRecifeCNAEGeoDataFrame['municipio']=='Recife']


# In[72]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife.shape


# In[73]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife.head(3)


# In[74]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife['bairro_nome'].unique()


# In[76]:


print(''.join(map(str,organizeddataRecifeCNAEGeoDataFrame_onlyRecife['points'].to_list())))


# In[77]:


import libpysal 


# In[ ]:





# In[ ]:





# In[85]:


w=libpysal.weights.DistanceBand(points,threshold=11)


# In[92]:


w_queen = weights.KNN.from_dataframe(organizeddataRecifeCNAEGeoDataFrame_onlyRecife['points'], k=5)
w_queen


# In[93]:


#try all these weight with geometry polygons and not geometry points


# In[94]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[95]:


bairrosgeojson


# In[96]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon = organizeddataRecifeCNAEGeoDataFrame_onlyRecife.merge(bairrosgeojson, how = 'inner', on='bairro_nome',indicator='_merge2')


# In[97]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.shape


# In[98]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.head(3)


# In[104]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon['geometry'] = organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon['geometry_y']


# In[107]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.head(3)


# In[109]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.drop(['geometry_y','_merge2'],axis=1,inplace=True)


# In[112]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.head(3)


# In[110]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.plot();


# In[128]:


#organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.plot(cmap='gist_gray', column='bairro_nome_ca_y', figsize=(10,10),legend=True);


# In[130]:


w_queen = weights.KNN.from_dataframe(organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon['points'], k=5)
w_queen


# In[ ]:


#agrregate groupby making aggregated data, see the other ipynb agg. etc


# In[134]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon.head(3)


# In[132]:


pd.set_option('display.max_columns',None)


# In[141]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD','bairro_nome','points','geometry']].head(3)


# In[142]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon_somecolumn = organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD','bairro_nome','points','geometry']]


# In[145]:


organizeddataRecifeCNAEGeoDataFrame_onlyRecife_geopolygon_somecolumn.groupby('bairro_nome').agg({'Age':'mean', 'Age 2':'mean','Non-white':'sum','White':'sum','Uninformed race':'sum','Complete primary education':'sum','Complete secondary education':'sum','Complete higher education':'sum','Minimum Wage':'mean', 'Accommodation And Food':'sum','Administrative Activities And Complementary Services':'sum','Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'sum','Construction':'sum','Education':'sum','Electricity and Gas':'sum','Extractive Industries':'sum','Human Health and Social Services':'sum','Information And Communication':'sum','Other Service Activities':'sum','Processing Industries':'sum','Professional, Scientific And Technical Activities':'sum','Public Administration':'sum','Public Administration, Defense And Social Security':'sum','Trade; Repair Of Motor Vehicles And Motorcycles':'sum','Transportation, Storage And Mail':'sum','Water, Sewage, Waste Management And Decontamination Activities':'sum','Arts, Culture, Sports And Recreation':'sum','Real Estate Activities':'sum','Financial, Insurance And Related Services Activities':'sum', 'Working hours':'mean','Job tenure':'sum','Distance to CBD':'mean'}).round(2)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[56]:


#merge with the correct bairros and see if the code for individual data runs from inverse distance matrix


# In[ ]:





# In[ ]:





# In[85]:


w


# In[88]:


y = organizeddataRecifeCNAE.y


# In[89]:


moran = Moran(y,w)
moran.I


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[43]:


pd.set_option('display.max_rows',100)


# In[83]:


print(organizeddataRecifeCNAEGeoDataFrame['points'])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


w=libpysal.weights.DistanceBand(points,threshold=11.2,binary=False)


# In[60]:


organizeddataRecifeCNAEGeoDataFrame['latitude'].knn()


# In[52]:


from libpysal.weights import Queen, Rook, KNN


# In[57]:


w = Queen.from_dataframe(organizeddataRecifeCNAEGeoDataFrame['bairro_nome'])


# In[51]:


w = weights.KNN.from_dataframe(organizeddataRecifeCNAEGeoDataFrame, k=2)
w.transform = 'r'


# In[ ]:





# ## Aggregate the data for the Spatial models there needs to be a defined neighbor

# In[1]:


import pandas as pd


# In[2]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[3]:


organizeddataRecifeCNAE


# In[4]:


pd.set_option('display.max_columns',None)


# In[5]:


organizeddataRecifeCNAE.head(3)


# In[6]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[7]:


organizeddataRecifeCNAE['y']


# In[8]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns


# In[9]:


organizeddataRecifeCNAE.shape


# In[10]:


import pandas as pd
import plotly.express as px
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from mpl_toolkits.basemap import Basemap


# In[11]:


import esda
from geopandas import GeoDataFrame
import libpysal as lps
from libpysal.weights import KNN
from shapely.geometry import Point
get_ipython().run_line_magic('matplotlib', 'inline')


# In[12]:


from libpysal.weights.contiguity import Queen
from libpysal import examples
import os
import splot


# In[13]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[14]:


bairrosgeojson


# In[15]:


bairrosgeojson.groupby(by='bairro_nome').sum()


# In[16]:


bairrosgeojson.groupby(by='bairro_nome_ca').sum()


# In[17]:


bairrosgeojson.plot();


# In[18]:


organizeddataRecifeCNAE['bairro']


# In[19]:


organizeddataRecifeCNAE['bairro_nome_ca']


# In[20]:


organizeddataRecifeCNAE['bairro_nome'].unique()


# In[21]:


organizeddataRecifeCNAE.shape


# In[22]:


bairrosgeojson.shape


# In[23]:


organizeddataRecifeCNAE['bairro'].unique()


# In[24]:


organizeddataRecifeCNAE_bairrosgeojsonmerge = organizeddataRecifeCNAE.merge(bairrosgeojson, on='bairro_nome_ca',how='inner',indicator=True)


# In[25]:


organizeddataRecifeCNAE_bairrosgeojsonmerge.shape


# In[26]:


organizeddataRecifeCNAE_bairrosgeojsonmerge.head(3)


# In[27]:


organizeddataRecifeCNAE_bairrosgeojsonmerge.plot();


# In[28]:


organizeddataRecifeCNAE_bairrosgeojsonmerge.groupby(by='bairro_nome_ca').sum()


# In[29]:


organizeddataRecifeCNAE_bairrosgeojsonmerge.groupby(by='bairro_nome_ca').agg({'y':'sum','Age':'mean','Age 2':'mean','Men':'sum','Non-white':'sum','White':'sum','Uninformed race':'mean',
                                                                              'Complete primary education':'sum','Complete secondary education':'sum','Complete higher education':'sum','Minimum Wage':'mean',
                                                                              'Accommodation And Food':'sum','Administrative Activities And Complementary Services':'sum',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'sum','Construction':'sum','Education':'sum', 'Electricity And Gas':'sum',
       'Extractive Industries':'sum','Human Health And Social Services':'sum', 'Information And Communication':'sum',
       'Other Service Activities':'sum', 'Processing Industries':'sum',
       'Professional, Scientific And Technical Activities':'sum',
       'Public Administration, Defense And Social Security':'sum','Trade; Repair Of Motor Vehicles And Motorcycles':'sum',
       'Transportation, Storage And Mail':'sum','Water, Sewage, Waste Management And Decontamination Activities':'sum',
                        'Arts, Culture, Sports And Recreation':'sum','Real Estate Activities':'sum','Financial, Insurance And Related Services Activities':'sum',
                        'Working hours':'mean','Job tenure':'mean','Distance to CBD':'mean'}).round(2)


# In[30]:


organizeddataRecifeCNAE_bairrosgeojsonmerge['Job tenure'].describe()


# In[31]:


598/12


# In[32]:


111/12 #if job tenure is in months


# In[33]:


111/52 #if job tenure is in weeks


# In[34]:


'''
organizeddataRecifeCNAE_bairrosgeojsonmerge[['y','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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
'''


# In[35]:


#organizeddataPEagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[36]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean = organizeddataRecifeCNAE_bairrosgeojsonmerge.groupby(by='bairro_nome_ca').agg({'y':'sum','Age':'mean','Age 2':'mean','Men':'sum','Non-white':'sum','White':'sum','Uninformed race':'mean',
                                                                              'Complete primary education':'sum','Complete secondary education':'sum','Complete higher education':'sum','Minimum Wage':'mean',
                                                                              'Accommodation And Food':'sum','Administrative Activities And Complementary Services':'sum',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'sum','Construction':'sum','Education':'sum', 'Electricity And Gas':'sum',
       'Extractive Industries':'sum','Human Health And Social Services':'sum', 'Information And Communication':'sum',
       'Other Service Activities':'sum', 'Processing Industries':'sum',
       'Professional, Scientific And Technical Activities':'sum',
       'Public Administration, Defense And Social Security':'sum','Trade; Repair Of Motor Vehicles And Motorcycles':'sum',
       'Transportation, Storage And Mail':'sum','Water, Sewage, Waste Management And Decontamination Activities':'sum',
                        'Arts, Culture, Sports And Recreation':'sum','Real Estate Activities':'sum','Financial, Insurance And Related Services Activities':'sum',
                        'Working hours':'mean','Job tenure':'mean','Distance to CBD':'mean'}).round(2)


# In[37]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.head(3)


# In[38]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.shape


# In[39]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.reset_index(level=0,inplace=True)


# In[40]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.head(3)


# In[41]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.plot();


# In[42]:


#get the geometry column polygon from the data to make the plot 


# In[43]:


bairrosgeojson = gpd.read_file('bairros.geojson')


# In[44]:


bairrosgeojson.head(2)


# In[45]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson = organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean.merge(bairrosgeojson, how='inner', on='bairro_nome_ca', indicator=True)


# In[46]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.shape


# In[47]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.head(3)


# In[48]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.plot();


# In[49]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.head(3)


# In[50]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.drop('_merge',axis=1,inplace=True)


# In[51]:


organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson.head(3)


# In[52]:


bairrosgeojson.plot()


# In[53]:


bairrosgeojson.head(3)


# In[54]:


bairrosgeojson.sort_values(by='bairro_nome')


# In[55]:


crs = {'init':'epsg:4326'}


# In[56]:


geometry = organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson['geometry']


# In[57]:


geodataframe = gpd.GeoDataFrame(organizeddataRecifeCNAE_bairrosgeojsonmerge_sum_mean_bairrosgeojson, crs = crs, geometry = geometry)
geodataframe.head()


# In[58]:


geodataframe.shape


# In[59]:


geodataframe.head(3)


# In[60]:


geodataframe.plot(cmap='gist_gray', column='bairro_nome_ca', figsize=(10,10),legend=True);


# In[61]:


f, ax = plt.subplots(1, figsize=(20, 20))
geodataframe.plot(ax=ax, column='Minimum Wage', legend=True, scheme = 'Quantiles', legend_kwds={'fmt':'{:.0f}'}, 
         cmap='binary', edgecolor='k')#, linewidth = 0.1)
ax.set_axis_off()
ax.set_title('Average Minimum Wages For Covid Cases Recife March 2020 until May 8th 2021', fontsize = 15)
plt.axis('equal')
plt.subplots_adjust(left=0.100, bottom=0.66, right=0.6, top=0.9, wspace=0.02, hspace=0.01) #default (left=0.125 [the left side of the subplots of the figure], bottom=0.1 [the bottom of the subplots of the figure], right=0.9 [the right side of the subplots of the figure], top=0.9[the top of the subplots of the figure], wspace=0.2[the amount of width reserved for blank space between subplots], hspace=0.2[the amount of height reserved for white space between subplots])
#plt.xlim(-41.5, -34.5)
#plt.ylim(-10,-4.5)
plt.show()


# In[62]:


#see the the lat and long to leave in the data
#see the spatial econometrics moran, sar, sem, etc
#test the inverse distance matrix


# In[63]:


geodataframe.crs


# In[64]:


#inverse matrix
#w=libpysal.weights.DistanceBand(points,threshold=11.2,binary=False)


# In[65]:


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
from libpysal import weights
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


# In[66]:


W = weights.KNN.from_dataframe(geodataframe,k=8)


# spatial weights [k-nearest neighbors](https://splot.readthedocs.io/en/stable/users/tutorials/weights.html)

# In[67]:


# Row-standardize W
W.transform = 'r'


# In[68]:


plot_spatial_weights(W, geodataframe)
plt.title('Spatial K-Nearest Neighbors Matrix For Centroid Neighbors')
plt.rcParams.update({'font.size': 10});


# In[69]:


W.neighbors


# In[70]:


W.min_neighbors


# In[71]:


W.mean_neighbors


# In[72]:


W.max_neighbors


# In[73]:


W.histogram


# In[74]:


bairrosgeojson


# In[75]:


bairrosgeojson.shape


# In[76]:


geodataframe.head(3)


# In[ ]:





# # Moran and LISA y

# In[77]:


y = geodataframe['y'].values
w = Queen.from_dataframe(geodataframe)
w.transform = 'r'


# In[78]:


from esda.moran import Moran

w = Queen.from_dataframe(geodataframe)
moran = Moran(y, w)
moran.I


# In[79]:


from splot.esda import moran_scatterplot


# In[80]:


fig, ax = moran_scatterplot(moran, aspect_equal=True)
plt.show()


# In[81]:


from splot.esda import plot_moran

plot_moran(moran, zstandard=True, figsize=(10,4))
plt.show()


# In[82]:


moran.p_sim


# In[83]:


#not significant 


# In[84]:


from splot.esda import moran_scatterplot
from esda.moran import Moran_Local

# calculate Moran_Local and plot
moran_loc = Moran_Local(y, w)
fig, ax = moran_scatterplot(moran_loc)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[85]:


fig, ax = moran_scatterplot(moran_loc, p=0.05)
ax.set_xlabel('Covid Cases')
ax.set_ylabel('Spatial Lag of Covid Cases')
plt.show()


# In[86]:


from splot.esda import lisa_cluster

lisa_cluster(moran_loc, geodataframe, p=0.05, figsize = (12,12))
plt.title('LISA Covid Cases')
'''font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 10}
plt.rc('font', **font)
'''
plt.rcParams.update({'font.size': 12})
plt.margins(0.22)
plt.show()


# In[87]:


from splot.esda import plot_local_autocorrelation
plot_local_autocorrelation(moran_loc, geodataframe, 'y')
plt.rcParams.update({'font.size': 9})
plt.show()


# # Bivariate LISA y x=many columns

# In[88]:


y = geodataframe['y'].values
w = Queen.from_dataframe(geodataframe)
w.transform = 'r'


# In[89]:


from esda.moran import Moran

w = Queen.from_dataframe(geodataframe)
moran = Moran(y, w)
moran.I


# In[90]:


from esda.moran import Moran_BV, Moran_Local_BV
from splot.esda import plot_moran_bv_simulation, plot_moran_bv


# In[91]:


x = geodataframe['Distance to CBD'].values


# In[92]:


moran = Moran(y,w)
moran_bv = Moran_BV(y, x, w)
moran_loc = Moran_Local(y, w)
moran_loc_bv = Moran_Local_BV(y, x, w)


# In[93]:


fig, axs = plt.subplots(2, 2, figsize=(15,10),
                        subplot_kw={'aspect': 'equal'})

moran_scatterplot(moran, ax=axs[0,0])
moran_scatterplot(moran_loc, p=0.05, ax=axs[1,0])
moran_scatterplot(moran_bv, ax=axs[0,1])
moran_scatterplot(moran_loc_bv, p=0.05, ax=axs[1,1])
plt.show()


# In[94]:


plot_moran_bv(moran_bv)
plt.show()


# In[95]:


from esda.moran import Moran_Local_BV


# In[96]:


moran_loc_bv = Moran_Local_BV(x, y, w)
fig, ax = moran_scatterplot(moran_loc_bv, p=0.05)
ax.set_xlabel('Distance to CBD')
ax.set_ylabel('Spatial lag of Covid Cases')
plt.show()


# In[97]:


plot_local_autocorrelation(moran_loc_bv, geodataframe, 'y')
plt.show()


# In[ ]:





# # Spatial Regressions OLS, SEM, SAR 

# In[98]:


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
from libpysal import weights
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


# In[99]:


geodataframe.crs


# In[100]:


#W = weights.KNN.from_dataframe(idhm_pe_merge, k=8)
W = weights.KNN.from_dataframe(geodataframe,k=8)

#W = weights.KNN.from_dataframe(gdf, k=6)
#W = weights.KNN.from_dataframe(gdf, k=4)


'''W = weights.Queen.from_dataframe(bairromergesumcovidmerge)'''
#W = weights.Rook.from_dataframe(gdf)

# Compute inverse distance squared based on maximum nearest neighbor distance between the n observations 
#maxMin = weights.min_threshold_dist_from_shapefile("map.shp")
#W = weights.DistanceBand.from_dataframe(gdf, threshold = maxMin, binary=False, alpha=-2)

# Row-standardize W
W.transform = 'r'


# In[101]:


plot_spatial_weights(W, geodataframe)
plt.title('Spatial K-Nearest Neighbors For Centroid Neighbors')
plt.rcParams.update({'font.size': 10});


# In[102]:


#w=libpysal.weights.DistanceBand(neighbors,threshold=11.2,binary=False)


# In[103]:


W.neighbors


# In[104]:


W.min_neighbors


# In[105]:


W.mean_neighbors


# In[106]:


W.max_neighbors


# In[107]:


W.histogram


# In[108]:


y = geodataframe['y'].values
y_name = 'positive cases'


# In[109]:


geodataframe[['Age','Men']]


# In[110]:


geodataframe[['Age','Men']].T


# In[111]:


np.array(geodataframe[['Age','Men']]).T


# In[112]:


'''
x = np.array(geodataframe[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD']]).T
x_name = 'independent variables'
'''


# In[113]:


x = np.array([geodataframe['Men']]).T
x_name = 'Men'


# In[114]:


#ols


# In[115]:


ols = OLS(y = y, x = x, w = W, 
          name_y=y_name, name_x = [x_name], name_w='W', name_ds='geodataframe', 
          white_test=True, spat_diag=True, moran=True)
print(ols.summary)


# In[116]:


#sem


# In[117]:


sem = ML_Error(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='geodataframe')
print(sem.summary)


# In[118]:


#sar


# In[119]:


sar = ML_Lag(y=y, x=x, w=W, 
          name_y=y_name, name_x = [x_name], name_w="W", name_ds='bairromergesumcovidmerge')
print(sar.summary)


# ### test ols, sar, sem with many variables, see somewhere else

# # HERE

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## the inverse distance band getting lat and long then the points from the geodataframe data

# In[ ]:





# ## testing the two stage least squares (S2SLS)

# Spatial [2SLS](https://pysal.org/spreg/notebooks/GM_Lag_example.html)

# In[120]:


import numpy as np 
import libpysal
import spreg


# In[121]:


geodataframe


# In[122]:


geodataframe.columns


# In[123]:


pandasgeodataframe = pd.DataFrame(geodataframe) # this was done because of the error below 'GeoDataFrame' object has no attribute 'by_col'


# In[124]:


pandasgeodataframe.head(3)


# dataframe to [csv](https://towardsdatascience.com/how-to-export-pandas-dataframe-to-csv-2038e43d9c03)

# In[125]:


pandasgeodataframe.to_csv('pandasgeodataframe.csv',index=False,encoding='utf-8')


# In[126]:


#pip install dbf                https://pypi.org/project/dbf/


# In[127]:


import dbf


# In[128]:


import sys


# In[129]:


pandasgeodataframe = pd.read_csv('pandasgeodataframe.csv')


# In[130]:


pandasgeodataframe.shape


# In[131]:


pandasgeodataframe.head(3)


# In[173]:


# importing the module
import sys
       
# fetching the maximum value
max_val = sys.maxsize
print(max_val)


# In[133]:


#pip install dbf --upgrade


# In[134]:


pandasgeodataframe.head(3)


# [_csv.Error: field larger than field limit (131072)](https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072)

# In[172]:


import sys
import csv
maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


# In[174]:


csv.field_size_limit(100000000)


# In[175]:


csv.field_size_limit()


# In[ ]:


#pandasgeodataframe.field_size_limit()


# In[193]:


import dbf

db = dbf.from_csv('pandasgeodataframe.csv',encoding='utf8')


# In[204]:


#db.export(db, 'db.dbf', header=False)


# In[205]:


db


# In[207]:


pandasgeodataframe.info()


# In[180]:


#'DataFrame' object has no attribute 'by_col'          still the same problem, maybe try to convert it to dbf


# [pandas dataframe to dbf file](https://stackoverflow.com/questions/44893505/write-pandas-dataframe-to-dbf-file)

# [pandas to dbf file](https://gis.stackexchange.com/questions/288422/saving-dataframe-as-dbf-with-simpledbf-in-python)

# In[181]:


#from pyGDsandbox.dataIO import df2dbf, dbf2df


# In[182]:


#pandasgeodataframe.to_file('pandas_geodataframe_shapefile.shp')


# In[ ]:





# In[184]:


#pip install libpysal --upgrade


# In[185]:


#pip install region


# In[186]:


#import libpysal.api as ps


# Spatial 2SLS, this is the [code](https://pysal.org/spreg/notebooks/GM_Lag_example.html)

# In[236]:


ds_name=['Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Construction', 'Education', 'Electricity And Gas',
       'Extractive Industries', 'Human Health And Social Services',
       'Information And Communication', 'Other Service Activities',
       'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
       'Arts, Culture, Sports And Recreation', 'Real Estate Activities',
       'Financial, Insurance And Related Services Activities', 'Working hours',
       'Job tenure', 'Distance to CBD']


y_name = ['Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Construction', 'Education', 'Electricity And Gas',
       'Extractive Industries', 'Human Health And Social Services',
       'Information And Communication', 'Other Service Activities',
       'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
       'Arts, Culture, Sports And Recreation', 'Real Estate Activities',
       'Financial, Insurance And Related Services Activities', 'Working hours',
       'Job tenure', 'Distance to CBD']
y = pandasgeodataframe[['Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Construction', 'Education', 'Electricity And Gas',
       'Extractive Industries', 'Human Health And Social Services',
       'Information And Communication', 'Other Service Activities',
       'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
       'Arts, Culture, Sports And Recreation', 'Real Estate Activities',
       'Financial, Insurance And Related Services Activities', 'Working hours',
       'Job tenure', 'Distance to CBD']].values.T
#y = y[:, np.newaxis]

x_names = ['Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Construction', 'Education', 'Electricity And Gas',
       'Extractive Industries', 'Human Health And Social Services',
       'Information And Communication', 'Other Service Activities',
       'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
       'Arts, Culture, Sports And Recreation', 'Real Estate Activities',
       'Financial, Insurance And Related Services Activities', 'Working hours',
       'Job tenure', 'Distance to CBD']
x = pandasgeodataframe[['Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Construction', 'Education', 'Electricity And Gas',
       'Extractive Industries', 'Human Health And Social Services',
       'Information And Communication', 'Other Service Activities',
       'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities',
       'Arts, Culture, Sports And Recreation', 'Real Estate Activities',
       'Financial, Insurance And Related Services Activities', 'Working hours',
       'Job tenure', 'Distance to CBD']].values.T


# In[237]:


w


# In[238]:


w.transform = 'r'


# In[239]:


model = spreg.GM_Lag(
    y,
    x,
    w=w,
    name_y=y_name,
    name_x=x_names,
    name_w='w',
    name_ds='geodataframe'
)
print(model.summary)


# # ONE OR MORE INPUT ARRAYS HAVE MORE COLUMNS THAN ROWS

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


x = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[9]:


import numpy
import libpysal
import spreg


# In[10]:


libpysal.examples.explain("baltim")


# In[11]:


# Read Baltimore data
db = libpysal.io.open(libpysal.examples.get_path("baltim.dbf"), "r")
ds_name = "baltim.dbf"

# Read dependent variable
y_name = "PRICE"
y = numpy.array(db.by_col(y_name)).T
y = y[:, numpy.newaxis]

# Read exogenous variables
x_names = ["NROOM", "NBATH", "PATIO", "FIREPL", "AC", "GAR", "AGE", "LOTSZ", "SQFT"]
x = numpy.array([db.by_col(var) for var in x_names]).T


# In[13]:


db


# In[16]:


# Read spatial data
ww = libpysal.io.open(libpysal.examples.get_path("baltim_q.gal"))
w = ww.read()
ww.close()
w_name = "baltim_q.gal"
w.transform = "r"


# In[17]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ### testing the Spatial Models with the individual data

# #### here is the [page](http://darribas.org/gds_scipy16/ipynb_md/08_spatial_regression.html)

# In[79]:


'''
E and/or Recife
1. Article_1 Question would be PE 

What is the probability of catching covid given the sector the person works and given the individual caracteristics 

That would mean what is the probability of catching covid given the individual works on sector 1  and given his individuals caracteristics for example 

Literature Review: Antonio Paes papers and many others

Method: Conditional Logit

Search Antonio Paes papers for Literature Review, on Conditional Logit, Multinominal Logit and Logit

The Conditional Logit would mean the probability of catching covid given the sectors the person works and given the individual caracteristics

Tatiane said the Y (dependent variables) would have many numbers 1, 2, 3... according to the sectors, but as she showed on the example and also on the 
pptx presentation, the Y would be a choice variable which is a column and that column has numbers based on each sector the person works



Recife 
2. Article_2

How the distance (the distance could be divided by 1km from CBD, 2km, 5km, 10km for example) 
from where the person lives to CBD (Marco Zero) impacts the conditional probability of catching covid /given individual caracteristics
and what sector the person works

Or this distance could be just a column (which already is) to be one of the individual's given caracteristics, but there's the need to separate the distance
by km, 1, 2, 5, 10, which is not separated.

Method: Conditional Logit, focusing more on the distance



PE and/or Recife
3. Article_3

IDHM for Recife, get the data (if there's no IDHM for bairros, get wage) from the bairros and use the spatial models
IDHM for PE, already have the data

Instead of using a Queen Matrix, use the inverse distance, instead of all bairros agregated, every single point could be used to consider
the other points as the individual neighbors, for Recife there are about over 68k rows. How the map would look like with over 68k neighbors, 
she said to used kernel map 

For PE there would be many more neighbors

Spatial Econometrics for PE and/or Recife
Method: OLS, SEM, SAR
Especially Durbin and SLX

SLX measures how the neighbors' characteristics influences the probability of catching covid

Durbin measures the neighbors' spillover 

'''


# In[80]:


'''
SLX measures how the neighbors' characteristics influences the probability of catching covid

Durbin measures the neighbors' spillover 
'''


# In[ ]:





# In[81]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[82]:


organizeddataRecifeCNAE


# In[83]:


pd.set_option('display.max_columns',None)


# In[84]:


organizeddataRecifeCNAE.head(3)


# In[85]:


organizeddataRecifeCNAE['y']


# In[86]:


#y = organizeddataRecifeCNAE['y']


# In[87]:


#y


# In[88]:


x1 = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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


# In[89]:


x1


# In[90]:


y


# In[91]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns


# In[92]:


x=sm.add_constant(x1)
results = sm.OLS(y,x).fit()
results.summary()


# In[141]:


x1 = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Public Administration, Defense And Social Security','Water, Sewage, Waste Management And Decontamination Activities',
                        'Working hours','Job tenure','Distance to CBD']]
y = organizeddataRecifeCNAE['y']


# In[142]:


x=sm.add_constant(x1)
results = sm.OLS(y,x).fit()
results.summary()


# In[143]:


#a bit better result


# # Here

# In[ ]:





# In[93]:


#bairrosgeojson


# In[94]:


#organizeddataRecifeCNAE needs the geometry column, I'm doing without it after I've done with it


# In[95]:


#organizeddataRecifeCNAE.head(3)


# In[96]:


organizeddataRecifeCNAE.shape


# In[97]:


#bairrosgeojson.shape


# In[98]:


#organizedataRecifeCNAE_polygonmerge = organizeddataRecifeCNAE.merge(bairrosgeojson,how='inner',on='bairro_codigo',indicator=True)


# In[99]:


#organizedataRecifeCNAE_polygonmerge.shape


# In[100]:


#organizedataRecifeCNAE_polygonmerge.head(3)


# In[101]:


#organizedataRecifeCNAE_polygonmerge.rename({'geometry':'geometrypoint', 'geometry_y':'geometry'},axis=1,inplace=True)


# In[102]:


#organizedataRecifeCNAE_polygonmerge.head(3)


# In[103]:


#organizedataRecifeCNAE_polygonmerge.rename({'geometry_x':'geometrypoint'},axis=1,inplace=True)


# In[104]:


'''
y = organizedataRecifeCNAE_polygonmerge['y'].values
w = Queen.from_dataframe(organizedataRecifeCNAE_polygonmerge)
w.transform = 'r'
'''
#it's taking forever to run


# In[105]:


#geometry = organizedataRecifeCNAE_polygonmerge['geometrypoint']


# In[106]:


#from shapely.wkt import loads
#gdf.geometry =  organizedataRecifeCNAE_polygonmerge['geometry_x'].apply(loads)


# In[107]:


'''crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(organizedataRecifeCNAE_polygonmerge['longitude'], organizedataRecifeCNAE_polygonmerge['latitude'])]
geometry[:5]
'''


# In[108]:


#organizedataRecifeCNAE_polygonmerge.head(3)


# In[109]:


'''
from shapely import wkt
organizedataRecifeCNAE_polygonmerge['geometry'] = organizedataRecifeCNAE_polygonmerge['geometry'].apply(wkt.loads)
geodataframeRecifeCNAEpolygonmerge = gpd.GeoDataFrame(organizedataRecifeCNAE_polygonmerge, crs = crs, geometry = geometry)
geodataframeRecifeCNAEpolygonmerge.head()
'''


# In[110]:


#organizedataRecifeCNAE_polygonmerge.dtypes


# In[111]:


'''
organizedataRecifeCNAE_polygonmerge = gpd.GeoDataFrame(organizedataRecifeCNAE_polygonmerge, crs = 'epsg:4326', geometry = geometry)
organizedataRecifeCNAE_polygonmerge.head()
'''


# In[112]:


#geodataframeRecifeCNAEpolygonmerge = gpd.GeoDataFrame(organizedataRecifeCNAE_polygonmerge, crs = 'epsg:4326', geometry = geometry)
#geodataframeRecifeCNAEpolygonmerge.head()


# In[113]:


#it's a GeoDataFrame now but the geometry column with polygon from the merge was overwritten by the other geometry


# In[114]:


organizeddataRecifeCNAE.head(3)


# In[115]:


crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(organizeddataRecifeCNAE['longitude'], organizeddataRecifeCNAE['latitude'])]
geometry[:5]


# In[116]:


organizeddataRecifeCNAEGeoDataFrame = gpd.GeoDataFrame(organizeddataRecifeCNAE, crs = crs, geometry = geometry)
organizeddataRecifeCNAEGeoDataFrame.head()


# In[117]:


organizeddataRecifeCNAEGeoDataFrame.plot(cmap='gist_gray', column='bairro_nome', figsize=(10,10),legend=False);
plt.title('Individual Data From Bairros in Recife')


# In[118]:


'''organizedataRecifeCNAE_polygonmerge.plot(cmap='gist_gray', column='bairro', figsize=(10,10),legend=False);
plt.title('Individual Data From Bairros in Recife')'''


# In[119]:


list(organizeddataRecifeCNAEGeoDataFrame['bairro_nome'].unique())


# In[120]:


'''y = organizedataRecifeCNAE_polygonmerge['y'].values
w = Queen.from_dataframe(organizedataRecifeCNAE_polygonmerge)
w.transform = 'r' 
'''


# In[121]:


#pip install pysal


# In[122]:


get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import libpysal as lps
import geopandas as gpd

sns.set(style="whitegrid")


# In[123]:


# I need the geometry with the polygon and not the points, I did it without the polygon later


# In[124]:


#organizedataRecifeCNAE_polygonmerge_again = organizedataRecifeCNAE_polygonmerge.merge(bairrosgeojson,how='inner',on='bairro_codigo',indicator='_merge2')


# In[125]:


#organizedataRecifeCNAE_polygonmerge_again.shape


# In[126]:


#organizedataRecifeCNAE_polygonmerge_again.head(3)


# In[127]:


#organizedataRecifeCNAE_polygonmerge_again.rename({'geometry_y':'geometry'},axis=1,inplace=True)


# In[128]:


#organizedataRecifeCNAE_polygonmerge_again.head(2)


# In[129]:


'''
y = organizedataRecifeCNAE_polygonmerge_again['y'].values
w = Queen.from_dataframe(organizedataRecifeCNAE_polygonmerge_again)
w.transform = 'r'
'''


# In[130]:


organizeddataRecifeCNAEGeoDataFrame.head(3)


# In[ ]:





# In[ ]:


w = ps.knnW_from_array(lst.loc[                               yxs.index,                               ['longitude', 'latitude']                              ].values)
w.transform = 'R'
w


# In[ ]:





# In[134]:


w = weights.KNN.from_dataframe(organizeddataRecifeCNAEGeoDataFrame, k=10)
w.transform = 'r'


# In[132]:


y = organizeddataRecifeCNAEGeoDataFrame['y'].values
#w = Queen.from_dataframe(organizeddataRecifeCNAEGeoDataFrame)
w = weights.KNN.from_dataframe(organizeddataRecifeCNAEGeoDataFrame, k=8)
w.transform = 'r'


# In[ ]:


from esda.moran import Moran

w = Queen.from_dataframe(organizeddataRecifeCNAEGeoDataFrame)
moran = Moran(y, w)
moran.I


# In[ ]:


organizeddataRecifeCNAEGeoDataFrame.head(3)


# In[135]:


from esda.moran import Moran

w = Queen.from_dataframe(organizeddataRecifeCNAEGeoDataFrame)
moran = Moran(y, w)
moran.I


# In[ ]:


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


# In[ ]:


X = organizeddataRecifeCNAEGeoDataFrame[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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
y = organizeddataRecifeCNAEGeoDataFrame['y']

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


# In[ ]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeCNAEGeoDataFrame[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[ ]:


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


# In[ ]:


X=os_data_X[cols]
y=os_data_y['y']


# In[ ]:


y = y.astype('int64')


# In[ ]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[ ]:





# In[ ]:


#Do OLS, SAR, SEM, SLX in Recife and PE with the individual data


# In[ ]:


#with geometry point it is not working, I might have to use polygon, but it should work with the point from lat and long 
#instead of polygon 

#anyways, try that


# In[ ]:





# In[ ]:


yxs = lst.loc[:, x + ['pool', 'price']].dropna()
y = np.log(           yxs['price'].apply(lambda x: float(x.strip('$').replace(',', '')))           + 0.000001
          )


# In[ ]:


w = ps.knnW_from_array(lst.loc[                               yxs.index,                               ['longitude', 'latitude']                              ].values)
w.transform = 'R'
w


# In[ ]:


m1 = ps.spreg.OLS(y.values[:, None], yxs.drop('price', axis=1).values,                   w=w, spat_diag=True,                   name_x=yxs.drop('price', axis=1).columns.tolist(), name_y='ln(price)')


# In[ ]:





# In[ ]:


w_pool = ps.knnW_from_array(lst.loc[                               yxs.index,                               ['longitude', 'latitude']                              ].values)
yxs_w = yxs.assign(w_pool=ps.lag_spatial(w_pool, yxs['pool'].values))


# In[ ]:


m2 = ps.spreg.OLS(y.values[:, None],                   yxs_w.drop('price', axis=1).values,                   w=w, spat_diag=True,                   name_x=yxs_w.drop('price', axis=1).columns.tolist(), name_y='ln(price)')


# In[ ]:





# In[ ]:





# In[ ]:



