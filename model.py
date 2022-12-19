import paddle
# Subclass mode: https://www.paddlepaddle.org.cn/documentation/docs/zh/guides/beginner/model_cn.html
# API Overview： https://www.paddlepaddle.org.cn/documentation/docs/zh/api/paddle/nn/Overview_cn.html
# Linear Op: https://www.paddlepaddle.org.cn/documentation/docs/zh/api/paddle/nn/Linear_cn.html#linear

class fcnet(paddle.nn.Layer):
    def __init__(self, in_num, out_num, layers = 5, nodes = 2048):
        '''
        Function: Initialize all variables.
        '''
        super(fcnet, self).__init__()
        fclayers = []
        for i in range(layers):
            if i == 0:
                fclayers.append(
                    paddle.nn.Linear( in_features = in_num,  out_features = nodes)
                    )
            elif i < (layers - 1):
                fclayers.append(
                    paddle.nn.Linear( in_features = nodes,  out_features = nodes)
                    )
            else:
                fclayers.append(
                    paddle.nn.Linear( in_features = nodes,  out_features = out_num)
                    )
        self.fclayers =  paddle.nn.LayerList(fclayers)
        self.silu = paddle.nn.Silu("Silu")
        self.layers = layers

    def forward(self, x):
        '''
        Function: Forward calculate the features of network.
        Structure: 
        0. Temporary and spatio ecoding
        1. Encoder: convolution layers, extract the features of inputs
        2. Decoder: convolution layers, rebuild the frame
        '''
        # encoder part
        for i in range(self.layers):
            x = self.silu(self.fclayers[i](x))
        return x

if __name__=="__main__":
    fcmodel = fcnet(20, 1)
    model_info = paddle.summary(fcmodel, (1, 20))
    print(model_info)
    '''
    ---------------------------------------------------------------------------
    Layer (type)       Input Shape          Output Shape         Param #
    ===========================================================================
    Linear-1          [[1, 20]]            [1, 2048]           43,008
     Silu-1            [[1, 1]]              [1, 1]               0
    Linear-2         [[1, 2048]]           [1, 2048]          4,196,352
    Linear-3         [[1, 2048]]           [1, 2048]          4,196,352
    Linear-4         [[1, 2048]]           [1, 2048]          4,196,352
    Linear-5         [[1, 2048]]             [1, 1]             2,049
    ===========================================================================
    Total params: 12,634,113
    Trainable params: 12,634,113
    Non-trainable params: 0
    ---------------------------------------------------------------------------
    Input size (MB): 0.00
    Forward/backward pass size (MB): 0.06
    Params size (MB): 48.20
    Estimated Total Size (MB): 48.26
    ---------------------------------------------------------------------------

    {'total_params': 12634113, 'trainable_params': 12634113}
    '''