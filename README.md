# Model Test

- 是否支持中文
- 准确率
- 识别实体类别
- 部署调用是否方便
- 执行速度

## NER Basics

| NE Type | Examples |
| :------| :------ |
| ORGANIZATION | Georgia-Pacific Corp., WHO |
| PERSON | Eddy Bonte, President Obama |
| LOCATION | Murray River, Mount Everest |
| DATE | June, 2008-06-29 |
| TIME | two fifty a m, 1:30 p.m. |
| MONEY | 175 million Canadian Dollars, GBP 10.40 |
| PERCENT | twenty pct, 18.75 % |
| FACILITY | Washington Monument, Stonehenge |
| GPE | such as city, state/province, and country. |

## stanford-corenlp

[reference](https://github.com/Lynten/stanford-corenlp/blob/master)

### 部署

1. 下载安装 JDK 1.8 及以上版本
2. 下载 Stanford CoreNLP 文件，解压
3. 处理中文还需要下载中文的模型 jar 文件，然后放到 stanford-corenlp-full-2016-10-31 根目录下即可

### simple test

#### errors

1.`permission denied`

Solution : 切换 root 权限

2.不断输出`Waiting until the server is available.`

Solution : 切换到 core nlp 目录下，执行 `java -mx1g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9011 -timeout 1500`，然后继续执行文件即可

3.中文分词浏览器直接输入可以使用，但是调用 NER 包返回空白分词字符串，检查过英文可用，下载最新中文包，待解决

### futher test



### 性能

- 支持中文
- 共有七种实体类别可以识别
  - Time
  - Location
  - Organization
  - Person
  - Money
  - Percent
  - Date
- 速度
  - 正常初始化需要十几秒的时间
- 便捷性
  - 部署非常便捷
  - 但是需要调用的时候需要在后台通过 java 开一个和 StanfordCoreNLPServer 相连接的进程才能正常使用，否则会一直显示等待
- 准确率
  - 