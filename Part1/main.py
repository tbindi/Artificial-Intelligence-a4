import sys
import classifyNB_continous
import classifyNB_binary
import binaryDT
import loadData_binary
import loadData_continous
import DT_continous_data
import DT_binary_data


if __name__ == "__main__":
    # Get the mode - train or test
    # mode = sys.argv[0];
    mode = "test"
    # Get the technique - bayes or decision tree
    # technique = sys.argv[1];
    technique = "DT"
    # Get the datapath - test and train
    # datapath = sys.argv[2];
    datapath = "part1/test"
    # Get the model
    # model = sys.argv[3];
    model = "model"
    # Store all the pickle in this directory
    picklepath = 'pickledata/'
    if mode == "train":
        if technique == "bayes":
            loadData_continous.loadData_main(datapath,picklepath) #working fine
            loadData_binary.loadData_binary_main(datapath,picklepath)
        else:
            DT_continous_data.DT_continous_main(datapath,mode)
            DT_binary_data.DT_binary_main(datapath,mode)
            # binaryDT.print_tree_new_(5, 1, "binary")
            # binaryDT.print_tree_new_(5, 1, "continous")



    elif mode == "test":
        if technique == "bayes":
            classifyNB_continous.NBcontinous_main(datapath,picklepath) #working fine
            classifyNB_binary.NBbinary_main(datapath,picklepath)

        else:
            #creates test data
            DT_continous_data.DT_continous_main(datapath, mode)
            DT_binary_data.DT_binary_main(datapath, mode)

            #creates tree to classify test data
            binaryDT.learn_bagged_binary(5, 1, picklepath)
            binaryDT.learn_bagged_continous(5, 1, picklepath)

