import glob
import preprocess
import pickle
import math




def compute_spam_prob(x,binary_dict,doc_count):
    final_prob = 0
    for i in x:
        if i in binary_dict.columns:
            temp = binary_dict.iloc[1][i]
            if temp != 0:
                pos_prob = math.log(float(temp) / doc_count[1])
                final_prob += pos_prob
    return final_prob


def compute_notspam_prob(x,binary_dict,doc_count):
    final_prob = 0
    for i in x:
        if i in binary_dict.columns:
            temp = binary_dict.iloc[0][i]
            if temp != 0:
                pos_prob = math.log(float(temp) / doc_count[0])
                final_prob += pos_prob
    return final_prob


def compute_confmatrix(tagged_docs):
    TP, TN, FP, FN = 0, 0, 0, 0
    for i in tagged_docs:
        if i[0] == 1 and i[1] == 1:
            TP += 1
        if i[0] == 1 and i[1] == 0:
            FN += 1
        if i[0] == 0 and i[1] == 0:
            TN += 1
        if i[0] == 0 and i[1] == 1:
            FP += 1
    confmatrix = [[TN, FP], [FN, TP]]
    return confmatrix

def NBbinary_main(datapath,picklepath):
    with open('pickledata/binary_dict10k_sf1.pickle') as f:
        binary_dict1 = pickle.load(f)

    binary_dict = binary_dict1.transpose()


    with open('pickledata/doc_count.pickle') as g:
        doc_count = pickle.load(g)

    tagged_docs = []
    spam_prior_prob = math.log(float(doc_count[1]) / (doc_count[0] + doc_count[1]))
    notspam_prior_prob = math.log(float(doc_count[0]) / (doc_count[0] + doc_count[1]))
    word_list = []
    tagged_docs_spam = {}
    tagged_docs_notspam = {}
    file_list = glob.glob(datapath + "/spam/*.*")

    for i in file_list:
        sprob =0
        ntsprob = 0
        spam_prob = 0
        notspam_prob =0
        x = preprocess.preprocess_data(i)
        spam_prob = compute_spam_prob(x,binary_dict,doc_count)
        spam_prob += spam_prior_prob
        notspam_prob = compute_notspam_prob(x,binary_dict,doc_count)
        notspam_prob += notspam_prior_prob
        sprob = float(spam_prob) / (spam_prob + notspam_prob)
        ntsprob = float(notspam_prob) / (spam_prob + notspam_prob)

        if sprob > ntsprob:
            tag = 0
        else:
            tag = 1

        tagged_docs.append([1, tag])



    file_list[:] =[]
    file_list = glob.glob(datapath + "/notspam/*.*")

    for i in file_list:
        x = preprocess.preprocess_data(i)
        spam_prob = compute_spam_prob(x,binary_dict,doc_count)
        spam_prob += spam_prior_prob

        notspam_prob = compute_notspam_prob(x,binary_dict,doc_count)
        notspam_prob += notspam_prior_prob

        sprob = float(spam_prob) / (spam_prob + notspam_prob)
        ntsprob = float(notspam_prob) / (spam_prob + notspam_prob)
        if sprob > ntsprob:
            tag = 0
        else:
            tag = 1
        tagged_docs.append([0, tag])


    # print tagged_docs

    conf_matrix = compute_confmatrix(tagged_docs)
    print "Bayes Binary ------------------------------------------------------"
    print "Confusion Matrix - [TN,FP],[FN,TP]"
    for i in conf_matrix:
        print i

    accuracy = float(conf_matrix[0][0] + conf_matrix[1][1]) / (conf_matrix[0][0] + conf_matrix[0][1] + conf_matrix[1][0] + conf_matrix[1][1])
    print "Accuracy", accuracy
    print "-------------------------------------------------------------------"
    # print "/n"


# if __name__ == "__main__":
#     NBbinary_main("part1/test", "pickle")