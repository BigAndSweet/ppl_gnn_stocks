import torch
import numpy as np
import os

def best_return(pct_returns, daily_investment=100, skip_n_steps=0):
    """Calculates the optimal return possible for the given parameters. The output 
    reflects a policy of buying the `daily_investment` amount of the stock with 
    the highest return each timestep and selling it at the same timestep to realize 
    the return. This removes the effect of compounding returns. 

    Keyword arguments:
    pct_returns      -- np.array of dim: (num_companies, num_timesteps), containing
                        the percent returns for companies at various timesteps.
    daily_investment -- constant dollar amount to be invested at each timestep.
    skip_n_steps     -- skips the first n steps when calculating total return,
                        used to account for the correlation tensor truncation.
    """
    return np.sum(np.multiply(daily_investment, np.max(pct_returns.T, axis=1)[skip_n_steps:]))

def avg_return(pct_returns, daily_investment=100, skip_n_steps=0):
    """Calculates the average return (i.e. the return of holding the entire index).
    The output reflects a policy of buying the `daily_investment` amount of the 
    index average at each timestep and selling it at the same timestep to realize 
    the return. This removes the effect of compounding returns. 

    Keyword arguments:
    pct_returns      -- np.array of dim: (num_companies, num_timesteps), containing
                        the percent returns for companies at various timesteps.
    daily_investment -- constant dollar amount to be invested at each timestep.
    skip_n_steps     -- skips the first n steps when calculating total return,
                        used to account for the correlation tensor truncation.
    """
    return np.sum(np.multiply(daily_investment, np.average(pct_returns.T, axis=1)[skip_n_steps:]))

def load_corr_timestep(data_path='data/relation/correlations', market_name='NASDAQ', t=0):
    '''
    Loads the correlational matrix for a given timestep t as a PyTorch tensor

    Keyword arguments:
    data_path   -- string path to the folder containing the numpy correlation matrices
    market_name -- string name of market, options: ['NASDAQ', 'NYSE']
    t           -- int representing the desired timestep
    '''
    load_path = os.path.join(data_path, market_name, os.listdir(os.path.join(data_path, market_name))[t])
    return torch.from_numpy(np.load(load_path)).float()

def save_corr_timestep(data, save_path='data/relation/correlations', market_name='NASDAQ', t=0):
    '''
    Saves the correlational matrix for a given timestep t as an .npy file
    **NOTE: Intended to store tensors after gradient adjustment.**

    Keyword arguments:
    data        -- PyTorch tensor to save
    save_path   -- string path to the destination folder of the PyTorch correlation matrices
    market_name -- string name of market, options: ['NASDAQ', 'NYSE']
    t           -- int representing the desired timestep
    '''
    # setup save directory
    save_path = os.path.join(save_path, market_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_file_path = os.path.join(save_path, market_name + '_correlation_init_' + str(t) + '.npy')
    np.save(save_file_path, data.cpu().numpy())
    
def get_dataset(price_data,n,train_size = 200, test_size = 20):
    
    start_point = n*test_size
    split_point = start_point + train_size
    final_point = split_point + test_size
    if final_point > len(price_data[0]):
        return len(price_data[0]) - start_point
    train = price_data[:,start_point:split_point]
    test = price_data[:,split_point:final_point]
    return train,test

def profit(test,truth):
    total = 0
    for i in range(0,len(test[0])):
        best_buy = np.argmax(test[:,i])
        prophet = 100*(truth[best_buy,i]-truth[best_buy-1,i])/truth[best_buy-1,i]
        total += prophet
    return total
