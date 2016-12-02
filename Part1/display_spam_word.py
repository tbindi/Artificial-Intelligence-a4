import pickle

# def display_spam_main():
with open('pickledata/main_spam_word_list.pickle') as g:
    main_word_list = pickle.load(g)

sorted_main_word_list = sorted(sorted(main_word_list), key=main_word_list.get, reverse=True)
top10_word = sorted_main_word_list[:10]
bottom10_word = sorted_main_word_list[-10:]

# print main_word_list
print top10_word
print bottom10_word