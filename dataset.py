import paddle
import pandas as pds
import pickle
import numpy as np

def cfgs_io(path: str, mode: str, struct = {}):
    if mode == 'out':
        with open(path, 'wb') as f:
            pickle.dump(struct, f)
    elif mode == 'in':
        with open(path, 'rb') as f:
            struct = pickle.load(f)
        return struct
    else:
        raise

class Dataset(paddle.io.Dataset):
    '''
    Step 1: inherit the class paddle.io.Dataset
    '''
    def __init__(self, csvpath):
        '''
        Step 2: realize __init__()
        initialize the dataset,
        mapping the samples and labels to list
        '''
        super(Dataset, self).__init__()
        self.encodelist = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 21]
        self.dataframe = pds.read_csv(csvpath)
        self.correspondingdict = {}
            # 'yes': np.array([1, 0, 0], dtype='float32'), 
            # 'no': np.array([0, 1, 0], dtype='float32'), 
            # 'unknown': np.array([0, 0, 1], dtype='float32')}
        # self.cate2onehot()
        self.labelencoder()

    def cate2onehot(self):
        for i in self.encodelist:
            uniquelist = self.dataframe.iloc[:,i].unique()
            onehot_matrix = np.eye((len(uniquelist)))
            for j in range(len(uniquelist)):
                if uniquelist[j] in self.correspondingdict:
                    continue
                else:
                    self.correspondingdict[uniquelist[j]] = onehot_matrix[j]
        cfgs_io("correspondingdict.pkl", "out", self.correspondingdict)

    def labelencoder(self):
        for i in self.encodelist:
            uniquedict = {}
            uniquelist = self.dataframe.iloc[:,i].unique()
            for j in range(len(uniquelist)):
                uniquedict[uniquelist[j]] = j
            self.dataframe.iloc[:,i] = self.dataframe.iloc[:,i].map(uniquedict)
            cfgs_io("statics/%d.pkl" % i, "out", uniquedict)
   
    def showlabel(self):
        for i in self.encodelist:
            struct = cfgs_io("statics/%d.pkl" % i, "in")
            print(struct)

    def __getitem__(self, index):
        record = self.dataframe.iloc[index].values
        label = record[-1:].copy()
        inp = record[1:-1].copy()
        # for i in range(2, 21):
        #     if i in self.encodelist:
        #         inp = np.append(inp, self.correspondingdict[record[i]])
        inp = np.float32(inp)
        label = np.float32(label)
        return inp, label

    def __len__(self):
        return len(self.dataframe)

if __name__=="__main__":
    dataset = Dataset("data/train.csv")
    print("Number of records: ", len(dataset))
    dataset.showlabel()
    # 取第i条记录
    x,y = dataset.__getitem__(0)
    print(x.shape, y.shape)
    '''
    {'admin.': 0, 'services': 1, 'blue-collar': 2, 'entrepreneur': 3, 'management': 4, 'technician': 5, 'housemaid': 6, 'self-employed': 7, 'unemployed': 8, 'retired': 9, 'student': 10, 'unknown': 11}
    {'divorced': 0, 'married': 1, 'single': 2, 'unknown': 3}
    {'professional.course': 0, 'high.school': 1, 'basic.9y': 2, 'university.degree': 3, 'unknown': 4, 'basic.4y': 5, 'basic.6y': 6, 'illiterate': 7}
    {'no': 0, 'unknown': 1, 'yes': 2}
    {'yes': 0, 'no': 1, 'unknown': 2}
    {'yes': 0, 'no': 1, 'unknown': 2}
    {'cellular': 0, 'telephone': 1}
    {'aug': 0, 'may': 1, 'apr': 2, 'nov': 3, 'jul': 4, 'jun': 5, 'oct': 6, 'dec': 7, 'sep': 8, 'mar': 9}
    {'mon': 0, 'wed': 1, 'fri': 2, 'tue': 3, 'thu': 4}
    {'failure': 0, 'nonexistent': 1, 'success': 2}
    {'no': 0, 'yes': 1}
    '''