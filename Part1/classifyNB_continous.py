import preprocess
import glob
import pickle
import math



# with open('main_spam_word_list.pickle') as f:  # Python 3: open(..., 'rb')
#     main_spam_word_list = pickle.load(f)
#
# main_spam_word_list = {k: v for k, v in main_spam_word_list.iteritems() if v > 35}





def compute_spam_prob(x,word_dict):
    final_prob = 0
    total_spam_words_count = sum(word_dict.values()[0])

    for i in x:
        temp = word_dict.get(i)

        if temp is not None:
            pos_prob = math.log(float(temp[0])/total_spam_words_count)
            final_prob += pos_prob

    return final_prob

def compute_notspam_prob(x,word_dict):

    final_prob = 0
    total_notspam_words_count = sum(word_dict.values()[1])

    for i in x:
        temp = word_dict.get(i)
        if temp is not None:
            pos_prob = math.log(float(temp[1])/total_notspam_words_count)
            final_prob += pos_prob

    return final_prob


def compute_confmatrix(tagged_docs):
    TP,TN,FP,FN = 0,0,0,0
    for i in tagged_docs:
        if i[0]==1 and i[1] ==1:
            TP += 1
        if i[0]==1 and i[1] ==0:
            FN += 1
        if i[0]==0 and i[1] ==0:
            TN += 1
        if i[0]==0 and i[1] ==1:
            FP += 1
    confmatrix = [[TN,FP],[FN,TP]]
    return confmatrix

def NBcontinous_main(datapath,picklepath):
    with open('pickledata/doc_count.pickle') as f:  # Python 3: open(..., 'rb')
        doc_count = pickle.load(f)

    with open('pickledata/word_spam_notspam_count_dict.pickle') as f:  # Python 3: open(..., 'rb')
        word_dict = pickle.load(f)

    tagged_docs = []
    spam_prior_prob = math.log(float(doc_count[1]) / (doc_count[0] + doc_count[1]))
    notspam_prior_prob = math.log(float(doc_count[0]) / (doc_count[0] + doc_count[1]))
    word_list = []
    tagged_docs_spam = {}
    tagged_docs_notspam = {}
    file_list = glob.glob(datapath + "/spam/*.*")
    j = 0
    for i in file_list:
        # temp,doc_name = tuple(i.split('\\'))
        x = preprocess.preprocess_data(i)
        spam_prob = compute_spam_prob(x,word_dict)
        spam_prob += spam_prior_prob

        notspam_prob = compute_notspam_prob(x,word_dict)
        notspam_prob += notspam_prior_prob

        sprob = float(spam_prob)/(spam_prob+notspam_prob)
        ntsprob = float(notspam_prob)/(spam_prob+notspam_prob)
        if sprob > ntsprob:
            tag = 1
        else : tag = 0

        tagged_docs.append([1,tag])


    #
    file_list = glob.glob(datapath + "/notspam/*.*")
    j = 0
    for i in file_list:
        # temp,doc_name = tuple(i.split('\\'))
        x = preprocess.preprocess_data(i)
        spam_prob = compute_spam_prob(x,word_dict)
        spam_prob += spam_prior_prob

        notspam_prob = compute_notspam_prob(x,word_dict)
        notspam_prob += notspam_prior_prob

        sprob = float(spam_prob)/(spam_prob+notspam_prob)
        ntsprob = float(notspam_prob)/(spam_prob+notspam_prob)

        if sprob > ntsprob:
            tag = 1
        else : tag = 0

        tagged_docs.append([0, tag])



    conf_matrix = compute_confmatrix(tagged_docs)
    print "Bayes Continous ---------------------------------------------------"
    print "Confusion Matrix - [TN,FP],[FN,TP]"
    for i in conf_matrix:
        print i

    accuracy = float(conf_matrix[0][0] + conf_matrix[1][1])/ (conf_matrix[0][0] + conf_matrix[0][1] + conf_matrix[1][0] + conf_matrix[1][1])
    print "Accuracy",accuracy
    print "-------------------------------------------------------------------"
    # print "/n"