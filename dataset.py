import paddle
import pandas as pds

class Dataset(paddle.io.Dataset):
    '''
    Step 1: inherit the class paddle.io.Dataset
    '''
    def __init__(self, 
                indir,
                h = 360, 
                w = 640
                ):
        '''
        Step 2: realize __init__()
        initialize the dataset,
        mapping the samples and labels to list
        '''
        super(Dataset, self).__init__()
        self.data_list = []
        filelist = os.listdir(indir)
        filelist.sort(key=lambda x:int(x[5:-4]))
        for i, filename in enumerate(filelist):
            if (i != 0) and (i < len(filelist)-1):
                self.data_list.append([
                    os.path.join(indir, filelist[i-1]), 
                    os.path.join(indir, filename),
                    os.path.join(indir, filelist[i+1])
                    ])
        codes = np.zeros((3, h, w))
        # Temporaray codes
        codes[0, :, :] = 0
        # Line direction
        for j in range(w):
            codes[1, :, j] = np.sin(j/w)
        # Row direction
        for j in range(h):
            codes[2, j, :] = np.sin(j/h)
        self.encodes = {"codes": codes, "length": 2}

    def temporary_and_spatial_encoding(self, *args):
        '''
        Function: This function is designed to encode
                  the tensor by axises of time, line 
                  and row.
        ---------------------------------------------
        Activate Function: sin

        Input:  numpy.array, 3-dims, data 
                format = CHW, shape = [C,H,W]
        Output: numpy.array, 3-dims, data 
                format = CHW, shape = [C+3, H, W]
        ---------------------------------------------
        Inner parameters:
        1. length = length of list
        1. h: height
        2. w: width
        '''
        if args[0].shape==self.encodes['codes'].shape:
            _, self.h, self.w = self.encodes['codes'].shape
        else:
            _, self.h, self.w = args[0].shape
            codes = np.zeros((3, self.h, self.w))
            # Temporaray codes
            codes[0, :, :] = 0
            # Line direction
            for j in range(self.w):
                codes[1, :, j] = np.sin(j/self.w)
            # Row direction
            for j in range(self.h):
                codes[2, j, :] = np.sin(j/self.h)
            self.encodes['codes'] = codes
        
        self.encodes['length'] = len(args)

        rtn = []
        for i, image in enumerate(args):
            self.encodes['codes'][0, :, :] = np.sin(i/(self.encodes['length']-1))
            image = np.concatenate([image, self.encodes['codes']], 0)
            rtn.append(image)
        return rtn

    def __getitem__(self, index):
        '''
        Step 3: realize __get_item__()
        Input: index
        RTN: data[index], label[index]
        '''
        # 根据索引，从列表中取出一个图像
        # print("[Dataset::__getitem__]",self.data_list[index])
        in0path, outpath, in1path = self.data_list[index]
        # 读取彩色图
        in0 = cv2.imread(in0path,  cv2.IMREAD_COLOR)
        in1 = cv2.imread(in1path,  cv2.IMREAD_COLOR)
        out = cv2.imread(outpath,  cv2.IMREAD_COLOR)
        # 飞桨训练时内部数据格式默认为float32，将图像数据格式转换为 float32
        in0 = in0.astype('float32').transpose((2,0,1))
        in1 = in1.astype('float32').transpose((2,0,1))
        out = out.astype('float32').transpose((2,0,1))
        in0, in1 = self.temporary_and_spatial_encoding(in0, in1)
        in0 = in0.astype('float32')
        in1 = in1.astype('float32')
        # 返回图像和对应标签
        return in0, in1, out

    def __len__(self):
        """
        步骤四：实现 __len__ 函数，返回数据集的样本总数
        """
        return len(self.data_list)
