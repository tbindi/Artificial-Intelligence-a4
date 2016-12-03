import sys
import os
import re
from pickle import load, dump, HIGHEST_PROTOCOL
import math
import operator


def display_accuracy(result, topics):
    print "v (Actual / Predicted) >"
    print "\t" + "\t".join(i[0:2] for i in topics)
    tn_tp = sum([result[j][j] for j in range(0, len(topics))])
    total = sum([sum(result[j]) for j in range(0, len(topics))])
    for i in topics:
        print i[0:2], "\t", "\t".join(str(i) for i in result[
            topics.index(i)]), "\t", sum(result[topics.index(i)])
    print " --- "
    print " Accuracy: ", tn_tp * 100.00 / total * 1.00


def accuracy(computed_list, topics):
    N = len(topics)
    confusion_matrix = [[0 for i in range(0, N)] for i in range(0, N)]
    for compute in computed_list:
        actual_value = compute[0]
        predic_value = compute[1]
        actual_index = topics.index(actual_value)
        predic_index = topics.index(predic_value)
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
        x = re.findall(r"(?:\s|^)([A-Za-z_\*\"\'-]+[,.!?/]+[A-Za-z_\*\"\'-]+)("
                       r"?=\s|$)", i.rstrip())
        for k in x:
            y.extend(re.split("[,.!?/]+", k))
        y = [''.join(e.lower() for e in j if e.isalnum()) for j in y]
        out_list.extend(y)
    out_list = [a for a in out_list if a not in stopWords]
    out_list = filter(None, out_list)
    return out_list


def calculate_norm(topic_word_dict, total_words_topic):
    topic_dict = dict()
    for word in topic_word_dict:
        if word not in topic_dict:
            topic_dict[word] = dict()
        for topic in topic_word_dict[word]:
            topic_dict[word][topic] = float(topic_word_dict[word][topic])/\
                                      total_words_topic[topic]
    return topic_dict


def load_train_data(dataset_dir, fraction):
    topics = dict()
    topic_word_dict = dict()
    dir_names = os.listdir(dataset_dir)
    total_words_topic = dict()
    total_files = 0
    total_uniq_words = dict()
    for dir_name in dir_names:
        curr_dir_path = os.path.join(dataset_dir, dir_name)
        topic_name = dir_name
        if topic_name not in topics:
            topics[topic_name] = 0
        if topic_name not in total_uniq_words:
            total_uniq_words[topic_name] = 0
        if topic_name not in total_words_topic:
            total_words_topic[topic_name] = 0

        if os.path.isdir(curr_dir_path):
            files = os.listdir(curr_dir_path)
            total_files += len(files)
            topics[topic_name] = len(files)
            keys = len(topic_word_dict.keys())
            for filename in files:
                file_path = os.path.join(curr_dir_path, filename)
                process_words = preprocess_data(file_path)
                total_words_topic[topic_name] += len(process_words)
                for word in process_words:
                    if word not in topic_word_dict:
                        topic_word_dict[word] = dict()
                        topic_word_dict[word][topic_name] = 1
                    else:
                        if topic_name not in topic_word_dict[word]:
                            topic_word_dict[word][topic_name] = 1
                        topic_word_dict[word][topic_name] += 1
            total_uniq_words[topic_name] = len(topic_word_dict.keys()) - keys
    for topic_name in topics:
        topics[topic_name] = float(topics[topic_name])/total_files
    return topic_word_dict, topics, total_words_topic, total_uniq_words


def predict_topic(words, topic_word_dict, topics_prob, total_words_topic,
                  total_uniq_words):
    topics = topics_prob.keys()
    prob_calc = dict()
    for topic in topics:
        if topics_prob[topic] == 0.0:
            continue
        prob_calc[topic] = math.log(float(topics_prob[topic]))
        for word in words:
            if word in topic_word_dict and topic in topic_word_dict[word]:
                prob_calc[topic] += (math.log(topic_word_dict[word][topic] +
                                             1.0) / (total_words_topic[topic]
                                                     + total_uniq_words[topic]))
            else:
                prob_calc[topic] += (math.log(1.0/(total_words_topic[topic]
                                                     + total_uniq_words[
                                                       topic])))
    sorted_topics = sorted(prob_calc.items(), key=operator.itemgetter(1),
                           reverse=True)
    return sorted_topics[0][0]


def load_test_data(dataset_dir, fraction, topic_word_dict,
                                  topics_prob, total_words_topic,
                   total_uniq_words):
    doc_dict = dict()
    dir_names = os.listdir(dataset_dir)
    final_result = []
    for dir_name in dir_names:
        curr_dir_path = os.path.join(dataset_dir, dir_name)
        topic_name = dir_name

        if os.path.isdir(curr_dir_path):
            files = os.listdir(curr_dir_path)
            for filename in files:
                file_path = os.path.join(curr_dir_path, filename)
                words = preprocess_data(file_path)
                predicted = predict_topic(words, topic_word_dict,
                                          topics_prob, total_words_topic, total_uniq_words)
                final_result.append([topic_name, predicted])
    return final_result


def main():
    mode = sys.argv[1]
    dataset_dir = sys.argv[2]
    model_file = sys.argv[3]
    fraction = float(sys.argv[4])
    print("-- Started --")
    if mode == "train":
        topic_word_dict, topics, total_words_topic, total_uniq_words = \
            load_train_data(dataset_dir, fraction)
        topic_word_ = calculate_norm(topic_word_dict, total_words_topic)
        with open(model_file, 'wb') as f:
            dump((topic_word_, topics, total_words_topic, total_uniq_words), f,
                 HIGHEST_PROTOCOL)

    elif mode == "test":
        with open(model_file, 'rb') as f:
            (topic_word_dict, topics_prob, total_words_topic,
             total_uniq_words) = load(f)
        final_result = load_test_data(dataset_dir, fraction, topic_word_dict,
                                  topics_prob, total_words_topic, total_uniq_words)
        topics = total_words_topic.keys()
        display_accuracy(accuracy(final_result, topics), topics)


if __name__ == "__main__":
    main()

