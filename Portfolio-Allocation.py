#!/usr/bin/env python
# coding: utf-8

# # Portfolio Allocation And Sharpe Ratio Calculation
# 
# In this Portfolio we have taken Data of 5 years from 2016-07-21 to 2021-07-20 of 4 Companies namely
# * HDFC
# * WIPRO
# * Larsen & Toubro
# * RELIANCE

# In[1]:


#importing Libraries
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # Importing Data (Source - Yahoo Finance)

# In[2]:


HDFC = pd.read_csv('HDFCBANK.NS (1).csv', index_col = 'Date' , parse_dates = True)
HDFC


# In[3]:


WIPRO= pd.read_csv('WIPRO.NS.csv' ,  index_col = 'Date' , parse_dates = True)
WIPRO


# In[4]:


LT = pd.read_csv('LT.NS.csv' ,  index_col = 'Date' , parse_dates = True)
LT


# In[5]:


RELIANCE = pd.read_csv('RELIANCE.NS.csv' ,  index_col = 'Date' , parse_dates = True)
RELIANCE


# In[6]:


#Dropping Of last (extra Column)
LT.drop(LT.tail(1).index,inplace=True)
RELIANCE.drop(RELIANCE.tail(1).index,inplace=True)
HDFC.drop(HDFC.tail(1).index,inplace=True)
HDFC


# In[7]:


#dropping Of Missing Values if Any
HDFC.dropna(inplace = True)
WIPRO.dropna(inplace = True)
LT.dropna(inplace = True)
RELIANCE.dropna(inplace = True)


# # Normalize Prices

# In[8]:


# calculating Normalized Return Value
for stock_df in (HDFC , RELIANCE , LT , WIPRO):
    stock_df['Normed Return'] = stock_df['Adj Close']/stock_df.iloc[0]['Adj Close']
    
HDFC.head()


# # Allocations
# 
# Let's pretend we had the following allocations for our total portfolio:
# 
# * 30% in WIPRO
# * 20% in HDFC
# * 40% in Reliance
# * 10% in LT
# 
# Let's have these values be reflected by multiplying our Norme Return by out Allocations

# In[9]:


for stock_df , allo in zip((HDFC , RELIANCE , LT , WIPRO) , [0.2 , 0.4 , 0.1 , 0.3]):
    stock_df['Allocation'] = stock_df['Normed Return']*allo


# In[10]:


HDFC.head()


# # Invesment
# 
# Let's pretend we invested a 1 lakh rupees in this portfolio

# In[11]:


for stock_df in ((HDFC , RELIANCE , LT , WIPRO)):
    stock_df['Position Values'] = stock_df['Allocation']*100000


# # Total Portfolio Value

# In[12]:


list1 = [HDFC['Position Values'] , RELIANCE['Position Values'] , LT['Position Values'] , WIPRO['Position Values']]
portfolio_val = pd.concat(list1 , axis = 1)


# In[13]:


portfolio_val.columns = ['HDFC', 'RELIANCE' , 'LT' , 'WIPRO']


# In[14]:


portfolio_val.head()


# In[15]:


portfolio_val['Total Value'] = portfolio_val.sum(axis = 1)


# In[16]:


portfolio_val


# Final Total Value Of our portfolio After 5 years is 325325.732281

# # Plotting Total Portfolio Value

# In[17]:


plt.figure(figsize =(10,8))
portfolio_val['Total Value'].plot()


# In[18]:


#visualizing Individual plots of the companies
plt.figure(figsize =(12,8) , dpi = 150)
portfolio_val.drop('Total Value' , axis = 1).plot(figsize = (10,8))


# # Portfolio Statistics

# In[19]:


# daily returns
portfolio_val['Daily Return'] = portfolio_val['Total Value'].pct_change(1)


# In[20]:


portfolio_val.head()


# In[21]:


#Cumulative Return
cum_ret = 100 * (portfolio_val['Total Value'][-1]/portfolio_val['Total Value'][0] -1 )
print('Our return was {} percent!'.format(cum_ret))


# In[22]:


# Avg daily Return
portfolio_val['Daily Return'].mean()


# In[23]:


#std daily return 
portfolio_val['Daily Return'].std()


# In[24]:


portfolio_val['Daily Return'].plot(kind='kde')


# # Calculating Sharpe Ratio
# 

# In[25]:


#For Yearly Data
SR = portfolio_val['Daily Return'].mean()/portfolio_val['Daily Return'].std()
SR


# # Sharpe Ratio
# * sharpe Ratio Above 1 is Acceptable
# * sharpe Ratio Above 2 is Great
# * sharpe Ratio Above 3 excellent

# In[26]:


# for Daily Data
(252**0.5)*SR


# Our Sharpe Ratio Came out to be 1.202
# 

# In[ ]:




