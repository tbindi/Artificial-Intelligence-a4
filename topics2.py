import sys
import os
import pickle
import operator
import re
import math
import random

topics_list = ['religion', 'christian', 'mideast', 'pc', 'windows',
               'medical', 'space', 'crypto', 'xwindows', 'atheism',
               'autos', 'mac', 'baseball', 'hockey', 'graphics',
               'politics', 'electronics', 'forsale', 'guns', 'motorcycles']


def display_accuracy(result):
    print "v (Actual / Predicted) >"
    print "\t" + "\t".join(i[0:2] for i in topics_list)
    tn_tp = sum([result[j][j] for j in range(0, len(topics_list))])
    total = sum([sum(result[j]) for j in range(0, len(topics_list))])
    for i in topics_list:
        print i[0:2], "\t", "\t".join(str(i) for i in result[
            topics_list.index(i)]), "\t", sum(result[topics_list.index(i)])
    print " --- "
    print " Accuracy: ", tn_tp * 100.00 / total * 1.00


def accuracy(computed_list):
    N = len(topics_list)
    confusion_matrix = [[0 for i in range(0, N)] for i in range(0, N)]
    for compute in computed_list:
        actual_value = compute[0]
        predic_value = compute[1]
        actual_index = topics_list.index(actual_value)
        predic_index = topics_list.index(predic_value)
        confusion_matrix[actual_index][predic_index] += 1
    return confusion_matrix


def preprocess_data(file_name):
    file_inp = open(file_name, 'rb')
    out_list = []
    g = open("english.txt", 'r')
    stopWords = g.read().split('\n')
    for i in file_inp.readlines():
        y = re.findall(
            r"(?:\s|^)([>\[,.!?]*[A-Za-z_\*\"\'-]+[,.!?\]]*)(?=\s|$)",
            i.rstrip())
        x = re.findall(r"(?:\s|^)([A-Za-z_\*\"\'-]+[,.!?]+[A-Za-z_\*\"\'-]+)("
                       r"?=\s|$)", i.rstrip())
        for k in x:
            y.extend(re.split("[,.!?]+", k))
        y = [''.join(e.lower() for e in j if e.isalnum()) for j in y]
        y = filter(None, y)
        y = [a for a in y if a not in stopWords]
        out_list.extend(y)
    return out_list


# def label_unlabelled(topic_word_dict):
def init_doc_dict():
    doc_dict_inside = dict()
    doc_dict_inside['WORDS'] = dict()
    doc_dict_inside['TOTAL_WORDS'] = 0
    doc_dict_inside['TOPICS'] = dict()
    doc_dict_inside['LABELLED'] = False
    doc_dict_inside['LABEL'] = ""
    return doc_dict_inside


def load_train_data(dataset_dir, fraction):
    doc_dict = dict()
    topic_doc_dict = dict()
    for dir_name in os.listdir(dataset_dir):
        current_dir_path = os.path.join(dataset_dir, dir_name)
        topic_name = dir_name
        if os.path.isdir(current_dir_path):
            files = os.listdir(current_dir_path)
            if topic_name not in topic_doc_dict:
                topic_doc_dict[topic_name] = 0
            topic_doc_dict[topic_name] = len(files)
            for filename in files:
                file_path = os.path.join(current_dir_path, filename)
                file_fd = open(file_path, 'r')
                words = preprocess_data(file_path)
                # words = file_fd.read(-1).split()
                doc_name = dir_name + "_" + filename
                if doc_name not in doc_dict:
                    doc_dict[doc_name] = init_doc_dict()
                else:
                    print("DOC exists"+doc_name)
                for word in words:
                    # print(doc_dict[doc_name])
                    if word not in doc_dict[doc_name]['WORDS']:
                        doc_dict[doc_name]['WORDS'][word] = 0
                    doc_dict[doc_name]['WORDS'][word] += 1
                    doc_dict[doc_name]['TOTAL_WORDS'] += 1

                # Check if this can be labelled
                cur_num = random.randint(1, 10)
                if cur_num <= fraction * 10:
                    doc_dict[doc_name]['TOPICS'][topic_name] = 1.0
                    doc_dict[doc_name]['LABELLED'] = True
                    doc_dict[doc_name]['LABEL'] = topic_name
                elif fraction == 0.0:
                    if cur_num <= 1:
                        topic_name = topics_list[random.randint(0,19)]
                        doc_dict[doc_name]['TOPICS'][topic_name] = 1.0
                        doc_dict[doc_name]['LABELLED'] = True
                        doc_dict[doc_name]['LABEL'] = topic_name
    return doc_dict, topic_doc_dict


def preprocess_topic_word(doc_dict):
    topic_word_dict = dict()

    for doc_name in doc_dict:
        if doc_dict[doc_name]['LABELLED']:
            topic_name = doc_dict[doc_name]['LABEL']
            words = doc_dict[doc_name]['WORDS']
            total_words = doc_dict[doc_name]['TOTAL_WORDS']

            if topic_name not in topic_word_dict:
                topic_word_dict[topic_name] = dict()
                topic_word_dict[topic_name]['TOTAL_WORDS'] = 0

            for word in words:
                if word not in topic_word_dict[topic_name]:
                    topic_word_dict[topic_name][word] = 0
                topic_word_dict[topic_name][word] += doc_dict[doc_name]['WORDS'][word]

            topic_word_dict[topic_name]['TOTAL_WORDS'] += total_words

    # for topic_name in topic_word_dict:
    #     for word in topic_word_dict[topic_name]:
    #         topic_word_dict[topic_name][word] = float(topic_word_dict [
    # topic_name][word])/topic_word_dict[topic_name]['TOTAL_WORDS']
    #     del topic_word_dict[topic_name]['TOTAL_WORDS']

    return topic_word_dict


# def build_topic_word_dict_from_dir(dataset_dir):
#     topic_word_dict = dict()
#
#     for dir_name in os.listdir(dataset_dir):
#         current_dir_path = os.path.join(dataset_dir, dir_name)
#         topic_name = dir_name
#         # total_words_in_topic = 0
#         # doc_word_count_dict = dict()
#
#         if topic_name not in topic_word_dict:
#             topic_word_dict[topic_name] = dict()
#
#         if os.path.isdir(current_dir_path):
#             for filename in os.listdir(current_dir_path):
#                 file_path = os.path.join(current_dir_path, filename)
#                 file_fd = open(file_path, 'r')
#                 # words = preprocess_data(file_path)
#                 words = file_fd.read(-1).split()
#
#                 for word in words:
#                     # print(doc_dict[doc_name])
#                     if word not in topic_word_dict[topic_name]:
#                         topic_word_dict[topic_name][word] = 0
#                     topic_word_dict[topic_name][word] += 1
#                     # total_words_in_topic += 1
#     return topic_word_dict


# return { 'Topic1': prob1, 'Topic2': prob2 }
def calculate_prob_doc(doc_dict_name, topic_doc_dict, topic_word_dict):
    prob_topic_dict = dict()
    total = sum([topic_doc_dict[i] for i in topic_doc_dict])
    for topic in topic_word_dict:
        if topic not in prob_topic_dict:
            prob_topic_dict[topic] = 0
        prob_topic_dict[topic] += math.log(float(topic_doc_dict[
                                                 topic]) / total)
        for word in doc_dict_name['WORDS']:
            if word in topic_word_dict[topic]:
                prob_topic_dict[topic] += math.log((topic_word_dict[topic][word] + 1.0) / (
                topic_word_dict[topic]['TOTAL_WORDS'] + len(topic_word_dict[topic])))
            else:
                prob_topic_dict[topic] += math.log(
                    1.0 / (topic_word_dict[topic]['TOTAL_WORDS'] + len(topic_word_dict[topic])))
    return prob_topic_dict


def retrain(doc_dict, topic_word_dict, topic_doc_dict):
    for doc_name in doc_dict:
        if not doc_dict[doc_name]['LABELLED']:
            doc_dict[doc_name]['TOPICS'] = calculate_prob_doc(doc_dict[doc_name], topic_doc_dict, topic_word_dict)

            topic_prob_list = sorted(doc_dict[doc_name]['TOPICS'].items(), key=operator.itemgetter(1), reverse=True)
            max_topic_name = topic_prob_list[0][0]
            topic_doc_dict[max_topic_name] += 1

            for word in doc_dict[doc_name]['WORDS']:
                if word not in topic_word_dict[max_topic_name]:
                    topic_word_dict[max_topic_name][word] = 0
                topic_word_dict[max_topic_name][word] += doc_dict[doc_name]['WORDS'][word]
            topic_word_dict[max_topic_name]['TOTAL_WORDS'] += doc_dict[doc_name]['TOTAL_WORDS']
    return doc_dict, topic_word_dict, topic_doc_dict


def label_docs(doc_dict, topic_word_dict, topic_doc_dict):

    final_result = []
    total = sum([topic_doc_dict[i] for i in topic_doc_dict])
    for doc_name in doc_dict:
        prob_topic_dict = dict()
        for topic in topic_word_dict:
            if topic not in prob_topic_dict:
                prob_topic_dict[topic] = 0
            prob_topic_dict[topic] += math.log(float(topic_doc_dict[
                                                         topic])/ total)
            for word in doc_dict[doc_name]['WORDS']:
                if word in topic_word_dict[topic]:
                    prob_topic_dict[topic] += math.log((topic_word_dict[topic][word]+1.0)/(topic_word_dict[topic]['TOTAL_WORDS']+len(topic_word_dict[topic])))
                else:
                    prob_topic_dict[topic] += math.log(1.0/(topic_word_dict[topic]['TOTAL_WORDS']+len(topic_word_dict[topic])))
        sorted_topics = sorted(prob_topic_dict.items(), key=operator.itemgetter(1), reverse=True)
        final_result.append((doc_name.split("_")[0], sorted_topics[0][0]))
    return final_result


def main():

    mode = sys.argv[1]
    dataset_dir = sys.argv[2]
    model_file = sys.argv[3]
    fraction = float(sys.argv[4])
    distinctive_words_file = "distinctive_words.txt"
    doc_dict = dict()
    retrain_times = 5

    if mode == "train":
        doc_dict, topic_doc_dict = load_train_data(dataset_dir, fraction)
        topic_word_dict = preprocess_topic_word(doc_dict)
        # topic_word_dict = build_topic_word_dict_from_dir(dataset_dir)

        if 0.0 < fraction < 1.0:
            for retrain_number in range(0, retrain_times):
                print("Hi !!!")
                doc_dict, topic_word_dict, topic_doc_dict = retrain(doc_dict, topic_word_dict, topic_doc_dict)

        dis_fd = open(distinctive_words_file, 'w')
        for topic in topic_word_dict:
            words_topic = topic_word_dict[topic]
            dis_word_string = topic+":"
            sorted_words = sorted(words_topic.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_words)
            for word_tuple in sorted_words[0:11]:
                if word_tuple[0] != 'TOTAL_WORDS':
                    dis_word_string += word_tuple[0]+","
            dis_word_string = dis_word_string[:-1]
            print(dis_word_string)
            dis_word_string += "\n"
            dis_fd.write(dis_word_string)
        dis_fd.close()

        # Store the model
        with open(model_file, 'w') as f:
            pickle.dump((topic_word_dict, topic_doc_dict), f,
                        pickle.HIGHEST_PROTOCOL)

    elif mode == "test":
        with open(model_file, 'r') as f:
            topic_word_dict, topic_doc_dict = pickle.load(f)

        doc_dict, test_word_dict = load_train_data(dataset_dir, 1.0)
        out_data = label_docs(doc_dict, topic_word_dict, topic_doc_dict)
        display_accuracy(accuracy(out_data))
    else:
        print("Invalid Mode")


if __name__ == '__main__':
    main()
