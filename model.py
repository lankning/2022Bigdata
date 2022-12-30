import paddle
import numpy as np
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
        self.fclayers0 =  paddle.nn.LayerList(fclayers)
        norms = []
        for i in range(layers - 1):
            norms.append(
                    paddle.nn.BatchNorm1D(num_features = nodes)
                    )
        self.norms =  paddle.nn.LayerList(norms)
        # fclayers = []
        # for i in range(layers):
        #     if i == 0:
        #         fclayers.append(
        #             paddle.nn.Linear( in_features = in_num,  out_features = nodes)
        #             )
        #     elif i < (layers - 1):
        #         fclayers.append(
        #             paddle.nn.Linear( in_features = nodes,  out_features = nodes)
        #             )
        #     else:
        #         fclayers.append(
        #             paddle.nn.Linear( in_features = nodes,  out_features = out_num)
        #             )
        # self.fclayers2 =  paddle.nn.LayerList(fclayers)
        self.relu = paddle.nn.ReLU()
        self.sigmoid = paddle.nn.Sigmoid()
        self.softmax = paddle.nn.Softmax()
        self.layers = layers

    def forward(self, x):
        '''
        Function: Forward calculate the features of network.
        '''
        # for i in range(self.layers):
        #     x0 = x
        #     x1 = x
        #     x2 = x
        #     x0 = self.fclayers0[i](x0)
        #     x0 = self.sigmoid(x0)
        #     x1 = self.fclayers1[i](x1)
        #     x1 = self.sigmoid(x1)
        #     x2 = self.fclayers2[i](x2)
        #     x2 = self.sigmoid(x2)
        #     x = paddle.multiply(paddle.multiply(x0, x1), x2)
        for i in range(self.layers):
            x = self.fclayers0[i](x)
            if i < self.layers -1:
                # x = self.norms[i](x)
                x = self.relu(x)
        x = self.relu(x)
        x = self.softmax(x)
        return x

class Precision(paddle.metric.Metric):
    """
    Precision (also called positive predictive value) is the fraction of
    relevant instances among the retrieved instances. Refer to
    https://en.wikipedia.org/wiki/Evaluation_of_binary_classifiers

    Noted that this class manages the precision score only for binary
    classification task.
    
    ......

    """

    def __init__(self, name='precision', *args, **kwargs):
        super(Precision, self).__init__(*args, **kwargs)
        self.tp = 0  # true positive
        self.sum = 0  # sum elements
        self._name = name

    def update(self, preds, labels):
        """
        Update the states based on the current mini-batch prediction results.

        Args:
            preds (numpy.ndarray): The prediction result, usually the output
                of two-class sigmoid function. It should be a vector (column
                vector or row vector) with data type: 'float64' or 'float32'.
            labels (numpy.ndarray): The ground truth (labels),
                the shape should keep the same as preds.
                The data type is 'int32' or 'int64'.
        """
        if isinstance(preds, paddle.Tensor):
            preds = preds.numpy()
        elif isinstance(preds, np.array):
            None
        else:
            raise ValueError("The 'preds' must be a numpy ndarray or Tensor.")

        if isinstance(labels, paddle.Tensor):
            labels = labels.numpy()
        elif isinstance(labels, np.array):
            None
        else:
            raise ValueError("The 'labels' must be a numpy ndarray or Tensor.")

        self.sum = np.prod(np.shape(labels))
        preds = np.round(preds).astype("int32")
        labels = np.round(labels).astype("int32")
        self.tp = np.sum([preds==labels])

    def reset(self):
        """
        Resets all of the metric state.
        """
        self.tp = 0
        self.sum = 0

    def accumulate(self):
        """
        Calculate the final precision.

        Returns:
            A scaler float: results of the calculated precision.
        """
        return float(self.tp/self.sum)

    def name(self):
        """
        Returns metric name
        """
        return self._name

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