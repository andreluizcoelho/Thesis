#!/usr/bin/env python
# coding: utf-8

# ## This csv new data came from part4

# In[1]:


import pandas as pd
import numpy as np 


# In[2]:


# I redid part 4 for to get a new data for Recife inside cep and cep estab from each lat and long


# In[3]:


organizeddataRecife = pd.read_csv('organizeddatawithinRecifeshapefileborderNEW.csv')


# In[4]:


organizeddataRecife.shape #this data has all lats and long, from individual cep and cep estab inside the shapefile 
#also the distance from individual cep (latitude and longitude to marcozero), distance from CEP estab (latitudestab and longitudestab to marcozero), 
#and the distance from cep (latitude and longitude) to CEP Estab (latitudestab and longitudestab)


# ## the data has fewer rows than before, because the CEP and CEP Estab are inside the 
# ## shapefile for Recife, and missing observations were excluded

# In[ ]:





# In[5]:


organizeddataRecife.head(3)


# In[6]:


pd.set_option('display.max_columns',None)


# In[7]:


organizeddataRecife.head(3)


# In[9]:


organizeddataRecife[organizeddataRecife['idade']<=4].head()


# In[8]:


organizeddataRecife.columns


# In[9]:


organizeddataRecife['Vl Remun Média Nom']


# In[10]:


organizeddataRecife['Vl Remun Média Nom'].str.lstrip('0').str.replace(',','.')


# In[11]:


organizeddataRecife['Vl Remun Média Nom'] = organizeddataRecife['Vl Remun Média Nom'].str.lstrip('0').str.replace(',','.')


# In[12]:


organizeddataRecife['Vl Remun Média Nom'].describe()


# In[13]:


organizeddataRecife['Vl Remun Média Nom'] = organizeddataRecife['Vl Remun Média Nom'].astype(float)


# In[14]:


organizeddataRecife['Vl Remun Média Nom'].describe()


# In[15]:


organizeddataRecife['Vl Remun Média Nom']


# In[16]:


organizeddataRecife['Vl Remun Média Nom'].isna().sum()


# In[17]:


organizeddataRecife['Vl Remun Média Nom'].sort_values(ascending=False)


# In[18]:


organizeddataRecife['Vl Remun Média Nom'].value_counts() #the 0s turns into NaN in the bin interval


# In[19]:


organizeddataRecife.rename({'Vl Remun Média Nom':'Nominal Wage'},axis=1,inplace=True)


# In[20]:


organizeddataRecife['Nominal Wage']


# In[21]:


list(organizeddataRecife['Nominal Wage'])


# In[22]:


organizeddataRecife['Nominal Wage'].isna().sum()


# In[23]:


organizeddataRecife['Nominal Wage'].value_counts()


# In[24]:


organizeddataRecife['Nominal Wage'].describe()


# In[25]:


organizeddataRecife['meanminimumwage'].value_counts() #the meanminimumwage variable was done on part1, but I will do it 
#again, cause there are no values for the 0 interval


# In[26]:


#https://www.dieese.org.br/notatecnica/2019/notaTec201SalarioMinimo.pdf


# 2019 Minimum Wage
# 
# R$998,00

# In[27]:


#Using the same division as in part1 for minimum wage
'''
sem rendimento (0)
1-499
499-998
998-1996
1996-4990
4990-9980
9980-19960
19960+


bins = [0, 1, 499, 998, 1996, 4990, 9980, 19960, np.inf]
names = ['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960']

organizeddataRecife['Nominal Wage Range'] = pd.cut(organizeddataRecife['Nominal Wage'], bins, labels=names)




sem rendimento (0)
até 1/2 salário mínimo
mais de 1/2 a 1 salário mínimo 
mais de 1 a 2 salários mínimos 
mais de 2 a 5 salários mínimos 
mais de 5 a 10 salários mínimos 
mais de 10 a 20 salários mínimos
mais de 20 salários mínimos

# In[199]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.1 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

bancoesusalltabsrais2019morelatlongcepestabselected['meanminimumwage'] = pd.cut(bancoesusalltabsrais2019morelatlongcepestabselected['Vl Remun Média (SM)'], bins, labels=names)

print(bancoesusalltabsrais2019morelatlongcepestabselected.dtypes)

'''


# In[28]:


bins = [0, 1, 499, 998, 1996, 4990, 9980, 19960, np.inf]
names = ['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+']

organizeddataRecife['Nominal Wage Range'] = pd.cut(organizeddataRecife['Nominal Wage'], bins, labels=names)


# In[29]:


organizeddataRecife['Nominal Wage Range'].dtype


# In[30]:


organizeddataRecife['Nominal Wage Range'].sort_values(ascending=False)


# In[31]:


organizeddataRecife['Nominal Wage Range'].isna().sum()


# In[32]:


organizeddataRecife['Nominal Wage Range'] = organizeddataRecife['Nominal Wage Range'].astype(str).replace('nan','0')
organizeddataRecife['Nominal Wage Range'] = organizeddataRecife['Nominal Wage Range'].astype('category')


# In[33]:


organizeddataRecife['Nominal Wage Range']


# In[34]:


organizeddataRecife['meanminimumwage'].sort_values(ascending=False) #the NaN should've been replaced by 0, but I will do the 
#interval again


# In[35]:


organizeddataRecife['Nominal Wage Range'].describe()


# In[36]:


organizeddataRecife.columns


# In[37]:


organizeddataRecife.rename({'Vl Remun Média (SM)':'Minimum Wage'},axis=1,inplace=True)


# In[38]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.1 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

organizeddataRecife['meanminimumwage'] = pd.cut(organizeddataRecife['Minimum Wage'], bins, labels=names)

print(organizeddataRecife.dtypes)


# In[39]:


organizeddataRecife['meanminimumwage'].value_counts()


# In[40]:


organizeddataRecife['meanminimumwage'].isna().sum() #the 0s in the bin turs into nan, I need to change it back 


# In[41]:


organizeddataRecife['meanminimumwage'] = organizeddataRecife['meanminimumwage'].astype(str).replace('nan','0')


# In[42]:


organizeddataRecife['meanminimumwage'] =  organizeddataRecife['meanminimumwage'].astype('category')


# In[43]:


organizeddataRecife['meanminimumwage'].dtype


# In[44]:


organizeddataRecife['meanminimumwage'].value_counts()


# In[45]:


organizeddataRecife['Nominal Wage Range'].value_counts()


# In[46]:


organizeddataRecife['Minimum Wage'].value_counts(ascending=False)


# In[47]:


organizeddataRecife['meanminimumwage'].value_counts()


# In[48]:


organizeddataRecife['Nominal Wage Range'].value_counts()


# In[49]:


organizeddataRecife['Nominal Wage Range'].isna().sum()


# In[50]:


organizeddataRecife['meanminimumwage'].isna().sum()


# In[ ]:





# In[ ]:





# In[51]:


organizeddataRecife['Qtd Dias Afastamento'].unique()


# In[52]:


organizeddataRecife['Qtd Dias Afastamento'].describe()


# In[53]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

organizeddataRecife['Days Not Working'] = pd.cut(organizeddataRecife['Qtd Dias Afastamento'], bins, labels=names)

print(organizeddataRecife.dtypes)


# In[54]:


organizeddataRecife['Days Not Working'].unique()


# In[55]:


organizeddataRecife['Days Not Working'].value_counts()


# In[56]:


organizeddataRecife['Days Not Working'].isna().sum()


# In[57]:


organizeddataRecife['Qtd Dias Afastamento'].isna().sum()


# In[58]:


organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[59]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[60]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype('category')


# In[61]:


organizeddataRecife['Days Not Working'].dtype


# In[62]:


organizeddataRecife.head(3)


# In[63]:


organizeddataRecife['Days Not Working'].value_counts()


# In[64]:


organizeddataRecife['Days Not Working'].isna().sum()


# In[65]:


organizeddataRecife['Qtd Dias Afastamento'].value_counts()


# In[66]:


organizeddataRecife['finalresult'].unique()


# In[67]:


organizeddataRecife['finalresult'].value_counts()


# In[68]:


organizeddataRecife['finalresult'].isna().sum()


# In[69]:


organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[70]:


organizeddataRecife = organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[71]:


organizeddataRecife.shape


# In[72]:


organizeddataRecife['finalresult'].unique()


# In[73]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].replace('negative','0').replace('positive','1')


# In[74]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].astype('uint8')


# In[75]:


organizeddataRecife['finalresult'].value_counts()


# In[76]:


organizeddataRecife['finalresult'].value_counts(normalize=True)


# In[77]:


organizeddataRecife.columns


# In[78]:


organizeddataRecife.head(2)


# In[79]:


organizeddataRecife.rename({'race':'Race'},axis=1,inplace=True)


# In[80]:


organizeddataRecife.rename({'finalresult':'Covid-19','idade':'Age','Escolaridade após 2005':'School Years','sex':'Sex','Qtd Dias Afastamento':'No Working Days','distancecepindfrommarcozero':'CEP to CBD', 'distancecepestabfrommarcozero':'CEP Estab to CBD','distance_cep_to_CEP_Estab':'CEP to CEP Estab'},axis=1,inplace=True)


# In[81]:


organizeddataRecife.rename({'Sex':'Men'},axis=1, inplace=True)


# In[82]:


organizeddataRecife['Men'] = organizeddataRecife['Men'].astype('uint8')


# In[83]:


organizeddataRecife.groupby('Nominal Wage Range').agg({'School Years':'mean','Age':'mean','Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Men':'sum','Covid-19':'sum','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2).reindex(['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])


# In[84]:


organizeddataRecife_nominalwagerangemean_sumean = organizeddataRecife.groupby('Nominal Wage Range').agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Men':'sum','Covid-19':'sum','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2).reindex(['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])


# In[85]:


organizeddataRecife_nominalwagerangemean_sumean.loc['Total'] = organizeddataRecife_nominalwagerangemean_sumean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Men':'sum','Covid-19':'sum','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[86]:


organizeddataRecife_nominalwagerangemean_sumean


# In[87]:


organizeddataRecife_nominalwagerangemean_sumean.dtypes


# In[88]:


organizeddataRecife_nominalwagerangemean_sumean.isna().sum()


# In[89]:


organizeddataRecife_nominalwagerangemean_sumean['Health Professionals'] = organizeddataRecife_nominalwagerangemean_sumean['Health Professionals'].astype(int)
organizeddataRecife_nominalwagerangemean_sumean['Security Professionals'] = organizeddataRecife_nominalwagerangemean_sumean['Security Professionals'].astype(int)
organizeddataRecife_nominalwagerangemean_sumean['Men'] = organizeddataRecife_nominalwagerangemean_sumean['Men'].astype(int)
organizeddataRecife_nominalwagerangemean_sumean['Covid-19'] = organizeddataRecife_nominalwagerangemean_sumean['Covid-19'].astype(int)


# In[90]:


organizeddataRecife_nominalwagerangemean_sumean


# In[91]:


organizeddataRecife['Men'].describe()


# In[92]:


organizeddataRecife['Covid-19'].describe()


# In[ ]:





# In[93]:


organizeddataRecife_nominalwagerangemean = organizeddataRecife.groupby('Nominal Wage Range').mean().round(2).reindex(['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])


# In[94]:


organizeddataRecife_nominalwagerangemean = organizeddataRecife_nominalwagerangemean.loc[:,{'School Years', 'Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}]


# In[95]:


organizeddataRecife_nominalwagerangemean


# In[96]:


organizeddataRecife_nominalwagerangemean.loc['Total'] = organizeddataRecife_nominalwagerangemean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[97]:


organizeddataRecife_nominalwagerangemean


# In[98]:


organizeddataRecife_nominalwagerangemean.columns


# In[99]:


organizeddataRecife.shape


# In[100]:


organizeddataRecife.isna().sum().head(20)


# ## Table 1: Variables Mean by Nominal Wage Range

# In[101]:


organizeddataRecife_nominalwagerangemean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[102]:


#getTablePNG(organizeddataRecife_nominalwagerangemean)


# In[103]:


organizeddataRecife.shape


# In[104]:


organizeddataRecife['Nominal Wage Range'].value_counts()


# In[105]:


organizeddataRecife['Nominal Wage'].sort_values(ascending=True)


# In[106]:


organizeddataRecife.loc[:,'Nominal Wage']


# In[107]:


organizeddataRecife.loc[:,['Nominal Wage','Nominal Wage Range']].sort_values(by='Nominal Wage', ascending=False)


# In[108]:


organizeddataRecife.loc[:,['Nominal Wage','Nominal Wage Range']][organizeddataRecife['Nominal Wage']==998] #answered 998 is on 
#499-998 interval and not on the interval 998-1996, remembering that by default python range is inclusive, includes the first 
#number on range and excludes the last number on range. Here 998 is inclusive on the lower interval range probably because
#when the variables was created one of the bins was equal to 998


# In[109]:


organizeddataRecife.shape


# In[110]:


organizeddataRecife['meanminimumwage'].value_counts()


# In[111]:


#there's no zero, this is not right, there should be zero


# In[112]:


#getting again the variables 


# In[113]:


organizeddataRecife.columns


# ### Table 2 mean minimum wage

# In[114]:


#See table 1


# In[115]:


organizeddataRecife.shape


# In[116]:


organizeddataRecife.rename({'meanminimumwage':'Minimum Wage Range'},axis=1,inplace=True)


# In[117]:


organizeddataRecife.groupby('Minimum Wage Range').mean().round(2).reindex(['0','0.1 - 1/2','1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+'])


# In[118]:


organizeddataRecife_meanminimumwage_mean = organizeddataRecife.groupby('Minimum Wage Range').mean().round(2).reindex(['0','0.1 - 1/2','1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+'])


# In[119]:


organizeddataRecife_meanminimumwage_mean = organizeddataRecife_meanminimumwage_mean.loc[:,{'School Years', 'Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}]


# In[120]:


organizeddataRecife_meanminimumwage_mean 


# In[121]:


organizeddataRecife_meanminimumwage_mean.loc['Total'] = organizeddataRecife_meanminimumwage_mean.agg({'School Years':'mean','Age':'mean','Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[122]:


organizeddataRecife_meanminimumwage_mean


# In[123]:


organizeddataRecife.shape


# ## Table 2 Variables Mean by Minimum Wage Range

# In[124]:


organizeddataRecife_meanminimumwage_mean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[125]:


organizeddataRecife.loc[:,['Minimum Wage','Minimum Wage Range']][organizeddataRecife['Minimum Wage']==0]


# ## Table 3 age cohort

# In[ ]:





# In[126]:


organizeddataRecife.shape


# In[127]:


organizeddataRecife.loc[:,['Age','agecohort']][organizeddataRecife['Age']==0]


# In[128]:


organizeddataRecife['agecohort'].isna().sum()


# In[129]:


organizeddataRecife['agecohort'] = organizeddataRecife['agecohort'].astype(str).replace('nan','0')


# In[130]:


organizeddataRecife['agecohort'] = organizeddataRecife['agecohort'].astype('category')


# In[131]:


organizeddataRecife.loc[:,['Age','agecohort']][organizeddataRecife['Age']==0]


# In[132]:


organizeddataRecife.rename({'agecohort':'Age Cohort'},axis=1,inplace=True)


# In[133]:


organizeddataRecife.groupby(by='Age Cohort').mean().round(2).reindex(['0 - 4','5 - 17','18 - 29','30 - 39','40 - 49','50 - 64','65 - 74','75 - 84','85+'])


# In[134]:


organizeddataRecife_agecohortmean = organizeddataRecife.groupby(by='Age Cohort').mean()


# In[135]:


organizeddataRecife_agecohortmean = organizeddataRecife_agecohortmean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[136]:


organizeddataRecife_agecohortmean


# In[137]:


organizeddataRecife_agecohortmean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[138]:


organizeddataRecife_agecohortmean = organizeddataRecife_agecohortmean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[139]:


organizeddataRecife_agecohortmean.loc['Total'] = organizeddataRecife_agecohortmean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[140]:


organizeddataRecife.shape


# ## Table 3 this one age cohort

# In[141]:


organizeddataRecife_agecohortmean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[142]:


organizeddataRecife.loc[:,['Age','Age Cohort']][organizeddataRecife['Age']==18] #falls into a lower range


# In[143]:


#doing agecohort again to try to fix the age to be in the right interval


# In[144]:


organizeddataRecife['Age']


# In[145]:


organizeddataRecife.loc[:,['Age','Age Cohort']][organizeddataRecife['Age']==1]


# In[146]:


organizeddataRecife.loc[:,['Age','Age Cohort']][organizeddataRecife['Age']==4] #falls into a lower range


# In[ ]:





# In[147]:


organizeddataRecife.columns


# ### Table 4 Schooling

# In[148]:


organizeddataRecife.shape


# In[149]:


organizeddataRecife.head(3)


# In[150]:


organizeddataRecife['School Years'].mean()


# In[151]:


organizeddataRecife['schooling']


# In[152]:


organizeddataRecife.rename({'schooling':'Educational Attainment'},axis=1,inplace=True)


# In[153]:


organizeddataRecife.groupby('Educational Attainment').mean().reindex(['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education'])


# In[154]:


organizeddataRecife_educationalattainmentmean = organizeddataRecife.groupby('Educational Attainment').mean().reindex(['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education'])


# In[155]:


organizeddataRecife_educationalattainmentmean = organizeddataRecife_educationalattainmentmean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[156]:


organizeddataRecife_educationalattainmentmean


# In[157]:


organizeddataRecife_educationalattainmentmean.loc['Total'] = organizeddataRecife_educationalattainmentmean.agg({'School Years':'mean','Age':'mean','Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[158]:


organizeddataRecife_educationalattainmentmean


# In[159]:


organizeddataRecife.shape


# ## Table 4 this one Educational Attainment 

# In[160]:


organizeddataRecife_educationalattainmentmean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# ## Race

# In[161]:


organizeddataRecife['Race']


# In[ ]:





# In[162]:


organizeddataRecife.groupby('Race').mean().reindex(['White','Yellow','Brown','Black','Indigenous','Ignored'])


# In[163]:


organizeddataRecife_racemean=organizeddataRecife.groupby('Race').mean().reindex(['White','Yellow','Brown','Black','Indigenous','Ignored'])


# In[164]:


organizeddataRecife_racemean


# In[165]:


organizeddataRecife_racemean = organizeddataRecife_racemean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[166]:


organizeddataRecife_racemean


# In[167]:


organizeddataRecife_racemean.loc['Total'] = organizeddataRecife_racemean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[168]:


organizeddataRecife.shape


# ## Table 5 this one Race

# In[169]:


organizeddataRecife_racemean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[170]:


'''-> From article
OBS: although the methodology won't be logit model, but conditional logit model, this article helped see a way to 
organize the variables


means adapting to my case

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


# In[171]:


organizeddataRecife.shape


# In[172]:


organizeddataRecife.head(3)


# In[173]:


#I am not doing Age 2 (age squared for now)
#organizeddataRecife['Age 2'] = organizeddataRecife['Age']**2


# In[174]:


organizeddataRecife_racemean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[175]:


organizeddataRecife['Educational Attainment'].isna().sum()


# In[176]:


organizeddataRecife['Educational Attainment']


# In[177]:


organizeddataRecife['School Years']


# In[178]:


organizeddataRecife['School Years'].isna().sum()


# In[179]:


organizeddataRecife.head(3)


# In[180]:


organizeddataRecife['Race'].unique()


# In[181]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['Race']


# In[182]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['Non-White/Ignored'].replace('Brown','Non-white').replace('Yellow','Non-white').replace('Black','Non-white').replace('Indigenous','Non-white').replace('Ignored','Uninformed race')


# In[183]:


organizeddataRecife['Non-White/Ignored'].unique()


# In[184]:


organizeddataRecife['Non-White/Ignored'].value_counts()


# In[185]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['Non-White/Ignored'])], axis=1)


# In[186]:


organizeddataRecife.rename({'Non-White/Ignored_Non-white':'Non-white', 'Non-White/Ignored_Uninformed race':'Uninformed race'},axis=1, inplace=True)


# In[187]:


organizeddataRecife.head(3)


# In[188]:


organizeddataRecife['Educational Attainment'].value_counts()


# In[189]:


organizeddataRecife['Educational Attainment'].isna().sum()


# In[190]:


organizeddataRecife['Educational Attainment'].value_counts(normalize=True)


# In[191]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['Educational Attainment'])], axis=1)


# In[192]:


organizeddataRecife.head(3)


# In[193]:


organizeddataRecife['Minimum Wage'].value_counts()


# In[194]:


organizeddataRecife['Qtd Hora Contr'].unique()


# In[195]:


organizeddataRecife['Qtd Hora Contr'].value_counts()


# In[196]:


organizeddataRecife.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[197]:


organizeddataRecife['Tempo Emprego'].unique()


# In[198]:


organizeddataRecife['Tempo Emprego'].describe()


# In[199]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.replace(',','.')


# In[200]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.lstrip('0')


# In[201]:


organizeddataRecife.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[202]:


organizeddataRecife['Job tenure'] = organizeddataRecife['Job tenure'].astype(float)


# In[203]:


organizeddataRecife['Job tenure'].unique()


# In[204]:


organizeddataRecife['Job tenure'].describe()


# In[205]:


#IBGE Subsector and CBO dummies will be skipped for now 


# In[206]:


organizeddataRecife['CEP to CEP Estab']


# In[207]:


organizeddataRecife['CEP to CEP Estab'].round(2)


# In[208]:


organizeddataRecife['CEP to CEP Estab'] = organizeddataRecife['CEP to CEP Estab'].round(2)


# In[209]:


organizeddataRecife['CNAE 2.0 Section Name'].unique()


# In[210]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[211]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[212]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[213]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].str.title()


# In[214]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['CNAE 2.0 Section Name'])], axis = 1)


# In[215]:


pd.Series(sorted(organizeddataRecife['CNAE 2.0 Section Name'].unique()))


# In[216]:


organizeddataRecife.head(3)


# In[217]:


organizeddataRecife.shape


# In[218]:


organizeddataRecife.columns


# In[219]:


organizeddataRecife['Days Not Working'].value_counts() #very different than on the other data, I will do it again


# In[220]:


organizeddataRecife['Days Not Working'].unique()


# In[221]:


organizeddataRecife['No Working Days'].value_counts()


# In[222]:


organizeddataRecife['No Working Days'].unique()


# In[223]:


organizeddataRecife[['Age','Men','Non-white','White','Uninformed race','Incomplete primary education','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','No Working Days','Job tenure','CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab']]


# In[224]:


organizeddataRecife['Incomplete primary education'].value_counts()


# In[225]:


organizeddataRecife['Incomplete primary education'].value_counts(normalize=True)


# # Continuing from part6 ipynb

# In[226]:


organizeddataRecife.groupby(by='Days Not Working').mean()


# In[227]:


organizeddataRecife_daysnotworkingmean = organizeddataRecife.groupby(by='Days Not Working').mean().reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+'])


# In[228]:


organizeddataRecife_daysnotworkingmean = organizeddataRecife_daysnotworkingmean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[229]:


organizeddataRecife_daysnotworkingmean


# In[230]:


organizeddataRecife_daysnotworkingmean.loc['Total'] = organizeddataRecife_daysnotworkingmean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# ## Table 6 here Days not working

# In[231]:


organizeddataRecife_daysnotworkingmean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[232]:


organizeddataRecife.groupby(by='CNAE 2.0 Section Name').mean()


# In[233]:


organizeddataRecife_CNAEmean = organizeddataRecife.groupby(by='CNAE 2.0 Section Name').mean()


# In[234]:


organizeddataRecife_CNAEmean = organizeddataRecife_CNAEmean.loc[:,{'School Years','Minimum Wage','Age','No Working Days','Health Professionals','Security Professionals','Men','Covid-19','CEP to CBD','CEP Estab to CBD','CEP to CEP Estab'}].round(2)


# In[235]:


organizeddataRecife_CNAEmean.loc['Total'] = organizeddataRecife_CNAEmean.agg({'School Years':'mean', 'Minimum Wage':'mean','Age':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Men':'mean','Covid-19':'mean','CEP to CBD':'mean','CEP Estab to CBD':'mean','CEP to CEP Estab':'mean'}).round(2)


# In[236]:


organizeddataRecife_CNAEmean


# ## Table 7 (Part 1) and Table 8 (Part 2) CNAE here below they're together

# In[237]:


organizeddataRecife_CNAEmean[['Minimum Wage','Covid-19','School Years','Age','Men','Health Professionals', 'Security Professionals','No Working Days','CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# ### on the thesis data from table 1-5 it has  48,816 individuals(1-5) 
# ### from table 6-8 it has 47,328 individuals (the removed ones are the NA's from Race
# ### I left the tables from 1-8 as they were on the thesis, the right thing to do is to 
# ### redo table 6,7 and 8 with the NA's from Race to be right
# ### to do the graphs 
# ### I will use the data with 48,816 to be the same 

# In[238]:


organizeddataRecife.shape


# In[239]:


organizeddataRecife.to_csv('organizeddataRecifeforgraphs.csv', index=False)


# # OrganizeddataRecifeforgraphs.csv data is for part8 to do the graphs

# In[102]:


organizeddataRecife['Race'].isna().sum()


# In[103]:


organizeddataRecife = organizeddataRecife.dropna(subset=['Race'])


# In[104]:


organizeddataRecife.shape


# In[339]:


organizeddataRecife['Working hours']


# In[340]:


organizeddataRecife['Working hours'].value_counts()


# In[341]:


organizeddataRecife['Job tenure']


# In[342]:


organizeddataRecife['Job tenure'].value_counts()


# In[343]:


#Should I put Working hours and Job tenure in all tables or is it a lot of information?


# In[344]:


organizeddataRecife.shape


# In[345]:


organizeddataRecife.head(3)


# In[346]:


organizeddataRecife[['Age','Men','Non-white','White','Uninformed race','Incomplete primary education','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','No Working Days','Job tenure','CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab']].dtypes


# ## Go to "Testing clogit for only y=1, that is the postive cases" on part6
# ## And before "Running the Conditional logit model CNAE Recife only postive cases"

# ## All Clogit Models on stata later (asclogit, cmclogit, mlogit) 
# ## Only for positive cases

# In[244]:


organizeddataRecife['Covid-19']


# In[245]:


organizeddataRecife.rename({'Covid-19':'y'}, axis=1, inplace=True)


# In[246]:


organizeddataRecife[organizeddataRecife['y']==1]


# In[247]:


organizeddataRecife = organizeddataRecife[organizeddataRecife['y']==1]


# In[248]:


organizeddataRecife.head(3)


# In[249]:


organizeddataRecife.shape


# In[250]:


organizeddataRecife[['Age','Men','Non-white','White','Uninformed race','Incomplete primary education','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','No Working Days','Job tenure','CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab']]


# In[251]:


X = organizeddataRecife[['CNAE 2.0 Section Name','Age','Men','Non-white','White','Uninformed race','Incomplete primary education','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','No Working Days','Job tenure','CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab']]


# In[252]:


y = organizeddataRecife['y']


# In[253]:


X


# In[254]:


X.reset_index(drop=True,inplace=True)


# In[255]:


X.head(3)


# In[256]:


y


# In[257]:


X.columns


# In[258]:


X['choice'] = np.where(X['Accommodation And Food'] == 1, 1, 
    np.where(X['Administrative Activities And Complementary Services'] == 1, 2, 
    np.where(X['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'] == 1, 3,         
    np.where(X['Construction']   == 1,4,
    np.where(X['Education']   == 1,5,
    np.where(X['Electricity And Gas']   == 1,6,
    np.where(X['Extractive Industries']   == 1,7,
    np.where(X['Human Health And Social Services']   == 1,8,
    np.where(X['Information And Communication']   == 1,9,
    np.where(X['Other Service Activities']   == 1,10,
    np.where(X['Processing Industries']   == 1,11,
    np.where(X['Professional, Scientific And Technical Activities']   == 1,12,
    np.where(X['Public Administration, Defense And Social Security']   == 1,13,
    np.where(X['Trade; Repair Of Motor Vehicles And Motorcycles']   == 1,14,
    np.where(X['Transportation, Storage And Mail']   == 1,15,
    np.where(X['Water, Sewage, Waste Management And Decontamination Activities']   == 1,16,
    np.where(X['Arts, Culture, Sports And Recreation']   == 1,17,
    np.where(X['Real Estate Activities']   == 1,18,
    np.where(X['Financial, Insurance And Related Services Activities']   == 1,19
             ,0)))))))))))))))))))


# In[259]:


X.head()


# In[260]:


X['choicenumber']=X['choice']


# In[261]:


X['id']=X.index


# In[262]:


X


# In[263]:


cols = list(X.columns)
cols = [cols[-1]] + cols[:-1]
X = X[cols]


# In[264]:


X.head(4)


# In[265]:


X['id']


# In[266]:


X['id'] = X['id']+1


# In[267]:


X_sameids = pd.DataFrame(np.repeat(X.values, 19, axis=0))
X_sameids.columns = X.columns
print(X_sameids)


#it repeats the rows 19 times, the number of choices of the economy sectors
#this replicates the first row 19 times, then the 20th row 19 times, then the 39th row 19 times


# In[268]:


X_sameids.head()


# In[269]:


X_sameids


# In[270]:


X_sameids.head(20)


# In[271]:


X_sameids.head(3)


# In[272]:


X_sameids.iloc[::19, :]


# In[273]:


X_sameids.iloc[::19, -2:-1]


# In[274]:


X_sameids['choice'].values[:] = 0


# In[275]:


X_sameids


# In[276]:


X_sameids.iloc[::19, -2:-1] = 1


# In[277]:


X_sameids


# In[278]:


X_sameids['choice']


# In[279]:


X_sameids[X_sameids['choice']==1]


# In[280]:


X_sameids['choice'].unique()


# In[281]:


X_sameids['choice'].dtype


# In[282]:


X_sameids.head(20)


# In[283]:


mode = pd.DataFrame({'Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities'})


# In[284]:


mode


# In[285]:


mode.rename({0:'mode'},axis=1,inplace=True)


# In[286]:


mode


# In[287]:


mode = mode.reindex(['Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities'])


# In[288]:


mode


# In[289]:


mode = mode.reset_index()


# In[290]:


mode


# In[291]:


mode = mode.loc[:,['index']]


# In[292]:


mode.rename({'index':'mode'},axis=1,inplace=True)


# In[293]:


mode


# In[294]:


X.shape


# In[295]:


mode.append([mode]*13805,ignore_index=True)


# In[296]:


mode = mode.append([mode]*13805,ignore_index=True)


# In[297]:


mode.shape


# In[298]:


mode


# In[299]:


pd.get_dummies(mode,columns=['mode'])


# In[300]:


pd.concat([mode, pd.get_dummies(mode['mode'])],axis=1)


# In[301]:


mode_dummies = pd.concat([mode, pd.get_dummies(mode['mode'])],axis=1)


# In[302]:


mode_dummies


# In[303]:


mode_dummies.columns


# In[304]:


mode['mode'].unique()


# In[305]:


mode_dummies[['mode','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities']]


# In[306]:


mode_dummies = mode_dummies[['mode','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities']]


# In[307]:


mode_dummies.shape


# In[308]:


mode_dummies.head(8)


# In[309]:


X_sameids.shape


# In[310]:


X_sameids.head(3)


# In[311]:


X_sameids.columns


# In[312]:


X_sameids[['id', 'CNAE 2.0 Section Name', 'Age', 'Men', 'Non-white',
       'White', 'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days',
       'Job tenure', 'CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab', 'choice', 'choicenumber']]


# In[313]:


X_sameidsforjoin = X_sameids[['id', 'CNAE 2.0 Section Name', 'Age', 'Men', 'Non-white',
       'White', 'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days',
       'Job tenure', 'CEP to CBD','CEP Estab to CBD', 'CEP to CEP Estab', 'choice', 'choicenumber']]


# In[314]:


mode_dummies.join(X_sameidsforjoin)


# In[315]:


Xjoined_mode_sameids = mode_dummies.join(X_sameidsforjoin)


# In[316]:


Xjoined_mode_sameids.head(6)


# In[317]:


Xjoined_mode_sameids.columns


# In[318]:


Xjoined_mode_sameids[['id','mode','CNAE 2.0 Section Name','choice', 'choicenumber','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities',
        'Age', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days','Job tenure', 'CEP to CBD','CEP Estab to CBD','CEP to CEP Estab']]


# In[319]:


Xjoined_mode_sameids.rename({'choice':'choice_cnaesectioname'},axis=1,inplace=True)


# In[320]:


Xjoined_mode_sameids[['id','mode','CNAE 2.0 Section Name','choice_cnaesectioname', 'choicenumber','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities',
        'Age', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days', 'Job tenure', 'CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[321]:


Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['mode'].eq(Xjoined_mode_sameids['CNAE 2.0 Section Name'])


# In[322]:


Xjoined_mode_sameids


# In[323]:


Xjoined_mode_sameids['choice'].dtype


# In[324]:


Xjoined_mode_sameids['choice'].astype(int)


# In[325]:


Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['choice'].astype(int)


# In[326]:


Xjoined_mode_sameids[['id','mode','CNAE 2.0 Section Name','choice','choice_cnaesectioname', 'choicenumber','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities',
        'Age', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days', 'Job tenure', 'CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[327]:


Xjoined_mode_sameids['choice'].sum()


# In[328]:


Xjoined_mode_sameids.tail(3)


# In[329]:


Xjoined_mode_sameids[['id','mode','CNAE 2.0 Section Name','choice','choice_cnaesectioname', 'choicenumber','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities',
        'Age', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days', 'Job tenure', 'CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[330]:


Xjoined_mode_sameids = Xjoined_mode_sameids[['id','mode','CNAE 2.0 Section Name','choice','choice_cnaesectioname', 'choicenumber','Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities',
        'Age', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Incomplete primary education','Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours','No Working Days', 'Job tenure', 'CEP to CBD', 'CEP Estab to CBD', 'CEP to CEP Estab']]


# In[331]:


Xjoined_mode_sameids


# In[332]:


Xjoined_mode_sameids['Age']


# In[333]:


Xjoined_mode_sameids['Age'].astype(int)


# In[334]:


Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].astype(int)


# In[335]:


list(Xjoined_mode_sameids['Age'].unique())


# In[336]:


Xjoined_mode_sameids.dtypes


# In[337]:


Xjoined_mode_sameids['id'] = Xjoined_mode_sameids['id'].astype(str)
Xjoined_mode_sameids['mode'] = Xjoined_mode_sameids['mode'].astype(str)
Xjoined_mode_sameids['CNAE 2.0 Section Name'] = Xjoined_mode_sameids['CNAE 2.0 Section Name'].astype(str)

Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['choice'].astype('uint8')

Xjoined_mode_sameids['choice_cnaesectioname'] = Xjoined_mode_sameids['choice_cnaesectioname'].astype('uint8')

Xjoined_mode_sameids['choicenumber'] = Xjoined_mode_sameids['choicenumber'].astype(int)

Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].astype(int)
#X_sameids_mode['Age 2'] = X_sameids_mode['Age 2'].astype(int)
Xjoined_mode_sameids['Men'] = Xjoined_mode_sameids['Men'].astype('uint8')
Xjoined_mode_sameids['Non-white'] = Xjoined_mode_sameids['Non-white'].astype('uint8')
Xjoined_mode_sameids['White'] = Xjoined_mode_sameids['White'].astype('uint8')
Xjoined_mode_sameids['Uninformed race'] = Xjoined_mode_sameids['Uninformed race'].astype('uint8')
Xjoined_mode_sameids['Incomplete primary education'] = Xjoined_mode_sameids['Incomplete primary education'].astype('uint8')
Xjoined_mode_sameids['Complete primary education'] = Xjoined_mode_sameids['Complete primary education'].astype('uint8')
Xjoined_mode_sameids['Complete secondary education'] = Xjoined_mode_sameids['Complete secondary education'].astype('uint8')
Xjoined_mode_sameids['Complete higher education'] = Xjoined_mode_sameids['Complete higher education'].astype('uint8')
Xjoined_mode_sameids['Minimum Wage'] = Xjoined_mode_sameids['Minimum Wage'].astype(int)
Xjoined_mode_sameids['Working hours'] = Xjoined_mode_sameids['Working hours'].astype(int)
Xjoined_mode_sameids['No Working Days'] = Xjoined_mode_sameids['No Working Days'].astype(int)
Xjoined_mode_sameids['Job tenure'] = Xjoined_mode_sameids['Job tenure'].astype(float)
Xjoined_mode_sameids['CEP to CBD'] = Xjoined_mode_sameids['CEP to CBD'].astype(float)
Xjoined_mode_sameids['CEP Estab to CBD'] = Xjoined_mode_sameids['CEP Estab to CBD'].astype(float)
Xjoined_mode_sameids['CEP to CEP Estab'] = Xjoined_mode_sameids['CEP to CEP Estab'].astype(float)


# In[338]:


Xjoined_mode_sameids.dtypes


# In[339]:


Xjoined_mode_sameids[['Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities']].dtypes


# In[340]:


Xjoined_mode_sameids[['Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities']] = Xjoined_mode_sameids[['Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities']].astype('uint8')


# In[341]:


Xjoined_mode_sameids.dtypes


# In[342]:


Xjoined_mode_sameids.to_csv('X_choice_mode_sameids_RecifeCNAE_NEW.csv',index=False)


# In[343]:


Xjoined_mode_sameids.to_stata('X_choice_mode_sameids_RecifeCNAE_NEW.dta')


# ## Continues on stata the Regression
# ## Also part8 for the graphs
# ## Also part9 for original RAIS for comparison

# ## initial estimates on stata are failing and it is not concave, see what's wrong

# In[344]:


import pandas as pd


# In[345]:


X_choice_mode_sameids_RecifeCNAE_NEW = pd.read_csv('X_choice_mode_sameids_RecifeCNAE_NEW.csv')


# In[346]:


X_choice_mode_sameids_RecifeCNAE_NEW.shape


# In[347]:


X_choice_mode_sameids_RecifeCNAE_NEW.head(3)


# In[348]:


pd.set_option('display.max_columns',None)


# In[349]:


X_choice_mode_sameids_RecifeCNAE_NEW.head(3)


# In[350]:


X_choice_mode_sameids_RecifeCNAE_NEW.isna().sum()


# In[351]:


X_choice_mode_sameids_RecifeCNAE_NEW['mode'].value_counts()


# In[352]:


X_choice_mode_sameids_RecifeCNAE_NEW['Accommodation And Food'].value_counts()


# In[353]:


X_choice_mode_sameids_RecifeCNAE_NEW['Processing Industries'].value_counts()


# In[354]:


X_choice_mode_sameids_RecifeCNAE_NEW['Real Estate Activities'].value_counts()


# In[355]:


X_choice_mode_sameids_RecifeCNAE_NEW['Arts, Culture, Sports And Recreation'].value_counts()


# In[356]:


X_choice_mode_sameids_RecifeCNAE_NEW['Water, Sewage, Waste Management And Decontamination Activities'].value_counts()


# In[357]:


X_choice_mode_sameids_RecifeCNAE_NEW['Transportation, Storage And Mail'].value_counts()


# In[358]:


X_choice_mode_sameids_RecifeCNAE_NEW['Trade; Repair Of Motor Vehicles And Motorcycles'].value_counts()


# In[359]:


X_choice_mode_sameids_RecifeCNAE_NEW['Public Administration, Defense And Social Security'].value_counts()


# In[360]:


X_choice_mode_sameids_RecifeCNAE_NEW['Professional, Scientific And Technical Activities'].value_counts()


# In[361]:


X_choice_mode_sameids_RecifeCNAE_NEW['Other Service Activities'].value_counts()


# In[362]:


X_choice_mode_sameids_RecifeCNAE_NEW['Administrative Activities And Complementary Services'].value_counts()


# In[363]:


X_choice_mode_sameids_RecifeCNAE_NEW['Information And Communication'].value_counts()


# In[364]:


X_choice_mode_sameids_RecifeCNAE_NEW['Human Health And Social Services'].value_counts()


# In[365]:


X_choice_mode_sameids_RecifeCNAE_NEW['Extractive Industries'].value_counts()


# In[366]:


X_choice_mode_sameids_RecifeCNAE_NEW['Electricity And Gas'].value_counts()


# In[367]:


X_choice_mode_sameids_RecifeCNAE_NEW['Education'].value_counts()


# In[368]:


X_choice_mode_sameids_RecifeCNAE_NEW['Construction'].value_counts()


# In[369]:


X_choice_mode_sameids_RecifeCNAE_NEW['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].value_counts()


# In[370]:


X_choice_mode_sameids_RecifeCNAE_NEW['Financial, Insurance And Related Services Activities'].value_counts()


# In[371]:


'''
The 3s below 1000
remove Extractive Industries because it is so low and run it again, to see if it coverges

Extractive Industries only 19
Agriculture, Livestock, Forestry Production, Fishing And Aquaculture only 399
Real Estate Activities only 893
'''


# In[372]:


## Actually that is not it, the mode dummies are built wrong, I fixed the dummies, but it is still not working


# In[373]:


X_choice_mode_sameids_RecifeCNAE_NEW.shape


# In[374]:


X_choice_mode_sameids_RecifeCNAE_NEW.head(3)


# In[375]:


X_choice_mode_sameids_RecifeCNAE_NEW[X_choice_mode_sameids_RecifeCNAE_NEW['mode']=='Extractive Industries']


# In[376]:


X_choice_mode_sameids_RecifeCNAE_NEW['Extractive Industries'].sum()


# In[377]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd = X_choice_mode_sameids_RecifeCNAE_NEW[X_choice_mode_sameids_RecifeCNAE_NEW['mode']!='Extractive Industries']


# In[378]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd.shape


# In[379]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd.head(3)


# In[380]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd.drop('Extractive Industries',axis=1,inplace=True)


# In[381]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd.head(3)


# In[382]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['mode']=='Extractive Industries']


# In[383]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['CNAE 2.0 Section Name']=='Extractive Industries']


# In[384]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['CNAE 2.0 Section Name']=='Extractive Industries'].shape


# In[385]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['CNAE 2.0 Section Name']!='Extractive Industries']


# In[386]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd = X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['CNAE 2.0 Section Name']!='Extractive Industries']


# In[387]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.shape


# In[388]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.head(3)


# In[389]:


X_choice_mode_sameids_RecifeCNAE_NEW.shape


# In[390]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.shape


# In[391]:


X_choice_mode_sameids_RecifeCNAE_NEW[X_choice_mode_sameids_RecifeCNAE_NEW['mode']=='Extractive Industries'].shape


# In[392]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd[X_choice_mode_sameids_RecifeCNAE_NEW_NomodeExtracInd['CNAE 2.0 Section Name']=='Extractive Industries'].shape


# In[393]:


262314-13806-18 #it makes sense now


# In[ ]:


# coincidently the id dropped exactly 1 unit because ['CNAE 2.0 Section Name']=='Extractive Industries'] had 18 rows 
#and the rows repeats 18 times 19 which is the number of different modes -1, after removing Extractive Industries


# In[ ]:


len(X_choice_mode_sameids_RecifeCNAE_NEW['mode'].unique())


# In[394]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.id.tail(20)


# ## Removed Extractive industries and the model worked on stata

# In[395]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.to_stata('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd.dta')


# In[396]:


X_choice_mode_sameids_RecifeCNAE_NEW_NomodecnaeExtracInd.to_csv('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd.csv',index=False)


# ## id's were removed because there is no Extractive Industries
# ### trying to put the id in order

# In[397]:


import pandas as pd


# In[398]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd = pd.read_csv('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd.csv')


# In[399]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd.shape


# In[400]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd.head(3)


# In[401]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd['mode'].isna().sum()


# In[402]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd['CNAE 2.0 Section Name'].isna().sum()


# In[403]:


'''
X_sameids = pd.DataFrame(np.repeat(X.values, 19, axis=0))
X_sameids.columns = X.columns
print(X_sameids)


#it repeats the rows 19 times, the number of choices of the economy sectors
#this replicates the first row 19 times, then the 20th row 19 times, then the 39th row 19 times
'''


# In[404]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd['id'].unique())


# In[405]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd['id'].value_counts()


# In[406]:


list(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd['id'])


# In[407]:


#index 25517 until index 25535, all id 1344 (Extractive Industries) disappeared using CNAE Section Name
#but using mode many indexes disappeared 13806 rows


# In[408]:


list(range(1,13806))


# In[409]:


pd.DataFrame(list(range(1,13806))).rename({0:'New_ID'},axis=1)


# In[410]:


df = pd.DataFrame(list(range(1,13806))).rename({0:'New_ID'},axis=1)


# In[411]:


df


# In[412]:


pd.DataFrame(np.repeat(df.values, 18, axis=0)).rename({0:'New_ID'},axis=1)


# In[413]:


df = pd.DataFrame(np.repeat(df.values, 18, axis=0)).rename({0:'New_ID'},axis=1)


# In[414]:


df['New_ID']


# In[415]:


df['New_ID'].isna().sum()


# In[416]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd


# In[417]:


df


# In[418]:


df.join(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd)


# In[419]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId = df.join(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd)


# In[420]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId


# In[421]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.drop(['id'],axis=1,inplace=True)


# In[422]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.head(3)


# In[423]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['New_ID'].dtype


# In[424]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['New_ID']


# In[425]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.rename({'New_ID':'id'},axis=1,inplace=True)


# In[426]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[427]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.head(3)


# In[428]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.tail(3)


# In[429]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode'].isna().sum()


# In[430]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[431]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['id'].unique())


# In[432]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.iloc[0:19]


# In[433]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[434]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[435]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.to_stata('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.dta')


# In[436]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.to_csv('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.csv',index=False)


# # Removing Agriculture, Livestock, Forestry Production Fishing 
# ## because it is an outlier, the standard errors are very big and so are the coefficients

# In[61]:


import pandas as pd
import numpy as np


# In[2]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId = pd.read_csv('X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.csv')


# In[3]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[4]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.head(3)


# In[5]:


pd.set_option('display.max_columns',None)


# In[6]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.head(3)


# In[7]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['CNAE 2.0 Section Name'].value_counts()


# In[8]:


48816/18


# In[9]:


248490/18


# In[10]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].value_counts()


# In[11]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[35]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].shape


# In[12]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['CNAE 2.0 Section Name']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[13]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].sum()


# ### Removing 'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture' first from mode

# In[105]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode']!='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[106]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc = X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode']!='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[107]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc.shape


# ### dropping the column Agriculture, Livestock, Forestry Production, Fishing And Aquaculture

# In[166]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc.drop('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',axis=1,inplace=True)


# In[ ]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc.shape


# In[ ]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc.head(3)


# In[ ]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['mode']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# ### dropping CNAE 2.0 Seciton Name

# In[167]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[168]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].shape


# In[169]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name']!='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[170]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc = X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name']!='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']


# In[171]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.shape


# In[172]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.head(3)


# In[173]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId.shape


# In[174]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.shape


# In[175]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['mode']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].shape


# In[176]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc[X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name']=='Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'].shape


# In[177]:


248490-13805-357


# In[178]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.shape


# ## organizing the id

# In[179]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc[['id']].tail(20)


# In[180]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc


# In[181]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.reset_index(drop=True,inplace=True)


# In[182]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['mode'].value_counts()


# In[183]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['id'].unique())


# In[184]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['CNAE 2.0 Section Name'].value_counts()


# In[185]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['id'].value_counts()


# In[186]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc


# In[187]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.tail()


# In[188]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['id'].unique())


# In[189]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId['id'].unique())


# In[190]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['id'].unique())


# In[191]:


13805-13784


# In[192]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.shape


# In[193]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['mode'].isna().sum()


# In[194]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodeAgriculturetc['CNAE 2.0 Section Name'].isna().sum()


# In[195]:


len(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['id'].unique())


# In[196]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc['id'].value_counts()


# In[197]:


list(range(1,13785))


# In[198]:


pd.DataFrame(list(range(1,13785))).rename({0:'New_ID'},axis=1)


# In[199]:


df = pd.DataFrame(list(range(1,13785))).rename({0:'New_ID'},axis=1)
df


# In[200]:


pd.DataFrame(np.repeat(df.values, 17, axis=0)).rename({0:'New_ID'},axis=1)


# In[201]:


df = pd.DataFrame(np.repeat(df.values, 17, axis=0)).rename({0:'New_ID'},axis=1)


# In[202]:


df['New_ID']


# In[203]:


df['New_ID'].isna().sum()


# In[204]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc


# In[205]:


df


# In[206]:


df.join(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc)


# In[207]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid = df.join(X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc)


# In[208]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid


# In[209]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.drop(['id'],axis=1,inplace=True)


# In[210]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.head(3)


# In[211]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.rename({'New_ID':'id'},axis=1,inplace=True)


# In[212]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.shape


# In[213]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NewId_NomodecnaeAgriculturetc.shape


# In[214]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid['mode'].isna().sum()


# In[215]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid[0:18]


# In[216]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.shape


# In[217]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.to_stata('X_choice_mode_sameids_RecifeCNAE_NoExtracInd_NoAgriculturetc_newid.dta')


# In[218]:


X_choice_mode_sameids_RecifeCNAE_NEW_NoExtracInd_NoAgriculturetc_newid.to_csv('X_choice_mode_sameids_RecifeCNAE_NoExtracInd_NoAgriculturetc_newid.csv',index=False)


# In[ ]:




