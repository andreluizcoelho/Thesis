#!/usr/bin/env python
# coding: utf-8

# # Graphs
# ## with the data from bancoesusalltabsrais2019morelatlongcepestab_part7_Recife_data_clogit,
# ### but for all cases and not only positive cases, it makes sense
# ### to make the graphs for all cases, and to make the graphs with the same data as was done for the tables
# ### seeing bancoesusalltabsrais2019morelatlongcepestab_part1 and bancoesusalltabsrais2019morelatlongcepestab_part2
# ### here the data already have only Recife inside the shape (CEP and CEP Estab) file organizedonly CNAE economic sectors

# [Plotly](https://plotly.com/python/)

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import missingno as msno


# In[2]:


organizeddataRecifeforgraphs = pd.read_csv('organizeddataRecifeforgraphs.csv')


# In[3]:


organizeddataRecifeforgraphs.shape


# In[4]:


organizeddataRecifeforgraphs.head(3)


# In[5]:


pd.set_option('display.max_columns',None)


# In[6]:


organizeddataRecifeforgraphs.head()


# In[7]:


#is there duplicates in cpf? yes 13771


# In[8]:


organizeddataRecifeforgraphs['cpf'].duplicated().sum()


# In[9]:


#the initial merge had duplicates on cpf? on both data? yep 


# In[10]:


dataA = {'A':[1,2,3,4,5,5,6,7,7]}
dfA = pd.DataFrame(dataA, index=['id1','id2','id3','id4','id5','id6','id7','id8','id9'])
dfA


# In[11]:


dataB = {'B':[3,4,7,7,8,9,10,11,12]}
dfB = pd.DataFrame(dataB, index=['id1','id2','id3','id4','id5','id6','id7','id8','id9'])
dfB


# In[12]:


#dataB = pd.DataFrame('B':[3,4,7,7,8,9,10,11]})


# In[13]:


dfAB = dfA.merge(dfB, left_on = 'A', right_on='B', how='inner', indicator=True)


# In[14]:


dfAB


# In[15]:


#if both have duplicates, both are kept, dictionaries can not be merged, if the dataframe is constructed with index it works


# # Going back to the graphs

# In[16]:


organizeddataRecifeforgraphs.dtypes


# In[17]:


organizeddataRecifeforgraphs.info()


# In[18]:


organizeddataRecifeforgraphs.memory_usage()


# In[19]:


msno.bar(organizeddataRecifeforgraphs);


# In[20]:


organizeddataRecifeforgraphs.isnull().sum().sort_values(ascending=False)


# In[21]:


organizeddataRecifeforgraphs.columns


# In[22]:


organizeddataRecifeforgraphs.head(3)


# In[23]:


organizeddataRecifeforgraphs[['disease evolution','Age','School Years', 'Nominal Wage', 'Minimum Wage', 'Job tenure','Working hours', 'No Working Days', 'Health Professionals', 'Security Professionals', 'Men','Covid-19','Race','Educational Attainment', 'Minimum Wage Range', 'Age Cohort','CNAE 2.0 Section Name', 'cep', 'latitude', 'longitude', 'CEP Estab', 'latitudestab', 'longitudestab','CEP to CBD', 'CEP Estab to CBD','CEP to CEP Estab', 'Nominal Wage Range', 'Days Not Working','Non-White/Ignored', 'Non-white', 'Uninformed race', 'White', 'Complete higher education', 'Complete primary education', 'Complete secondary education', 'Incomplete primary education', 'Accommodation And Food','Administrative Activities And Complementary Services','Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Arts, Culture, Sports And Recreation','Construction', 'Education', 'Electricity And Gas', 'Extractive Industries', 'Financial, Insurance And Related Services Activities','Human Health And Social Services','Information And Communication','Other Service Activities','Processing Industries','Professional, Scientific And Technical Activities','Public Administration, Defense And Social Security','Real Estate Activities','Trade; Repair Of Motor Vehicles And Motorcycles','Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities']]


# In[24]:


organizeddataRecifeforgraphsselected = organizeddataRecifeforgraphs[['disease evolution','Age','School Years', 'Nominal Wage', 'Minimum Wage', 'Job tenure','Working hours', 'No Working Days', 'Health Professionals', 'Security Professionals', 'Men','Covid-19','Race','Educational Attainment', 'Minimum Wage Range', 'Age Cohort','CNAE 2.0 Section Name', 'cep', 'latitude', 'longitude', 'CEP Estab', 'latitudestab', 'longitudestab','CEP to CBD', 'CEP Estab to CBD','CEP to CEP Estab', 'Nominal Wage Range', 'Days Not Working','Non-White/Ignored', 'Non-white', 'Uninformed race', 'White', 'Complete higher education', 'Complete primary education', 'Complete secondary education', 'Incomplete primary education', 'Accommodation And Food','Administrative Activities And Complementary Services','Agriculture, Livestock, Forestry Production, Fishing And Aquaculture','Arts, Culture, Sports And Recreation','Construction', 'Education', 'Electricity And Gas', 'Extractive Industries', 'Financial, Insurance And Related Services Activities','Human Health And Social Services','Information And Communication','Other Service Activities','Processing Industries','Professional, Scientific And Technical Activities','Public Administration, Defense And Social Security','Real Estate Activities','Trade; Repair Of Motor Vehicles And Motorcycles','Transportation, Storage And Mail','Water, Sewage, Waste Management And Decontamination Activities']]


# In[25]:


organizeddataRecifeforgraphsselected.head(3)


# In[26]:


organizeddataRecifeforgraphsselected.shape


# In[27]:


msno.bar(organizeddataRecifeforgraphsselected);


# In[28]:


organizeddataRecifeforgraphsselected.isnull().sum().sort_values(ascending=False)


# In[29]:


organizeddataRecifeforgraphsselected.dropna().shape


# In[30]:


'''fig= px.pie(organizeddataRecifeforgraphsselected, names='Minimum Wage')
fig.show('svg')'''
#the graph did not turn out good 


# In[31]:


'''fig = px.pie(organizeddataRecifeforgraphsselected, names='Minimum Wage')
fig.update_layout(
    title={
        'text':'Minimum Wage',
        'y':0.95,
        'x':0.4,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show('svg')
'''
#the graph did not turn out good


# In[32]:


'''fig = px.histogram(organizeddataRecifeforgraphsselected['Minimum Wage'], x='Minimum Wage',color='Minimum Wage',
                   title='Minimum Wage',
                   labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Minimum Wage',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Minimum Wage')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')
'''
#the graph did not turn out good


# In[33]:


'''fig = px.histogram(organizeddataRecifeforgraphsselected['Minimum Wage'].dropna(), x='Minimum Wage',color='Minimum Wage',
                   title='Minimum Wage',
                   labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   )
fig.update_layout(
    title={
        'text': 'Minimum Wage',
        'y':0.90,
        'x':0.44,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 70000])
fig.update_xaxes(title='Minimum Wage')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')
'''
#the graph did not turn out good


# In[34]:


'''fig = px.bar(organizeddataRecifeforgraphsselected, x='test type',y='count', color='test type')
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
'''


# In[35]:


organizeddataRecifeforgraphsselected.shape


# In[36]:


organizeddataRecifeforgraphsselected.head(3)


# In[37]:


organizeddataRecifeforgraphsselected.isna().sum()


# In[38]:


organizeddataRecifeforgraphsselected.dtypes


# In[108]:


organizeddataRecifeforgraphsselected.shape


# # Figure 11 Proportion of Men

# In[39]:


organizeddataRecifeforgraphsselected['Men'].unique()


# In[120]:


#labels=['Men','Women']
fig = px.pie(organizeddataRecifeforgraphsselected, names='Men',color='Men',
            color_discrete_map={0:'darkred',1:'darkblue'})
fig.update_traces(textinfo='percent+value')
fig.update_layout(
    title={
        'text':'Proportion of Men',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# ## See descriptive info.pdf and .pptx

# # See how to add % on the graph, probably on plotly manual will have that

# Histogram Complete Guide [Medium](https://towardsdatascience.com/histograms-with-plotly-express-complete-guide-d483656c5ad7)

# Another plotly histogram [medium article](https://towardsdatascience.com/histograms-with-plotly-express-e9e134ae37ad)

# # Figure 12 Race

# In[41]:


organizeddataRecifeforgraphsselected['Race'].dropna().shape


# In[42]:


organizeddataRecifeforgraphsselected['Security Professionals'].dropna().shape


# In[43]:


organizeddataRecifeforgraphsselected[['Security Professionals','Race']].dropna().shape


# In[44]:


organizeddataRecifeforgraphsselected[['Security Professionals','Race','Non-White/Ignored']].dropna().shape                                                      


# In[45]:


organizeddataRecifeforgraphsselected['Race'].isna().sum()


# In[119]:


fig = px.histogram(organizeddataRecifeforgraphsselected['Race'].dropna(), x='Race',color='Race',text_auto=True)#,
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
fig.update_yaxes(title=' ',range=[0, 20000])
fig.update_xaxes(title=' ')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:.s}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# # Figure 13 Age Cohort

# In[118]:


fig = px.histogram(organizeddataRecifeforgraphsselected['Age Cohort'], x='Age Cohort',color='Age Cohort',
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
fig.update_yaxes(title=' ',range=[0, 25000])#,showgrid=True,ticks='outside')#.update_yaxes(categoryorder='total descending')
fig.update_xaxes(title=' ',categoryorder='array', categoryarray= ['0', '0 - 4', '5 - 17', '18 - 29', '30 - 39', '40 - 49', '50 - 64', '65 - 74', '75 - 84', '85+'])#.update_xaxes(categoryorder='total ascending')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:.s}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# In[48]:


organizeddataRecifeforgraphsselected.columns


# In[49]:


organizeddataRecifeforgraphsselected.value_counts(['Men','Race','Age Cohort','Health Professionals', 
                                                   'Security Professionals', 'Covid-19', 'Educational Attainment',
                                                   'Minimum Wage Range','Nominal Wage Range','CNAE 2.0 Section Name'])


# In[50]:


organizeddataRecifeforgraphsselected[['Men','Race','Age Cohort','Health Professionals', 
                                                   'Security Professionals', 'Covid-19', 'Educational Attainment',
                                                   'Minimum Wage Range','Nominal Wage Range','CNAE 2.0 Section Name']].sum(axis=0)


# In[51]:


organizeddataRecifeforgraphsselected['Men'].sum()


# In[52]:


organizeddataRecifeforgraphsselected['Health Professionals'].sum()


# In[53]:


organizeddataRecifeforgraphsselected.shape


# In[54]:


organizeddataRecifeforgraphsselected['Minimum Wage Range'].value_counts()


# In[55]:


organizeddataRecifeforgraphsselected['Nominal Wage Range'].value_counts()


# In[56]:


#https://www.dieese.org.br/notatecnica/2019/notaTec201SalarioMinimo.pdf

#2019 Minimum Wage
#R$998,00


# In[57]:


organizeddataRecifeforgraphsselected.head(3)


# In[58]:


organizeddataRecifeforgraphsselected['Minimum Wage'].isna().sum()


# In[59]:


organizeddataRecifeforgraphsselected[organizeddataRecifeforgraphsselected['Minimum Wage']==0]


# In[60]:


bins = [0, 0.1, 0.5,1 ,2 , 5, 10, 20, np.inf]
names = ['0', '0.01 - 1/2', '1/2 - 1','1 - 2','2 - 5','5 - 10','10 - 20', '20+']

organizeddataRecifeforgraphsselected['meanminimumwage_2'] = pd.cut(organizeddataRecifeforgraphsselected['Minimum Wage'], bins, labels=names)

print(organizeddataRecifeforgraphsselected.dtypes)


# In[61]:


organizeddataRecifeforgraphsselected['meanminimumwage_2'].value_counts()


# In[62]:


organizeddataRecifeforgraphsselected['meanminimumwage_2'].isna().sum()


# In[63]:


organizeddataRecifeforgraphsselected['Minimum Wage Range'].value_counts()


# In[64]:


organizeddataRecifeforgraphsselected['Minimum Wage Range'].isna().sum()


# In[65]:


organizeddataRecifeforgraphsselected['Nominal Wage Range'].value_counts()


# In[66]:


organizeddataRecifeforgraphsselected[organizeddataRecifeforgraphsselected['Nominal Wage']==0]


# In[67]:


organizeddataRecifeforgraphsselected['Minimum Wage'].isna().sum()


# In[68]:


organizeddataRecifeforgraphsselected['Nominal Wage Range'].isna().sum()


# In[69]:


bins = [0, 1, 499, 998, 1996, 4990, 9980, 19960, np.inf]
names = ['0','0-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+']

organizeddataRecifeforgraphsselected['Nominal Wage Range_2'] = pd.cut(organizeddataRecifeforgraphsselected['Nominal Wage'], bins, labels=names)


# In[70]:


organizeddataRecifeforgraphsselected['Nominal Wage Range_2'].value_counts()


# In[71]:


organizeddataRecifeforgraphsselected['Nominal Wage Range_2'].isna().sum()


# In[72]:


organizeddataRecifeforgraphsselected['Nominal Wage Range_2'].replace('NaN',0)


# In[73]:


organizeddataRecifeforgraphsselected['Nominal Wage Range_2'] = organizeddataRecifeforgraphsselected['Nominal Wage Range_2'].astype('category')


# In[74]:


organizeddataRecifeforgraphsselected['Nominal Wage Range_2'].value_counts()


# In[75]:


#might be something incongruent in the original data and not in the interval division see part9 for it, and also do the graphs
#there


# In[107]:


organizeddataRecifeforgraphsselected.shape


# # Figure 14 Health Professionals

# In[117]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='Health Professionals', color='Health Professionals',
            color_discrete_map={1:'darkblue',0:'darkred'})
fig.update_traces(textinfo='percent+value')
fig.update_layout(
    title={
        'text':'Proportion of Health Professionals',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# # Figure 15 Proportion of Security Professionals

# In[116]:


fig = px.pie(organizeddataRecifeforgraphsselected.dropna(), names='Security Professionals',color='Security Professionals',
            color_discrete_map={1:'darkblue',0:'darkred'})
fig.update_traces(textinfo='percent+value')
fig.update_layout(
    title={
        'text':'Proportion Security Professionals',
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# # Figure 16 Covid-19 Cases

# In[115]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='Covid-19',color='Covid-19',
            color_discrete_map={1:'darkblue',0:'darkred'})
fig.update_traces(textinfo='percent+value')
fig.update_layout(
    title={
        'text':'Proportion Covid-19',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show()


# In[79]:


organizeddataRecifeforgraphsselected.head(3)


# # Testing graphs 

# In[80]:


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# data
df = pd.DataFrame({'x':['a', 'b', 'c', 'd'],
                       'y1':[1, 4, 9, 16],
                       'y2':[1, 4, 9, 16],
                       'y3':[6, 8, 4.5, 8]})
df = df.set_index('x')

# calculations
# column sums for transposed dataframe
sums= []
for col in df.T:
    sums.append(df.T[col].sum())

# change dataframe format from wide to long for input to plotly express
df = df.reset_index()
df = pd.melt(df, id_vars = ['x'], value_vars = df.columns[1:])

fig = px.bar(df, x='x', y='value', color='variable')
fig.data[-1].text = sums

fig.update_traces(textposition='inside')
fig.show('svg')


# In[81]:


'''fig=px.bar(organizeddataRecifeforgraphsselected, y = 'Nominal Wage', x='Educational Attainment', text='Nominal Wage')
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()'''


# In[82]:


organizeddataRecifeforgraphsselected[['Educational Attainment']]


# In[83]:


organizeddataRecifeforgraphsselected['Educational Attainment']


# In[84]:


organizeddataRecifeforgraphsselected['Educational Attainment'].squeeze()


# In[85]:


eduattseries = organizeddataRecifeforgraphsselected['Educational Attainment'].squeeze()


# In[86]:


print(eduattseries)


# In[87]:


fig=go.Figure()
fig.add_trace(go.Histogram(x=eduattseries, name='count'))
fig.show('svg')


# In[88]:


fig = px.histogram(organizeddataRecifeforgraphsselected, x='Educational Attainment', y='Nominal Wage', histfunc='count')
fig.show('svg')


# In[89]:


organizeddataRecifeforgraphsselected['Educational Attainment'].value_counts()


# example from stackoverflow [textposition](https://stackoverflow.com/questions/61986676/plotly-how-to-display-individual-value-on-histogram)

# In[90]:


# data
df = pd.DataFrame({'x':['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education'],
                       'y':[3037, 20945, 23237, 1597]})
df = df.set_index('x')

# calculations
# column sums for transposed dataframe
sums= []
for col in df.T:
    sums.append(df.T[col].sum())

# change dataframe format from wide to long for input to plotly express
df = df.reset_index()
df = pd.melt(df, id_vars = ['x'], value_vars = df.columns[1:])

fig = px.bar(df, x='x', y='value', color='value',title='Educational Attainment')
fig.data[-1].text = sums

fig.update_traces(textposition='outside',showlegend=False)
fig.update_yaxes(title=' ',range=[0, 25000])
fig.update_layout(
    title={
        'text': 'Educational Attainment',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)',showlegend=False)
fig.update_xaxes(title=' ')
fig.show('svg')


# In[91]:


pip list


# In[92]:


#pip install -U plotly


# In[ ]:





# In[93]:


'''fig = px.bar(organizeddataRecifeforgraphsselected, x='Educational Attainment', y='Educational Attainment', color='Educational Attainment', text_auto=True)
fig.show()'''


# good example of textposition on [stackoverflow](https://stackoverflow.com/questions/63945330/plotly-how-to-add-text-labels-to-a-histogram)

# [texttemplate plotly](https://plotly.com/python/reference/)

# change unit in vertical [text](https://community.plotly.com/t/how-to-change-unit-in-vertical-text/34731)

# hover text and formatting [plotly](https://plotly.com/python/hover-text-and-formatting/)

# # Figure 17 Educational Attainment

# In[114]:


fig = px.histogram(organizeddataRecifeforgraphsselected['Educational Attainment'], x='Educational Attainment',color='Educational Attainment',
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
fig.update_yaxes(title=' ',range=[0, 25000])
fig.update_xaxes(title=' ',categoryorder='array',categoryarray=['Incomplete primary education', 'Complete primary education', 'Complete secondary education', 'Complete higher education'])#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(name='count',texttemplate="%{x}", textfont_size=20)
#fig.update_traces(organizeddataRecifeforgraphsselected='%{text:.2s}', textposition='outside')
fig.update_traces(texttemplate='%{y:.s}',textposition='outside', textfont_size=14) #%{y:.1s},%{y:.2s},%{y:.3s}
#fig.update_traces(marker=dict(color='grey'))
#fig.update_traces(textsrc='outside')
fig.show()


# # Figure 18 Mininum Wage Range

# In[113]:


fig = px.histogram(organizeddataRecifeforgraphsselected['Minimum Wage Range'], x='Minimum Wage Range',color='Minimum Wage Range',
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
fig.update_yaxes(title=' ',range=[0, 21000])
fig.update_xaxes(title=' ',categoryorder='array', categoryarray= ['0', '0.1 - 1/2', '1/2 - 1', '1 - 2', '2 - 5', '5 - 10', '10 - 20', '20+'])#.update_xaxes(categoryorder='total ascending')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:.s}',textposition='outside', textfont_size=14) 
#fig.update_traces(marker=dict(color='grey'))
fig.show()


# # Figure (19) Repetitive, don't put it on thesis Nominal Wage Range

# In[96]:


fig = px.histogram(organizeddataRecifeforgraphsselected['Nominal Wage Range'], x='Nominal Wage Range',color='Nominal Wage Range',
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
fig.update_yaxes(title=' ',range=[0, 21000])
fig.update_xaxes(title=' ',categoryorder='array', categoryarray =['0','1-499','499-998','998-1996','1996-4990','4990-9980','9980-19960','19960+'])#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
fig.update_traces(texttemplate='%{y:.s}',textposition='outside',textfont_size=14)
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')


# In[97]:


'''fig = px.bar(organizeddataRecifeforgraphsselected, x='Nominal Wage Range', y='Minimum Wage Range', color='Minimum Wage Range', text_auto=True)
fig.show('svg')'''


# # Figure 19 and 20 CNAE 2.0 Economy Sectors

# In[98]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show('svg')


# In[99]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent+value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show('svg')


# In[100]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},showlegend=False)
fig.show('svg')


# In[101]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})#,showlegend=False)
fig.show('svg')


# # Figure 19 CNAE 2.0 Economy Sectors %

# In[102]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='percent')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.32,
        'xanchor': 'center',
        'yanchor': 'top'})#,showlegend=False)
fig.show()


# # Figure 20 CNAE 2.0 Economy Sectors Values

# In[103]:


fig = px.pie(organizeddataRecifeforgraphsselected, names='CNAE 2.0 Section Name')
fig.update_traces(textinfo='value')
fig.update_layout(
    title={
        'text':'CNAE Economy Sectors',
        'y':0.96,
        'x':0.32,
        'xanchor': 'center',
        'yanchor': 'top'})#,showlegend=False)
fig.show()


# In[104]:


len(organizeddataRecifeforgraphsselected['CNAE 2.0 Section Name'].unique())


# In[105]:


'''fig = px.sunburst(organizeddataRecifeforgraphsselected, path=['Nominal Wage'], values='School Years',
                  color='Nominal Wage', hover_data=['Age'])
fig.show('svg')'''
#it took forever, it did not work 


# In[106]:


'''fig = px.histogram(organizeddataRecifeforgraphsselected['CNAE 2.0 Section Name'], x='CNAE 2.0 Section Name',color='CNAE 2.0 Section Name',
                   title='CNAE 2.0 Section Name')#,
                   #labels={'Minimum Wage':'Minimum Wage', 'count':'Frequency'},
                   #)
fig.update_layout(
    title={
        'text': 'CNAE 2.0 Section Name',
        'y':0.90,
        'x':0.48,
        'xanchor': 'center',
        'yanchor': 'top'}, paper_bgcolor='rgb(255,255,255)', plot_bgcolor='rgb(255,255,255)')
#fig.update_yaxes(title='Frequency',range=[0, 20000])
fig.update_xaxes(title=' ')#, tickvals=(0, 0.1, 0.2, 0.3, 0.4))
#fig.update_traces(marker=dict(color='grey'))
fig.show('svg')
'''
#did not work good


# [Plotly](https://plotly.com/python/plotly-express/)

# In[ ]:




