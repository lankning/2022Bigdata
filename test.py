import paddle
from dataset import *
from tqdm import tqdm

fcmodel = paddle.jit.load("model.save/fcmodel")
fcmodel.eval()
params_info = paddle.summary(fcmodel,(1, 20))
print(params_info)
dataset = Dataset("data/train.csv", 'test', False)
dataset.showlabel()

for i in range(3):
    inp = []
    for j in range(2500*i, 2500*i+2500):
        inp_j, _ = dataset.__getitem__(j)
        inp.append(inp_j)
    inp = np.float32(np.array(inp))
    pred = fcmodel(inp)
#     print(np.round(pred))
    print(pred)