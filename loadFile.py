import numpy as np
import pandas as pd
import os 
import xlrd

def read_excel(fname):
    # df=pd.read_excel(fname,sheet_name='Sheet1',
    # header=2,
    # dtype={'a':str, 'b':np.int64, 'c':np.int64},
    # index_col='id',
    # na_values='NaN',
    # thousands=',',
    # nrows=10,
    # comment='#'
    # )
    # print(fname)
    df=pd.read_excel(fname)
    print(df)



