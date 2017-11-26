import numpy as np
import math
import Utility
import matplotlib.pyplot as plt
from matplotlib import cm

def read_file(label_file, images_file):
    label_array = []
    with open(label_file) as f:
        for line in f:
            label_array.append(int(line[0]))
    line_counter = 0
    occurence_array = np.zeros((10,28,28,2))
    with open(images_file) as f:
        for line in f:
            curr_num = label_array[line_counter // 28]
            char_counter = 0
            for char in line:
                if char == ' ':
                    occurence_array[curr_num][line_counter%28][char_counter][0]+=1
                elif char == '+' or char == '#':
                    occurence_array[curr_num][line_counter%28][char_counter][1]+=1
                char_counter+=1
            line_counter+=1
    # np.save("training_result.npy", )
    denominator_array = np.zeros(10)
    for i in label_array:
        denominator_array[i]+=1
    return occurence_array, denominator_array

def analyze_number(number_image, training_result, occurence, k, pos_idx):
    #print number_image
    occurence = np.array(occurence)
    p_class_array = occurence/5000
    probability_array = np.array([0,0,0,0,0,0,0,0,0,0])
    row_number = len(number_image)
    col_number = len(number_image[0])
    for i in range(10):
        for j in range(row_number):
            for h in range(col_number):
                if number_image[j][h] == ' ':
                    probability_array[i] += math.log((training_result[i, j, h, 0]+k)/(occurence[i]+2*k))
                elif number_image[j][h] == '+' or number_image[j][h] == '#':
                    probability_array[i] += math.log((training_result[i, j, h, 1]+k)/(occurence[i]+2*k))
        probability_array[i] += math.log(p_class_array[i])

    posteriori_matrix[pos_idx] = probability_array
    index = np.argmax(probability_array)
    test_results.append(str(index))


def map_test(test_image_file, training_result, occurence, k_value, pos_idx):
    line_counter = 0
    with open(test_image_file) as f:
        number_image = []
        for line in f:
            if line_counter == 27999: #don't know why it doesn't read line 28000
                analyze_number(number_image, training_result, occurence, k_value, pos_idx)
                number_image = []
                number_image.append(list(line))
                pos_idx += 1
            if line_counter % 28 == 0 and line_counter != 0:
                analyze_number(number_image, training_result, occurence, k_value, pos_idx)
                number_image = []
                number_image.append(list(line))
                pos_idx += 1
            else:
                number_image.append(list(line))
            line_counter += 1


training_results, occurence = read_file("traininglabels", "trainingimages")
print "training_finished"



#begin test
test_results = []
posteriori_matrix = np.zeros((1000, 10))

map_test("testimages.txt", training_results, occurence, 5, 0)

#write results to a result.txt
results_file = open("result.txt", "w+")
for res in test_results:
    results_file.write(res)
    results_file.write("\n")
results_file.close

### To do ###
#highest four pairs in our confusion_matrix are (5,2),(1,4),(0,7),(3,8)
#and for each pair, display the maps of feature likelihoods for both classes
#as well as the odds ratio for the two classes
#For example, for the odds ratio map, you can use '+' to denote features with positive log odds,
# ' ' for features with log odds close to 1, and '-' for features with negative log odds

# For 5,2
# For 5 










#report will cover following three things:
np.set_printoptions(linewidth=200)
##### compute accuracy in Utility.py to avoid writing synchronization #####
# print "Accuracy is : ", Utility.calculate_accuracy("result.txt", "testlabels.txt")*100.0, "%"
# print "Confusion matrix is : "
# print Utility.confusion_matrix("result.txt", "testlabels.txt")
print "highest_prototype: "
print Utility.highest_prototype(posteriori_matrix, "testlabels.txt")
print "lowest_prototype: "
print Utility.lowest_prototype(posteriori_matrix, "testlabels.txt")

# print "for five"
# print occurence[5]
# print training_results[5,:,:,1]
# print training_results[5,:,:,1] + 5

Utility.save_graphs((5,2), training_results, occurence)
Utility.save_graphs((1,4), training_results, occurence)
Utility.save_graphs((0,7), training_results, occurence)
Utility.save_graphs((3,8), training_results, occurence)




# visual_matrix_for_five = np.log((training_results[5, :, :, 1]+5) / (occurence[5] + 10))
# fig, ax = plt.subplots()
# cax = ax.imshow(visual_matrix_for_five, interpolation='nearest', cmap=cm.coolwarm)
# ax.set_title('For Five')
# cbar = fig.colorbar(cax)
# plt.savefig()

