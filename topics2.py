import sys
import os
import pickle
import operator
import re
import math


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
    total_words_topic = dict()
    for dir_name in os.listdir(dataset_dir):
        current_dir_path = os.path.join(dataset_dir, dir_name)
        topic_name = dir_name
        if os.path.isdir(current_dir_path):
            for filename in os.listdir(current_dir_path):
                file_path = os.path.join(current_dir_path, filename)
                file_fd = open(file_path, 'r')
                # words = preprocess_data(file_path)
                words = file_fd.read(-1).split()
                doc_name = dir_name + "_" + filename
                if doc_name not in doc_dict:
                    doc_dict[doc_name] = init_doc_dict()
                else:
                    print("DOC exists"+doc_name)
                if topic_name not in total_words_topic:
                    total_words_topic[topic_name] = 0
                total_words_topic[topic_name] += len(words)
                for word in words:
                    # print(doc_dict[doc_name])
                    if word not in doc_dict[doc_name]['WORDS']:
                        doc_dict[doc_name]['WORDS'][word] = 0
                    doc_dict[doc_name]['WORDS'][word] += 1
                    doc_dict[doc_name]['TOTAL_WORDS'] += 1

                    # Check if this can be labelled
                    # cur_num = random.randint(1, 10)
                    # if cur_num <= fraction * 10:
                    #     doc_dict[doc_name]['TOPICS'][topic_name] = 1.0
                    #     doc_dict[doc_name]['LABELLED'] = True
                    #     doc_dict[doc_name]['LABEL'] = topic_name
    return doc_dict, total_words_topic


def preprocess_topic_word(doc_dict):
    topic_word_dict = dict()

    for doc_name in doc_dict:
        topic_name = doc_name.split("_")[0]
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


def build_topic_word_dict_from_dir(dataset_dir):
    topic_word_dict = dict()

    for dir_name in os.listdir(dataset_dir):
        current_dir_path = os.path.join(dataset_dir, dir_name)
        topic_name = dir_name
        # total_words_in_topic = 0
        # doc_word_count_dict = dict()

        if topic_name not in topic_word_dict:
            topic_word_dict[topic_name] = dict()

        if os.path.isdir(current_dir_path):
            for filename in os.listdir(current_dir_path):
                file_path = os.path.join(current_dir_path, filename)
                file_fd = open(file_path, 'r')
                # words = preprocess_data(file_path)
                words = file_fd.read(-1).split()

                for word in words:
                    # print(doc_dict[doc_name])
                    if word not in topic_word_dict[topic_name]:
                        topic_word_dict[topic_name][word] = 0
                    topic_word_dict[topic_name][word] += 1
                    # total_words_in_topic += 1
    return topic_word_dict


def retrain(doc_dict):
    topic_word_dict = preprocess_topic_word()
    total_log = ""
    for doc_name in doc_dict:

        if not doc_dict[doc_name]['LABELLED']:
            topic_sel = dict()
            for topic in topic_word_dict:

                if topic not in topic_sel:
                    topic_sel[topic] = 0
                for word in doc_dict[doc_name]:
                    topic_sel[topic] += math.log(topic_word_dict[topic][word])
                if topic in doc_dict[doc_name]['TOPICS']:
                    topic_sel[topic] += math.log(doc_dict[doc_name]['TOPICS'][topic])


def label_docs(doc_dict, topic_word_dict, total_words_topic):

    final_result = []
    total = sum([total_words_topic[i] for i in total_words_topic])
    for doc_name in doc_dict:
        prob_topic_dict = dict()
        for topic in topic_word_dict:
            if topic not in prob_topic_dict:
                prob_topic_dict[topic] = 0
            prob_topic_dict[topic] += math.log(float(total_words_topic[
                                                         topic])/ total)
            for word in doc_dict[doc_name]['WORDS']:
                if word in topic_word_dict[topic]:
                    prob_topic_dict[topic] += math.log((topic_word_dict[topic][word]+1.0)/(topic_word_dict[topic]['TOTAL_WORDS']+len(topic_word_dict[topic])))
                else:
                    prob_topic_dict[topic] += math.log(1.0/(topic_word_dict[topic]['TOTAL_WORDS']+len(topic_word_dict[topic])))
                    # prob_topic_dict[topic] += topic_word_dict[topic][word]
                    # prob_topic_dict[topic] += math.log((float(doc_dict[doc_name]['WORDS'][word])/doc_dict[doc_name]['TOTAL_WORDS'])*topic_word_dict[topic][word])
                # else:
                #     prob_topic_dict[topic] += math.log((float(doc_dict[doc_name]['WORDS'][word])/doc_dict[doc_name]['TOTAL_WORDS'])*float(random.randint(1,10))/1.0)

        sorted_topics = sorted(prob_topic_dict.items(), key=operator.itemgetter(1), reverse=True)
        final_result.append((doc_name.split("_")[0], sorted_topics[0][0]))
    return final_result


def main():

    mode = sys.argv[1]
    dataset_dir = sys.argv[2]
    model_file = sys.argv[3]
    fraction = float(sys.argv[4])
    distinctive_words_file = "distinctive words.txt"
    doc_dict = dict()
    retrain_times = 10
    out_data = []
    print("-----")

    if mode == "train":
        doc_dict, total_words_topic = load_train_data(dataset_dir, fraction)
        topic_word_dict = preprocess_topic_word(doc_dict)
        # topic_word_dict = build_topic_word_dict_from_dir(dataset_dir)

        # if 0.0 < fraction < 1.0:
        #     for retrain_number in range(0, retrain_times):
        #         retrain(doc_dict)


            # Process probability
            # for word in topic_word_dict[topic]:
            #     topic_word_dict[topic][word] = float(topic_word_dict[topic][word])/total_words_in_topic

            # Probability based on number of documents had a word to number of documents in the topic
            #     total_documents = len(os.listdir(current_dir_path))
            #     for word in doc_word_count_dict:
            #         topic_word_dict[topic][word] = float(len(doc_word_count_dict[word]))/total_documents


        #
        # dis_fd = open(distinctive_words_file, 'w')
        # for topic in topic_word_dict:
        #     words_topic = topic_word_dict[topic]
        #     dis_word_string = topic
        #     sorted_words = sorted(words_topic.items(), key=operator.itemgetter(1), reverse=True)
        #     # print(sorted_words)
        #     for word_tuple in sorted_words[0:10]:
        #         dis_word_string += ":"+word_tuple[0]
        #     dis_word_string += "\n"
        #     print(dis_word_string)
        #     dis_fd.write(dis_word_string)
        # dis_fd.close()

        # Store the model
        with open(model_file, 'wb') as f:
            pickle.dump((topic_word_dict, total_words_topic), f,
                        pickle.HIGHEST_PROTOCOL)

    elif mode == "test":

        with open(model_file, 'rb') as f:
            topic_word_dict, total_words_topic = pickle.load(f)

        # total_words = 0
        # for topic in topic_word_dict:
        #     for word in topic_word_dict[topic]:
        #         total_words += topic_word_dict[topic][word]
        # print("total_words:" + str(total_words))

        doc_dict, test_word_dict = load_train_data(dataset_dir, fraction)
        out_data = label_docs(doc_dict, topic_word_dict, total_words_topic)
        # print out_data
        display_accuracy(accuracy(out_data))
        # print(out_data)



        # Read the model


        # for dirname in os.listdir(dataset_dir):
        #     current_dir_path = os.path.join(dataset_dir, dirname)
        #
        #     if os.path.isdir(current_dir_path):
        #         for filename in os.listdir(current_dir_path):
        #             total_for_topic_dict = dict()
        #             file_path = os.path.join(current_dir_path, filename)
        #             # print filename
        #             file_fd = open(file_path, 'r')
        #             # words = preprocess_data(file_path)
        #             words = file_fd.read(-1).split()
        #             for word in words:
        #                 for topic in topic_word_dict:
        #                     if word in topic_word_dict[topic]:
        #                         if topic not in total_for_topic_dict:
        #                             total_for_topic_dict[topic] = 0
        #
        #                         total_for_topic_dict[topic] += math.log(topic_word_dict[topic][word])
        #             sorted_topics = sorted(total_for_topic_dict.items(), key=operator.itemgetter(1))
        #             print(file_path, sorted_topics[0])

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