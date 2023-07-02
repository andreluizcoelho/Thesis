#!/usr/bin/env python
# coding: utf-8

# #### Clogit Model Recife

# In[1]:


#see the end of bancoesusalltabsrais2019 moralatlongcepestab_part4
#towards the end that's whre the data for Recife is 


# In[2]:


import pandas as pd
import numpy as np


# In[3]:


organizeddataRecife = pd.read_csv('organizeddatawithinRecifeshapefileborder.csv')


# In[4]:


organizeddataRecife.shape


# In[5]:


pd.set_option('display.max_columns',None)


# In[6]:


organizeddataRecife.head(3)


# In[7]:


organizeddataRecife.columns


# In[8]:


organizeddataRecife['Qtd Dias Afastamento'].unique()


# In[9]:


organizeddataRecife['Qtd Dias Afastamento'].describe()


# In[10]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

organizeddataRecife['Days Not Working'] = pd.cut(organizeddataRecife['Qtd Dias Afastamento'], bins, labels=names)

print(organizeddataRecife.dtypes)


# In[11]:


organizeddataRecife['Days Not Working'].unique()


# In[12]:


organizeddataRecife['Days Not Working'].value_counts()


# In[13]:


organizeddataRecife['Days Not Working'].isna().sum() 


# In[14]:


organizeddataRecife['Qtd Dias Afastamento'].isna().sum()


# In[15]:


organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[16]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype(str).replace('nan','0')


# In[17]:


organizeddataRecife['Days Not Working'] = organizeddataRecife['Days Not Working'].astype('category')


# In[18]:


organizeddataRecife['Days Not Working'].dtype


# In[19]:


organizeddataRecife.head(3)


# In[20]:


organizeddataRecife['Days Not Working'].value_counts()


# In[21]:


organizeddataRecife['Days Not Working'].isna().sum()


# ### Logit Model 

# In[22]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt


# In[23]:


organizeddataRecife['finalresult'].unique()


# In[24]:


organizeddataRecife['finalresult'].value_counts()


# In[25]:


organizeddataRecife['finalresult'].isna().sum()


# In[26]:


organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[27]:


organizeddataRecife = organizeddataRecife[(organizeddataRecife['finalresult']=='negative')|(organizeddataRecife['finalresult']=='positive')]


# In[28]:


organizeddataRecife.shape


# In[29]:


organizeddataRecife['finalresult'].unique()


# In[30]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].replace('negative','0').replace('positive','1')


# In[31]:


organizeddataRecife['finalresult'] = organizeddataRecife['finalresult'].astype('uint8')


# In[32]:


organizeddataRecife['finalresult'].value_counts()


# In[33]:


organizeddataRecife['finalresult'].value_counts(normalize=True)


# In[34]:


organizeddataRecife.columns


# In[35]:


organizeddataRecife.rename({'Escolaridade após 2005':'School Years', 'Vl Remun Média (SM)':'Minimum Wage','Qtd Dias Afastamento':'No Working Days','sex':'Sex','finalresult':'Final Result','distancefrommarcozero':'Distance to CBD'}, axis = 1, inplace = True)


# In[36]:


organizeddataRecife.groupby(by='agecohort').mean()


# In[37]:


organizeddataRecife.groupby(by='IBGE Subsector').mean()


# In[38]:


organizeddataRecife_IBGEmean = organizeddataRecife.groupby(by='IBGE Subsector').mean()


# In[39]:


organizeddataRecife_IBGEmean = organizeddataRecife_IBGEmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[40]:


organizeddataRecife_IBGEmean 


# In[41]:


organizeddataRecife_IBGEmean.loc['Total'] = organizeddataRecife_IBGEmean .agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Sex':'mean','Final Result':'mean','Distance to CBD':'mean'}).round(2)


# In[42]:


organizeddataRecife_IBGEmean


# In[43]:


organizeddataRecife.groupby(by='CBO Main SubGroup Name 2002 with Others').mean()


# In[44]:


organizeddataRecife_CBOmean = organizeddataRecife.groupby(by='CBO Main SubGroup Name 2002 with Others').mean()


# In[45]:


organizeddataRecife_CBOmean


# In[46]:


organizeddataRecife_CBOmean = organizeddataRecife_CBOmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[47]:


organizeddataRecife_CBOmean = organizeddataRecife_CBOmean.groupby('CBO Main SubGroup Name 2002 with Others').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Sex':'mean','Final Result':'mean','Distance to CBD':'mean'}).round(2)


# In[48]:


organizeddataRecife_CBOmean


# In[49]:


organizeddataRecife_CBOmean.loc['Total'] = organizeddataRecife_CBOmean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'mean','Security Professionals':'mean','Sex':'mean','Final Result':'mean', 'Distance to CBD':'mean'}).round(2)


# In[50]:


organizeddataRecife_CBOmean


# In[51]:


organizeddataRecife.groupby(by='CNAE 2.0 Section Name').mean()


# In[52]:


organizeddataRecife_CNAEmean = organizeddataRecife.groupby(by='CNAE 2.0 Section Name').mean()


# In[53]:


organizeddataRecife_CNAEmean = organizeddataRecife_CNAEmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[54]:


organizeddataRecife_CNAEmean


# In[55]:


organizeddataRecife_CNAEsum = organizeddataRecife.groupby(by='CNAE 2.0 Section Name').sum()


# In[56]:


organizeddataRecife_CNAEsum 


# In[57]:


organizeddataRecife_CNAEsum.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[58]:


organizeddataRecife_CNAE_summean = organizeddataRecife.groupby('CNAE 2.0 Section Name').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[59]:


organizeddataRecife_CNAE_summean 


# In[60]:


organizeddataRecife_CNAE_summean.loc['Total'] = organizeddataRecife_CNAE_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[61]:


organizeddataRecife_CNAE_summean


# In[62]:


organizeddataRecife_agecohortmean = organizeddataRecife.groupby(by='agecohort').mean()


# In[63]:


organizeddataRecife_agecohortmean = organizeddataRecife_agecohortmean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[64]:


organizeddataRecife_agecohortmean


# In[65]:


organizeddataRecife_agecohortmean.loc[:,{'School Years','Minimum Wage','No Working Days','Health Professionals','Security Professionals','Sex','Final Result','Distance to CBD'}].round(2)


# In[66]:


organizeddataRecife_agecohortsum = organizeddataRecife.groupby(by='agecohort').sum()


# In[67]:


organizeddataRecife_agecohortsum


# In[68]:


organizeddataRecife_agecohortsum = organizeddataRecife_agecohortsum.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[69]:


organizeddataRecife_agecohortsum


# In[70]:


organizeddataRecife_agecohortsum.loc[:,{'Health Professionals','Security Professionals','Sex','Final Result'}]


# In[71]:


organizeddataRecife_summean = organizeddataRecife.groupby('agecohort').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[72]:


organizeddataRecife_summean


# In[73]:


organizeddataRecifeagecohort_summean = organizeddataRecife_summean.reindex(['0 - 4', '5 - 17', '18 - 29','30 - 39','40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])


# In[74]:


organizeddataRecifeagecohort_summean


# In[75]:


organizeddataRecifeagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[76]:


organizeddataRecifeagecohort_summean.loc['Total'] = organizeddataRecifeagecohort_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[77]:


organizeddataRecifeagecohort_summean


# In[78]:


organizeddataRecife.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[79]:


organizeddataRecifemeanminimumwage_summean = organizeddataRecife.groupby('meanminimumwage').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[80]:


organizeddataRecifemeanminimumwage_summean


# In[81]:


organizeddataRecifemeanminimumwage_summean = organizeddataRecifemeanminimumwage_summean.reindex(['0.1 - 1/2', '1/2 - 1', '1 - 2','2 - 5','5 - 10', '10 - 20', '20+'])


# In[82]:


organizeddataRecifemeanminimumwage_summean


# In[83]:


organizeddataRecifemeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[84]:


organizeddataRecifemeanminimumwage_summean.loc['Total'] = organizeddataRecifemeanminimumwage_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[85]:


organizeddataRecifemeanminimumwage_summean


# In[86]:


organizeddataRecife.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[87]:


organizeddataRecife_racesummean = organizeddataRecife.groupby('race').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[88]:


organizeddataRecife_racesummean


# In[89]:


organizeddataRecife_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[90]:


organizeddataRecife_racesummean.loc['Total'] = organizeddataRecife_racesummean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[91]:


organizeddataRecife_racesummean


# In[92]:


organizeddataRecifeschooling_summean = organizeddataRecife.groupby('schooling').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2) 


# In[93]:


organizeddataRecifeschooling_summean


# In[94]:


organizeddataRecifeschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[95]:


organizeddataRecifeschooling_summean.loc['Total'] = organizeddataRecifeschooling_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[96]:


organizeddataRecifeschooling_summean


# In[97]:


organizeddataRecifedaysnotworking_summean = organizeddataRecife.groupby('Days Not Working').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[98]:


organizeddataRecifedaysnotworking_summean


# In[99]:


organizeddataRecifedaysnotworking_summean = organizeddataRecifedaysnotworking_summean.reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+'])


# In[100]:


organizeddataRecifedaysnotworking_summean


# In[101]:


organizeddataRecifedaysnotworking_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[102]:


organizeddataRecifedaysnotworking_summean.loc['Total'] = organizeddataRecifedaysnotworking_summean.agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[103]:


organizeddataRecifedaysnotworking_summean


# In[ ]:





# In[ ]:





# In[104]:


organizeddataRecife.shape


# In[105]:


organizeddataRecife.head(3)


# In[106]:


#from the article


# In[107]:


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


# ### article explanatory variables

# In[108]:


#Age and Age 2


# In[109]:


organizeddataRecife['idade']


# In[110]:


organizeddataRecife.rename({'idade':'Age'}, axis=1, inplace=True)


# In[111]:


organizeddataRecife['Age']


# In[112]:


organizeddataRecife['Age']**2


# In[113]:


organizeddataRecife['Age 2'] = organizeddataRecife['Age']**2


# In[114]:


organizeddataRecife.head(3)


# In[115]:


#Men


# In[116]:


organizeddataRecife['Sex'].unique()


# In[117]:


organizeddataRecife['Sex'].value_counts()


# In[118]:


organizeddataRecife['Sex'].value_counts(normalize=True)


# In[119]:


organizeddataRecife.rename({'Sex':'Men'},axis=1, inplace=True)


# In[120]:


organizeddataRecife['Men'].dtype


# In[121]:


organizeddataRecife['Men'] = organizeddataRecife['Men'].astype('uint8')


# In[122]:


organizeddataRecife['Men'].dtype


# In[123]:


#Non-white and Uninformed race


# In[124]:


organizeddataRecife['race'].unique()


# In[125]:


organizeddataRecife['race'].value_counts()


# In[126]:


organizeddataRecife['race'].value_counts(normalize=True)


# In[127]:


organizeddataRecife['race'].isna().sum()


# In[128]:


organizeddataRecife = organizeddataRecife.dropna(subset=['race'])


# In[129]:


organizeddataRecife.shape


# In[130]:


organizeddataRecife['race'].unique()


# In[131]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['race']


# In[132]:


organizeddataRecife['Non-White/Ignored'] = organizeddataRecife['Non-White/Ignored'].replace('Brown','Non-white').replace('Yellow','Non-white').replace('Black','Non-white').replace('Indigenous','Non-white').replace('Ignored','Uninformed race')


# In[133]:


organizeddataRecife['Non-White/Ignored'].unique()


# In[134]:


organizeddataRecife['Non-White/Ignored'].value_counts()


# In[135]:


organizeddataRecife['Non-White/Ignored'].value_counts(normalize=True)


# In[136]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['Non-White/Ignored'])], axis=1)


# In[137]:


organizeddataRecife.head(3)


# In[138]:


organizeddataRecife.rename({'Non-White/Ignored_Non-white':'Non-white', 'Non-White/Ignored_Uninformed race':'Uninformed race'},axis=1, inplace=True)


# In[139]:


organizeddataRecife.head(3)


# In[140]:


#dummies for complete primary, secondary and high education


# In[141]:


organizeddataRecife['schooling'].unique()


# In[142]:


organizeddataRecife['schooling'].value_counts()


# In[143]:


organizeddataRecife['schooling'].value_counts(normalize=True)


# In[144]:


organizeddataRecife = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['schooling'])], axis=1)


# In[145]:


organizeddataRecife.head(3)


# In[146]:


#wage


# In[147]:


organizeddataRecife['Minimum Wage'].value_counts()


# In[148]:


organizeddataRecife['Qtd Hora Contr'].unique()


# In[149]:


organizeddataRecife['Qtd Hora Contr'].value_counts()


# In[150]:


organizeddataRecife.rename({'Qtd Hora Contr':'Working hours'}, axis=1, inplace=True)


# In[151]:


organizeddataRecife['Tempo Emprego'].unique()


# In[152]:


organizeddataRecife['Tempo Emprego'].describe()


# In[153]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.replace(',','.')


# In[154]:


organizeddataRecife['Tempo Emprego'] = organizeddataRecife['Tempo Emprego'].str.lstrip('0')


# In[155]:


organizeddataRecife.rename({'Tempo Emprego':'Job tenure'},axis=1,inplace=True)


# In[156]:


organizeddataRecife['Job tenure'] = organizeddataRecife['Job tenure'].astype(float)


# In[157]:


organizeddataRecife['Job tenure'].unique()


# In[158]:


organizeddataRecife['Job tenure'].describe()


# In[159]:


organizeddataRecife['IBGE Subsector'].unique()


# In[160]:


organizeddataRecife['IBGE Subsector'].value_counts()


# In[161]:


organizeddataRecifeIBGE = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['IBGE Subsector'])], axis=1)


# In[162]:


organizeddataRecifeIBGE.shape


# In[ ]:





# In[163]:


organizeddataRecifeIBGE.to_csv('organizeddataRecifeIBGE.csv',index=False)


# In[164]:


organizeddataRecife['CBO Broad Group Name 2002'].unique()


# In[165]:


organizeddataRecife['CBO Main SubGroup Name 2002'].unique()


# In[166]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].unique()


# In[167]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].value_counts()


# In[168]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].str.title().value_counts()


# In[169]:


organizeddataRecife['CBO Main SubGroup Name 2002 with Others'] = organizeddataRecife['CBO Main SubGroup Name 2002 with Others'].str.title()


# In[170]:


organizeddataRecifeCBO = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['CBO Main SubGroup Name 2002 with Others'])],axis=1)


# In[171]:


organizeddataRecifeCBO.shape


# In[172]:


organizeddataRecifeCBO.head(3)


# In[173]:


organizeddataRecifeCBO.to_csv('organizeddataRecifeCBO.csv',index=False)


# In[ ]:





# In[174]:


organizeddataRecife['CNAE 2.0 Section Name'].unique()


# In[175]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[176]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].replace('AGRICULTURA, PECUÁRIA, PRODUÇÃO FLORESTAL, PESCA E AQÜICULTURA',
'AGRICULTURE, LIVESTOCK, FORESTRY PRODUCTION, FISHING AND AQUACULTURE')


# In[177]:


organizeddataRecife['CNAE 2.0 Section Name'].value_counts()


# In[178]:


organizeddataRecife['CNAE 2.0 Section Name'] = organizeddataRecife['CNAE 2.0 Section Name'].str.title()


# In[179]:


organizeddataRecifeCNAE = pd.concat([organizeddataRecife, pd.get_dummies(organizeddataRecife['CNAE 2.0 Section Name'])], axis = 1)


# In[180]:


pd.Series(sorted(organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()))


# In[181]:


organizeddataRecifeCNAE.head(3)


# In[182]:


organizeddataRecifeCNAE.to_csv('organizeddataRecifeCNAE.csv',index=False)


# ### preparing the variables for the logit model

# In[183]:


organizeddataRecife.shape


# In[184]:


organizeddataRecifeIBGE.shape


# In[185]:


organizeddataRecifeCBO.shape


# In[186]:


organizeddataRecifeCNAE.shape


# In[187]:


organizeddataRecife.head(3)


# ### model 1 IBGE Subsector

# In[43]:


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


# In[44]:


organizeddataRecifeIBGE = pd.read_csv('organizeddataRecifeIBGE.csv')


# In[45]:


organizeddataRecifeIBGE.shape


# In[46]:


organizeddataRecifeIBGE.head(3)


# In[47]:


pd.set_option('display.max_columns',None)


# In[48]:


organizeddataRecifeIBGE.head(3)


# In[49]:


organizeddataRecifeIBGE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[50]:


organizeddataRecifeIBGE['y']


# In[51]:


#removed No Working Days because it was not significant


# In[52]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]


# In[53]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']].dtypes


# In[54]:


organizeddataRecifeIBGE.columns.duplicated()


# In[55]:


~organizeddataRecifeIBGE.columns.duplicated()


# In[40]:


#to save it in stata


# In[56]:


organizeddataRecifeIBGE.columns


# In[41]:


organizeddataRecifeIBGE[['y','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']].to_stata('organizeddataRecifelogitIBGE.dta')


# In[57]:


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



'''
#Feature scaling
from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_train = scale.fit_transform(X_train)
X_test = scale.transform(X_test)

#the coefficients presents a better results but they are not significant anymore
'''


os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[15]:


#pip install -U scikit-learn


# In[16]:


'''
data_final_vars=X.values.tolist()
y=['y']
X=[i for i in data_final_vars if i not in y]

from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression()

rfe = RFE(logreg,20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)
'''


# The medium article where REF comes [from](https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8)

# In[58]:


#data_final_vars=X.columns.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[18]:


#the false should be removed according to Recursive Feature Elimination (RFE) and the order of the columns are in X


# In[59]:


X


# In[60]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']


# In[61]:


os_data_y['y']=os_data_y['y'].astype('int64')


# In[22]:


#I saw somewhere before that might be the dtypes the reason for getting these errors in the logit model
#"Divide by zero encountered in log" when not dividing by zero 
#inverting hessian failed, no bse or cov_params

#Chaning the y dtype from uint8 to int64 worked!!!


# In[62]:


X=os_data_X[cols]
y=os_data_y['y']


# In[72]:


#join the balanced X joined with the balanced y to save it and run it in stata


# In[65]:


X


# In[66]:


y


# In[71]:


pd.DataFrame(y)


# In[73]:


column_y = pd.DataFrame(y)


# In[75]:


column_y.join(X)


# In[76]:


column_y.join(X).to_stata('organizeddataRecifelogitIBGEbalanced.dta')


# In[63]:


y.dtype


# All StatsModels Discrete Model Logit Method to [try](https://www.statsmodels.org/devel/generated/statsmodels.discrete.discrete_model.Logit.fit.html)

# In[64]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# #### Pseudo R-squared inf

# ### model 2 CBO for Recife 

# In[213]:


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


# In[77]:


organizeddataRecifeCBO = pd.read_csv('organizeddataRecifeCBO.csv')


# In[78]:


organizeddataRecifeCBO.head(3)


# In[79]:


organizeddataRecifeCBO.shape


# In[80]:


organizeddataRecifeCBO.rename({'Final Result':'y'},axis=1,inplace=True)


# In[81]:


organizeddataRecifeCBO.rename({'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Middle Level Technicians in Biological, Biochemical, Health And Related Scis','Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences':'Middle Level Technicians In Physical, Chemical, Engineering And Related Scis'},axis=1,inplace=True)


# In[82]:


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


# In[83]:


#removing No Working Days because it was not significant 
#removing Men because it was also not significant, I put back Men, I did not put back Working Days cause in the logitcnae
#there was also not working days


# In[ ]:


#for stata


# In[90]:


organizeddataRecifeCBO[['y','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
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
                       'Distance to CBD']].to_stata('organizeddataRecifelogitCBO.dta')


# In[91]:


X = organizeddataRecifeCBO[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
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


'''
#Feature scaling
from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_train = scale.fit_transform(X_train)
X_test = scale.transform(X_test)

#the coefficients presents a better results but they are not significant anymore
'''




os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[92]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeCBO[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
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
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[93]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education',
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


# In[94]:


X=os_data_X[cols]
y=os_data_y['y']


# In[95]:


y = y.astype('int64')


# In[100]:


#for stata


# In[101]:


pd.DataFrame(y).join(X)


# In[99]:


pd.DataFrame(y).join(X).to_stata('organizeddataRecifelogitCBObalanced.dta')


# In[98]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[227]:


#pseudo R 2 inf again


# ### model 3 CNAE 2.0 Section Name

# In[102]:


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


# In[103]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[104]:


organizeddataRecifeCNAE.shape


# In[105]:


organizeddataRecifeCNAE.head(3)


# In[106]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[107]:


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


# In[ ]:


#for stata


# In[110]:


organizeddataRecifeCNAE[['y','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD']].to_stata('organizeddataRecifelogitCNAE.dta')


# In[108]:


#removing No Working Days because it was not significant


# In[111]:


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


'''
#Feature scaling
from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_train = scale.fit_transform(X_train)
X_test = scale.transform(X_test)

#the coefficients presents a better results but they are not significant anymore
'''


os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[112]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
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
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[113]:


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


# In[114]:


X=os_data_X[cols]
y=os_data_y['y']


# In[115]:


y = y.astype('int64')


# In[ ]:


#for stata


# In[117]:


pd.DataFrame(y).join(X)


# In[118]:


pd.DataFrame(y).join(X).to_stata('organizeddataRecifelogitCNAEbalanced.dta')


# In[116]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# simple interpretation of logistic regression coefficients odds ratios simply [explained](https://towardsdatascience.com/a-simple-interpretation-of-logistic-regression-coefficients-e3a40a62e8cf)
# 
# another place to interpret [it](https://www.displayr.com/how-to-interpret-logistic-regression-coefficients/)

# # Try clogit in CNAE with less variables

# In[9]:


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


# In[10]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[11]:


organizeddataRecifeCNAE.head(3)


# In[12]:


organizeddataRecifeCNAE.shape


# In[13]:


organizeddataRecifeCNAE['y']


# In[14]:


#organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[15]:


X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']]
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


# In[16]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[17]:


cols=['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']


# In[18]:


X=os_data_X[cols]
y=os_data_y['y']


# In[19]:


y = y.astype('int64')


# In[20]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[ ]:


#try to z scale in CBO and ibge


# In[22]:


#still not a good result


# In[23]:


X = organizeddataRecifeCNAE[['Age','Men','Non-white','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']]
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


# In[24]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeCNAE[['Age','Men','Non-white','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[25]:


cols=['Age','Men','Non-white','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities',
       'Public Administration, Defense And Social Security',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities','Working hours','Job tenure','Distance to CBD']


# In[26]:


X=os_data_X[cols]
y=os_data_y['y']


# In[27]:


y = y.astype('int64')


# In[28]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[29]:


#even worse


# # Probit Regression 

# probit [regression](https://jbhender.github.io/Stats506/F18/GP/Group14.html)

# In[ ]:


'''
Y = data["lfp"]
X = data.drop(["lfp"], 1)
X = sm.add_constant(X)
model = Probit(Y, X.astype(float))
probit_model = model.fit()
print(probit_model.summary())
'''


# In[31]:


from statsmodels.discrete.discrete_model import Probit
Y = organizeddataRecifeCNAE['y']
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
X=sm.add_constant(X)
model = Probit(Y, X.astype(float))
probit_model = model.fit()
print(probit_model.summary())


# In[32]:


#not a good choice, and probit is not on sklearn to balance the data and run the algorithm for better results as the Logistic Regresion


# In[21]:


#still not a good result


# ### Logit with the unbalanced data

# In[35]:


from statsmodels.discrete.discrete_model import Logit
Y = organizeddataRecifeCNAE['y']
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
X=sm.add_constant(X)
model = Logit(Y, X.astype(float))
logit_model = model.fit()
print(logit_model.summary())


# In[36]:


#horrible


# # Make logit results better

# [here](https://www.analyticsvidhya.com/blog/2021/09/guide-for-building-an-end-to-end-logistic-regression-model/)

# In[37]:


#Checking the unique value counts in columns
featureValues={}
for d in organizeddataRecifeCNAE.columns.tolist():
    count=organizeddataRecifeCNAE[d].nunique()
    if count==1:
        featureValues[d]=count
# List of columns having same 1 unique value        
cols_to_drop= list(featureValues.keys())
print("Columns having 1 unique value are :n",cols_to_drop)


# In[38]:


organizeddataRecifeCNAE.isna().sum()


# In[39]:


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
                        'Working hours','Job tenure','Distance to CBD']].isna().sum()


# In[40]:


from sklearn.model_selection import train_test_split
#split data into dependent variables(X) and independent variable(y) that we would predict
y = organizeddataRecifeCNAE['y']
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
#Let’s split X and y using Train test split
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=42,train_size=0.8)
#get shape of train and test data
print("train size X : ",X_train.shape)
print("train size y : ",y_train.shape)
print("test size X : ",X_test.shape)
print("test size y : ",y_test.shape)


# In[41]:


#Feature scaling
from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_train = scale.fit_transform(X_train)
X_test = scale.transform(X_test)


# In[42]:


#check for distribution of labels
y_train.value_counts(normalize=True)


# In[ ]:





# In[ ]:





# In[ ]:





# coefficients for binary logisti [regression](https://support.minitab.com/en-us/minitab-express/1/help-and-how-to/modeling-statistics/regression/how-to/binary-logistic-regression/interpret-the-results/all-statistics-and-graphs/coefficients/)

# [interpreting the coefficients](https://www.reddit.com/r/statistics/comments/4begf8/question_about_interpreting_negative_coefficients/)

# In[ ]:


'''
Here is the literal interpretation of these outputs:

Example 1: "A one-unit increase in X increases the odds ratio of a 1 versus a 0 by a factor of 0.67." 
Note that an "increase by a factor of 0.67" means that the odds ratio actually decreases by about 33%. 
In other words, the negative coefficient (-0.4) indicates that as X gets larger, the probability of a 1 decreases.

Example 2: "A one-unit increase in X increases the odds ratio of a 1 versus a 0 by a factor of 1.49." 
So, when X is increased by one unit, the probability of a 1 increases. 
Specifically, the odds ratio increases by 49% with a one-unit increase in X. 
So, when the coefficient is positive, as X gets larger, the probability of a 1 increases.

'''


# In[ ]:





# # Clogit Model CNAE Recife

# In[1]:


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


# this page will [help](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Converting%20Long-Format%20to%20Wide-Format.ipynb)

# In[2]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[3]:


organizeddataRecifeCNAE.head(3)


# In[4]:


organizeddataRecifeCNAE.shape


# In[5]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[657]:


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


# In[658]:


65953*20


# In[659]:


organizeddataRecifeCNAE.columns


# In[660]:


X


# In[661]:


y


# In[662]:


X.columns


# In[663]:


'''
'Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities'
'''


# ###### [new column based on if-elif-else condition](https://stackoverflow.com/questions/21702342/creating-a-new-column-based-on-if-elif-else-condition)

# In[664]:


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


# In[665]:


X


# In[666]:


X['choicenumber']=X['choice']


# In[667]:


X['id']=X.index


# In[668]:


X


# In[669]:


cols = list(X.columns)
cols = [cols[-1]] + cols[:-1]
X = X[cols]


# In[670]:


X


# In[671]:


X['id'] = X['id']+1


# In[672]:


pd.set_option('display.max_columns',None)


# In[673]:


X


# In[674]:


X_sameids = pd.DataFrame(np.repeat(X.values, 19, axis=0))
X_sameids.columns = X.columns
print(X_sameids)

#it repeats the rows 19 times, the number of choices of the economy sectors


# In[675]:


X_sameids


# In[676]:


X_sameids.head(20)


# In[677]:


#replicate the rows first, do the dummy later, it might work , nah


# In[678]:


X_sameids.head(3)


# In[679]:


#duplicate, keep first line on a column, the rest have 0 values for that column


# In[680]:


'''
https://stackoverflow.com/questions/57006508/changing-the-values-of-every-second-row-pandas-data-frame
    
https://stackoverflow.com/questions/25055712/pandas-every-nth-row
'''


# In[681]:


X_sameids.head(20)


# In[682]:


X_sameids.iloc[::19, :]


# In[683]:


X_sameids['choice'].dtype


# In[684]:


X_sameids.iloc[::19, :]


# In[685]:


X_sameids.iloc[::19, -2:-1]


# In[686]:


#X_sameids[X_sameids['Choice']>0]=0


# In[687]:


#X_sameids['choice'] = X_sameids['choice'].astype('int')


# In[688]:


X_sameids['choice'].values[:] = 0


# In[689]:


X_sameids


# In[690]:


#for col in df.columns:
#    df[col].values[:] = 0


# In[691]:


#https://stackoverflow.com/questions/42636765/how-to-set-all-the-values-of-an-existing-pandas-dataframe-to-zero


# In[692]:


X_sameids.iloc[::19, -2:-1] = 1


# In[693]:


X_sameids


# In[694]:


X_sameids['choice']


# In[695]:


X_sameids.head(20)


# In[696]:


X_sameids[X_sameids['choice']==1]


# In[697]:


X_sameids['choice'].unique()


# In[698]:


X_sameids['choice'].dtype


# In[699]:


X_sameids.head(4).T


# In[700]:


X_sameids.dtypes


# In[701]:


#X['Choice'] = X['Choice'].astype('int64')


# In[702]:


from collections import OrderedDict    # For recording the model specification 

import pandas as pd                    # For file input/output
import numpy as np                     # For vectorized math operations

import pylogit as pl                   # For MNL model estimation and
                                       # conversion from wide to long format


# see [pylogit](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Converting%20Long-Format%20to%20Wide-Format.ipynb)

# In[703]:


'''
# Create the list of individual specific variables
ind_variables = X_sameids.columns.tolist()[:15]

# Specify the variables that vary across individuals and some or all alternatives
# The keys are the column names that will be used in the long format dataframe.
# The values are dictionaries whose key-value pairs are the alternative id and
# the column name of the corresponding column that encodes that variable for
# the given alternative. Examples below.

alt_varying_variables = {u'travel_time': dict([(1, 'TRAIN_TT'),
                                               (2, 'SM_TT'),
                                               (3, 'CAR_TT')]),
                          u'travel_cost': dict([(1, 'TRAIN_CO'),
                                                (2, 'SM_CO'),
                                                (3, 'CAR_CO')]),
                          u'headway': dict([(1, 'TRAIN_HE'),
                                            (2, 'SM_HE')]),
                          u'seat_configuration': dict([(2, "SM_SEATS")])}

# Specify the availability variables
# Note that the keys of the dictionary are the alternative id's.
# The values are the columns denoting the availability for the
# given mode in the dataset.


availability_variables = {1: 'Accommodation And Food',
                          2: 'Administrative Activities And Complementary Services', 
                          3: 'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
                          4: 'Construction',
                          5: 'Education',
                          6: 'Electricity And Gas',
                          7: 'Extractive Industries',
                          8: 'Human Health And Social Services',
                          9: 'Information And Communication',
                          10: 'Other Service Activities',
                          11: 'Processing Industries',
                          12: 'Professional, Scientific And Technical Activities',
                          13: 'Public Administration, Defense And Social Security',
                          14: 'Trade; Repair Of Motor Vehicles And Motorcycles',
                          15: 'Transportation, Storage And Mail',
                          16: 'Water, Sewage, Waste Management And Decontamination Activities',
                          17: 'Arts, Culture, Sports And Recreation',
                          18: 'Real Estate Activities',
                          19: 'Financial, Insurance And Related Services Activities'}

##########
# Determine the columns for: alternative ids, the observation ids and the choice
##########
# The 'custom_alt_id' is the name of a column to be created in the long-format data
# It will identify the alternative associated with each row.
custom_alt_id = 'mode_id'

# Create a custom id column that ignores the fact that this is a 
# panel/repeated-observations dataset. Note the +1 ensures the id's start at one.
obs_id_column = 'custom_id'
X_sameids[obs_id_column] = np.arange(X_sameids.shape[0], dtype=int) + 1


# Create a variable recording the choice column
choice_column ='choice'

'''


# In[704]:


X_sameids['choicenumber'].value_counts()


# In[705]:


#the mode column need to have the same number of options, that is 1-19, then 1-19, ...


# In[706]:


X_sameids.shape


# In[707]:


X_sameids.head(n=20)


# In[708]:


list(range(1,20))


# In[709]:


df = pd.DataFrame(range(1,20))


# In[710]:


df


# In[711]:


1253107/19


# In[712]:


pd.DataFrame(df*65953)


# In[713]:


pd.concat([df]*65953)


# In[714]:


df1 = pd.concat([df]*65953)


# In[715]:


df1.head(20)


# In[716]:


df1.shape


# In[717]:


df1.rename({0:'mode'},axis=1,inplace=True)


# In[718]:


df1.head(20)


# In[719]:


X_sameids.shape


# In[720]:


df1.shape


# In[721]:


X_sameids.head(20)


# In[722]:


df1.head(20)


# In[723]:


df1.reset_index(inplace=True, drop=True)


# In[724]:


df1.head(20)


# In[725]:


df1.join(X_sameids)


# In[726]:


X_sameids = df1.join(X_sameids)


# In[727]:


X_sameids.columns


# In[728]:


X_sameids = X_sameids[['id', 'Age', 'Age 2', 'Men', 'Non-white', 'White',
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
       'Job tenure', 'Distance to CBD', 'choice', 'choicenumber','mode']]


# In[777]:


X_sameids.head(n=20)


# In[779]:


X_sameids.shape


# # X_sameids to csv and to stata

# In[778]:


X_sameids.to_csv('cnaeclogit.csv',index=False)


# In[782]:


X_sameids.to_stata('cnaeclogit.dta')


# below I adapted from the code that comes from the [swiss metro](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Main%20PyLogit%20Example.ipynb) and the train [example](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Converting%20Long-Format%20to%20Wide-Format.ipynb)

# In[767]:


# ind_vars is a list of strings denoting the column
# headings of data that varies across choice situations,
# but not across alternatives. In our data, this is
# the household income and party size.
ind_variables = X_sameids.columns.tolist()[:]

# alt_specific_vaars is a list of strings denoting the
# column headings of data that vary not only across
# choice situations but also across all alternatives.
# These are columns such as the "level of service"
# variables.


alt_varying_variables = ['Age','Age 2', 'Men','Non-white','Uninformed race', 
                                 'Complete primary education','Complete secondary education', 
                                 'Complete higher education', 'Minimum Wage','Working hours',
                                 'Job tenure', 'Distance to CBD']

#actually I don't have that, no column values vary for the same id, but I am repeating the variables to see if it runs

# subset_specific_vars is a dictionary. Each key is a
# string that denotes a variable that is subset specific.
# Each value is a list of alternative ids, over which the
# variable actually varies. Note that subset specific
# variables vary across choice situations and across some
# (but not all) alternatives. This is most common when
# using variables that are not meaningfully defined for
# all alternatives. An example of this in our dataset is
# terminal time ("ttme"). This variable is not meaningfully
# defined for the "car" alternative. Therefore, it is always
# zero. Note "4" is the id for the "car" alternative

#alternative_name_dict = {'mode':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]} 

availability_variables = {'mode':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]} 

'''
availability_variables = {1: 'Accommodation And Food',
                          2: 'Administrative Activities And Complementary Services', 
                          3: 'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
                          4: 'Construction',
                          5: 'Education',
                          6: 'Electricity And Gas',
                          7: 'Extractive Industries',
                          8: 'Human Health And Social Services',
                          9: 'Information And Communication',
                          10: 'Other Service Activities',
                          11: 'Processing Industries',
                          12: 'Professional, Scientific And Technical Activities',
                          13: 'Public Administration, Defense And Social Security',
                          14: 'Trade; Repair Of Motor Vehicles And Motorcycles',
                          15: 'Transportation, Storage And Mail',
                          16: 'Water, Sewage, Waste Management And Decontamination Activities',
                          17: 'Arts, Culture, Sports And Recreation',
                          18: 'Real Estate Activities',
                          19: 'Financial, Insurance And Related Services Activities'}
'''

#actually I don't have that, no column values vary for the same id, but I am repeating the variables to see if it runs

custom_alt_id='choicenumber'

# obs_id_col is the column denoting the id of the choice
# situation. If one was using a panel dataset, with multiple
# choice situations per unit of observation, the column
# denoting the unit of observation would be listed in
# ind_vars (i.e. with the individual specific variables)
obs_id_column = 'id' #the individual

# alt_id_col is the column denoting the id of the alternative
# corresponding to a given row.

#this is probably equivalent to the custom_alt_id

#alternative_id_column = 'mode'


    
# choice_col is the column denoting whether the alternative
# on a given row was chosen in the corresponding choice situation
choice_column = 'choice'

# Lastly, alt_name_dict is not necessary. However, it is useful.
# It records the names corresponding to each alternative, if there
# are any, and allows for the creation of meaningful column names
# in the wide-format data (such as when creating the columns
# denoting the available alternatives in each choice situation).
# The keys of alt_name_dict are the unique alternative ids, and
# the values are the names of each alternative.


# In[768]:


X_sameids.head(3)


# In[769]:


X_sameids.tail()


# In[770]:


X_sameids.head(21)


# In[776]:


# Finally, we can create the wide format dataframe
wide_X_sameids = pl.convert_long_to_wide(X_sameids,
                                         ind_variables, 
                                         alt_varying_variables, 
                                         availability_variables, 
                                         obs_id_column, 
                                         choice_column,
                                         custom_alt_id)

# Let's look at the created dataframe, transposed for easy viewing
wide_X_sameids.head().T


# In[761]:


#the positional argument error will keep appearing when one of the 7 required variables is missing for the code to run


# [example](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/mlogit%20Benchmark--Train%20and%20Fishing.ipynb)

# In[762]:


'''
# Create the model specification
train_spec = OrderedDict()
train_names = OrderedDict()

# Note that for the specification dictionary, the
# keys should be the column names from the long format
# dataframe and the values should be a list with a combination
# of alternative id's and/or lists of alternative id's. There 
# should be one element for each beta that will be estimated 
# in relation to the given column. Lists of alternative id's
# mean that all of the alternatives in the list will get a
# single beta for them, for the given variable.
# The names dictionary should contain one name for each
# element (that is each alternative id or list of alternative 
# ids) in the specification dictionary value for the same 
# variable

for col, display_name in [("price_euros", "price"), 
                          ("time_hours", "time"), 
                          ("change", "change"), 
                          ("comfort", "comfort")]:
    train_spec[col] = [[1, 2]]
    train_names[col] = [display_name]
'''


# In[763]:


X_sameids.columns


# In[764]:


'''
cnae_spec = OrderedDict()
cnae_names = OrderedDict()

for col, display_name in [('Accommodation And Food','Administrative Activities And Complementary Services'),
       ('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction'), 
        ('Education', 'Electricity And Gas'),
       ('Extractive Industries', 'Human Health And Social Services'),
       ('Information And Communication', 'Other Service Activities'),
       ('Processing Industries','Professional, Scientific And Technical Activities'),
       ('Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles'),
       ('Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities'),
       ('Arts, Culture, Sports And Recreation', 'Real Estate Activities'),
       ('Financial, Insurance And Related Services Activities')]:


    cnae_spec[col]=[[1,2]]
    cnae_names[col]=[cnae_names]

'''


# In[765]:


cnae_spec = OrderedDict()
cnae_names = OrderedDict()

for col, display_name in [('Accommodation And Food','Administrative Activities And Complementary Services'),
       ('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction'), 
        ('Education', 'Electricity And Gas'),
       ('Extractive Industries', 'Human Health And Social Services'),
       ('Information And Communication', 'Other Service Activities'),
       ('Processing Industries','Professional, Scientific And Technical Activities'),
       ('Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles'),
       ('Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities'),
       ('Arts, Culture, Sports And Recreation', 'Real Estate Activities'),
       ('Financial, Insurance And Related Services Activities','Distance to CBD')]:


    cnae_spec[col]=[[1,2]]
    cnae_names[col]=[cnae_names]


# In[766]:


wide_X_sameids.columns


# In[754]:


list(wide_X_sameids.columns)


# In[468]:


# Estimate the multinomial logit model (MNL)
X_mnl = pl.create_choice_model(data=wide_X_sameids,
                                        alt_id_col=alternative_id_column,
                                        obs_id_col=obs_id_column,
                                        choice_col=choice_column,
                                        specification=cnae_spec,
                                        model_type='MNL',
                                        names=cnae_names)

# Specify the initial values and method for the optimization.
X_mnl.fit_mle(np.zeros(14))

# Look at the estimation results
X_mnl.get_statsmodels_summary()


# In[783]:


#I'm convinced that it is not a good choice because every economic section column should vary,
#that is, all of them should have a 1 as a choice for dummy for each id that is repeated 19 times
#if each one is 1 and the rest of the economic sectors are zeros, how do I know which one was chosen, 
#that's where the choice column comes in handy, but without the 1s for each id it won't work, 
#that is, although each id will be repeated 19 times, and each row for that id will have a 1 for each economic 
#sector and 0 for the rest, the choice column will show which one was actually chosen
#besides that there need to be other columns where the numbers will vary for each different 19 rows with the same id, 
#it can be a row repeated 19 times with all equal values for a the other columns besides the economic sectors


# In[784]:


#https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Main%20PyLogit%20Example.ipynb
#https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Converting%20Long-Format%20to%20Wide-Format.ipynb
#https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/mlogit%20Benchmark--Train%20and%20Fishing.ipynb


# In[ ]:





# # Testing clogit for only y = 1, that is the positive cases

# In[27]:


'''
21/02/2022 15:32 call from tatiane

clogit, multilogit
clogit with only all positive covid individual cases
multilogit categorical variable for each sector 
'''


# In[28]:


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


# In[29]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[30]:


organizeddataRecifeCNAE.head(3)


# In[31]:


organizeddataRecifeCNAE.shape


# In[32]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[33]:


organizeddataRecifeCNAE.head(3)


# In[34]:


organizeddataRecifeCNAE[organizeddataRecifeCNAE['y']==1]


# In[35]:


organizeddataRecifeCNAE_onlypositives = organizeddataRecifeCNAE[organizeddataRecifeCNAE['y']==1] #only positive cases


# In[36]:


organizeddataRecifeCNAE_onlypositives.columns


# In[37]:


organizeddataRecifeCNAE_onlypositives['CNAE 2.0 Section Name']


# In[38]:


X = organizeddataRecifeCNAE_onlypositives[['CNAE 2.0 Section Name','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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
y = organizeddataRecifeCNAE_onlypositives['y']


# In[39]:


X


# In[40]:


X.reset_index(drop=True, inplace=True)


# In[41]:


X.head(3)


# In[42]:


y


# In[43]:


X.columns


# In[44]:


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


# In[45]:


X.head()


# In[46]:


X['choicenumber']=X['choice']


# In[47]:


X['id']=X.index


# In[48]:


X


# In[49]:


X


# In[50]:


cols = list(X.columns)
cols = [cols[-1]] + cols[:-1]
X = X[cols]


# In[51]:


X


# In[52]:


X['id'] = X['id']+1


# In[53]:


pd.set_option('display.max_columns',None)


# In[54]:


X.head()


# In[55]:


X_sameids = pd.DataFrame(np.repeat(X.values, 19, axis=0))
X_sameids.columns = X.columns
print(X_sameids)


#it repeats the rows 19 times, the number of choices of the economy sectors
#this replicates the first row 19 times, then the 20th row 19 times, then the 39th row 19 times


# In[56]:


X_sameids.head()


# In[57]:


X_sameids


# In[58]:


X_sameids.head(20)


# In[59]:


X_sameids.head(3)


# In[60]:


#replicate the rows first, do the dummy later, it might work , nah


# In[61]:


#duplicate, keep first line on a column, the rest have 0 values for that column


# In[62]:


'''
https://stackoverflow.com/questions/57006508/changing-the-values-of-every-second-row-pandas-data-frame
    
https://stackoverflow.com/questions/25055712/pandas-every-nth-row
'''


# In[63]:


X_sameids.head(20)


# In[64]:


X_sameids.iloc[::19, :]


# In[65]:


X_sameids['choice'].dtype


# In[66]:


X_sameids.iloc[::19, :]


# In[67]:


X_sameids.iloc[::19, -2:-1]


# In[68]:


X_sameids['choice'].values[:] = 0


# In[69]:


X_sameids


# In[70]:


X_sameids.iloc[::19, -2:-1] = 1


# In[71]:


X_sameids


# In[72]:


X_sameids['choice']


# In[73]:


X_sameids.head()


# In[74]:


X_sameids[X_sameids['choice']==1]


# In[75]:


X_sameids['choice'].unique()


# In[76]:


X_sameids['choice'].dtype


# In[77]:


X_sameids


# In[78]:


#do keep first, the rest 0, for every single column in the econmomic sector, just like was done with the choice column
#it won't work 


# In[79]:


#add one to all economics sectors columns, the 0s will become 1s, the 1s will become 2s


# In[80]:


'''
X_sameids['Accommodation And Food'] = X_sameids['Accommodation And Food']+1
X_sameids['Administrative Activities And Complementary Services'] = X_sameids['Administrative Activities And Complementary Services']+1
X_sameids['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture'] = X_sameids['Agriculture, Livestock, Forestry Production, Fishing And Aquaculture']+1
X_sameids['Construction'] = X_sameids['Construction']+1
X_sameids['Education'] = X_sameids['Education']+1
X_sameids['Electricity And Gas'] = X_sameids['Electricity And Gas']+1
X_sameids['Extractive Industries'] = X_sameids['Extractive Industries']+1
X_sameids['Human Health And Social Services'] = X_sameids['Human Health And Social Services']+1
X_sameids['Information And Communication'] = X_sameids['Information And Communication']+1
X_sameids['Other Service Activities'] = X_sameids['Other Service Activities']+1
X_sameids['Processing Industries'] = X_sameids['Processing Industries']+1
X_sameids['Professional, Scientific And Technical Activities'] = X_sameids['Professional, Scientific And Technical Activities']+1
X_sameids['Public Administration, Defense And Social Security'] = X_sameids['Public Administration, Defense And Social Security']+1
X_sameids['Trade; Repair Of Motor Vehicles And Motorcycles'] = X_sameids['Trade; Repair Of Motor Vehicles And Motorcycles']+1
X_sameids['Transportation, Storage And Mail'] = X_sameids['Transportation, Storage And Mail']+1
X_sameids['Water, Sewage, Waste Management And Decontamination Activities'] = X_sameids['Water, Sewage, Waste Management And Decontamination Activities']+1
X_sameids['Arts, Culture, Sports And Recreation'] = X_sameids['Arts, Culture, Sports And Recreation']+1
X_sameids['Real Estate Activities'] = X_sameids['Real Estate Activities'] +1
X_sameids['Financial, Insurance And Related Services Activities'] = X_sameids['Financial, Insurance And Related Services Activities'] +1
'''


# In[81]:


X_sameids


# In[82]:


#does it make sense for the clogit to have only y = 1, or would it make sense for the multilogit to have y = 1?
#it makes sense for both


# In[83]:


#X_sameids.head(20)


# In[84]:


X_sameids.head()


# In[85]:


#pd.set_option('display.max_rows',100)


# In[86]:


X_sameids.head(100)


# In[87]:


#need to build the dummy columns of having 1s for each column and 0 for the choice, only one row in each column can be choice column
#of 1


# In[88]:


#mode column with all the dummies vertically


# In[89]:


#make the mode column after the ids are divided or or keep the original mode column?


# In[90]:


X_sameids.head()


# In[91]:


#X_sameids won't help much because it gets the first row and repeats it for 19 rows 


# In[92]:


X


# In[93]:


X.head()


# In[94]:


X.columns


# In[95]:


'''
X[['id','CNAE 2.0 Section Name','Age','Accommodation And Food',
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
'''


# In[96]:


X_idagecnaesectionnames = X[['id','CNAE 2.0 Section Name','Age','Accommodation And Food',
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


# In[97]:


X_idagecnaesectionnames.head()


# In[98]:


X_idagecnaesectionnames


# In[99]:


X_idagecnaesectionnames.append([X_idagecnaesectionnames]*18,ignore_index=True) #it repeats the whole dataframe 


# In[100]:


X_idagecnaesectionnames_repeatedataframe = X_idagecnaesectionnames.append([X_idagecnaesectionnames]*18,ignore_index=True)


# In[101]:


X.head()


# In[102]:


X


# In[103]:


X_idagecnaesectionnames_repeatedataframe.head()


# In[104]:


X_idagecnaesectionnames_repeatedataframe.columns


# In[105]:


X_idagecnaesectionnames_repeatedataframe.rename({'id':'id_1', 'CNAE 2.0 Section Name':'CNAE 2.0 Section Name_1', 'Age':'Age_1', 'Accommodation And Food':'Accommodation And Food_1',
       'Administrative Activities And Complementary Services':'Administrative Activities And Complementary Services_1',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture_1',
       'Construction':'Construction_1', 'Education':'Education_1', 'Electricity And Gas':'Electricity And Gas_1',
       'Extractive Industries':'Extractive Industries_1', 'Human Health And Social Services':'Human Health And Social Services_1',
       'Information And Communication':'Information And Communication_1', 'Other Service Activities':'Other Service Activities_1',
       'Processing Industries':'Processing Industries_1',
       'Professional, Scientific And Technical Activities':'Professional, Scientific And Technical Activities_1',
       'Public Administration, Defense And Social Security':'Public Administration, Defense And Social Security_1',
       'Trade; Repair Of Motor Vehicles And Motorcycles':'Trade; Repair Of Motor Vehicles And Motorcycles_1',
       'Transportation, Storage And Mail':'Transportation, Storage And Mail_1',
       'Water, Sewage, Waste Management And Decontamination Activities':'Water, Sewage, Waste Management And Decontamination Activities_1',
       'Arts, Culture, Sports And Recreation':'Arts, Culture, Sports And Recreation_1', 'Real Estate Activities':'Real Estate Activities_1',
       'Financial, Insurance And Related Services Activities':'Financial, Insurance And Related Services Activities_1'},axis=1,inplace=True)


# In[106]:


X_idagecnaesectionnames_repeatedataframe.head()


# In[107]:


X_idagecnaesectionnames_repeatedataframe.shape


# In[108]:


X_sameids.shape


# In[109]:


X_sameids.head()


# when the error 'columns overlap but no suffix specified' occurs it's probably because the columns have the same names, you can either use merge instead of join, or you can pass suffixes in your [call](https://stackoverflow.com/questions/63311271/pandas-columns-overlap-but-no-suffix-specified)
# example: df_joined = df_games.set_index('player_id').join(players.set_index('player_id'), lsuffix="_games", rsuffix="_players")

# In[110]:


X_sameids.join(X_idagecnaesectionnames_repeatedataframe)


# In[111]:


Xjoined_repeatedsamerowsids_repeateddataframe = X_sameids.join(X_idagecnaesectionnames_repeatedataframe)


# In[112]:


Xjoined_repeatedsamerowsids_repeateddataframe.shape


# In[113]:


Xjoined_repeatedsamerowsids_repeateddataframe.head(7)


# In[114]:


Xjoined_repeatedsamerowsids_repeateddataframe.columns


# In[115]:


Xjoined_repeatedsamerowsids_repeateddataframe[['id', 'CNAE 2.0 Section Name', 'Age', 'Age 2', 'Men', 'Non-white',
       'White', 'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours',
       'Job tenure', 'Distance to CBD', 'choice', 'choicenumber', 'id_1',
       'CNAE 2.0 Section Name_1', 'Age_1', 'Accommodation And Food_1',
       'Administrative Activities And Complementary Services_1',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture_1',
       'Construction_1', 'Education_1', 'Electricity And Gas_1',
       'Extractive Industries_1', 'Human Health And Social Services_1',
       'Information And Communication_1', 'Other Service Activities_1',
       'Processing Industries_1',
       'Professional, Scientific And Technical Activities_1',
       'Public Administration, Defense And Social Security_1',
       'Trade; Repair Of Motor Vehicles And Motorcycles_1',
       'Transportation, Storage And Mail_1',
       'Water, Sewage, Waste Management And Decontamination Activities_1',
       'Arts, Culture, Sports And Recreation_1', 'Real Estate Activities_1',
       'Financial, Insurance And Related Services Activities_1']].head(7)


# In[116]:


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


# In[117]:


mode


# In[118]:


mode.rename({0:'mode'},axis=1,inplace=True)


# In[119]:


mode


# In[120]:


mode.reindex(['Accommodation And Food',
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


# In[121]:


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


# In[122]:


mode.reset_index()


# In[123]:


mode = mode.reset_index()


# In[124]:


mode.loc[:,['index']]


# In[125]:


mode = mode.loc[:,['index']]


# In[126]:


mode.rename({'index':'mode'},axis=1,inplace=True)


# In[127]:


mode


# In[128]:


[mode]*18


# In[129]:


Xjoined_repeatedsamerowsids_repeateddataframe.shape


# In[130]:


X.shape


# In[131]:


mode.append([mode]*19519,ignore_index=True)


# In[132]:


mode = mode.append([mode]*19519,ignore_index=True)


# In[133]:


mode.shape


# In[134]:


mode


# In[135]:


mode.join(Xjoined_repeatedsamerowsids_repeateddataframe)


# In[136]:


Xjoinedmode_repeatedsamerowsids_repeateddataframe = mode.join(Xjoined_repeatedsamerowsids_repeateddataframe)


# In[137]:


Xjoinedmode_repeatedsamerowsids_repeateddataframe.shape


# In[138]:


Xjoinedmode_repeatedsamerowsids_repeateddataframe.head(7)


# In[139]:


#make rows = column being equal to 1, or make another pd.DataFrame and repeat it


# In[140]:


mode


# In[141]:


pd.get_dummies(mode,columns=['mode'])


# In[142]:


pd.concat([mode, pd.get_dummies(mode['mode'])],axis=1)


# In[143]:


mode_dummies = pd.concat([mode, pd.get_dummies(mode['mode'])],axis=1)


# In[144]:


mode_dummies


# In[145]:


mode_dummies.columns


# In[146]:


mode['mode'].unique()


# In[147]:


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


# In[148]:


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


# In[149]:


mode_dummies.shape


# In[150]:


mode_dummies.head(7)


# In[151]:


Xjoinedmode_repeatedsamerowsids_repeateddataframe.head(7)


# In[152]:


X_sameids.head(7)


# In[153]:


X_sameids.columns


# In[154]:


X_sameids[['id', 'CNAE 2.0 Section Name', 'Age', 'Age 2', 'Men', 'Non-white',
       'White', 'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours',
       'Job tenure', 'Distance to CBD', 'choice', 'choicenumber']]


# In[155]:


X_sameidsforjoin = X_sameids[['id', 'CNAE 2.0 Section Name', 'Age', 'Age 2', 'Men', 'Non-white',
       'White', 'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours',
       'Job tenure', 'Distance to CBD', 'choice', 'choicenumber']]


# In[156]:


mode_dummies.join(X_sameidsforjoin)


# In[157]:


Xjoined_mode_sameids = mode_dummies.join(X_sameidsforjoin)


# In[158]:


Xjoined_mode_sameids.head(6)


# In[159]:


Xjoined_mode_sameids.columns


# In[160]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']]


# In[161]:


Xjoined_mode_sameids.rename({'choice':'choice_cnaesectioname'},axis=1,inplace=True)


# In[162]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']]


# In[163]:


Xjoined_mode_sameids['mode'].equals(Xjoined_mode_sameids['CNAE 2.0 Section Name'])


# Check if column value is in other columns in [pandas](https://stackoverflow.com/questions/43093394/check-if-column-value-is-in-other-columns-in-pandas)
# Pandas: Check if row exists with certain [values](https://stackoverflow.com/questions/24761133/pandas-check-if-row-exists-with-certain-values)
# Pandas conditional creation of a series/dataframe [column](https://stackoverflow.com/questions/19913659/pandas-conditional-creation-of-a-series-dataframe-column)

# In[164]:


Xjoined_mode_sameids['mode'].isin(Xjoined_mode_sameids['CNAE 2.0 Section Name']) #checks all rows in any order


# In[165]:


Xjoined_mode_sameids['mode'].eq(Xjoined_mode_sameids['CNAE 2.0 Section Name']) #check for that especific row position


# In[166]:


Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['mode'].eq(Xjoined_mode_sameids['CNAE 2.0 Section Name'])


# In[167]:


Xjoined_mode_sameids


# In[168]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].head(40)


# In[169]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].head(6)


# In[170]:


Xjoined_mode_sameids['choice'].dtype


# In[171]:


Xjoined_mode_sameids['choice'].astype(int)


# In[172]:


Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['choice'].astype(int)


# In[173]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].head(6)


# In[174]:


Xjoined_mode_sameids['choice'].sum()


# In[175]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].tail(3)


# In[176]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].head(3)


# In[177]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']]


# In[178]:


Xjoined_mode_sameids.shape


# In[179]:


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
        'Age', 'Age 2', 'Men', 'Non-white', 'White',
       'Uninformed race', 'Complete primary education',
       'Complete secondary education', 'Complete higher education',
       'Minimum Wage', 'Working hours', 'Job tenure', 'Distance to CBD']].shape


# In[180]:


Xjoined_mode_sameids


# In[181]:


Xjoined_mode_sameids['Age']


# In[182]:


Xjoined_mode_sameids['Age'].astype(int)


# In[183]:


Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].astype(int)


# In[184]:


list(Xjoined_mode_sameids['Age'].unique())


# In[185]:


Xjoined_mode_sameids['Age 2'] = Xjoined_mode_sameids['Age 2'].astype(int)


# In[186]:


#Xjoined_mode_sameids['Age'].str.rstrip('.0') using this the 0 disappeared, leving empty string, which is tricky to replace 


# In[187]:


Xjoined_mode_sameids['Age 2']


# In[188]:


#Xjoined_mode_sameids['Age 2'].str.rstrip('.0')


# In[189]:


#test 
'''

data = {'test': [100, 0.0, 00.00, 10.0, 1],
        'test1':[0.1,00.1,000.1,10.00,10.0]
       }
df = pd.DataFrame(data)
df

df['test']=df['test'].astype(str)
df['test'].str.rstrip('.0')
'''


# In[190]:


#Xjoined_mode_sameids['Age'].replace(np.nan,0) did not replace the '' by 0


# In[191]:


#Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].str.replace(' ','0') did not replace the '' by 0


# In[192]:


#Xjoined_mode_sameids['Age'].str.replace("''",'0') also did not replace


# In[193]:


#Xjoined_mode_sameids[Xjoined_mode_sameids['Age']=='']


# In[194]:


#Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].fillna(0)


# In[195]:


#Xjoined_mode_sameids['Age'].replace(r'^\s*$','0',regex=True)


# In[196]:


#Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].str.rstrip('.0')
#Xjoined_mode_sameids['Age 2'] = Xjoined_mode_sameids['Age 2'].str.rstrip('.0')


# In[197]:


#Xjoined_mode_sameids.to_stata('X_choice_mode_sameids.dta')

'''
ValueError: Column `id` cannot be exported.

Only string-like object arrays
containing all strings or a mix of strings and None can be exported.
Object arrays containing only null values are prohibited. Other object
types cannot be exported and must first be converted to one of the
supported types
'''
#all the other variables with dtypes object had the same error


# In[198]:


Xjoined_mode_sameids.dtypes


# In[199]:


Xjoined_mode_sameids['id'] = Xjoined_mode_sameids['id'].astype(str)
Xjoined_mode_sameids['mode'] = Xjoined_mode_sameids['mode'].astype(str)
Xjoined_mode_sameids['CNAE 2.0 Section Name'] = Xjoined_mode_sameids['CNAE 2.0 Section Name'].astype(str)

Xjoined_mode_sameids['choice'] = Xjoined_mode_sameids['choice'].astype('uint8')

Xjoined_mode_sameids['choice_cnaesectioname'] = Xjoined_mode_sameids['choice_cnaesectioname'].astype('uint8')

Xjoined_mode_sameids['choicenumber'] = Xjoined_mode_sameids['choicenumber'].astype(int)

Xjoined_mode_sameids['Age'] = Xjoined_mode_sameids['Age'].astype(int)
Xjoined_mode_sameids['Age 2'] = Xjoined_mode_sameids['Age 2'].astype(int)
Xjoined_mode_sameids['Men'] = Xjoined_mode_sameids['Men'].astype('uint8')
Xjoined_mode_sameids['Non-white'] = Xjoined_mode_sameids['Non-white'].astype('uint8')
Xjoined_mode_sameids['White'] = Xjoined_mode_sameids['White'].astype('uint8')
Xjoined_mode_sameids['Uninformed race'] = Xjoined_mode_sameids['Uninformed race'].astype('uint8')
Xjoined_mode_sameids['Complete primary education'] = Xjoined_mode_sameids['Complete primary education'].astype('uint8')
Xjoined_mode_sameids['Complete secondary education'] = Xjoined_mode_sameids['Complete secondary education'].astype('uint8')
Xjoined_mode_sameids['Complete higher education'] = Xjoined_mode_sameids['Complete higher education'].astype('uint8')
Xjoined_mode_sameids['Minimum Wage'] = Xjoined_mode_sameids['Minimum Wage'].astype(int)
Xjoined_mode_sameids['Working hours'] = Xjoined_mode_sameids['Working hours'].astype(int)
Xjoined_mode_sameids['Job tenure'] = Xjoined_mode_sameids['Job tenure'].astype(float)
Xjoined_mode_sameids['Distance to CBD'] = Xjoined_mode_sameids['Distance to CBD'].astype(float)


# In[200]:


Xjoined_mode_sameids.dtypes


# In[201]:


Xjoined_mode_sameids.to_csv('X_choice_mode_sameids.csv',index=False)


# In[202]:


Xjoined_mode_sameids.to_stata('X_choice_mode_sameids.dta')


# In[ ]:





# # Running the Conditional logit model CNAE Recife only positive cases

# In[3]:


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
from collections import OrderedDict 
import pylogit as pl


# In[4]:


X_choice_mode_sameids = pd.read_csv('X_choice_mode_sameids.csv')


# In[5]:


X_choice_mode_sameids.shape


# In[6]:


pd.set_option('display.max_columns',None)


# In[7]:


X_choice_mode_sameids.head(4)


# In[9]:


X_choice_mode_sameids.dtypes


# # Before running the clogit make the rows in the columns vary
# #### otherwise it won't work 

# In[1]:


'''
reunião 15-03-2022 17:30

criar individuos representativos 
criar uma dummy

pegar a média de cada setor por idade

w-age salário médio de todas as pessoas que tiverem a idade dele em cada setor 
w-anosdeestudo  salário médio em cada um dos setores das pessoas que tem mesmos anos de estudo 
w-raça salário médio em cada setor das pessoas que tem a mesma raça

Fazer isso com todas as colunas
Deixar as colunas variando
'''


# ### w-age salário médio de todas as pessoas que tiverem a idade dele em cada setor  

# In[10]:


X_choice_mode_sameids.head(4)


# In[11]:


X_choice_mode_sameids['Age']


# In[12]:


X_choice_mode_sameids['Age'].unique()


# In[13]:


X_choice_mode_sameids['Age'].describe()


# In[14]:


X_choice_mode_sameids['Age'].value_counts()


# In[17]:


#age 10 1 person that repeats 19 rows, it will be for only 1 sector
#so, if wanting to get the average for each sector for that age, age 10 will only have one sector


# In[16]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==10].groupby('CNAE 2.0 Section Name').mean()


# In[18]:


X_choice_mode_sameids['Age'].value_counts(normalize=True)*100


# In[19]:


X_choice_mode_sameids.head(20)


# In[20]:


X_choice_mode_sameids['mode'].value_counts()


# In[21]:


X_choice_mode_sameids['CNAE 2.0 Section Name'].value_counts()


# In[22]:


X_choice_mode_sameids['Minimum Wage'].describe()


# In[23]:


X_choice_mode_sameids['Minimum Wage'].value_counts(normalize=True)*100


# In[ ]:





# In[ ]:


### w-age salário médio de todas as pessoas que tiverem a idade dele em cada setor  


# In[24]:


X_choice_mode_sameids.groupby(by='CNAE 2.0 Section Name').mean()


# In[25]:


X_choice_mode_sameids.groupby(by='mode').mean()


# In[26]:


X_choice_mode_sameids.head(20)


# In[24]:


X_choice_mode_sameids.groupby(by='CNAE 2.0 Section Name').mean('Age')


# In[27]:


X_choice_mode_sameids.groupby(by='CNAE 2.0 Section Name').mean('Age'==47) #no difference, with or without 47


# In[28]:


X_choice_mode_sameids.head(3)


# In[29]:


X_choice_mode_sameids.columns


# In[31]:


X_choice_mode_sameids.loc[:,['id', 'mode', 'CNAE 2.0 Section Name', 'choice',
       'choice_cnaesectioname', 'choicenumber','Age', 'Age 2',
       'Complete primary education', 'Complete secondary education',
       'Complete higher education', 'Minimum Wage']]


# In[32]:


X_choice_mode_sameids.groupby('Age')['CNAE 2.0 Section Name'].sum()


# In[33]:


X_choice_mode_sameids.groupby('Age').agg({'CNAE 2.0 Section Name':'sum'})

#X_choice_mode_sameids.groupby('Age').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[32]:


#X_choice_mode_sameids.groupby('Age').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[71]:


#X_choice_mode_sameids.groupby('Age').agg({'School Years':'mean', 'Minimum Wage':'mean','No Working Days':'mean','Health Professionals':'sum','Security Professionals':'sum','Sex':'sum','Final Result':'sum'}).round(2)


# In[34]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==47]


# In[35]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name').mean()


# In[36]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==56].groupby('CNAE 2.0 Section Name').mean()


# In[37]:


X_choice_mode_sameids['Age'].unique()


# In[38]:


X_choice_mode_sameids['Age'].value_counts()


# In[39]:


X_choice_mode_sameids['Age'].head(50)


# In[78]:


'''
array([ 47,  56,  60,  53,  57,  63,  48,  51,  50,  58,  59,  54,  61,
        46,  70,  49,  55,  62,  30,  52,  40,  25,  66,  26,  64,  67,
        44,  22,  19,  71,  65,  24,  45,  15,  35,  43,  42,  69,  27,
        33,  23,  31,  21,  68,  28,  39,  72,  38,   0,  77,  20,  41,
        16,  37,  74,  34,  32,  29,  73,  78,  36,  76,  11,  80,   1,
       103,  84,  82,  18,  12,   2,  17,  83,  86,  13,  94,  75,   7,
        14,  81,  10], dtype=int64)
'''


# In[40]:


X_choice_mode_sameids.head(3)


# groupby [stackoverflow](https://stackoverflow.com/questions/24980437/pandas-groupby-and-then-merge-on-original-table)

# three-way [joining](https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns)

# ### 8 most used commands from [pandas medium](https://towardsdatascience.com/i-have-been-using-pandas-for-3-years-here-are-the-8-functions-i-use-the-most-4e54f4db5656) 

# ### Multiple Dataframes concat, [stackoverlow](https://stackoverflow.com/questions/36526282/append-multiple-pandas-data-frames-at-once)

# In[77]:


w_age47 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age56 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==56].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age60 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==60].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age53 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==53].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age57 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==57].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age63 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==63].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age48 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==48].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age51 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==51].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age50 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==50].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age58 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==58].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age59 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==59].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age54 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==54].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age61 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==61].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age46 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==46].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age70 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==70].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age49 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==49].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age55 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==55].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age62 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==62].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age30 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==30].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age52 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==52].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age40 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==40].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age25 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==25].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age66 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==66].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age26 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==26].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age64 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==64].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age67 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==67].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age44 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==44].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age22 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==22].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age19 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==19].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age71 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==71].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age65 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==65].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age24 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==24].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age45 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==45].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age15 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==15].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age35 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==35].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age43 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==43].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age42 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==42].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age69 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==69].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age27 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==27].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age33 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==33].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age23 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==23].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age31 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==31].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age21 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==21].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age68 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==68].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age28 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==28].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age39 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==39].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age72 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==72].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age38 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==38].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age0 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==0].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age77 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==77].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age20 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==20].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age41 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==41].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age16 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==16].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age37 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==37].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age74 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==74].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age34 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==34].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age32 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==32].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age29 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==29].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age73 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==73].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age78 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==78].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age36 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==36].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age76 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==76].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age11 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==11].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age80 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==80].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age1 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==1].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age103 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==103].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age84 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==84].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age82 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==82].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age18 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==18].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age12 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==12].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age2 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==2].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age17 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==17].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age83 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==83].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age86 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==86].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age13 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==13].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age94 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==94].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age75 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==75].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age7 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==7].groupby('CNAE 2.0 Section Name').mean().reset_index()

w_age14 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==14].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age81 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==81].groupby('CNAE 2.0 Section Name').mean().reset_index()
w_age10 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==10].groupby('CNAE 2.0 Section Name').mean().reset_index()


# In[61]:


X_choice_mode_sameids['Age'].unique()


# In[76]:


#w_age47 = X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name').mean()


# In[78]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name').mean().reset_index()


# In[79]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name',as_index=False).mean()


# In[65]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==56].groupby('CNAE 2.0 Section Name',as_index=False).mean()


# In[43]:


X_choice_mode_sameids.shape


# In[66]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==47].groupby('CNAE 2.0 Section Name').mean().shape


# In[67]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==56].groupby('CNAE 2.0 Section Name').mean().shape


# In[68]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==60].groupby('CNAE 2.0 Section Name').mean().shape


# In[69]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==53].groupby('CNAE 2.0 Section Name').mean().shape


# In[70]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==57].groupby('CNAE 2.0 Section Name').mean().shape


# In[71]:


X_choice_mode_sameids[X_choice_mode_sameids['Age']==63].groupby('CNAE 2.0 Section Name').mean().shape


# In[72]:


#the shapes are different from each dataframe


# In[81]:


w_age47.append(w_age56, ignore_index=True)


# In[52]:


#w_age47.append(w_age56, w_age60)


# In[53]:


X_choice_mode_sameids['Age'].unique()


# In[84]:


w_age = pd.concat([w_age47, w_age56, w_age60, w_age53, w_age57, w_age63, w_age48, w_age51, w_age50, w_age58, w_age59, w_age54, w_age61,
          w_age46, w_age70, w_age49, w_age55, w_age62, w_age30, w_age52, w_age40, w_age25, w_age66, w_age26, w_age64, w_age67,
          w_age44, w_age22, w_age19, w_age71, w_age65, w_age24, w_age45, w_age15, w_age35, w_age43, w_age42, w_age69, w_age27,
          w_age33, w_age23, w_age31, w_age21, w_age68, w_age28, w_age39, w_age72, w_age38, w_age0, w_age77, w_age20, w_age41,
          w_age16, w_age37, w_age74, w_age34, w_age32, w_age29, w_age73, w_age78, w_age36, w_age76, w_age11, w_age80, w_age1,
          w_age103, w_age84, w_age82, w_age18, w_age12, w_age2, w_age17, w_age83, w_age86, w_age13, w_age94, w_age75, w_age7,
          w_age14, w_age81, w_age10], ignore_index=True)


# In[83]:


pd.concat([w_age47, w_age56, w_age60, w_age53, w_age57, w_age63, w_age48, w_age51, w_age50, w_age58, w_age59, w_age54, w_age61,
          w_age46, w_age70, w_age49, w_age55, w_age62, w_age30, w_age52, w_age40, w_age25, w_age66, w_age26, w_age64, w_age67,
          w_age44, w_age22, w_age19, w_age71, w_age65, w_age24, w_age45, w_age15, w_age35, w_age43, w_age42, w_age69, w_age27,
          w_age33, w_age23, w_age31, w_age21, w_age68, w_age28, w_age39, w_age72, w_age38, w_age0, w_age77, w_age20, w_age41,
          w_age16, w_age37, w_age74, w_age34, w_age32, w_age29, w_age73, w_age78, w_age36, w_age76, w_age11, w_age80, w_age1,
          w_age103, w_age84, w_age82, w_age18, w_age12, w_age2, w_age17, w_age83, w_age86, w_age13, w_age94, w_age75, w_age7,
          w_age14, w_age81, w_age10])


# In[85]:


w_age.shape


# In[96]:


885*19


# In[97]:


X_choice_mode_sameids.shape


# In[86]:


w_age.head(20)


# In[88]:


w_age.sort_values('Age').head(20)


# In[92]:


X_choice_mode_sameids.shape


# In[93]:


X_choice_mode_sameids.sort_values('Age').shape


# In[94]:


X_choice_mode_sameids.head(20)


# In[95]:


#### w-age salário médio de todas as pessoas que tiverem a idade dele em cada setor  

#nem todas as idades estão em todos os setores, praticamente nenhuma na verdade


# In[ ]:





# ## w_sectorinfomean salário médio, e outras informações de cada setor  

# In[102]:


X_choice_mode_sameids


# In[107]:


X_choice_mode_sameids.head(40)


# In[103]:


X_choice_mode_sameids.choice.sum()


# In[105]:


X_choice_mode_sameids['Age'].isna().sum()


# In[101]:


X_choice_mode_sameids.groupby('CNAE 2.0 Section Name').mean().reset_index()


# In[108]:


X_choice_mode_sameids.groupby('mode').mean().reset_index()


# In[110]:


370880/19


# In[113]:


w_sectorinfomean = X_choice_mode_sameids.groupby('CNAE 2.0 Section Name').mean().reset_index()


# In[116]:


w_sectorinfomean.shape


# In[117]:


w_sectorinfomean.head()


# In[118]:


[w_sectorinfomean]*19520


# In[121]:


w_sectorinfomeanallrows = pd.concat([w_sectorinfomean]*19520)


# In[122]:


w_sectorinfomeanallrows.shape


# In[123]:


w_sectorinfomeanallrows.head(4)


# In[128]:


w_sectorinfomeanallrows.reset_index(drop=True, inplace = True)


# In[132]:


w_sectorinfomeanallrows.columns


# In[135]:


w_sectorinfomeanallrows.rename({'CNAE 2.0 Section Name':'CNAE 2.0 Section Name_mean', 'id':'id_mean', 'choice':'choice_mean', 'choice_cnaesectioname':'choice_cnaesectionname_mean',
       'choicenumber':'choicenumber_mean', 'Accommodation And Food':'Accommodation And Food_mean',
       'Administrative Activities And Complementary Services':'Administrative Activities And Complementary Services_mean',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture_mean',
       'Construction':'Construction_mean', 'Education':'Education_mean', 'Electricity And Gas':'Electricity And Gas_mean',
       'Extractive Industries':'Extractive Industries_mean', 'Human Health And Social Services':'Human Health And Social Services_mean',
       'Information And Communication':'Information And Communication_mean', 'Other Service Activities':'Other Service Activities_mean',
       'Processing Industries':'Processing Industries_mean',
       'Professional, Scientific And Technical Activities':'Professional, Scientific And Technical Activities_mean',
       'Public Administration, Defense And Social Security':'Public Administration, Defense And Social Security_mean',
       'Trade; Repair Of Motor Vehicles And Motorcycles':'Trade; Repair Of Motor Vehicles And Motorcycles_mean',
       'Transportation, Storage And Mail':'Transportation, Storage And Mail_mean',
       'Water, Sewage, Waste Management And Decontamination Activities':'Water, Sewage, Waste Management And Decontamination Activities_mean',
       'Arts, Culture, Sports And Recreation':'Arts, Culture, Sports And Recreation_mean', 'Real Estate Activities':'Real Estate Activities_mean',
       'Financial, Insurance And Related Services Activities':'Financial, Insurance And Related Services Activities_mean', 'Age':'Age_mean', 'Age 2':'Age 2_mean',
       'Men':'Men_mean', 'Non-white':'Non_white_mean', 'White':'White_mean', 'Uninformed race':'Uninformed race_mean',
       'Complete primary education':'Complementary primary education_mean', 'Complete secondary education':'Complete secondary education_mean',
       'Complete higher education':'Complete higher education_mean', 'Minimum Wage':'Minimum Wage_mean', 'Working hours':'Working hours_mean',
       'Job tenure':'Job tenure_mean', 'Distance to CBD':'Distance to CBD_mean'}, axis = 1)


# In[136]:


w_sectorinfomeanallrows.rename({'CNAE 2.0 Section Name':'CNAE 2.0 Section Name_mean', 'id':'id_mean', 'choice':'choice_mean', 'choice_cnaesectioname':'choice_cnaesectionname_mean',
       'choicenumber':'choicenumber_mean', 'Accommodation And Food':'Accommodation And Food_mean',
       'Administrative Activities And Complementary Services':'Administrative Activities And Complementary Services_mean',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture_mean',
       'Construction':'Construction_mean', 'Education':'Education_mean', 'Electricity And Gas':'Electricity And Gas_mean',
       'Extractive Industries':'Extractive Industries_mean', 'Human Health And Social Services':'Human Health And Social Services_mean',
       'Information And Communication':'Information And Communication_mean', 'Other Service Activities':'Other Service Activities_mean',
       'Processing Industries':'Processing Industries_mean',
       'Professional, Scientific And Technical Activities':'Professional, Scientific And Technical Activities_mean',
       'Public Administration, Defense And Social Security':'Public Administration, Defense And Social Security_mean',
       'Trade; Repair Of Motor Vehicles And Motorcycles':'Trade; Repair Of Motor Vehicles And Motorcycles_mean',
       'Transportation, Storage And Mail':'Transportation, Storage And Mail_mean',
       'Water, Sewage, Waste Management And Decontamination Activities':'Water, Sewage, Waste Management And Decontamination Activities_mean',
       'Arts, Culture, Sports And Recreation':'Arts, Culture, Sports And Recreation_mean', 'Real Estate Activities':'Real Estate Activities_mean',
       'Financial, Insurance And Related Services Activities':'Financial, Insurance And Related Services Activities_mean', 'Age':'Age_mean', 'Age 2':'Age 2_mean',
       'Men':'Men_mean', 'Non-white':'Non_white_mean', 'White':'White_mean', 'Uninformed race':'Uninformed race_mean',
       'Complete primary education':'Complementary primary education_mean', 'Complete secondary education':'Complete secondary education_mean',
       'Complete higher education':'Complete higher education_mean', 'Minimum Wage':'Minimum Wage_mean', 'Working hours':'Working hours_mean',
       'Job tenure':'Job tenure_mean', 'Distance to CBD':'Distance to CBD_mean'}, axis = 1, inplace = True)


# In[137]:


w_sectorinfomeanallrows.join(X_choice_mode_sameids)


# In[138]:


X_choice_mode_sameids.join(w_sectorinfomeanallrows)


# In[139]:


cnaesectorsinfomean = X_choice_mode_sameids.join(w_sectorinfomeanallrows)


# In[140]:


cnaesectorsinfomean.shape


# In[141]:


cnaesectorsinfomean.columns 


# In[143]:


cnaesectorsinfomean.head()


# In[148]:


cnaesectorsinfomean.loc[:,['id', 'mode', 'CNAE 2.0 Section Name', 'choice',
       'choice_cnaesectioname', 'choicenumber', 'Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities','Age_mean',
       'Age 2_mean', 'Men_mean', 'Non_white_mean', 'White_mean',
       'Uninformed race_mean', 'Complementary primary education_mean',
       'Complete secondary education_mean', 'Complete higher education_mean',
       'Minimum Wage_mean', 'Working hours_mean', 'Job tenure_mean',
       'Distance to CBD_mean']]


# In[149]:


cnaesectorsinfomean.loc[:,['id', 'mode', 'CNAE 2.0 Section Name', 'choice',
       'choice_cnaesectioname', 'choicenumber', 'Accommodation And Food',
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
       'Financial, Insurance And Related Services Activities','Age_mean',
       'Age 2_mean', 'Men_mean', 'Non_white_mean', 'White_mean',
       'Uninformed race_mean', 'Complementary primary education_mean',
       'Complete secondary education_mean', 'Complete higher education_mean',
       'Minimum Wage_mean', 'Working hours_mean', 'Job tenure_mean',
       'Distance to CBD_mean']].to_stata('cnaesectorsinfomeanRecife.dta')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## w-anosdeestudo  salário médio em cada um dos setores das pessoas que tem mesmos anos de estudo

# In[65]:


X_choice_mode_sameids.head(3)


# In[66]:


X_choice_mode_sameids[X_choice_mode_sameids['Complete higher education']==1].groupby('CNAE 2.0 Section Name').mean()


# In[67]:


X_choice_mode_sameids[X_choice_mode_sameids['White']==1].groupby('CNAE 2.0 Section Name').mean()


# In[ ]:





# In[68]:


X_choice_mode_sameids[X_choice_mode_sameids['White']==1].groupby('CNAE 2.0 Section Name').mean()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# ## w-raça salário médio em cada setor das pessoas que tem a mesma raça

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


#run clogit in Python 

#see why it had the error on stata 'omitted because of no within-group variance.'
#the results on stata were better with clogit than with logit


# In[10]:


'''
correct the omitted variable because of no within group variance stata
run the clogit in python, all below in python
organize the data
run with with positive and negatives
run it for cbo, ibge sector, with positive and negatives
do all of it for Pernambuco too, not only Recife
know how to interpret it, the theory behind it
do multilogit for CNAE sectors, Recife
and all other cbo, ibge sectors, postiive and negative, Recife and Pernambuco
know the interpretation adn the theory behind it
this will take the whole month

'''


# In[208]:


'''
correct the omitted variable because of no within group variance stata
it is because the variables in the column does not vary for each individual (id)
age, age 2, Men, Non_white, White, Complete_primary_education, etc. All variables are repeated
for all rows for the same individual, 
they do not vary, that's why the error "omitted because of no within-group variance"
'''


# Stata Styled Conditional [Logit](https://github.com/statsmodels/statsmodels/issues/5904)
# Within group collinearity in [clogit](https://www.stata.com/support/faqs/statistics/within-group-collinearity-and-clogit/) 

# below I adapted from the code that comes from the [swiss metro](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Main%20PyLogit%20Example.ipynb) and the train [example](https://github.com/timothyb0912/pylogit/blob/master/examples/notebooks/Converting%20Long-Format%20to%20Wide-Format.ipynb)

# In[6]:


X_choice_mode_sameids.head().T


# In[7]:


X_choice_mode_sameids.columns


# In[8]:


X_choice_mode_sameids.columns.tolist()[:38]


# In[9]:


pd.set_option('display.max_columns',None)


# In[10]:


X_choice_mode_sameids.head(4)


# In[51]:


X_choice_mode_sameids['choicenumber'].unique()


# In[52]:


# Create the list of individual specific variables
ind_variables = X_choice_mode_sameids.columns.tolist()[:38]

# Specify the variables that vary across individuals and some or all alternatives
# The keys are the column names that will be used in the long format dataframe.
# The values are dictionaries whose key-value pairs are the alternative id and
# the column name of the corresponding column that encodes that variable for
# the given alternative. Examples below.
alt_varying_variables =  {'Age':dict([(1,'Age')]),
                        'Age 2':dict([(1,'Age 2')]),
                        'Men':dict([(1,'Men')]),
                        'Non-white':dict([(1,'Non-white')]),
                        'White':dict([(1,'White')]),
                        'Uninformed race':dict([(1,'Uninformed race')]),
                        'Complete primary education':dict([(1,'Complete primary education')]),
                        'Complete secondary education':dict([(1,'Complete secondary education')]),
                        'Complete higher education':dict([(1,'Complete higher education')]) ,                               
                        'Minimum Wage':dict([(1,'Minimum Wage')]),                                
                        'Working hours':dict([(1,'Working hours')]),
                        'Job tenure':dict([(1,'Job tenure')]),
                        'Distance to CBD':dict([(1,'Distance to CBD')])}


#in my case there are no alternative variables, which is need for the clogit model


# Specify the availability variables
# Note that the keys of the dictionary are the alternative id's.
# The values are the columns denoting the availability for the
# given mode in the dataset.
availability_variables = {1: 'Accommodation And Food',
                          2: 'Administrative Activities And Complementary Services', 
                          3: 'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
                          4: 'Construction',
                          5: 'Education',
                          6: 'Electricity And Gas',
                          7: 'Extractive Industries',
                          8: 'Human Health And Social Services',
                          9: 'Information And Communication',
                          10:'Other Service Activities',
                          11:'Processing Industries',
                          12:'Professional, Scientific And Technical Activities',
                          13:'Public Administration, Defense And Social Security',
                          14:'Trade; Repair Of Motor Vehicles And Motorcycles',
                          15:'Transportation, Storage And Mail',
                          16:'Water, Sewage, Waste Management And Decontamination Activities',
                          17:'Arts, Culture, Sports And Recreation',
                          18:'Real Estate Activities',
                          19:'Financial, Insurance And Related Services Activities'}

##########
# Determine the columns for: alternative ids, the observation ids and the choice
##########
# The 'custom_alt_id' is the name of a column to be created in the long-format data
# It will identify the alternative associated with each row.
custom_alt_id = 'mode_id'

# Create a custom id column that ignores the fact that this is a 
# panel/repeated-observations dataset. Note the +1 ensures the id's start at one.
obs_id_column = 'custom_id'
X_choice_mode_sameids[obs_id_column] = np.arange(X_choice_mode_sameids.shape[0],
                                            dtype=int) + 1


# Create a variable recording the choice column
choice_column = 'choicenumber'


# In[53]:


# Perform the conversion to long-format
long_X_choice_mode_sameids = pl.convert_wide_to_long(X_choice_mode_sameids, 
                                           ind_variables, 
                                           alt_varying_variables, 
                                           availability_variables, 
                                           obs_id_column, 
                                           choice_column,
                                           new_alt_id_name=custom_alt_id)
# Look at the resulting long-format dataframe
long_X_choice_mode_sameids.head(10).T


# In[65]:


basic_specification = OrderedDict()
basic_names = OrderedDict()


# In[67]:


# Estimate the multinomial logit model (MNL)
clogit_mnl = pl.create_choice_model(data=X_choice_mode_sameids,
                                        alt_id_col=custom_alt_id,
                                        obs_id_col=obs_id_column,
                                        choice_col=choice_column,
                                        specification=basic_specification,
                                        model_type="MNL",
                                        names=basic_names)

# Specify the initial values and method for the optimization.
clogit_mnl.fit_mle(np.zeros(39))

# Look at the estimation results
clogit_mnl.get_statsmodels_summary()


# In[68]:


#the error above is because the code did not run three cells above


# In[209]:


#it won't work the information for each individual has to vary, they can't be repeated


# xtreg — Fixed-, between-, and random-effects and population-averaged linear [models](https://www.stata.com/manuals/xtxtreg.pdf)

# In[ ]:





# # Multinomial Logit dependent variable y = 1 2 3 4 5... all sectors

# iris short [example](https://statcompute.wordpress.com/2013/08/23/multinomial-logit-with-python/)
# 
# Multinomial Logistic Regression With [Python](https://machinelearningmastery.com/multinomial-logistic-regression-with-python/)
# 
# Multinomial logit: [mlogit vs statsmodels](https://stats.stackexchange.com/questions/202264/multinomial-logit-mlogit-vs-statsmodels)
# 
# statsmodels.discrete.discrete_model. [MNLogit](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.MNLogit.html)
# 
# Python multinomial logit with statsmodels module: Change base value of mlogit regression, [stackoverflow question, not answered](https://stackoverflow.com/questions/44096234/python-multinomial-logit-with-statsmodels-module-change-base-value-of-mlogit-re)
# 
# Multinomial Logit model Python and Stata different results [stackoverflow, answered](https://stackoverflow.com/questions/49086721/multinomial-logit-model-python-and-stata-different-results)
# 
# MNLogit in statsmodel returning nan [stackoverflow, answered](https://stackoverflow.com/questions/31507396/mnlogit-in-statsmodel-returning-nan)
# 
# Multinomial/conditional Logit Regression, Why StatsModel fails on mlogit package example? [stackoverflow answered question 2016](https://stackoverflow.com/questions/34548375/multinomial-conditional-logit-regression-why-statsmodel-fails-on-mlogit-package)
# 
# Multinomial Logistic Regression [!!!!!good example from DataSklr](https://www.datasklr.com/logistic-regression/multinomial-logistic-regression)
# 
# Multinomial logistic regression scikit-learn [!!!!!good example but with prediction perspective](https://michael-fuchs-python.netlify.app/2019/11/15/multinomial-logistic-regression/) 
# 
# Random utility model and the multinomial logit model [on R](https://cran.r-project.org/web/packages/mlogit/vignettes/c3.rum.html)
# 
# Multinomial Logistic Regression, theory and example on [R](https://it.unt.edu/sites/default/files/mlr_jds_aug2011.pdf)
# 
# Multinomial Logit with Python, [short example with iris](https://www.r-craft.org/r-news/multinomial-logit-with-python/)
# 
# Understanding Logistic Regression in Python Tutorial [Datacamp example, prediction perspective](https://www.datacamp.com/community/tutorials/understanding-logistic-regression-python)
# 
# Theory and some assumptions [from statstest](https://www.statstest.com/multinomial-logistic-regression/)
# 
# Multinomial Logistic Regression in Python [another small example from CodeSpeedy with prediction perspective](https://www.codespeedy.com/multinomial-logistic-regression-in-python/)
# 
# Multinomial Logistic Regression in Python [from dataaspirant another example with prediction perspective](https://dataaspirant.com/implement-multinomial-logistic-regression-python/)
# 
# another short example for MLR in [Machine Learning](https://sweetcode.io/machine-learning-multinomial-logistic-regression/)
# 
# Long example from towardscience [not very simple](https://towardsdatascience.com/ml-from-scratch-multinomial-logistic-regression-6dda9cbacf9d)
# 
# Don’t Sweat the Solver Stuff Tips for Better Logistic Regression Models in Scikit-Learn [from towards science](https://towardsdatascience.com/dont-sweat-the-solver-stuff-aea7cddc3451)
# 
# Logistic Regression: A Simplified Approach Using Python [towards science](https://towardsdatascience.com/logistic-regression-a-simplified-approach-using-python-c4bc81a87c31)
# 
# A32 Multi-class Logistic Regression prediction perspective [painenglish.io](https://python.plainenglish.io/a32-multi-class-classification-using-logistic-regression-96eb692db8fa)
# 
# Real Python good theory and example, still [prediction](https://realpython.com/logistic-regression-python/)
# 
# Multinomial Logistic Regression for beginners [!!!kagle](https://www.kaggle.com/saurabhbagchi/multinomial-logistic-regression-for-beginners)
# 
# mlogit [stata](https://stats.oarc.ucla.edu/stata/dae/multinomiallogistic-regression/)
# 
# mlogit [stata manual](https://www.stata.com/manuals13/rmlogit.pdf)

# From Quora
# 
# How do you do multinomial logistic regression in Python?
# 
# You can use the LogisticRegression() in scikit-learn and set the multiclass parameter equal to “multinomial”. 
# The documentation states that only the ‘newton-cg’, ‘sag’,’saga’ and ‘lbfgs’ solvers are supported when you use the 
# “multinomial” option. More details can be found here: [sklearn.linear_model.LogisticRegression - scikit-learn 0.22.1 
# documentation](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html?highlight=logistic%20regression#sklearn.linear_model.LogisticRegression)
# 
# There is also the MNLogit() in statsmodels. The documentation for MNLogit() is at this link: [statsmodels.discrete.discrete_model.MNLogit - statsmodels](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.MNLogit.html?highlight=mnlogit#statsmodels.discrete.discrete_model.MNLogit)
# 
# Here is a link to a similar question you asked at StackOverflow:
# [Python : How to use Multinomial Logistic Regression using SKlearn](https://stackoverflow.com/questions/36760000/python-how-to-use-multinomial-logistic-regression-using-sklearn)
# 
# Here is a link to an example of multinomial logistic regression in Python using the “Iris” dataset:
# [Multinomial Logistic Regression](https://chrisalbon.com/machine_learning/naive_bayes/multinomial_logistic_regression/)

# Multinomial logit [stata youtube](https://www.youtube.com/watch?v=csqgBOgVgJ4)

# In[ ]:





# A Note on Interpreting Multinomial [Logit Coefficients, stata](https://data.princeton.edu/wws509/stata/mlogit)

# how to guide [stata](https://methods.sagepub.com/dataset/howtoguide/mlogit-in-brfss-2013-stata)

# Comparison of multinomial Logistic Regression between sklearn and [!!!statsmodels](https://www.youtube.com/watch?v=T9KLoRmLlMQ)

# Logistic Regression Part III [StatsModel](https://www.youtube.com/watch?v=JwUj5M8QY4U)

# Multinomail Logistic Regression STATA DATA ANalysis [Examples](https://stats.oarc.ucla.edu/stata/dae/multinomiallogistic-regression/) 

# Multinomail Logit with Python Statsmodels [!!!!!!!Simple short example](https://statcompute.wordpress.com/2013/08/23/multinomial-logit-with-python/)

# Practical Example running Multinomial Logistic Regression [!!!!!!youtube Kagle Logistic Regression](https://www.youtube.com/watch?v=Fwt5S9M6F0A)
# 
# 
# page of the above video [kagle!!!](https://www.kaggle.com/abhishekmungoli/logistic-regression-iris-dataset/notebook)

# In[ ]:





# # Recife CNAE Multilogit

# In[462]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import statsmodels.api as sm

import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

import scipy as scp

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import metrics 
from sklearn.metrics import confusion_matrix

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


# NaN values from logit and multinomial [logit](https://stackoverflow.com/questions/35419882/cost-function-in-logistic-regression-gives-nan-as-a-result) can be because of non standardized [data](https://stackoverflow.com/questions/28689807/how-does-this-code-for-standardizing-data-work/28690441#28690441)
# 
# 2 easy ways to standardized [data](https://www.askpython.com/python/examples/standardize-data-in-python)
# 

# In[463]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[464]:


organizeddataRecifeCNAE.shape


# In[465]:


organizeddataRecifeCNAE.head(3)


# In[466]:


#organizeddataRecifeCNAE.info()


# In[467]:


#organizeddataRecifeCNAE.dtypes


# In[468]:


pd.set_option('display.max_columns',None)


# In[469]:


organizeddataRecifeCNAE[['CNAE 2.0 Section Name','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities','Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities',
                        'Working hours','Job tenure','Distance to CBD']].head()


# In[470]:


'''organizeddataRecifeCNAE.drop(['Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Construction','Education', 'Electricity And Gas',
       'Extractive Industries','Human Health And Social Services', 'Information And Communication',
       'Other Service Activities','Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security','Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities',
                        'Arts, Culture, Sports And Recreation','Real Estate Activities','Financial, Insurance And Related Services Activities'],axis=1,inplace=True)
'''                        


# In[471]:


organizeddataRecifeCNAE.head(3)


# In[472]:


#organizeddataRecifeCNAE['CNAE 2.0 Section Name'] = organizeddataRecifeCNAE['CNAE 2.0 Section Name'].replace('Financial, Insurance And Related Services Activities','Other Service Activities').replace('Information And Communication','Other Service Activities').replace('Arts, Culture, Sports And Recreation','Other Service Activities').replace('Water, Sewage, Waste Management And Decontamination Activities','Other Service Activities').replace('Electricity And Gas','Other Service Activities').replace('Real Estate Activities','Other Service Activities').replace('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Other Service Activities').replace('Extractive Industries','Other Service Activities').replace('Domestic Services','Other Service Activities')


# In[473]:


'''
replacers = {'Public Administration, Defense And Social Security':'1',
       'Professional, Scientific And Technical Activities':'2',
       'Administrative Activities And Complementary Services':'3',
       'Trade; Repair Of Motor Vehicles And Motorcycles':'4',
       'Human Health And Social Services':'5',
       'Construction':'6',
       'Education':'7',
       'Accommodation And Food':'8',
       'Processing Industries':'9',
       'Transportation, Storage And Mail':'10',
       'Other Service Activities':'11'}
organizeddataRecifeCNAE['CNAE 2.0 Section Name'] = organizeddataRecifeCNAE['CNAE 2.0 Section Name'].replace(replacers)
'''


# In[474]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].value_counts()


# In[475]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()


# In[476]:


'''
Public Administration, Defense And Social Security                      21237
#Trade; Repair Of Motor Vehicles And Motorcycles                          9131
Administrative Activities And Complementary Services                     7487
Human Health And Social Services                                         5868
#Education                                                                5401
#Processing Industries                                                    2648
#Professional, Scientific And Technical Activities                        2265
Transportation, Storage And Mail                                         2193
Accommodation And Food                                                   2097
Other Service Activities                                                 1728
#Construction                                                             1601
#Financial, Insurance And Related Services Activities                     1404
#Information And Communication                                            1282
#Arts, Culture, Sports And Recreation                                      519
#Water, Sewage, Waste Management And Decontamination Activities            344
#Electricity And Gas                                                       323
#Real Estate Activities                                                    254
#Agriculture, Livestock, Forestry Production, Fishing And Aquaculture      148
#Extractive Industries                                                      22
#Domestic Services                                                           1
'''
replacers = {
       'Trade; Repair Of Motor Vehicles And Motorcycles':'Other Service Activities',
       'Education':'Other Service Activities',
       'Processing Industries':'Other Service Activities',
       'Professional, Scientific And Technical Activities':'Other Service Activities',
       'Construction':'Other Service Activities',
       'Financial, Insurance And Related Services Activities':'Other Service Activities',
       'Information And Communication':'Other Service Activities',
       'Arts, Culture, Sports And Recreation':'Other Service Activities',
       'Water, Sewage, Waste Management And Decontamination Activities':'Other Service Activities',
       'Electricity And Gas':'Other Service Activities',
       'Real Estate Activities':'Other Service Activities',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture':'Other Service Activities',
       'Extractive Industries':'Other Service Activities',
       'Domestic Services':'Other Service Activities'}
organizeddataRecifeCNAE['CNAE 2.0 Section Name'] = organizeddataRecifeCNAE['CNAE 2.0 Section Name'].replace(replacers)


# In[477]:


organizeddataRecifeCNAE.loc[:,['CNAE 2.0 Section Name','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[478]:


organizeddataRecifeCNAE['Age'] = organizeddataRecifeCNAE['Age'].astype('int64')
organizeddataRecifeCNAE['Age 2'] = organizeddataRecifeCNAE['Age 2'].astype('int64')


# In[479]:


organizeddataRecifeCNAE = organizeddataRecifeCNAE.loc[:,['CNAE 2.0 Section Name','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[480]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].value_counts()


# In[481]:


organizeddataRecifeCNAE.head(3)


# In[482]:


organizeddataRecifeCNAE.isnull().sum()


# In[483]:


organizeddataRecifeCNAE.dtypes


# In[484]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name']


# In[485]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()


# In[486]:


#organizeddataRecifeCNAE['CNAE 2.0 Section Name'].value_counts()


# In[487]:


#organizeddataRecifeCNAE['CNAE 2.0 Section Name'] = organizeddataRecifeCNAE['CNAE 2.0 Section Name'].astype('int')


# In[488]:


#dropping Age 2 because it might be messing the model (making it return nan values) because of colinearity with Age
#I put Age 2 back later

#excluding Uninformed race
#excluding Complete primary education

#to see how the model reacts


# In[489]:


organizeddataRecifeCNAE = organizeddataRecifeCNAE.loc[:,['CNAE 2.0 Section Name','Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[490]:


organizeddataRecifeCNAE.dtypes


# In[491]:


organizeddataRecifeCNAE.head(3)


# In[492]:


organizeddataRecifeCNAE.to_stata('organizeddataRecifeCNAEmlogit.dta')


# In[493]:


X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]

y = organizeddataRecifeCNAE['CNAE 2.0 Section Name']


# In[494]:


y.dtypes


# In[495]:


y.head(10)


# In[496]:


#y = y.astype('int64')


# In[497]:


y.value_counts()


# In[498]:


#y = y.replace('Financial, Insurance And Related Services Activities','Other Service Activities').replace('Information And Communication','Other Service Activities').replace('Arts, Culture, Sports And Recreation','Other Service Activities').replace('Water, Sewage, Waste Management And Decontamination Activities','Other Service Activities').replace('Electricity And Gas','Other Service Activities').replace('Real Estate Activities','Other Service Activities').replace('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Other Service Activities').replace('Extractive Industries','Other Service Activities').replace('Domestic Services','Other Service Activities')


# In[499]:


y.unique()


# In[500]:


y.value_counts()


# In[501]:


#test this combination of fewer sectors in the origital logit and see if there's any difference


# In[502]:


#import statsmodels.api as sm
#X = sm.add_constant(X)


# In[503]:


X.head(3)


# In[504]:


'''Expected 2D array, got 1D array instead:
array=[ 1.  2.  3. ... 11.  4.  1.].
Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample.


Well, it actually looks like the warning is telling you what to do.
As part of sklearn.pipeline stages' uniform interfaces, as a rule of thumb:
when you see X, it should be an np.array with two dimensions
when you see y, it should be an np.array with a single dimension.
'''


# Preprocessing in scikit learn - single sample - Depreciation warning [reshape](https://stackoverflow.com/questions/35082140/preprocessing-in-scikit-learn-single-sample-depreciation-warning)

# In[505]:


y


# In[506]:


#y = ([y])


# In[507]:


#y


# In[508]:


'''scale= StandardScaler()
y = scale.fit_transform(y) 
y'''


# In[ ]:





# In[509]:


#X.dtypes


# In[510]:


#X


# In[511]:


#y.dtypes


# In[512]:


'''
mdl = sm.MNLogit(y,X)
mdl_fit = mdl.fit()
print(mdl_fit.summary())
'''


# In[513]:


#why am I still getting all nan values even after combining the sectors
#on python it can not be string probably it has to be int or categorical check it tomorrow 


# In[514]:


#because CNAE 2.0 Section Name is string, on stata is also getting no observation, on stata valuelabels are used, redo it
#without combining the sections and combining the sections


# this is based on DataSkler multinomial logistic regression [page](https://www.datasklr.com/logistic-regression/multinomial-logistic-regression)

# In[515]:


#print(list(X.columns.values)) 


# In[516]:


#print(list(X.columns.values))
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.20, random_state = 5)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# different solvers, for multiclass probless only 'newton-cg','sag','saga', and 'lbfgs',[here](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)

# In[517]:


model1 = LogisticRegression(random_state=0, multi_class='multinomial', penalty='none', solver='newton-cg').fit(X_train, y_train)
preds = model1.predict(X_test)

#print the tunable parameters (They were not tuned in this example, everything kept as default)
params = model1.get_params()
print(params)


# In[518]:


print('Intercept: \n', model1.intercept_)
print('Coefficients: \n', model1.coef_)


# In[519]:


np.exp(model1.coef_)


# In[520]:


X.corr()


# In[521]:


corr = X.corr()
kot = corr[corr>=.5]
plt.figure(figsize=(12,8))
sns.heatmap(kot, cmap='Reds')
plt.title('Variables with Correlation > .5');


# In[522]:


#instead of using result=logit_model.fit() using result=logit_model.fit_regularized() will get some values, 
#but there will still be nan


# In[523]:


#Use statsmodels to assess variables

logit_model=sm.MNLogit(y_train,sm.add_constant(X_train))
logit_model
result=logit_model.fit()
stats1=result.summary()
stats2=result.summary2()
print(stats1)
print(stats2)


# In[ ]:





# In[530]:


#the goal here is not to predict but the econometrics


# In[ ]:


#accuracy


# In[524]:


confusion_matrix(y_test, preds)


# In[525]:


confmtrx = np.array(confusion_matrix(y_test, preds))


# In[ ]:


#pd.DataFrame(confmtrx, index=['Female','Infant', 'Male'],
#columns=['predicted_Female', 'predicted_Infant', 'predicted_Male'])


# In[526]:


confmtrx


# In[528]:


print('Accuracy Score:', metrics.accuracy_score(y_test, preds)) 


# In[529]:


class_report=classification_report(y_test, preds)
print(class_report)


# In[ ]:





# # Recife CBO Multilogit

# In[51]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import statsmodels.api as sm

import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

import scipy as scp

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import metrics 
from sklearn.metrics import confusion_matrix

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


# In[52]:


organizeddataRecifeCBO = pd.read_csv('organizeddataRecifeCBO.csv')


# In[53]:


organizeddataRecifeCBO.shape


# In[54]:


pd.set_option('display.max_columns',None)


# In[55]:


organizeddataRecifeCBO.head(3)


# In[56]:


organizeddataRecifeCBO.columns


# In[57]:


organizeddataRecifeCBO[['CBO Main SubGroup Name 2002 with Others','Age','Age 2','Men','Non-white',
                        'White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education', 
                        'Clerk',
       'Cross Functional Workers', 'Lay Teachers And Middle Level', 'Managers',
       'Medium-Level Technicians In Administrative Sciences',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences',
       'Others', 'Professionals In Biological, Health And Related Sciences',
       'Professionals Of Social And Human Sciences', 'Public Service Workers',
       'Sellers And Service Providers', 'Service Workers',
       'Superior Members And Officers Of The Public Authority',
       'Teaching Professionals','Workers In The Extractive Industry And Civil Construction',
                          'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries',
                        'Working hours','Job tenure','Distance to CBD']].head()


# In[58]:


organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'].value_counts()


# In[59]:


organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'].unique()


# In[60]:


'''
Clerk                                                                               12239
Service Workers                                                                     11649
Teaching Professionals                                                               5172
Others                                                                               4933
Professionals In Biological, Health And Related Sciences                             4619
Sellers And Service Providers                                                        4210
#Public Service Workers                                                               3694
#Professionals Of Social And Human Sciences                                           2947
#Medium-Level Technicians In Administrative Sciences                                  2840
#Managers                                                                             2797
#Middle Level Technicians In Biological, Biochemical, Health And Related Sciences     2498
#Cross Functional Workers                                                             2328
#Superior Members And Officers Of The Public Authority                                2096
#Lay Teachers And Middle Level                                                        1943
#Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences     1035
#Workers In The Extractive Industry And Civil Construction                             657
#Workers In The Textile, Tanning, Clothing And Graphic Arts Industries                 296

'''
replacers = {
       'Public Service Workers':'Others',
       'Professionals Of Social And Human Sciences':'Others',
       'Medium-Level Technicians In Administrative Sciences':'Others',
       'Managers':'Others',
       'Middle Level Technicians In Biological, Biochemical, Health And Related Sciences':'Others',
       'Cross Functional Workers':'Others',
       'Superior Members And Officers Of The Public Authority':'Others',
       'Lay Teachers And Middle Level':'Others',
       'Middle Level Technicians In Physical, Chemical, Engineering And Related Sciences':'Others',
       'Workers In The Extractive Industry And Civil Construction':'Others',
       'Workers In The Textile, Tanning, Clothing And Graphic Arts Industries':'Others'}
organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'] = organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'].replace(replacers)


# In[61]:


organizeddataRecifeCBO.loc[:,['CBO Main SubGroup Name 2002 with Others','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[62]:


organizeddataRecifeCBO['Age'] = organizeddataRecifeCBO['Age'].astype('int64')
organizeddataRecifeCBO['Age 2'] = organizeddataRecifeCBO['Age 2'].astype('int64')


# In[63]:


organizeddataRecifeCBO = organizeddataRecifeCBO.loc[:,['CBO Main SubGroup Name 2002 with Others','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[64]:


organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'].value_counts()


# In[65]:


organizeddataRecifeCBO.head(3)


# In[66]:


organizeddataRecifeCBO.isnull().sum()


# In[67]:


organizeddataRecifeCBO.dtypes


# In[68]:


organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others']


# In[69]:


organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others'].unique()


# In[70]:


#dropping Age 2 because it might be messing the model (making it return nan values) because of colinearity with Age
#I put Age 2 back later

#excluding Uninformed race
#excluding Complete primary education

#to see how the model reacts


# In[71]:


organizeddataRecifeCBO = organizeddataRecifeCBO.loc[:,['CBO Main SubGroup Name 2002 with Others','Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[72]:


organizeddataRecifeCBO.dtypes


# In[73]:


organizeddataRecifeCBO.head(3)


# In[74]:


organizeddataRecifeCBO.to_stata('organizeddataRecifeCBOmlogit.dta')


# In[75]:


X = organizeddataRecifeCBO[['Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]

y = organizeddataRecifeCBO['CBO Main SubGroup Name 2002 with Others']


# In[76]:


y.dtypes


# In[77]:


y.head(10)


# In[78]:


y.value_counts()


# In[79]:


y.unique()


# In[80]:


X.head(3)


# In[81]:


X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.20, random_state = 5)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[82]:


model1 = LogisticRegression(random_state=0, multi_class='multinomial', penalty='none', solver='newton-cg').fit(X_train, y_train)
preds = model1.predict(X_test)

#print the tunable parameters (They were not tuned in this example, everything kept as default)
params = model1.get_params()
print(params)


# In[83]:


print('Intercept: \n', model1.intercept_)
print('Coefficients: \n', model1.coef_)


# In[84]:


np.exp(model1.coef_)


# In[85]:


corr = X.corr()
kot = corr[corr>=.5]
plt.figure(figsize=(12,8))
sns.heatmap(kot, cmap='Reds')
plt.title('Variables with Correlation > .5');


# In[86]:


#Use statsmodels to assess variables

logit_model=sm.MNLogit(y_train,sm.add_constant(X_train))
logit_model
result=logit_model.fit()
stats1=result.summary()
stats2=result.summary2()
print(stats1)
print(stats2)


# In[87]:


#the goal here is not to predict but the econometrics


# In[88]:


#accuracy


# In[89]:


confusion_matrix(y_test, preds)


# In[90]:


confmtrx = np.array(confusion_matrix(y_test, preds))


# In[91]:


confmtrx


# In[92]:


print('Accuracy Score:', metrics.accuracy_score(y_test, preds)) 


# In[93]:


class_report=classification_report(y_test, preds)
print(class_report)


# In[ ]:





# # Recife IBGE Multilogit

# In[94]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 
plt.rc("font", size=14)
import statsmodels.api as sm

import seaborn as sns
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

import scipy as scp

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn import metrics 
from sklearn.metrics import confusion_matrix

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler


# In[95]:


organizeddataRecifeIBGE = pd.read_csv('organizeddataRecifeIBGE.csv')


# In[96]:


organizeddataRecifeIBGE.head(3)


# In[97]:


organizeddataRecifeIBGE.shape


# In[98]:


pd.set_option('display.max_columns',None)


# In[101]:


organizeddataRecifeIBGE.columns


# In[103]:


organizeddataRecifeIBGE[['IBGE Subsector','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Communication Accommodation', 'Construction', 'Education',
       'Food and Drink', 'Human health activities', 'Other activities',
       'Professional Technical Administration', 'Public Administration',
       'Retail trade', 'Transport and Communication', 'Wholesale',
                        'Working hours','Job tenure','Distance to CBD']].head()


# In[104]:


organizeddataRecifeIBGE['IBGE Subsector'].value_counts()


# In[105]:


organizeddataRecifeIBGE['IBGE Subsector'].unique()


# In[106]:


'''
Public Administration                    21156
Professional Technical Administration    10004
Retail trade                              6967
Human health activities                   5518
Education                                 5324
#Communication Accommodation               5203
Other activities                          4255
#Transport and Communication               2617
#Wholesale                                 2300
#Construction                              1413
#Food and Drink                            1196                                                          
'''
replacers = {
       'Communication Accommodation':'Other activities',
       'Transport and Communication':'Other activities',
       'Wholesale':'Other activities',
       'Construction':'Other activities',
       'Food and Drink':'Other activities'}
organizeddataRecifeIBGE['IBGE Subsector'] = organizeddataRecifeIBGE['IBGE Subsector'].replace(replacers)


# In[107]:


organizeddataRecifeIBGE.loc[:,['IBGE Subsector','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[108]:


organizeddataRecifeIBGE['Age'] = organizeddataRecifeIBGE['Age'].astype('int64')
organizeddataRecifeIBGE['Age 2'] = organizeddataRecifeIBGE['Age 2'].astype('int64')


# In[109]:


organizeddataRecifeIBGE = organizeddataRecifeIBGE.loc[:,['IBGE Subsector','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[110]:


organizeddataRecifeIBGE['IBGE Subsector'].value_counts()


# In[113]:


organizeddataRecifeIBGE.head(3)


# In[114]:


organizeddataRecifeIBGE.isnull().sum()


# In[115]:


organizeddataRecifeIBGE.dtypes


# In[116]:


organizeddataRecifeIBGE['IBGE Subsector']


# In[117]:


organizeddataRecifeIBGE['IBGE Subsector'].unique()


# In[ ]:


#dropping Age 2 because it might be messing the model (making it return nan values) because of colinearity with Age
#I put Age 2 back later

#excluding Uninformed race
#excluding Complete primary education

#to see how the model reacts


# In[118]:


organizeddataRecifeIBGE = organizeddataRecifeIBGE.loc[:,['IBGE Subsector','Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]


# In[120]:


organizeddataRecifeIBGE.dtypes


# In[121]:


organizeddataRecifeIBGE.head(3)


# In[122]:


organizeddataRecifeIBGE.to_stata('organizeddataRecifeIBGEmlogit.dta')


# In[123]:


X = organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Complete secondary education',
      'Complete higher education','Minimum Wage','Working hours','Job tenure','Distance to CBD']]

y = organizeddataRecifeIBGE['IBGE Subsector']


# In[124]:


y.dtypes


# In[125]:


y.head(10)


# In[126]:


y.value_counts()


# In[127]:


y.unique()


# In[128]:


X.head(3)


# In[129]:


y


# In[130]:


#print(list(X.columns.values))
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 0.20, random_state = 5)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


# In[131]:


model1 = LogisticRegression(random_state=0, multi_class='multinomial', penalty='none', solver='newton-cg').fit(X_train, y_train)
preds = model1.predict(X_test)

#print the tunable parameters (They were not tuned in this example, everything kept as default)
params = model1.get_params()
print(params)


# In[132]:


print('Intercept: \n', model1.intercept_)
print('Coefficients: \n', model1.coef_)


# In[133]:


np.exp(model1.coef_)


# In[134]:


corr = X.corr()
kot = corr[corr>=.5]
plt.figure(figsize=(12,8))
sns.heatmap(kot, cmap='Reds')
plt.title('Variables with Correlation > .5');


# In[135]:


#Use statsmodels to assess variables

logit_model=sm.MNLogit(y_train,sm.add_constant(X_train))
logit_model
result=logit_model.fit()
stats1=result.summary()
stats2=result.summary2()
print(stats1)
print(stats2)


# In[136]:


#the goal here is not ML prediction but the econometrics


# In[137]:


#accuracy


# In[138]:


confusion_matrix(y_test, preds)


# In[139]:


confmtrx = np.array(confusion_matrix(y_test, preds))


# In[140]:


confmtrx


# In[141]:


print('Accuracy Score:', metrics.accuracy_score(y_test, preds)) 


# In[142]:


class_report=classification_report(y_test, preds)
print(class_report)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# # Try the Regular Logit with combined variables

# In[ ]:


import pandas as pd


# In[80]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[81]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[82]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()


# In[84]:


organizeddataRecifeCNAE.head(3)


# In[86]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()


# In[88]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'] = organizeddataRecifeCNAE['CNAE 2.0 Section Name'].replace('Financial, Insurance And Related Services Activities','Other Service Activities').replace('Information And Communication','Other Service Activities').replace('Arts, Culture, Sports And Recreation','Other Service Activities').replace('Water, Sewage, Waste Management And Decontamination Activities','Other Service Activities').replace('Electricity And Gas','Other Service Activities').replace('Real Estate Activities','Other Service Activities').replace('Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Other Service Activities').replace('Extractive Industries','Other Service Activities').replace('Domestic Services','Other Service Activities')


# In[90]:


organizeddataRecifeCNAE.head(3)


# In[91]:


organizeddataRecifeCNAE.columns


# In[94]:


organizeddataRecifeCNAE.drop(['Accommodation And Food',
       'Administrative Activities And Complementary Services',
       'Agriculture, Livestock, Forestry Production, Fishing And Aquaculture',
       'Arts, Culture, Sports And Recreation', 'Construction',
       'Domestic Services', 'Education', 'Electricity And Gas',
       'Extractive Industries',
       'Financial, Insurance And Related Services Activities',
       'Human Health And Social Services', 'Information And Communication',
       'Other Service Activities', 'Processing Industries',
       'Professional, Scientific And Technical Activities',
       'Public Administration, Defense And Social Security',
       'Real Estate Activities',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation, Storage And Mail',
       'Water, Sewage, Waste Management And Decontamination Activities'],axis=1,inplace=True)


# In[95]:


organizeddataRecifeCNAE.columns


# In[96]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].value_counts()


# In[97]:


organizeddataRecifeCNAE = pd.concat([organizeddataRecifeCNAE, pd.get_dummies(organizeddataRecifeCNAE['CNAE 2.0 Section Name'])],axis=1)


# In[99]:


organizeddataRecifeCNAE['CNAE 2.0 Section Name'].unique()


# In[100]:


X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration, Defense And Social Security',
       'Professional, Scientific And Technical Activities',
       'Administrative Activities And Complementary Services',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Other Service Activities', 'Human Health And Social Services',
       'Construction', 'Education', 'Accommodation And Food',
       'Processing Industries', 'Transportation, Storage And Mail','Working hours','Job tenure','Distance to CBD']]
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


# In[101]:


X


# In[102]:


y


# In[104]:


#data_final_vars=X.values.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeCNAE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration, Defense And Social Security',
       'Professional, Scientific And Technical Activities',
       'Administrative Activities And Complementary Services',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Other Service Activities', 'Human Health And Social Services',
       'Construction', 'Education', 'Accommodation And Food',
       'Processing Industries', 'Transportation, Storage And Mail','Working hours','Job tenure','Distance to CBD']]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)#, 20)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[105]:


cols = ['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration, Defense And Social Security',
       'Professional, Scientific And Technical Activities',
       'Administrative Activities And Complementary Services',
       'Trade; Repair Of Motor Vehicles And Motorcycles',
       'Other Service Activities', 'Human Health And Social Services',
       'Construction', 'Education', 'Accommodation And Food',
       'Processing Industries', 'Transportation, Storage And Mail','Working hours','Job tenure','Distance to CBD']


# In[106]:


X=os_data_X[cols]
y=os_data_y['y']


# In[107]:


y = y.astype('int64')


# In[108]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[109]:


#the results were about the same 


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





# # RDD test

# In[ ]:





# In[1]:


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


# In[2]:


organizeddataRecifeCNAE = pd.read_csv('organizeddataRecifeCNAE.csv')


# In[3]:


organizeddataRecifeCNAE.head(3)


# In[4]:


organizeddataRecifeCNAE.shape


# In[5]:


organizeddataRecifeCNAE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[6]:


rddtest = organizeddataRecifeCNAE[['y','Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
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


# In[7]:


rddtest


# In[8]:


pd.set_option('display.max_columns',None)


# In[9]:


rddtest.head(3)


# In[10]:


rddtest['Distance to CBD'].sort_values


# In[12]:


rddtest['Distance to CBD'].describe()


# In[13]:


rddtest['distancetocbd>5km'] = rddtest['Distance to CBD'] >= 5.00


# In[14]:


rddtest['distancetocbd>5km'].astype(int)


# In[15]:


rddtest['distancetocbd>5km'] = rddtest['distancetocbd>5km'].astype(int)


# In[16]:


rddtest.head(3)


# In[17]:


rddtest.tail(3)


# In[20]:


rddtest['distancetocbd>5km'].describe()


# In[23]:


rddtest.sort_values(by='Distance to CBD')


# In[22]:


#McCrary Test
#Manipulation Testing Based on Density Discontinuity
#Smoothness at the Threshold


# In[24]:


import plotly.express as px
px.histogram(rddtest, x='Distance to CBD')


# In[25]:


import plotly.express as px
px.histogram(rddtest, x='Distance to CBD', labels={'Distance to CBD':'Distance to CBD', 'count':'Frequency'}, title = 'Distance to CBD histogram')


# In[28]:


import plotly.express as px
fig = px.histogram(rddtest, x='Distance to CBD',
                   title='Distance to CBD histogram',
                   labels={'Distance to CBD':'Distance to CBD', 'count':'Frequency'},
                   )
'''
fig.update_layout(
    title={
        'text': 'Distance to CBD histogram',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_yaxes(title='Frequency',range=[0, 2000])
fig.update_xaxes(title='Distance to CBD', tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(marker=dict(color='grey'))
'''
fig.show()


# In[29]:


#not good, it should look like this 


# In[30]:


url = 'https://github.com/scunning1975/causal-inference-class/blob/master/hansen_dwi.dta?raw=true'
hansen_dwi = pd.read_stata(url)


# In[31]:


import plotly.express as px
fig = px.histogram(hansen_dwi, x='bac1',
                   title='BAC histogram',
                   labels={'bac1':'BAC', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'BAC histogram',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_yaxes(title='Frequency',range=[0, 2000])
fig.update_xaxes(title='BAC', tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[ ]:





# In[ ]:





# In[ ]:





# # Combine activities

# In[1]:


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


# In[2]:


organizeddataRecifeIBGE = pd.read_csv('organizeddataRecifeIBGE.csv')


# In[3]:


organizeddataRecifeIBGE.shape


# In[4]:


pd.set_option('display.max_columns',None)


# In[5]:


organizeddataRecifeIBGE.head(3)


# In[7]:


organizeddataRecifeIBGE.columns


# In[6]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]


# In[8]:


from IPython.display import Image
Image(filename='25 subsetor ibge.jpg')


# In[9]:


organizeddataRecifeIBGE['IBGE Subsector'].unique() 


# In[10]:


'''
this is from bancoesusalltabsrais2019morelatlongcepestab_part1
where the original file is 


bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].unique()

array([24, 21, 16, 11,  1, 19, 20, 22, 17,  2, 23, 18,  8, 13, 15, 10, 14,
        4, 25,  5,  9,  3,  7,  6, 12], dtype=int64)

bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].value_counts()
24    91090
16    29915
19    27516
22    17021
21    16808
      ...  
9       586
5       515
7       485
1       159
12       67
Name: IBGE Subsetor, Length: 25, dtype: int64

bancoesusalltabsrais2019morelatlongcepestabselected['IBGE Subsetor'].value_counts(normalize=True)*100
24    37.687995
16    12.377170
19    11.384596
22     7.042347
21     6.954219
        ...    
9      0.242454
5      0.213078
7      0.200666
1      0.065785
12     0.027721
Name: IBGE Subsetor, Length: 25, dtype: float64


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


# In[12]:


#there's not much to combine, let's combine wholesale and retail 


# In[13]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Retail trade','Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]


# In[14]:


organizeddataRecifeIBGE.head(3)


# In[ ]:


#Wholesale and Retail trade


# In[15]:


organizeddataRecifeIBGE['Wholesale and Retail trade'] = np.where(organizeddataRecifeIBGE['Wholesale']==1, 1,
                                                        np.where(organizeddataRecifeIBGE['Retail trade']==1, 1,
                                                        0))


# In[16]:


organizeddataRecifeIBGE.head(3)


# In[18]:


organizeddataRecifeIBGE[organizeddataRecifeIBGE['Wholesale and Retail trade']==1]


# In[19]:


organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation'
                         ,'Other activities','Human health activities','Professional Technical Administration','Construction',
                         'Wholesale and Retail trade','Food and Drink','Education','Transport and Communication',
                         'Working hours','Job tenure',
                       'Distance to CBD']]


# In[21]:


organizeddataRecifeIBGE.rename({'Final Result':'y'},axis=1,inplace=True)


# In[22]:


X = organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation',
      'Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale and Retail trade','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]
y = organizeddataRecifeIBGE['y']

from imblearn.over_sampling import SMOTE

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns



'''
#Feature scaling
from sklearn.preprocessing import StandardScaler
scale=StandardScaler()
X_train = scale.fit_transform(X_train)
X_test = scale.transform(X_test)

#the coefficients presents a better results but they are not significant anymore
'''


os_data_X,os_data_y=os.fit_resample(X_train, y_train)
os_data_X = pd.DataFrame(data=os_data_X,columns=columns)
os_data_y= pd.DataFrame(data=os_data_y,columns=['y'])
# we can Check the numbers of our data
print("length of oversampled data is ",len(os_data_X))
print("Number of negative result for covid cases in oversampled data",len(os_data_y[os_data_y['y']==0]))
print("Number of covid cases",len(os_data_y[os_data_y['y']==1]))
print("Proportion of negative results for covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==0])/len(os_data_X))
print("Proportion of covid cases data in oversampled data is ",len(os_data_y[os_data_y['y']==1])/len(os_data_X))


# In[23]:


#data_final_vars=X.columns.tolist()
y=['y']
#X=[i for i in data_final_vars if i not in y]
X = organizeddataRecifeIBGE[['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation'
                             ,'Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale and Retail trade','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']]
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
rfe = RFE(logreg)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)


# In[27]:


cols = ['Age','Age 2','Men','Non-white','White','Uninformed race','Complete primary education','Complete secondary education',
      'Complete higher education','Minimum Wage','Public Administration','Communication Accommodation'
                             ,'Other activities','Human health activities','Professional Technical Administration','Construction',
    'Wholesale and Retail trade','Food and Drink','Education','Transport and Communication','Working hours','Job tenure',
                       'Distance to CBD']


# In[28]:


os_data_y['y']=os_data_y['y'].astype('int64')


# In[29]:


X=os_data_X[cols]
y=os_data_y['y']


# In[30]:


import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())


# In[ ]:




