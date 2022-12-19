import pandas as pds
from model import *

data = pds.read_csv("data/train.csv")
# print(data.iloc[0])
# for i in range(1,21):
#     print(data.iloc[:,i].nunique())
print(data.iloc[:,1].nunique())
print(data.iloc[:,1].unique())
print(data.iloc[0].values)
# fcmodel = fcnet(20, 1)
# model_info = paddle.summary(fcmodel, (1, 20))
# print(model_info)