import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def file_to_array(file_name):
    array = []
    with open(file_name) as f:
        for line in f:
            for char in line:
                if char != "\n":
                    array.append(char)
    f.close
    return array


def calculate_accuracy(file_name1, file_name2):
    acc_count = 0
    array1 = file_to_array(file_name1)
    array2 = file_to_array(file_name2)
    for i in range(len(array1)):
        if array1[i] == array2[i]:
            acc_count += 1
    return float(acc_count)/len(array1)


def confusion_matrix(res_name, test_name): #order is inforced
    confusion_matrix = np.zeros((10,10))
    res_arr = file_to_array(res_name)
    test_arr = file_to_array(test_name)
    res_arr = [int(numeric_string) for numeric_string in res_arr]
    test_arr = [int(numeric_string) for numeric_string in test_arr]

    for i in range(10):
        number_of_class_i = 0
        for j in range(len(test_arr)):
            if test_arr[j] == i:
                number_of_class_i += 1
                confusion_matrix[i][res_arr[j]] += 1
        confusion_matrix[i] = (confusion_matrix[i]/number_of_class_i)*100
    return confusion_matrix

def highest_prototype(posteriori_matrix, test_name):
        highest_arr = []
        test_arr = file_to_array(test_name)
        test_arr = [int(numeric_string) for numeric_string in test_arr]

        for i in range(10):
            class_i_prob_arr = np.zeros((120,2))
            for k in range(len(class_i_prob_arr)):
                class_i_prob_arr[k][0] = -999

            class_i_idx = 0
            for j in range(len(test_arr)):
                if test_arr[j] == i:
                    class_i_prob_arr[class_i_idx][0] = posteriori_matrix[j][i]
                    class_i_prob_arr[class_i_idx][1] = j
                    class_i_idx += 1
            highest_idx = np.argmax(class_i_prob_arr[:, 0])
            highest_pair = class_i_prob_arr[highest_idx]
            highest_arr.append(highest_pair)
        return highest_arr


def lowest_prototype(posteriori_matrix, test_name):
        lowest_arr = []
        test_arr = file_to_array(test_name)
        test_arr = [int(numeric_string) for numeric_string in test_arr]

        for i in range(10):
            class_i_prob_arr = np.zeros((120,2))
            for k in range(len(class_i_prob_arr)):
                class_i_prob_arr[k][0] = 0

            class_i_idx = 0
            for j in range(len(test_arr)):
                if test_arr[j] == i:
                    class_i_prob_arr[class_i_idx][0] = posteriori_matrix[j][i]
                    class_i_prob_arr[class_i_idx][1] = j
                    class_i_idx += 1
            lowest_idx = np.argmin(class_i_prob_arr[:, 0])
            lowest_pair = class_i_prob_arr[lowest_idx]
            lowest_arr.append(lowest_pair)
        return lowest_arr



def save_fig(data, save_file_name):
    fig, ax = plt.subplots()
    cax = ax.imshow(data, interpolation='nearest', cmap=cm.coolwarm)
    ax.set_title(save_file_name)
    cbar = fig.colorbar(cax)
    plt.savefig(save_file_name)
    plt.close(fig)
    print 'finished save ' + save_file_name


def save_graphs(number_pair, training_results, occurence):
    first_number, second_number = number_pair
    first_number_file_name = str(first_number) + "_likely_hood.png" 
    second_number_file_name = str(second_number) +"_likely_hood.png"
    odds_ratio_name = str(first_number) + "_" + str(second_number)+ "_odds_ration.png" 
    visual_matrix_for_first_number = np.log((training_results[first_number, :, :, 1]+5) / (occurence[first_number] + 10))
    visual_matrix_for_second_number = np.log((training_results[second_number, :, :, 1]+5) / (occurence[second_number] + 10))
    first_number_result = (training_results[first_number, :, :, 1]+5) / (occurence[first_number] + 10)
    second_number_result = (training_results[second_number, :, :, 1]+5) / (occurence[second_number] + 10)
    visual_matrix_for_odds_ratio = np.log(first_number_result / second_number_result)
    save_fig(visual_matrix_for_first_number, first_number_file_name)
    save_fig(visual_matrix_for_second_number, second_number_file_name)
    save_fig(visual_matrix_for_odds_ratio, odds_ratio_name)
    print "finished saving"


np.set_printoptions(linewidth=200)
# print "Accuracy is : ", calculate_accuracy("result.txt", "testlabels.txt")*100.0, "%"
# print "Confusion matrix is : "
# print confusion_matrix("result.txt", "testlabels.txt")
