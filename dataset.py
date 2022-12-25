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
            self.dataframe[i] = self.dataframe[i].map(uniquedict)
            cfgs_io("%d.pkl" % i, "out", uniquedict)
   
    def showlabel(self):
        for i in self.encodelist:
            struct = cfgs_io("%d.pkl" % i, "in")
            print(struct)

    def __getitem__(self, index):
        record = self.dataframe.iloc[index].values
        label = record[-1]
        if label == 'yes':
            label = np.array((1, 0), dtype='float32')
        else:
            label = np.array((0, 1), dtype='float32')
        inp = record[:-1].copy()
        # for i in range(2, 21):
        #     if i in self.encodelist:
        #         inp = np.append(inp, self.correspondingdict[record[i]])
        inp = np.float32(inp)
        return inp, label

    def __len__(self):
        return len(self.dataframe)

if __name__=="__main__":
    dataset = Dataset("data/train.csv")
    print("Number of records: ", len(dataset))
    dataset.showlabel()
    # struct = cfgs_io("correspondingdict.pkl", "in")
    # [print(k,v) for k,v in struct.items()]
    # 取第i条记录
    for i in range(10):
        x,y = dataset.__getitem__(i)
        print(x, y)
    '''
    yes [1. 0. 0.]
    no [0. 1. 0.]
    unknown [0. 0. 1.]
    admin. [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    services [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    blue-collar [0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    entrepreneur [0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
    management [0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
    technician [0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
    housemaid [0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
    self-employed [0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]
    unemployed [0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
    retired [0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]
    student [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
    unknown_c [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
    divorced [1. 0. 0. 0.]
    married [0. 1. 0. 0.]
    single [0. 0. 1. 0.]
    unknown_d [0. 0. 0. 1.]
    professional.course [1. 0. 0. 0. 0. 0. 0. 0.]
    high.school [0. 1. 0. 0. 0. 0. 0. 0.]
    basic.9y [0. 0. 1. 0. 0. 0. 0. 0.]
    university.degree [0. 0. 0. 1. 0. 0. 0. 0.]
    unknown_e [0. 0. 0. 0. 1. 0. 0. 0.]
    basic.4y [0. 0. 0. 0. 0. 1. 0. 0.]
    basic.6y [0. 0. 0. 0. 0. 0. 1. 0.]
    illiterate [0. 0. 0. 0. 0. 0. 0. 1.]
    cellular [1. 0.]
    telephone [0. 1.]
    aug [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
    may [0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]
    apr [0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]
    nov [0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]
    jul [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
    jun [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]
    oct [0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
    dec [0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]
    sep [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
    mar [0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]
    mon [1. 0. 0. 0. 0.]
    wed [0. 1. 0. 0. 0.]
    fri [0. 0. 1. 0. 0.]
    tue [0. 0. 0. 1. 0.]
    thu [0. 0. 0. 0. 1.]
    failure [1. 0. 0.]
    nonexistent [0. 1. 0.]
    success [0. 0. 1.]
    '''