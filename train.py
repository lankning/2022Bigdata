import pandas as pds
from model import *

data = pds.read_csv("data/train.csv")


fcmodel = fcnet(20, 1)
model_info = paddle.summary(fcnet, ((1,20), (1,1)))
print(model_info)