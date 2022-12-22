from dataset import *
from model import *

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
    fcmodel = fcnet(54, 2)
    fcmodel.train()
    dataset = Dataset("data/train.csv")
    train_loader = paddle.io.DataLoader(dataset, batch_size=1, shuffle=True)

    epochs = 5
    optim = paddle.optimizer.Adam(parameters=fcmodel.parameters())
    loss_fn = paddle.nn.MSELoss()

    losslist = []
    for epoch in range(epochs):
        for batch_id, data in enumerate(train_loader()):
            inp = data[0]
            label = data[1]
            """
            unknown in |C|D|E| has different length
            """
            predicts = fcmodel(inp)
            loss = loss_fn(predicts, label)
            loss.backward()
            print("[Train] epoch: {}, batch_id: {}, loss is: {}".format(epoch, batch_id+1, loss.numpy()))
            losslist.append(loss.numpy())
            optim.step()
            optim.clear_grad()