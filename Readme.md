# 阿里天池竞赛
[【教学赛】金融数据分析赛题1：银行客户认购产品预测](https://tianchi.aliyun.com/competition/entrance/531993/introduction?spm=5176.12281925.0.0.46e67137PjhlEt)
![](https://img.alicdn.com/imgextra/i3/O1CN01fBX9JF1XbwO78w3zP_!!6000000002943-2-tps-1440-438.png)

**[课程论文](statics/大数据期论文_朱文康_2021206520006.pdf)**

# 数据

**To DO: 预测用户是否进行购买产品**

## 数据解释

| 字段             | 说明                                                 |
| ---------------- | ---------------------------------------------------- |
| age              | 年龄                                                 |
| job              | 职业：admin, unknown, unemployed, management…        |
| marital          | 婚姻：married, divorced, single                      |
| education        | 受教育程度                                           |
| default          | 信用卡是否有违约: yes or no                          |
| housing          | 是否有房贷: yes or no                                |
| contact          | 联系方式：unknown, telephone, cellular               |
| month            | 上一次联系的月份：jan, feb, mar, …                   |
| day_of_week      | 上一次联系的星期几：mon, tue, wed, thu, fri          |
| duration         | 上一次联系的时长（秒）                               |
| campaign         | 活动期间联系客户的次数                               |
| pdays            | 上一次与客户联系后的间隔天数                         |
| previous         | 在本次营销活动前，与客户联系的次数                   |
| poutcome         | 之前营销活动的结果：unknown, other, failure, success |
| emp_var_rate     | 就业变动率（季度指标）                               |
| cons_price_index | 消费者价格指数（月度指标）                           |
| cons_conf_index  | 消费者信心指数（月度指标）                           |
| lending_rate3m   | 银行同业拆借率 3个月利率（每日指标）                 |
| nr_employed      | 雇员人数（季度指标）                                 |
| subscribe        | 客户是否进行购买：yes 或 no                          |

## 训练数据

共有22500条记录，每条记录有21个字段（包括subscribe）

| id   | age  | job          | marital  | education           | default | housing | loan | contact  | month | day_of_week | duration | campaign | pdays | previous | poutcome    | emp_var_rate | cons_price_index | cons_conf_index | lending_rate3m | nr_employed | subscribe |
| ---- | ---- | ------------ | -------- | ------------------- | ------- | ------- | ---- | -------- | ----- | ----------- | -------- | -------- | ----- | -------- | ----------- | ------------ | ---------------- | --------------- | -------------- | ----------- | --------- |
| 1    | 51   | admin.       | divorced | professional.course | no      | yes     | yes  | cellular | aug   | mon         | 4621     | 1        | 112   | 2        | failure     | 1.4          | 90.81            | -35.53          | 0.69           | 5219.74     | no        |
| 2    | 50   | services     | married  | high.school         | unknown | yes     | no   | cellular | may   | mon         | 4715     | 1        | 412   | 2        | nonexistent | -1.8         | 96.33            | -40.58          | 4.05           | 4974.79     | yes       |
| 3    | 48   | blue-collar  | divorced | basic.9y            | no      | no      | no   | cellular | apr   | wed         | 171      | 0        | 1027  | 1        | failure     | -1.8         | 96.33            | -44.74          | 1.5            | 5022.61     | no        |
| 4    | 26   | entrepreneur | single   | high.school         | yes     | yes     | yes  | cellular | aug   | fri         | 359      | 26       | 998   | 0        | nonexistent | 1.4          | 97.08            | -35.55          | 5.11           | 5222.87     | yes       |
| 5    | 45   | admin.       | single   | university.degree   | no      | no      | no   | cellular | nov   | tue         | 3178     | 1        | 240   | 4        | success     | -3.4         | 89.82            | -33.83          | 1.17           | 4884.7      | no        |

## 测试数据

共有7500条记录，每条记录有20个字段（去除了subscribe）

| id    | age  | job         | marital | education           | default | housing | loan | contact   | month | day_of_week | duration | campaign | pdays | previous | poutcome    | emp_var_rate | cons_price_index | cons_conf_index | lending_rate3m | nr_employed |
| ----- | ---- | ----------- | ------- | ------------------- | ------- | ------- | ---- | --------- | ----- | ----------- | -------- | -------- | ----- | -------- | ----------- | ------------ | ---------------- | --------------- | -------------- | ----------- |
| 22501 | 35   | technician  | single  | professional.course | no      | yes     | yes  | cellular  | aug   | mon         | 3295     | 1        | 476   | 0        | success     | 1.4          | 95.37            | -33.04          | 3.63           | 5204.54     |
| 22502 | 26   | admin.      | single  | high.school         | no      | yes     | no   | cellular  | may   | thu         | 2872     | 1        | 166   | 2        | success     | -1.8         | 91.75            | -44.42          | 3.16           | 4924.78     |
| 22503 | 44   | blue-collar | married | basic.6y            | no      | no      | no   | telephone | may   | mon         | 268      | 3        | 968   | 0        | nonexistent | 1.1          | 89.67            | -36.9           | 5.04           | 4947.02     |
| 22504 | 36   | blue-collar | married | basic.9y            | no      | yes     | no   | telephone | nov   | thu         | 30       | 1        | 432   | 5        | success     | -0.1         | 89.87            | -41.66          | 3.27           | 5203.33     |
| 22505 | 41   | blue-collar | married | basic.4y            | no      | yes     | no   | telephone | may   | thu         | 1670     | 1        | 944   | 3        | success     | 1.1          | 97.64            | -36.32          | 3.95           | 4992.02     |

## 提交格式

| id    | subscribe |
| ----- | --------- |
| 22501 | no        |
| 22502 | no        |
| 22503 | no        |
| 22504 | no        |
| 22505 | no        |

## 数据编码

数据编码分为两种，1是将所有数据全部编码为0-1范围内，2是采用独热编码

- 编码方式1：全部编码到0-1内

| 字段        | 字段值                                                       | 编码                                                         |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| job         | admin.  services  blue-collar  entrepreneur  management  technician  housemaid  self-employed  unemployed  retired  student  unknown | 0.00  0.09  0.18  0.27  0.36  0.45  0.55  0.64  0.73  0.82  0.91  1.00 |
| marital     | divorced  married  single  unknown                           | 0.00  0.33  0.67  1.00                                       |
| education   | professional.course  high.school  basic.9y  university.degree  unknown  basic.4y  basic.6y  illiterate | 0.00  0.14  0.29  0.43  0.57  0.71  0.86  1.00               |
| default     | no  unknown  yes                                             | 0.00  0.50  1.00                                             |
| housing     | yes  no  unknown                                             | 0.00  0.50  1.00                                             |
| loan        | yes  no  unknown                                             | 0.00  0.50  1.00                                             |
| contact     | cellular  telephone                                          | 0.00  1.00                                                   |
| month       | aug  may  apr  nov  jul  jun  oct  dec  sep  mar             | 0.00  0.11  0.22  0.33  0.44  0.56  0.67  0.78  0.89  1.00   |
| day_of_week | mon  wed  fri  tue  thu                                      | 0.00  0.25  0.50  0.75  1.00                                 |
| poutcome    | failure  nonexistent  success                                | 0.00  0.50  1.00                                             |
| subscribe   | no  yes                                                      | 0.00  1.00                                                   |

- 编码方式2：独热编码

| 字段        | 字段值                                                       | 编码                                                         |
| ----------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| job         | admin.  services  blue-collar  entrepreneur  management  technician  housemaid  self-employed  unemployed  retired  student  unknown | [1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1.] |
| marital     | divorced  married  single  unknown                           | [1. 0. 0. 0.]  [0. 1. 0. 0.]  [0. 0. 1. 0.]  [0. 0. 0. 1.]   |
| education   | professional.course  high.school  basic.9y  university.degree  unknown  basic.4y  basic.6y  illiterate | [1. 0. 0. 0. 0. 0. 0. 0.]  [0. 1. 0. 0. 0. 0. 0. 0.]  [0. 0. 1. 0. 0. 0. 0. 0.]  [0. 0. 0. 1. 0. 0. 0. 0.]  [0. 0. 0. 0. 1. 0. 0. 0.]  [0. 0. 0. 0. 0. 1. 0. 0.]  [0. 0. 0. 0. 0. 0. 1. 0.]  [0. 0. 0. 0. 0. 0. 0. 1.] |
| default     | no  unknown  yes                                             | [1. 0. 0.]  [0. 1. 0.]  [0. 0. 1.]                           |
| housing     | yes  no  unknown                                             | [1. 0. 0.]  [0. 1. 0.]  [0. 0. 1.]                           |
| loan        | yes  no  unknown                                             | [1. 0. 0.]  [0. 1. 0.]  [0. 0. 1.]                           |
| contact     | cellular  telephone                                          | [1. 0.]  [0. 1.]                                             |
| month       | aug  may  apr  nov  jul  jun  oct  dec  sep  mar             | [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 1. 0. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 1. 0. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 1. 0. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 1. 0. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]  [0. 0. 0. 0. 0. 0. 0. 0. 0. 1.] |
| day_of_week | mon  wed  fri  tue  thu                                      | [1. 0. 0. 0. 0.]  [0. 1. 0. 0. 0.]  [0. 0. 1. 0. 0.]  [0. 0. 0. 1. 0.]  [0. 0. 0. 0. 1.] |
| poutcome    | failure  nonexistent  success                                | [1. 0. 0.]  [0. 1. 0.]  [0. 0. 1.]                           |
| subscribe   | no  yes                                                      | [1. 0.]  [0. 1.]                                             |

# 模型结构

全连接神经网络，5层，每层2048节点。可选：ReLU激活函数、batch normlization、onehot编码。

![](statics/model-arch1.png)

![](statics/model-arch2.png)

# 结果

MSE & Accuracy during training process. Training settings: batch_size = 2500, epochs = 10.

- Encode strings into a value
  - **1-1 normalization & ReLU，提交得分：0.9117**
  - 1-2 ~~normalization~~ & ReLU，提交得分：0.9007
  - 1-3 normalization & Sigmoid，提交得分：0.7845
  - **1-4 ~~normalization~~ & Sigmoid，提交得分：0.9224**
- Onehot
  - 2-1 normalization & ReLU，提交得分：0.9029
  - 2-2 ~~normalization~~ & ReLU，提交得分：0
  - **2-3 normalization & Sigmoid，提交得分：0.9217**
  - 2-4 ~~normalization~~ & Sigmoid，提交得分：0

| MSE (1-1 normalization & ReLU) 0.01               | Accuracy (1-1 normalization & ReLU) 98.88%            |
| ------------------------------------------------- | ----------------------------------------------------- |
| ![](statics/loss_fcmodel_norm_relu.png)           | ![](statics/acc_fcmodel_norm_relu.png)                |
| **MSE (1-2 ~~normalization~~ & ReLU) 0.01**       | **Accuracy (1-2 ~~normalization~~ & ReLU) 98.60%**    |
| ![](statics/loss_fcmodel_relu.png)                | ![](statics/acc_fcmodel_relu.png)                     |
| **MSE (1-3 normalization & Sigmoid) 0.07**        | **Accuracy (1-3 normalization & Sigmoid) 91.40%**     |
| ![](statics/loss_fcmodel_norm_sigmoid.png)        | ![](statics/acc_fcmodel_norm_sigmoid.png)             |
| **MSE (1-4 ~~normalization~~ & Sigmoid) 0.13**    | **Accuracy (1-4 ~~normalization~~ & Sigmoid) 86.84%** |
| ![](statics/loss_fcmodel_sigmoid.png)             | ![](statics/acc_fcmodel_sigmoid.png)                  |
| **MSE 2-1 normalization & ReLU 0.01**             | **Accuracy 2-1 normalization & ReLU 98.84%**          |
| ![](statics/loss_fcmodel_norm_relu_onehot.png)    | ![](statics/acc_fcmodel_norm_relu_onehot.png)         |
| **MSE 2-2 ~~normalization~~ & ReLU 0.13**         | **Accuracy 2-2 ~~normalization~~ & ReLU 87.24%**      |
| ![](statics/loss_fcmodel_relu_onehot.png)         | ![](statics/acc_fcmodel_relu_onehot.png)              |
| **MSE 2-3 normalization & Sigmoid 0.10**          | **Accuracy 2-3 normalization & Sigmoid 94.48%**       |
| ![](statics/loss_fcmodel_norm_sigmoid_onehot.png) | ![](statics/acc_fcmodel_norm_sigmoid_onehot.png)      |
| **MSE 2-4 ~~normalization~~ & Sigmoid 0.13**      | **Accuracy 2-4 ~~normalization~~ & Sigmoid 86.68%**   |
| ![](statics/loss_fcmodel_sigmoid_onehot.png)      | ![](statics/acc_fcmodel_sigmoid_onehot.png)           |

# **参赛队伍**

**我组件了一支单人队伍，队伍名称是finishtheless**

**![image-20221214153011503](statics/image-20221214153011503.png)**