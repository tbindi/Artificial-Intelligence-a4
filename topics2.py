import sys
import os
import pickle
import operator
import re
from string import digits
import math


temp = []


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
        # y = list(set(y))
        y = [''.join(e.lower() for e in j if e.isalnum()) for j in y]
        y = filter(None, y)
        y = [a for a in y if a not in stopWords]
        out_list.extend(y)
    return out_list


def main():

    mode = sys.argv[1]
    dataset_dir = sys.argv[2]
    model_file = sys.argv[3]
    fraction = float(sys.argv[4])
    distinctive_words_file = "distinctive words.txt"

    print("-----")
    topic_word_dict = {}

    if mode == "train":

        for dir_name in os.listdir(dataset_dir):
            current_dir_path = os.path.join(dataset_dir, dir_name)
            topic = dir_name
            total_words_in_topic = 0
            doc_word_count_dict = dict()
            if topic not in topic_word_dict:
                topic_word_dict[topic] = dict()

            if os.path.isdir(current_dir_path):
                for filename in os.listdir(current_dir_path):
                    file_path = os.path.join(current_dir_path, filename)
                    file_fd = open(file_path, 'r')
                    words = preprocess_data(file_path)
                    # words = file_fd.read(-1).split()
                    for word in words:
                        total_words_in_topic += 1
                        # if word not in topic_word_dict[topic]:
                        #     topic_word_dict[topic][word] = 1
                        if word not in doc_word_count_dict:
                            doc_word_count_dict[word] = dict()
                        doc_name = dir_name+"_"+filename
                        if doc_name not in doc_word_count_dict[word]:
                            doc_word_count_dict[word][doc_name] = 1
                        # topic_word_dict[topic][word] += 1

            # Process probability
            # for word in topic_word_dict[topic]:
            #     topic_word_dict[topic][word] = float(topic_word_dict[topic][word])/total_words_in_topic

            # Probability based on number of documents had a word to number of documents in the topic
                total_documents = len(os.listdir(current_dir_path))
                for word in doc_word_count_dict:
                    topic_word_dict[topic][word] = float(len(doc_word_count_dict[word]))/total_documents

        dis_fd = open(distinctive_words_file, 'w')
        for topic in topic_word_dict:
            words_topic = topic_word_dict[topic]
            dis_word_string = topic
            sorted_words = sorted(words_topic.items(), key=operator.itemgetter(1), reverse=True)
            # print(sorted_words)
            for word_tuple in sorted_words[0:10]:
                dis_word_string += ":"+word_tuple[0]
            dis_word_string += "\n"
            print(dis_word_string)
            dis_fd.write(dis_word_string)
        dis_fd.close()

        # Store the model
        with open(model_file, 'wb') as f:
            pickle.dump(topic_word_dict, f, pickle.HIGHEST_PROTOCOL)

    elif mode == "test":
        # Read the model
        with open(model_file, 'rb') as f:
            topic_word_dict = pickle.load(f)

        for dirname in os.listdir(dataset_dir):
            current_dir_path = os.path.join(dataset_dir, dirname)

            if os.path.isdir(current_dir_path):
                for filename in os.listdir(current_dir_path):
                    total_for_topic_dict = dict()
                    file_path = os.path.join(current_dir_path, filename)
                    # print filename
                    file_fd = open(file_path, 'r')
                    words = preprocess_data(file_path)
                    # words = file_fd.read(-1).split()
                    for word in words:
                        for topic in topic_word_dict:
                            if word in topic_word_dict[topic]:
                                if topic not in total_for_topic_dict:
                                    total_for_topic_dict[topic] = 0

                                total_for_topic_dict[topic] += math.log(topic_word_dict[topic][word])
                    sorted_topics = sorted(total_for_topic_dict.items(),
                                           key=operator.itemgetter(1))
                    print(file_path, sorted_topics[0])

    else:
        print("Invalid Mode")
if __name__ == '__main__':
    main()

# print topic_word_dict['guns']['encryption']
# print len(topic_word_dict['guns'])
# print new_word_dict['guns']['encryption']
# print topic_word_dict['crypto']['encryption']





# x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
# sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
# print(sorted_x)