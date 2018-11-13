# Chinese NER Solutions

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

简单测试用例

### futher test

复杂测试用例，并生成准确率等参数

### errors

1.`permission denied`

Solution : 切换 root 权限

2.不断输出`Waiting until the server is available.`

Solution : 切换到 core nlp 目录下，执行 `java -mx1g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9011 -timeout 1500`，然后继续执行文件即可

3.中文分词浏览器直接输入可以使用，但是调用 NER 包返回空白分词字符串，检查过英文可用，下载最新中文包，待解决 (fixed)

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

PS : 最新版本已经有支持如下实体类别

```
'PERCENT', 'ORDINAL', 'GPE', 'LOCATION', 'MISC', 'CITY', 'O', 'RELIGION', 'NATIONALITY', 'TITLE', 'ORGANIZATION', 'TIME', 'FACILITY', 'DEMONYM', 'MONEY', 'COUNTRY', 'STATE_OR_PROVINCE', 'DATE', 'CRIMINAL_CHARGE', 'PERSON', 'CAUSE_OF_DEATH', 'IDEOLOGY', 'NUMBER', 'URL', 'EMAIL'
```

## Chinese_models_for_SpaCy

[reference](https://github.com/howl-anderson/Chinese_models_for_SpaCy)

### 部署

1. 从 [releases](https://github.com/howl-anderson/Chinese_models_for_SpaCy/releases) 页面下载模型，假设所下载的模型名为 zh_core_web_sm-2.x.x.tar.gz
2. 安装模型 `pip install zh_core_web_sm-2.x.x.tar.gz`
3. 建立链接 `spacy link zh_core_web_sm zh` (optional)

### Test

```python
import spacy

import zh_core_web_sm

nlp = spacy.load('zh')

def simple_test():
    doc = nlp("帮我订一张明天上午到深圳的机票")
    for token in doc:
        print(token.text, token.ent_iob_, token.ent_type_)

def single_step(sentence):
    return nlp(sentence)


def custom_test(filename='corpus/test'):
    with open(filename, 'r') as f:
        lines = f.readlines()
        with open('out_spacy', 'w') as fout:
            for sentence in lines:
                pred = []
                doc = single_step(sentence)
                for token in doc:
                    pred.append((token.text, token.ent_type_))
                fout.write(str(pred) + '\n')
                pred = []
            fout.close()
        f.close()

custom_test()
```

> 效果有待检验

## Duckling

调用方法：

```python
from duckling import DucklingWrapper
language = 'zh'

try:
    # languages in duckling are eg "de$core"
    duckling = DucklingWrapper(language=language)
except ValueError as e:  # pragma: no cover
    raise Exception("Duckling error. {}".format(e))

matches = duckling.parse('帮我订一张30号去上海的机票')
print(matches)
```

Duckling还提供了parse_duration和parse_time的接口，初步具备识别口语化表达的能力，包括早上下午，上周六，明天后天，下周末等，如需使用还要详细调研

## Transfer Learning for ner

### Structure

![](http://ww1.sinaimg.cn/large/e1ac6bd5ly1fwq2lqapizj21ba16ajzt.jpg)

### Result

- boson数据集本身训练f1-score：> 65 (9000训练数据)
- **boson数据集通过迁移学习f1-score：> 50 (800训练数据)**

是否可行需要更多的数据集和实际对话数据进行测试

## Pretrained Language Model

- [BERT](https://github.com/google-research/bert)(output 与传统词向量不同，数据较大)
- [ELMo](https://allennlp.org/elmo)(最可行)
- [GPT](https://github.com/huggingface/pytorch-openai-transformer-lm)
