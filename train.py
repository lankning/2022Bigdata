from dataset import *
from model import *
from tqdm import tqdm
# data = pds.read_csv("data/train.csv")
# print(data.iloc[0])
# for i in range(1,21):
#     print(data.iloc[:,i].nunique())
# print(data.iloc[:,1].nunique())
# print(data.iloc[:,1].unique())
# print(data.iloc[0].values)
# fcmodel = fcnet(20, 1)
# model_info = paddle.summary(fcmodel, (1, 20))
# print(model_info)

if __name__=="__main__":
    fcmodel = fcnet(20, 1, 5, 2048)
    fcmodel.train()
    dataset = Dataset("data/train.csv")
    train_loader = paddle.io.DataLoader(dataset, batch_size=2500, shuffle=True)

    epochs = 20
    optim = paddle.optimizer.Adam(parameters=fcmodel.parameters())
    loss_fn = paddle.nn.MSELoss()
    acc_fn = Precision()
    losslist = []
    with tqdm(total=epochs*len(dataset)/2500) as pbar:
        pbar.set_description('[Training] loss: nan, acc: 0.00%')
        for epoch in range(epochs):
            for batch_id, data in enumerate(train_loader()):
                inp = data[0]
                label = data[1]
                predicts = fcmodel(inp)
                acc_fn.update(predicts, label)
                acc = acc_fn.accumulate()
                acc_fn.reset()
                loss = loss_fn(predicts, label)
                loss.backward()
                losslist.append(loss.numpy())
                optim.step()
                optim.clear_grad()
                pbar.set_description('[Training] loss: %.2f, acc: %.2f%%' % (loss.numpy(), 100*acc))
                pbar.update(1)