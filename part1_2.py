import numpy as np
import math

def process_matrix(training_results, temp_matrix, label, row_size, col_size):
    for i in range(0, len(temp_matrix), row_size):
        for j in range(0, len(temp_matrix[0]), col_size):
            tmp = temp_matrix[i:i+row_size,j:j+col_size]
            # print tmp
            window_sum = 0
            counter = 0
            for t in range(len(tmp)):
                for s in range(len(tmp[0])):
                    window_sum += (2**counter)*tmp[t][s]
                    counter += 1
            window_sum = int(window_sum)
            training_i_index = i / row_size
            training_j_index = j / col_size
            training_results[label,training_i_index, training_j_index, window_sum] += 1

    return training_results


def read_file_to_matrix(training_file_name, label_file_name, row_size, col_size):
    training_results = np.zeros((10,28//row_size,28//col_size,2**(row_size*col_size)))
    label_array = []
    with open(label_file_name) as f:
        for line in f:
            label_array.append(int(line[0]))
    f.close

    line_counter = 0
    line_number = 0
    temp_matrix = np.zeros((28,28))
    with open(training_file_name) as f:
        for line in f:
            if line_counter == 27:
                line_counter = 0
                training_results = process_matrix(training_results, temp_matrix, label, row_size, col_size)
                temp_matrix = np.zeros((28,28))
            else:
                char_counter = 0
                label = label_array[line_number//28]
                for char in line:
                    if char == " ":
                        temp_matrix[line_counter][char_counter] = 0
                    elif char == "#" or char == "+":
                        temp_matrix[line_counter][char_counter] = 1
                    char_counter += 1
            line_counter += 1
            line_number += 1
    denominator_array = np.zeros(10)
    for i in label_array:
        denominator_array[i]+=1
    return training_results, denominator_array

def analyze_number(number_image, training_results, occurence, k, pos_idx):
    #print number_image
    occurence = np.array(occurence)
    p_class_array = occurence/5000
    probability_array = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
    row_number = len(number_image)
    col_number = len(number_image[0])
    _, training_row_size, training_col_size, _ = np.shape(training_results)
    for i in range(10):
        for j in range(0, row_number, 28/training_row_size):
            for h in range(0, col_number, 28/training_col_size):
                tmp = number_image[j:j+28/training_row_size, h:h+28/training_col_size]
                counter = 0
                window_sum = 0
                for x in range(len(tmp)):
                    for y in range(len(tmp[0])):
                        window_sum += (2**counter)*tmp[x][y]
                        counter += 1
                # print tmp
                # print window_sum
                tra_res = training_results[i, j//(28/training_row_size), h//(28/training_col_size), int(window_sum)]+k
                occu = occurence[i]+2*k
                resu = tra_res/occu
                print resu
                probability_array[i] += math.log(resu)
        probability_array[i] += math.log(p_class_array[i])
    #posteriori_matrix[pos_idx] = probability_array
    print probability_array
    index = np.argmax(probability_array)
    print index
    test_results.append(str(index))

def map_test(test_image_file, training_results, occurence, k_value, pos_idx):
    line_counter = 0
    with open(test_image_file) as f:
        number_image = []
        for line in f:
            if line_counter % 28 == 0 and line_counter != 0:
                temp_array = np.zeros((28, 28))
                for i in range(28):
                    for j in range(28):
                        if number_image[i][j] == ' ':
                            temp_array[i][j] = 0
                        else:
                            temp_array[i][j] = 1
                analyze_number(temp_array, training_results, occurence, k_value, pos_idx)
                number_image = []
                number_image.append(list(line))
                pos_idx += 1
            else:
                number_image.append(list(line))
            line_counter += 1


training_results, occurence = read_file_to_matrix("trainingimages", "traininglabels", 2, 2)

test_results = []
map_test("testimages_small.txt", training_results, occurence, 9, 0)

#write results to a result.txt
results_file = open("result_part_1_2.txt", "w+")
for res in test_results:
    results_file.write(res)
    results_file.write("\n")
results_file.close

# print np.shape(training_results)
# print training_results[5, :, :, 15]
