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
    def __init__(self, csvpath, mode = 'train', onehot = True, norm = True):
        '''
        Step 2: realize __init__()
        initialize the dataset,
        mapping the samples and labels to list
        '''
        super(Dataset, self).__init__()
        self.encodelist = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 21]
        self.dataframe = pds.read_csv(csvpath)
        self.onehot = onehot
        self.mode = mode
        self.norm = norm
        self.labelencoder()

    def labelencoder(self):
        '''
        mode: train / test
            train: auto encode and save to .pkls
            test:  encode string by .pkls
        '''
        if self.mode == 'train':
            if self.onehot:
                for i in range(22):
                    if i in self.encodelist:
                        uniquedict = {}
                        uniquelist = self.dataframe.iloc[:,i].unique()
                        onehot_matrix = np.eye((len(uniquelist)))
                        for j in range(len(uniquelist)):
                            uniquedict[uniquelist[j]] = onehot_matrix[j]
                        self.dataframe[self.dataframe.columns[i]] = self.dataframe[self.dataframe.columns[i]].map(uniquedict)
                        cfgs_io("statics/onehot_%d.pkl" % i, "out", uniquedict)
                    elif self.norm:
                        max = self.dataframe[self.dataframe.columns[i]].max()
                        min = abs(self.dataframe[self.dataframe.columns[i]].min())
                        max = max if max > min else min
                        self.dataframe[self.dataframe.columns[i]] /= max
            else:
                for i in range(22):
                    if i in self.encodelist:
                        uniquedict = {}
                        uniquelist = self.dataframe.iloc[:,i].unique()
                        if self.norm:
                            for j in range(len(uniquelist)):
                                uniquedict[uniquelist[j]] = j / (len(uniquelist)-1)
                        else:
                            for j in range(len(uniquelist)):
                                uniquedict[uniquelist[j]] = j
                        self.dataframe[self.dataframe.columns[i]] = self.dataframe[self.dataframe.columns[i]].map(uniquedict)
                        cfgs_io("statics/%d.pkl" % i, "out", uniquedict)
                    elif self.norm:
                        max = self.dataframe[self.dataframe.columns[i]].max()
                        min = abs(self.dataframe[self.dataframe.columns[i]].min())
                        max = max if max > min else min
                        self.dataframe[self.dataframe.columns[i]] /= max
        elif self.mode == 'test':
            if self.onehot:
                for i in self.encodelist:
                    uniquedict = cfgs_io("statics/onehot_%d.pkl" % i, "in")
                    self.dataframe[self.dataframe.columns[i]] = self.dataframe[self.dataframe.columns[i]].map(uniquedict)
            else:
                for i in self.encodelist:
                    uniquedict = cfgs_io("statics/%d.pkl" % i, "in")
                    self.dataframe[self.dataframe.columns[i]] = self.dataframe[self.dataframe.columns[i]].map(uniquedict)
        else: 
            raise ValueError('[Dateset::labelencoder] mode must be train or test')
   
    def showlabel(self):
        if self.onehot:
            for i in self.encodelist:
                struct = cfgs_io("statics/onehot_%d.pkl" % i, "in")
                print(struct)
        else:
            for i in self.encodelist:
                struct = cfgs_io("statics/%d.pkl" % i, "in")
                print(struct)

    def __getitem__(self, index):
        if self.onehot:
            record = self.dataframe.iloc[index].values
            if self.mode == 'train':
                label = record[-1].copy()
                inp = record[1:2]
                for i in record[2:-1]:
                    inp = np.append(inp, i)
                inp = np.float32(inp)
                label = np.float32(label)
            elif self.mode == 'test':
                label = ''
                inp = record[1:2]
                for i in record[2:21]:
                    inp = np.append(inp, i)
                inp = np.float32(inp)
        else:
            record = self.dataframe.iloc[index].values
            label = record[-1:].copy()
            inp = record[1:21].copy()
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
    # labels = []
    # for i in range(7500):
    #     _, label = dataset.__getitem__(i)
    #     labels.append(label)
    # labels = np.float32(np.array(labels))
    # print("No/All = %.2f%%" % (np.sum(labels==0.)/75))
    '''
    # 1. Encode string to a value (with normalization)
    Number of records:  22500
    {'admin.': 0.0, 'services': 0.08333333333333333, 'blue-collar': 0.16666666666666666, 'entrepreneur': 0.25, 'management': 0.3333333333333333, 'technician': 0.4166666666666667, 'housemaid': 0.5, 'self-employed': 0.5833333333333334, 'unemployed': 0.6666666666666666, 'retired': 0.75, 'student': 0.8333333333333334, 'unknown': 0.9166666666666666}
    {'divorced': 0.0, 'married': 0.25, 'single': 0.5, 'unknown': 0.75}
    {'professional.course': 0.0, 'high.school': 0.125, 'basic.9y': 0.25, 'university.degree': 0.375, 'unknown': 0.5, 'basic.4y': 0.625, 'basic.6y': 0.75, 'illiterate': 0.875}
    {'no': 0.0, 'unknown': 0.3333333333333333, 'yes': 0.6666666666666666}
    {'yes': 0.0, 'no': 0.3333333333333333, 'unknown': 0.6666666666666666}
    {'yes': 0.0, 'no': 0.3333333333333333, 'unknown': 0.6666666666666666}
    {'cellular': 0.0, 'telephone': 0.5}
    {'aug': 0.0, 'may': 0.1, 'apr': 0.2, 'nov': 0.3, 'jul': 0.4, 'jun': 0.5, 'oct': 0.6, 'dec': 0.7, 'sep': 0.8, 'mar': 0.9}
    {'mon': 0.0, 'wed': 0.2, 'fri': 0.4, 'tue': 0.6, 'thu': 0.8}
    {'failure': 0.0, 'nonexistent': 0.3333333333333333, 'success': 0.6666666666666666}
    {'no': 0.0, 'yes': 0.5}
    (20,) (1,)
    No/All = 87.31%
    # 2. Encode string to a value (without normalization)
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
    # 3. Onehot
    {'admin.': array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 'services': array([0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 'blue-collar': 
    array([0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 'entrepreneur': array([0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0.]), 'management': array([0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0.]), 'technician': array([0., 0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0.]), 'housemaid': array([0., 0., 0., 
    0., 0., 0., 1., 0., 0., 0., 0., 0.]), 'self-employed': array([0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0., 0.]), 'unemployed': array([0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0., 0.]), 'retired': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.]), 'student': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1., 0.]), 'unknown': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 1.])}
    {'divorced': array([1., 0., 0., 0.]), 'married': array([0., 1., 0., 0.]), 'single': array([0., 0., 1., 0.]), 'unknown': array([0., 0., 0., 1.])}
    {'professional.course': array([1., 0., 0., 0., 0., 0., 0., 0.]), 'high.school': array([0., 1., 0., 0., 0., 0., 0., 0.]), 'basic.9y': array([0., 0., 1., 
    0., 0., 0., 0., 0.]), 'university.degree': array([0., 0., 0., 1., 0., 0., 0., 0.]), 'unknown': array([0., 0., 0., 0., 1., 0., 0., 0.]), 'basic.4y': array([0., 0., 0., 0., 0., 1., 0., 0.]), 'basic.6y': array([0., 0., 0., 0., 0., 0., 1., 0.]), 'illiterate': array([0., 0., 0., 0., 0., 0., 0., 1.])}        
    {'no': array([1., 0., 0.]), 'unknown': array([0., 1., 0.]), 'yes': array([0., 0., 1.])}
    {'yes': array([1., 0., 0.]), 'no': array([0., 1., 0.]), 'unknown': array([0., 0., 1.])}
    {'yes': array([1., 0., 0.]), 'no': array([0., 1., 0.]), 'unknown': array([0., 0., 1.])}
    {'cellular': array([1., 0.]), 'telephone': array([0., 1.])}
    {'aug': array([1., 0., 0., 0., 0., 0., 0., 0., 0., 0.]), 'may': array([0., 1., 0., 0., 0., 0., 0., 0., 0., 0.]), 'apr': array([0., 0., 1., 0., 0., 0., 0., 0., 0., 0.]), 'nov': array([0., 0., 0., 1., 0., 0., 0., 0., 0., 0.]), 'jul': array([0., 0., 0., 0., 1., 0., 0., 0., 0., 0.]), 'jun': array([0., 0., 0., 0., 0., 1., 0., 0., 0., 0.]), 'oct': array([0., 0., 0., 0., 0., 0., 1., 0., 0., 0.]), 'dec': array([0., 0., 0., 0., 0., 0., 0., 1., 0., 0.]), 'sep': 
    array([0., 0., 0., 0., 0., 0., 0., 0., 1., 0.]), 'mar': array([0., 0., 0., 0., 0., 0., 0., 0., 0., 1.])}
    {'mon': array([1., 0., 0., 0., 0.]), 'wed': array([0., 1., 0., 0., 0.]), 'fri': array([0., 0., 1., 0., 0.]), 'tue': array([0., 0., 0., 1., 0.]), 'thu': 
    array([0., 0., 0., 0., 1.])}
    {'failure': array([1., 0., 0.]), 'nonexistent': array([0., 1., 0.]), 'success': array([0., 0., 1.])}
    {'no': array([1., 0.]), 'yes': array([0., 1.])}
    '''