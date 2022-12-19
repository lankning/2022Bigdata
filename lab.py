# ref: https://blog.csdn.net/weixin_40493501/article/details/106406110

import pickle

def cfgs_io(path: str, mode: str, struct = {}):
    if mode == 'out':
        with open(path, 'wb') as f:
            pickle.dump(struct, f)
    elif mode == 'in':
        with open('lab.pkl', 'rb') as f:
            struct = pickle.load(f)
        return struct
    else:
        raise

def t():
    import numpy as np
    a = np.zeros((3,1)).flatten()
    b = 2
    c = np.array([a, b])
    print(c.shape)
    print(c)
    return 1

if __name__ == "__main__":
    struct = {'edu': [0,0,1], 'ddd': [0,1,0,0]}
    cfgs_io("lab.pkl", 'out', struct)
    struct = cfgs_io("lab.pkl", 'in')
    print(struct)
    # struct = cfgs_io("lab.pkl", 'xxx')
    t()