import sys
import classifyNB_continous
import classifyNB_binary
import binaryDT
import loadData_binary
import loadData_continous
import DT_continous_data
import DT_binary_data
import NB_word_prob


if __name__ == "__main__":
    # Get the mode - train or test
    mode = sys.argv[1];
    # mode = "test"
    # Get the technique - bayes or decision tree
    technique = sys.argv[2];
    # technique = "DT"
    # Get the datapath - test and train
    datapath = sys.argv[3];
    # datapath = "part1/test"
    # Get the model
    model = sys.argv[4];
    # model = "model"
    # Store all the pickle in this directory
    picklepath = 'pickledata/'
    if mode == "train":
        if technique == "bayes":
            loadData_continous.loadData_main(datapath,picklepath)
            loadData_binary.loadData_binary_main(datapath,picklepath)
            NB_word_prob.NB_word_main()
        else:
            DT_continous_data.DT_continous_main(datapath,mode)
            DT_binary_data.DT_binary_main(datapath,mode)
            #Print tree in the train mode but takes time to compute.
            # binaryDT.print_tree_new_(5, 1, "binary")
            # binaryDT.print_tree_new_(5, 1, "continous")



    elif mode == "test":
        if technique == "bayes":
            classifyNB_continous.NBcontinous_main(datapath,picklepath)
            classifyNB_binary.NBbinary_main(datapath,picklepath)

        else:
            # creates test data
            DT_continous_data.DT_continous_main(datapath, mode)
            DT_binary_data.DT_binary_main(datapath, mode)

            #creates tree to classify test data
            binaryDT.learn_bagged_binary(5, 1, picklepath,"binary")
            binaryDT.learn_bagged_continous(5, 1, picklepath,"DT")

