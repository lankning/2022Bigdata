from dataset import *
from model import *
from tqdm import tqdm
import os
import matplotlib.pyplot as plt

class trainfc():
    def __init__(self, in_num, out_num, layers, node_num, csv_path, batchsize, epochs):
        self.fcmodel = fcnet(in_num, out_num, layers, node_num)
        self.in_num = in_num
        self.fcmodel.train()
        self.dataset = Dataset(csv_path)
        self.batchsize = batchsize
        self.train_loader = paddle.io.DataLoader(self.dataset, batch_size=batchsize, shuffle=True)
        self.epochs = epochs
        self.losslist = []
        self.acclist = []
        model_info = paddle.summary(self.fcmodel, (1, 20))
        print(model_info)
        self.dataset.showlabel()
        
    def train(self):
        optim = paddle.optimizer.Adam(parameters=self.fcmodel.parameters())
        loss_fn = paddle.nn.MSELoss()
        acc_fn = Precision()
        with tqdm(total=self.epochs*len(self.dataset)/self.batchsize) as pbar:
            pbar.set_description('[Training] loss: nan, acc: 0.00%')
            for _ in range(self.epochs):
                for _, data in enumerate(self.train_loader()):
                    inp = data[0]
                    label = data[1]
                    predicts = self.fcmodel(inp)
                    acc_fn.update(predicts, label)
                    acc = acc_fn.accumulate()
                    acc_fn.reset()
                    loss = loss_fn(predicts, label)
                    loss.backward()
                    optim.step()
                    optim.clear_grad()
                    pbar.set_description('[Training] loss: %.2f, acc: %.2f%%' % (loss.numpy(), 100*acc))
                    pbar.update(1)
                    self.losslist.append(loss.numpy())
                    self.acclist.append(100*acc)
    
    def visualize(self, path2save):
        l = np.array(self.losslist)
        x_axis = len(l)
        step = np.linspace(1,x_axis,x_axis)
        plt.plot(step,l,label="Train Loss")
        plt.legend(loc='upper right')
        plt.title('step-loss')
        plt.xlim((0, x_axis))
        plt.ylim((0, 1))
        plt.gca().set_ylim(bottom=0)
        plt.xlabel('step')
        plt.ylabel('loss')
        plt.savefig(os.path.join(path2save, 'loss.png'), bbox_inches='tight')
        plt.show()

        a = np.array(self.acclist)
        plt.plot(step,a,label="Train Acc")
        plt.legend(loc='upper right')
        plt.title('step-acc')
        plt.xlim((0, x_axis))
        plt.ylim((0, 100))
        plt.gca().set_ylim(bottom=0)
        plt.xlabel('step')
        plt.ylabel('acc')
        plt.savefig(os.path.join(path2save,'acc.png'), bbox_inches='tight')
        plt.show()
        print("[Visualization] Done!")
    
    def save(self, path2save):
        paddle.jit.save(
            layer=self.fcmodel,
            path=os.path.join(path2save, "fcmodel"),
            input_spec=[
                paddle.static.InputSpec(shape=[1, self.in_num], dtype='float32')
                ])

        paddle.onnx.export(
            self.fcmodel, 
            os.path.join(path2save, "fcmodel"), 
            input_spec = [
                paddle.static.InputSpec(shape=[1, self.in_num], dtype='float32')
                ], opset_version=12)
        print("[Model Save] Done!")

if __name__=="__main__":
    fcmodel = trainfc(20, 1, 5, 2048, "data/train.csv", 2500, 20)
    fcmodel.train()
    fcmodel.save('model.save')
    fcmodel.visualize('statics')