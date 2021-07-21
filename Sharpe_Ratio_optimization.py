#!/usr/bin/env python
# coding: utf-8

# # Portfolio Optimization
# “Modern Portfolio Theory (MPT), a hypothesis put forth by Harry Markowitz in his paper “Portfolio Selection,” (published in 1952 by the Journal of Finance) is an investment theory based on the idea that risk-averse investors can construct portfolios to optimize or maximize expected return based on a given level of market risk, emphasizing that risk is an inherent part of higher reward. It is one of the most important and influential economic theories dealing with finance and investment.

# We will Be working On same Data

# In[1]:


#importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# # Importing Data (Source - Yahoo Finance)

# In[2]:


hdfc = pd.read_csv('HDFCBANK.NS (1).csv', index_col = 'Date' , parse_dates = True)
hdfc.drop(hdfc.tail(1).index,inplace=True)
hdfc


# In[3]:


lt = pd.read_csv('LT.NS.csv' ,  index_col = 'Date' , parse_dates = True)
lt.drop(lt.tail(1).index,inplace=True)
lt


# In[4]:


reliance = pd.read_csv('RELIANCE.NS.csv' ,  index_col = 'Date' , parse_dates = True)
reliance.drop(reliance.tail(1).index,inplace=True)
reliance


# In[5]:


wipro = pd.read_csv('WIPRO.NS.csv' ,  index_col = 'Date' , parse_dates = True)
wipro


# In[6]:


# removing Not required Columns
hdfc.drop(['Open' , 'High' , 'Low' , 'Close' , 'Volume'] , axis = 1 , inplace = True)
lt.drop(['Open' , 'High' , 'Low' , 'Close' , 'Volume'] , axis = 1 , inplace = True)
reliance.drop(['Open' , 'High' , 'Low' , 'Close' , 'Volume'] , axis = 1 , inplace = True)
wipro.drop(['Open' , 'High' , 'Low' , 'Close' , 'Volume'] , axis = 1 , inplace = True)
hdfc


# # Monte Carlo Simulation for Optimization Search
# We could randomly try to find the optimal portfolio balance using Monte Carlo simulation

# In[7]:


stocks = pd.concat([hdfc , lt , reliance , wipro] , axis = 1)
stocks.columns = ['HDFC' , 'LT' , ' REALINCE' , 'WIPRO']
stocks


# In[8]:


# mean of Daily Return
stocks.pct_change(1).mean()


# In[9]:


# correlation Between Daily Return Price
stocks.pct_change(1).corr()


# There is a slight correlation between LT and HDFC

# In[10]:


#plotting Normalized Return
stock_normed = stocks/stocks.iloc[0]
stock_normed.plot(figsize = (12,8))


# # Log Returns vs Arithmetic Returns
# 
# We will now switch over to using log returns instead of arithmetic returns, for many of our use cases they are almost the same,but most technical analyses require detrending/normalizing the time series and using log returns is a nice way to do that. Log returns are convenient to work with in many of the algorithms we will encounter.

# In[11]:


#logarithmic daily return
log_ret = np.log(stocks/stocks.shift(1))
log_ret.head()


# In[12]:


#plotting logarithmic daily return for each Company
log_ret.hist(bins = 100 , figsize = (12,8))
plt.tight_layout()


# In[13]:


#average logarithmic daily return
log_ret.mean()


# In[14]:


# Covariance of logarithmic return
log_ret.cov()*252


# In[15]:


# now will be taking 7000 different combinations of Weight and then plot them
np.random.seed(101)
count = 7000
all_weights = np.zeros((count , len(stocks.columns)))
ret_arr = np.zeros(count)
vol_arr = np.zeros(count)
sharpe_arr = np.zeros(count)
for i in range(count):
    
    weights = np.array(np.random.random(4))
    weights = weights/np.sum(weights)
    all_weights[i , :] = weights

    #expected Return 

    ret_arr[i] = np.sum(log_ret.mean()*weights*252)
    

    #expected Volatility

    vol_arr[i] = np.sqrt(np.dot(weights.T , np.dot(log_ret.cov()*252 , weights)))

    #Sharpe Ratio

    sharpe_arr[i] = ret_arr[i]/vol_arr[i]


# In[16]:


# Maximum Value Of Sharpe Ratio
sharpe_arr.max()


# In[17]:


# Index of Maximum Value Of Sharpe Ratio
sharpe_arr.argmax()


# In[18]:


plt.figure(figsize = (12,8))
plt.scatter(vol_arr , ret_arr , c = sharpe_arr , cmap = 'plasma')
plt.colorbar(label = 'Sharpe Ratio')
plt.xlabel('Volatilty')
plt.ylabel('Return')


# Now we will highlight the point on Graph with maximum Sharpe_ratio

# In[19]:


all_weights[4262 , :]


# In[20]:


max_sr_ret = ret_arr[4262]
max_sr_vol = vol_arr[4262]


# In[21]:


plt.figure(figsize = (12,8))
plt.scatter(vol_arr , ret_arr , c = sharpe_arr , cmap = 'plasma')
plt.colorbar(label = 'Sharpe Ratio')
plt.xlabel('Volatilty')
plt.ylabel('Return')
# Add red dot for max Sharpe Ratio
plt.scatter(max_sr_vol , max_sr_ret , c = 'red' , s = 50 , edgecolors='black')


# 

# In[ ]:




