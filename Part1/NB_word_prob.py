import pickle

def NB_word_main():
    with open('pickledata/binary_dict5k_sf.pickle') as g:
        main_word_list = pickle.load(g)

    # print main_word_list
    # print type(main_word_list)

    temp = main_word_list.sort_values([1], ascending=[False])
    # print temp
    spam_words = list(temp.index)
    top10_words = spam_words[:10]
    least10_words = spam_words[-10:]

    print "Words most associated with spam :-"
    print ", ".join(str(e) for e in top10_words)
    print " "
    print "Words least associated with spam :-"
    print ", ".join(str(e) for e in least10_words)
