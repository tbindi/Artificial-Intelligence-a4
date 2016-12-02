import glob
import preprocess
import copy
from collections import Counter
import pickle
def loadData_main(datapath,picklepath):
    word_list = []
    spam_word_list = []
    notspam_word_list = []

    smooth_filter = 10e-6


    spam_count1,notspam_count1 = 0,0

    file_list =  glob.glob(datapath + "/spam/*.*")
    for i in file_list:
        spam_count1 += 1
        x = preprocess.preprocess_data(i)
        spam_word_list.append(x)
        word_list.append(x)

    file_list =  glob.glob(datapath + "/notspam/*.*")
    for j in file_list:
        notspam_count1 += 1
        y = preprocess.preprocess_data(j)
        word_list.append(y)
        notspam_word_list.append(y)


    word_list = [item for sublist in word_list for item in sublist]
    main_word_list = dict(Counter(word_list))

    spam_word_list = [item for sublist in spam_word_list for item in sublist]
    main_spam_word_list = dict(Counter(spam_word_list))

    notspam_word_list = [item for sublist in notspam_word_list for item in sublist]
    main_notspam_word_list = dict(Counter(notspam_word_list))

    sorted_main_word_list = sorted(sorted(main_word_list), key=main_word_list.get, reverse=True)
    sorted_main_word_list_reduced = sorted_main_word_list[:30000]

    # main_dict = { word : [spam_count,non_spamcount]}
    word_dict = {}
    for i in sorted_main_word_list_reduced:
        temp = 0
        spam_count2 = 0
        notspam_count2 = 0
        temp1 = 0
        temp = main_spam_word_list.get(i)
        if temp is None:
            spam_count2 = smooth_filter
        else:
            spam_count2 = temp + smooth_filter

        temp1 = main_notspam_word_list.get(i)
        if temp1 is None:
            notspam_count2 = smooth_filter
        else:
            notspam_count2 = temp1 + smooth_filter
        word_dict[i] = [spam_count2, notspam_count2]
    # print word_dict

    with open('pickledata/word_spam_notspam_count_dict.pickle', 'w') as a:  # Python 3: open(..., 'wb')
        pickle.dump(word_dict, a)

    with open('pickledata/doc_count.pickle', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([notspam_count1,spam_count1], f)

    with open('pickledata/main_word_list.pickle', 'w') as g:  # Python 3: open(..., 'wb')
        pickle.dump(main_word_list, g)

    with open('pickledata/main_spam_word_list.pickle', 'w') as h:  # Python 3: open(..., 'wb')
        pickle.dump(main_spam_word_list, h)

    with open('pickledata/main_notspam_word_list.pickle', 'w') as i:  # Python 3: open(..., 'wb')
        pickle.dump(main_notspam_word_list, i)