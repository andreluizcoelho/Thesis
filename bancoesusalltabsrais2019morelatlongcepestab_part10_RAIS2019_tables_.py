#!/usr/bin/env python
# coding: utf-8

# the csv file comes from running 'bancoesusalltabsrais2019morelatlongcepestab_part9_RAIS2019_graphs_.ipynb'
# it needed to be separate because part9 is already above 500mb because of the graphs
# if I were to make the tables there, jupyter notebook would crash

# In[2]:


import pandas as pd
import numpy as np 


# In[3]:


rais2019Recifetables = pd.read_csv('rais2019Recifefortables.csv')


# In[4]:


rais2019Recifetables.shape


# In[5]:


rais2019Recifetables.head(3)


# In[6]:


rais2019Recifetables['Minimum Wage Range'].value_counts()


# In[7]:


rais2019Recifetables.drop(['Sexo Trabalhador', 'CNAE 2.0 Classe', 'CNAE 2.0 Division', 'Tempo Emprego','CNAE 2.0 Section'],axis=1,inplace=True)


# In[8]:


rais2019Recifetables.head(3)


# In[9]:


rais2019Recifetables.rename({'Idade':'Age','Escolaridade após 2005':'School Years', 'Vl Remun Média (SM)':'Minimum Wage', 'Vl Remun Média Nom':'Nominal Wage', 'Qtd Dias Afastamento':'No Working Days'},axis=1,inplace=True)


# In[10]:


rais2019Recifetables.head(3)


# In[11]:


rais2019Recifetables.columns


# In[12]:


rais2019Recifetables[['Minimum Wage', 'Nominal Wage','Minimum Wage Range', 'Nominal Wage Range','School Years','Age','Men',
                      'No Working Days','Race', 'Age Cohort', 'Educational Attainment','CNAE 2.0 Section Name']]


# In[13]:


rais2019Recifetables = rais2019Recifetables[['Minimum Wage', 'Nominal Wage','Minimum Wage Range', 'Nominal Wage Range','School Years','Age','Men',
                      'No Working Days','Race', 'Age Cohort', 'Educational Attainment','CNAE 2.0 Section Name']]


# In[14]:


rais2019Recifetables.drop('Nominal Wage',axis=1,inplace=True)


# In[15]:


#Nominal Wage Range


# In[16]:


rais2019Recifetables.groupby('Nominal Wage Range').mean().round(2).reindex(['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])


# In[17]:


rais2019Recifetables_nominalwagerange_mean = rais2019Recifetables.groupby('Nominal Wage Range').mean().round(2).reindex(['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])


# In[18]:


rais2019Recifetables_nominalwagerange_mean = rais2019Recifetables_nominalwagerange_mean.loc[:,{'Minimum Wage','School Years','Age','Men','No Working Days'}]


# In[19]:


rais2019Recifetables_nominalwagerange_mean


# In[20]:


rais2019Recifetables_nominalwagerange_mean.loc['Total'] = rais2019Recifetables_nominalwagerange_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# In[21]:


rais2019Recifetables_nominalwagerange_mean


# # Table 9: Variables Mean by Nominal Wage Range RAIS 2019

# In[22]:


rais2019Recifetables_nominalwagerange_mean[['Minimum Wage','School Years','Age','Men','No Working Days']]


# In[23]:


#Minimum Wage Range


# In[24]:


rais2019Recifetables.groupby('Minimum Wage Range').mean().round(2).reindex(['0','0.1 - 1/2','1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+'])


# In[25]:


rais2019Recifetables_minimumwagerange_mean = rais2019Recifetables.groupby('Minimum Wage Range').mean().round(2).reindex(['0','0.1 - 1/2','1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+'])


# In[26]:


rais2019Recifetables_minimumwagerange_mean = rais2019Recifetables_minimumwagerange_mean.loc[:,{'Minimum Wage','School Years','Age','Men','No Working Days'}]


# In[27]:


rais2019Recifetables_minimumwagerange_mean


# In[28]:


rais2019Recifetables_minimumwagerange_mean.loc['Total'] = rais2019Recifetables_minimumwagerange_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# In[29]:


rais2019Recifetables_minimumwagerange_mean


# # Table 10: Variables Mean by Minimum Wage Range RAIS 2019

# In[30]:


rais2019Recifetables_minimumwagerange_mean[['Minimum Wage','School Years','Age','Men','No Working Days']]


# In[31]:


#Age Cohort


# In[32]:


rais2019Recifetables[rais2019Recifetables['Age'] <= 4]


# In[33]:


rais2019Recifetables['Age Cohort'].value_counts()


# In[34]:


rais2019Recifetables['Age Cohort'].isna().sum()


# In[35]:


rais2019Recifetables['Age Cohort'].value_counts()


# In[36]:


rais2019Recifetables.groupby('Age Cohort').mean().round(2).reindex(['0 - 4','5 - 17','18 - 29','30 - 39','40 - 49','50 - 64','65 - 74','75 - 84','85+'])


# In[37]:


rais2019Recifetables_agecohort_mean = rais2019Recifetables.groupby('Age Cohort').mean().round(2).reindex(['0 - 4','5 - 17','18 - 29','30 - 39','40 - 49','50 - 64','65 - 74','75 - 84','85+'])


# In[38]:


rais2019Recifetables[rais2019Recifetables['Age'] <= 4]


# In[39]:


rais2019Recifetables[rais2019Recifetables['Age'] <= 10]


# In[40]:


rais2019Recifetables[rais2019Recifetables['Age'] <= 11]


# In[41]:


#the first Age that someone is working in this data is 11 years old


# In[42]:


rais2019Recifetables_agecohort_mean


# In[43]:


rais2019Recifetables_agecohort_mean.astype(str).replace('nan',0.0)


# In[44]:


rais2019Recifetables_agecohort_mean = rais2019Recifetables_agecohort_mean.astype(str).replace('nan',0.00)


# In[45]:


rais2019Recifetables_agecohort_mean


# In[46]:


rais2019Recifetables_agecohort_mean.astype('float')


# In[47]:


rais2019Recifetables_agecohort_mean = rais2019Recifetables_agecohort_mean.astype('float')


# In[48]:


rais2019Recifetables_agecohort_mean = rais2019Recifetables_agecohort_mean.loc[:,{'Minimum Wage','School Years','Age','Men','No Working Days'}]


# 10 tricks for converting Data to a Numeric Type in Pandas [medium article](https://towardsdatascience.com/converting-data-to-a-numeric-type-in-pandas-db9415caab0b) I did not use this article to solve the problem though

# In[49]:


rais2019Recifetables_agecohort_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean'}).round(2)


# In[50]:


rais2019Recifetables_agecohort_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# In[51]:


rais2019Recifetables_agecohort_mean.loc['Total'] = rais2019Recifetables_agecohort_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# In[52]:


rais2019Recifetables_agecohort_mean


# # Table 11: Variables Mean by Age Cohort RAIS 2019

# In[53]:


rais2019Recifetables_agecohort_mean[['Minimum Wage','School Years','Age','Men','No Working Days']]


# In[54]:


# Educational Attainment 


# In[55]:


rais2019Recifetables


# In[56]:


rais2019Recifetables_educationalattainment_mean = rais2019Recifetables.groupby('Educational Attainment').mean().reindex(['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education']).round(2)


# In[57]:


rais2019Recifetables_educationalattainment_mean


# In[58]:


rais2019Recifetables_educationalattainment_mean.loc['Total']=rais2019Recifetables_educationalattainment_mean.agg({'Minimum Wage':'mean','School Years':'mean', 'Age':'mean', 'Men':'mean','No Working Days':'mean'}).round(2)


# # Table 12: Variables Mean by Educational Attainment RAIS 2019 

# In[59]:


rais2019Recifetables_educationalattainment_mean


# In[60]:


#Race


# In[61]:


rais2019Recifetables_race_mean = rais2019Recifetables.groupby('Race').mean().reindex(['White','Yellow','Brown','Black','Indigenous','Ignored']).round(2)


# In[62]:


rais2019Recifetables_race_mean


# In[63]:


rais2019Recifetables_race_mean.loc['Total'] = rais2019Recifetables_race_mean.agg({'Minimum Wage':'mean','School Years':'mean', 'Age':'mean', 'Men':'mean','No Working Days':'mean'}).round(2)


# # Table 13: Variables Mean by Race RAIS 2019

# In[64]:


rais2019Recifetables_race_mean


# In[65]:


#Days Not Working


# In[66]:


rais2019Recifetables['No Working Days']


# In[67]:


rais2019Recifetables['No Working Days'].value_counts()


# In[68]:


rais2019Recifetables.groupby('No Working Days').mean()


# In[69]:


rais2019Recifetables


# In[70]:


bins = [0, 1, 10, 20, 30, 40, 50, 100, 150, 200, 250, 300, np.inf]
names = ['0', '1 - 9','10 - 19', '20 - 29','30 - 39', '40 - 49', '50 - 99','100 - 149','150 - 199','200 - 249','250 - 299', '300+']

rais2019Recifetables['Days Not Working'] = pd.cut(rais2019Recifetables['No Working Days'], bins, labels=names)

print(rais2019Recifetables.dtypes)


# In[71]:


rais2019Recifetables.groupby('Days Not Working').mean().reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+']).round(2)


# In[72]:


rais2019Recifetables_daysnotworking_mean = rais2019Recifetables.groupby('Days Not Working').mean().reindex(['0', '1 - 9', '10 - 19','20 - 29','30 - 39','40 - 49', '50 - 99', '100 - 149', '150 - 199', '200 - 249','250 - 299','300+']).round(2)


# In[73]:


rais2019Recifetables_daysnotworking_mean 


# In[74]:


rais2019Recifetables_daysnotworking_mean.loc['Total']= rais2019Recifetables_daysnotworking_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# # Table 14: Variables Mean by Days Not Working RAIS 2019

# In[75]:


rais2019Recifetables_daysnotworking_mean 


# In[76]:


#CNAE 2.0 Section Name


# In[77]:


rais2019Recifetables


# In[78]:


rais2019Recifetables['CNAE 2.0 Section Name'].value_counts()


# In[79]:


rais2019Recifetables['CNAE 2.0 Section Name'] = rais2019Recifetables['CNAE 2.0 Section Name'].str.title()


# In[80]:


rais2019Recifetables['CNAE 2.0 Section Name']


# In[81]:


rais2019Recifetables.groupby('CNAE 2.0 Section Name').mean().round(2)


# In[82]:


rais2019Recifetables_CNAE_mean = rais2019Recifetables.groupby('CNAE 2.0 Section Name').mean().round(2)


# In[83]:


rais2019Recifetables_CNAE_mean.loc['Total'] = rais2019Recifetables_CNAE_mean.agg({'Minimum Wage':'mean','School Years':'mean','Age':'mean','Men':'mean','No Working Days':'mean'}).round(2)


# # Table 15: Variables Mean by CNAE 2.0 RAIS 2019

# In[84]:


rais2019Recifetables_CNAE_mean


# In[89]:


rais2019Recifetables_CNAE_mean.to_excel('rais2019Recifetables_CNAE_mean.xlsx',sheet_name='Table 15 CNAE RAIS 2019', index=False)


# In[91]:


rais2019Recifetables_daysnotworking_mean.to_excel('rais2019Recifetables_CNAE_mean.xlsx',sheet_name='Table 14 dnw RAIS 2019', index=False)
#it overwrites the previous existing file
#what if I could save different table outputs into a single excel file into different sheets


# save table output from Jupyter Notebook to a single excelfile by different sheets [pandas.DataFrame.to_excel]
# (https://pandas.pydata.org/pandas-docs/version/0.24/reference/api/pandas.DataFrame.to_excel.html)

# In[94]:


with pd.ExcelWriter('rais2019Recifetables14and15.xlsx') as writer:
    rais2019Recifetables_daysnotworking_mean.to_excel(writer, sheet_name='Table 14 dnw RAIS 2019', index=False)
    rais2019Recifetables_CNAE_mean.to_excel(writer, sheet_name='Table 15 CNAE RAIS 2019', index=False)
    #AMAZING IT WORKDS!!!


# In[ ]:




