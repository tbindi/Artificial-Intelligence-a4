import glob
import preprocess
from collections import defaultdict
import cPickle as pickle
import pandas as pd
binary_dict = defaultdict()
binary_spamdict = defaultdict()
binary_notspamdict = defaultdict()


# def insert_dict(x,doc_name,tag):
#     if doc_name not in binary_dict:
#         binary_dict[doc_name] = {}
#         binary_dict[doc_name]["#class_label"] = tag
#     for i in sorted_main_word_list_reduced:
#         if i not in binary_dict[doc_name]:
#             binary_dict[doc_name][i] = 0
#         if i in x:
#             binary_dict[doc_name][i] += 1


def insert_dict(x,doc_name,tag,sorted_main_word_list_reduced):
    if doc_name not in binary_dict:
        binary_dict[doc_name]={}
        binary_dict[doc_name]["#class_label"] = tag
        for i in sorted_main_word_list_reduced:
            binary_dict[doc_name][i] = 0

    for i in x:
        if binary_dict[doc_name].get(i) is not None:
            binary_dict[doc_name][i] += 1



def DT_continous_main(datapath,tag):

    with open('pickledata/main_word_list.pickle') as f:  # Python 3: open(..., 'rb')
        main_word_list = pickle.load(f)


    sorted_main_word_list = sorted(sorted(main_word_list), key=main_word_list.get, reverse=True)
    sorted_main_word_list_reduced = sorted_main_word_list[:5000]


    file_list = []
    file_list =  glob.glob(datapath + "/spam/*.*")
    for i in file_list:
        doc_name1 = tuple(i.split('\\'))
        x = preprocess.preprocess_data(i)
        insert_dict(x,doc_name1[-1],1,sorted_main_word_list_reduced)


    file_list[:] = []
    file_list =  glob.glob(datapath + "/notspam/*.*")
    for j in file_list:
        doc_name2 = tuple(j.split('\\'))
        y = preprocess.preprocess_data(j)
        insert_dict(y, doc_name2[-1],0,sorted_main_word_list_reduced)


    data_dict = pd.DataFrame(binary_dict)
    data_dict1 = data_dict.transpose()

    if tag == "train":
        data_dict1.to_csv('pickledata/DT_continous_5k_train.csv')
    else:
        data_dict1.to_csv('pickledata/DT_continous_5k_test.csv')


