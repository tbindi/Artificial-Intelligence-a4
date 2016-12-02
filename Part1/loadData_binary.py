import glob
import preprocess
import copy
from collections import Counter
from collections import defaultdict
import cPickle as pickle
import pandas as pd

smooth_filter = 10e-6
binary_dict = defaultdict()
spam_word_prob_dict = {}
notspam_word_prob_dict = {}

def initialize_dict(i):
    binary_dict[i] = {}
    binary_dict[i][0] = smooth_filter  # notspam
    binary_dict[i][1] = smooth_filter  # spam


def insert_dict(x, doc_name, tag, sorted_main_word_list_reduced):
    for i in sorted_main_word_list_reduced:
        if i not in binary_dict:
            initialize_dict(i)
        if i in x:
            binary_dict[i][tag] += 1


def loadData_binary_main(datapath, pickldata):
    with open('pickledata/main_word_list.pickle') as g:
        main_word_list = pickle.load(g)
    # print main_word_list
    # raw_input()
    sorted_main_word_list = sorted(sorted(main_word_list), key=main_word_list.get, reverse=True)
    sorted_main_word_list_reduced = sorted_main_word_list[:50]

    # print sorted_main_word_list_reduced

    file_list = []
    file_list = glob.glob(datapath +"/spam/*.*")
    for i in file_list:
        doc_name1 = tuple(i.split('/'))
        x = preprocess.preprocess_data(i)
        insert_dict(x, doc_name1[-1], 1, sorted_main_word_list_reduced)

    # print binary_dict


    #
    #
    file_list = []
    file_list = glob.glob(datapath + "/notspam/*.*")
    # print len(file_list)

    for j in file_list:
        doc_name2 = tuple(j.split('/'))
        y = preprocess.preprocess_data(j)
        insert_dict(y, doc_name2[-1], 0, sorted_main_word_list_reduced)

    # print binary_dict
    data_dict = pd.DataFrame(binary_dict)
    data_dict1 = data_dict.transpose()

    # print data_dict1

    with open('pickledata/binary_dict50_sf.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump(data_dict1, f)

        # with open('binary_spamdict.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump(data_spam1, f)
        # f.close()
        #
        # with open('binary_notspamdict.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        #     pickle.dump(data_notspam1, f)
        # f.close()

        # print binary_dict