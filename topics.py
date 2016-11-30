import sys
import os
import pickle
import operator

mode = sys.argv[1]
dataset_dir = sys.argv[2]
model_file = sys.argv[3]
fraction = float(sys.argv[4])
distinctive_words_file = "distinctive words.txt"

print("-----")
topic_word_dict = {}

for dirname in os.listdir(dataset_dir):
    # print(dirname)
    current_dir_path = os.path.join(dataset_dir, dirname)
    topic = dirname
    total_words_in_topic = 0
    if topic not in topic_word_dict:
        topic_word_dict[topic] = dict()

    if os.path.isdir(os.path.join(dataset_dir, dirname)):
        for filename in os.listdir(os.path.join(dataset_dir, dirname)):
            file_path = os.path.join(current_dir_path, filename)
            # print filename
            file_fd = open(file_path, 'r')
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
    print(dis_word_string)
    dis_fd.write(dis_word_string)
dis_fd.close()
#Store the model
# with open(model_file, 'wb') as f:
#     pickle.dump(topic_word_dict, f, pickle.HIGHEST_PROTOCOL)
#
# with open(model_file, 'rb') as f:
#     new_word_dict = pickle.load(f)

print topic_word_dict['guns']['encryption']
print len(topic_word_dict['guns'])
# print new_word_dict['guns']['encryption']
# print topic_word_dict['crypto']['encryption']



x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_x)