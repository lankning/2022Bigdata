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
                    paddle.nn.Linear( in_features = in_num,  out_features=nodes)
                    )
            elif i < (layers - 1):
                fclayers.append(
                    paddle.nn.Linear( in_features = nodes,  out_features=nodes)
                    )
            else:
                fclayers.append(
                    paddle.nn.Linear( in_features = nodes,  out_features=out_num)
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