# -*- coding: UTF8 -*-
# ===================================================
# 由于是累积预测
# inputs是个list会不断叠加用户新的输入作为预测
# 因此如果要开始新的一轮预测，要么初始化类，要么清空inputs
#
# 如果交互比较多, inputs需要换成最新的N句话
# 而不是现在所有的输入
# =====================================================


import tensorflow as tf
from entity_parse import *
import re
import fastText


class NLU(object):
    def __init__(self, vocab_path, task_label_path, intent_label_path, model_path, uni_model_path):
        self.vocab_path = vocab_path
        self.task_label_path = task_label_path
        self.intent_label_path = intent_label_path
        self.model_path = model_path

        self.uni_model_path = uni_model_path

        self.vocab, self.task_label, self.intent_label = self.load_vocab()

        self.inputs = []
        self.max_sent_len = 22
        self.max_input_len = 14

        self.sess = tf.Session()
        self.load_model()

    def load_vocab(self):
        vocabulary = {}
        with open(self.vocab_path, "r") as f:
            for line in f:
                w = line.lower().strip().split()
                vocabulary[w[0]] = int(w[1])

        task_label = {}
        with open(self.task_label_path, "r") as f:
            for line in f:
                w = line.lower().strip().split()
                task_label[w[1]] = w[0]

        intent_label = {}
        with open(self.intent_label_path, "r") as f:
            for line in f:
                w = line.lower().strip().split()
                intent_label[w[1]] = w[0]

        return vocabulary, task_label, intent_label

    def process_inputs(self):
        if len(self.inputs) == 0:
            raise ValueError('Not valid user inputs')
        sent_list = []
        sent_len_list = []
        for inp in self.inputs:
            word_list = []
            for w in inp:
                word_list.append(self.vocab.get(w, 1))
            sent_len_list.append(len(word_list))
            word_list = word_list[0: self.max_sent_len] + [0]*max(self.max_sent_len-len(word_list), 0)
            sent_list.append(word_list)
        if len(sent_list) <= self.max_input_len:
            input_len_batch = [len(sent_list)]
            input_batch = [sent_list[0:] + [[0]*self.max_sent_len]*(self.max_input_len-len(sent_list))]
            sent_len_batch = [sent_len_list[0:] + [0]*(self.max_input_len-len(sent_list))]
        else:
            input_len_batch = [self.max_input_len]
            input_batch = [sent_list[(len(sent_list)-self.max_input_len):]]
            sent_len_batch = [sent_len_list[(len(sent_list)-self.max_input_len):]]

        return input_batch, input_len_batch, sent_len_batch

    def load_model(self):
        graph_def = tf.GraphDef()
        with open(self.model_path, 'rb') as f:
            graph_def.ParseFromString(f.read())
        self.sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

        self.uni_model = fastText.load_model(self.uni_model_path)

    def predict(self, sentence):
        slot_filling_result = self.slot_filling(sentence)
        sentence = slot_filling_result["utterance"]
        sentence = sentence.lower().strip()
        sentence = re.sub(r"'s|'d|'ve", ' ', sentence)
        sentence = re.sub(r"n't", ' not ', sentence)
        sentence = re.sub(r"[-.*,/?#&~()<>{}\[\]!%$@;+:\'\"=^|\\]", " ", sentence)  # not remove _
        sentence = re.sub(r"88", "bye", sentence)
        sentence = re.sub(r'\d', ' ', sentence)
        if sentence.strip() == '':
            sentence = 'this_is_an_empty_line'

        uni_result = self.uni_model.predict(sentence)
        if uni_result[0][0] == '__label__0':
            return {"task": "universal", "intent": "universal", "slot": {}}

        self.inputs.append(sentence.split())
        input_batch, input_len_batch, sent_len_batch = self.process_inputs()


        # pred_res = tf.import_graph_def(self.graph_def, input_map={"input_ids": np.array(input_batch, dtype='int32'),
        #                                                           "sentence_length": np.array(sent_len_batch, dtype='int32'),
        #                                                           "input_length": np.array(input_len_batch, dtype='int32'),
        #                                                           "dropout": 1.0},
        #                                return_elements=['task_prediction:0', 'intent_prediction:0'])

        # pred_res = tf.import_graph_def(self.graph_def, input_map={"input_ids": np.array(input_batch, dtype='int32'),
        #                                                           "sentence_length": np.array(sent_len_batch,
        #                                                                                       dtype='int32'),
        #                                                           "input_length": np.array(input_len_batch,
        #                                                                                    dtype='int32'),
        #                                                           "dropout": 1.0},
        #                                return_elements=['task_prob:0', 'intent_prob:0'])

        input_ids = self.sess.graph.get_tensor_by_name("input_ids:0")
        sentence_length = self.sess.graph.get_tensor_by_name("sentence_length:0")
        input_length = self.sess.graph.get_tensor_by_name("input_length:0")
        drop_out = self.sess.graph.get_tensor_by_name("dropout:0")

        task_prob = self.sess.graph.get_tensor_by_name("task_prob:0")
        intent_prob = self.sess.graph.get_tensor_by_name("intent_prob:0")

        task_index, intent_index = self.sess.run([task_prob, intent_prob], feed_dict={input_ids: np.array(input_batch, dtype='int32'),
                                                                        sentence_length: np.array(sent_len_batch, dtype='int32'),
                                                                        input_length: np.array(input_len_batch, dtype='int32'),
                                                                        drop_out: 1.0})

        # task_index, intent_index = self.sess.run(pred_res)
        # # task = self.task_label[str(task_index[0])]
        # # intent = self.intent_label[str(intent_index[0])]

        task = self.task_label[str(np.argmax(task_index[0]))]
        intent = self.intent_label[str(np.argmax(intent_index[0]))]

        # slots = {"wbs_code": slot_filling_result["wbs_code"], "hours": slot_filling_result["hours"],
        #         "from_time": slot_filling_result["from_time"], "to_time": slot_filling_result["to_time"]}
        slots = {}
        for k in ["wbs_code", "hours", "from_time", "to_time"]:
            if slot_filling_result[k] != 'NULL':
                slots[k] = slot_filling_result[k]

        nlu_result = {"task": task, "intent": intent, "slots": slots}

        return nlu_result

        # return task_index, intent_index

    @staticmethod
    def slot_filling(string, repl=True):
        result = {"utterance": string, "wbs_code": "NULL", "hours": "NULL", "from_time": "NULL", "to_time": "NULL",
                  "period_text": "NULL", "hours_text": "NULL"}
        string = string.strip().lower()
        if len(string) == 0:
            return result

        parse_res = code_parse(string)
        if parse_res:
            # string = string.replace(parse_res, "wbs_code")
            # result["utterance"] = string
            result["wbs_code"] = parse_res

        if result["wbs_code"] != 'NULL':
            parse_res = (half_month_parse(string.replace(result["wbs_code"], "wbs_code"))
                         or period_parse(string.replace(result["wbs_code"], "wbs_code"))
                         or from_to_parse(string.replace(result["wbs_code"], "wbs_code"))
                         or single_date_parse(string.replace(result["wbs_code"], "wbs_code"))
                         or from_to_parse_2(string.replace(result["wbs_code"], "wbs_code"))
                         or digit_date_parse(string.replace(result["wbs_code"], "wbs_code")))
        else:
            parse_res = (half_month_parse(string) or period_parse(string) or from_to_parse(string) or
                         single_date_parse(string) or from_to_parse_2(string) or digit_date_parse(string))
        if parse_res:
            # string = string.replace(parse_res[0], "time_period")
            # result["utterance"] = string
            result["period_text"] = parse_res[0]
            result["from_time"] = parse_res[1]
            result["to_time"] = parse_res[2]

        # parse period first, then replace period expression, based on which parse hours to reduce single number errors
        if result["period_text"] != 'NULL':
            parse_res = hours_parse(string.replace(result["period_text"], " time_period "))
        else:
            parse_res = hours_parse(string)
        if parse_res:
            # string = string.replace(parse_res[0], "working_hours")
            # result["utterance"] = string
            result["hours_text"] = parse_res[0]
            result["hours"] = int(parse_res[1])

        if repl:
            if result["wbs_code"] != "NULL":
                string = string.replace(result["wbs_code"], " wbs_code ")
            if result["period_text"] != "NULL":
                string = string.replace(result["period_text"], " time_period ")
            if result["hours_text"] != "NULL":
                try:
                    # 2 between 0216 and 0228，直接替换把2都替换掉了
                    int(result["hours_text"])
                    p1 = "( |,|:)" + result["hours_text"] + "( |,)?"
                    p2 = "( |,|:)?" + result["hours_text"] + "( |,)"
                    string = re.sub(p1, " working_hours ", string)
                    string = re.sub(p2, " working_hours ", string)
                except:
                    string = string.replace(result["hours_text"], " working_hours ")

            result["utterance"] = string

        return result

