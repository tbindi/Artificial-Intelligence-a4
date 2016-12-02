import sys
import os
import pickle
import operator
import re
from string import digits
import math

temp = []
topics_list = ['religion', 'christian', 'mideast', 'pc', 'windows',
               'medical', 'space', 'crypto', 'xwindows', 'atheism',
               'autos', 'mac', 'baseball', 'hockey', 'graphics',
               'politics', 'electronics', 'forsale', 'guns', 'motorcycles']

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def preprocess_data(i):
    temp[:] = []
    f = open(i, 'r')
    x = f.read()
    # x = f.read()
    f.close()
    x = cleanhtml(x)
    x = x.split()


    for i in x:
        temp.append(re.findall(r"\b\w+\b",i))

    data = [item for sublist in temp for item in sublist]

    data = [word.lower() for word in data]

    # https://github.com/Alir3z4/stop-words/blob/master/english.txt
    g = open("english.txt",'r')
    stopWords = g.read().split('\n')
    data = ' '.join([word for word in data if word not in stopWords])

    char_Remove = "[!@#$).\_%^&*()#@|-](){}+\n:<>?;,='"
    char_Remove1 = '"'
    data =  data.translate(None, char_Remove)
    data =  data.translate(None, char_Remove1)
    data =  data.translate(None,digits)

    # Remove url links
    # data = re.sub(r'http\S+', '', data)

    data = data.split()
    data = data[1:]

    return data


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

def main():

    mode = sys.argv[1]
    dataset_dir = sys.argv[2]
    model_file = sys.argv[3]
    fraction = float(sys.argv[4])
    distinctive_words_file = "distinctive words.txt"
    final_result = []
    print("-----")
    topic_word_dict = {}

    if mode == "train":

        for dir_name in os.listdir(dataset_dir):
            current_dir_path = os.path.join(dataset_dir, dir_name)
            topic = dir_name
            total_words_in_topic = 0
            if topic not in topic_word_dict:
                topic_word_dict[topic] = dict()

            if os.path.isdir(current_dir_path):
                for filename in os.listdir(current_dir_path):
                    file_path = os.path.join(current_dir_path, filename)
                    file_fd = open(file_path, 'r')
                    # words = preprocess_data(file_path)
                    words = file_fd.read(-1).split()
                    for word in words:
                        total_words_in_topic += 1
                        if word not in topic_word_dict[topic]:
                            topic_word_dict[topic][word] = 0
                        topic_word_dict[topic][word] += 1

            # Process probability
            for word in topic_word_dict[topic]:
                topic_word_dict[topic][word] = float(topic_word_dict[topic][word])/total_words_in_topic


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

        total_words = 0
        for topic in topic_word_dict:
            total_words += len(topic_word_dict[topic])
        print("total_words:"+str(total_words))

        for dirname in os.listdir(dataset_dir):
            current_dir_path = os.path.join(dataset_dir, dirname)

            if os.path.isdir(current_dir_path):
                for filename in os.listdir(current_dir_path):
                    total_for_topic_dict = dict()
                    file_path = os.path.join(current_dir_path, filename)
                    # print filename
                    file_fd = open(file_path, 'r')
                    # words = preprocess_data(file_path)
                    words = file_fd.read(-1).split()
                    for word in words:
                        for topic in topic_word_dict:
                            if word in topic_word_dict[topic]:
                                if topic not in total_for_topic_dict:
                                    total_for_topic_dict[topic] = math.log(topic_word_dict[topic][word])
                                else:
                                    total_for_topic_dict[topic] += math.log(topic_word_dict[topic][word])
                    sorted_topics = sorted(total_for_topic_dict.items(), key=operator.itemgetter(1))
                    # print(file_path, sorted_topics[0])
                    final_result.append((dirname, sorted_topics[0][0]))
        display_accuracy(accuracy(final_result))
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