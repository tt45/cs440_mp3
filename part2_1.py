import numpy as np
import math

def complete_txt(txt_file, result_file):
    line_counter = 0
    result_file_descriptor = open(result_file, "w+")
    with open(txt_file) as f:
        for line in f:
            if line_counter<25:
                char_counter = 0
                for char in line:
                    if char == '\n' and char_counter < 10:
                        result_file_descriptor.write(' ' * (10-char_counter))
                        result_file_descriptor.write('\n')
                        break
                    else:
                        result_file_descriptor.write(char)
                    char_counter += 1
            else:
                result_file_descriptor.write('\n')
            line_counter += 1
            if line_counter == 28:
                line_counter = 0


def train_to_3dmatrix(file_name):
    file_matrix = np.zeros((25,10,2))
    total_number = 1
    line_counter = 0
    with open(file_name) as f:
        for line in f:
            if line_counter < 25:
                char_counter = 0
                for char in line:
                    if char == " ":
                        file_matrix[line_counter][char_counter][1] += 1
                    elif char == "%":
                        file_matrix[line_counter][char_counter][0] += 1
                    elif char == '\n' and char_counter == 0:
                        file_matrix[line_counter,:,1] += 1
                    char_counter += 1
            line_counter += 1
            if line_counter == 28:
                line_counter = 0
                total_number += 1
    return file_matrix, total_number


def analyze_sound_image(sound_image, training_result, yes_utterance, no_utterance, k, offset):
    #print number_image
    p_class_array = np.zeros(2)
    p_class_array[0] = yes_utterance/float(yes_utterance + no_utterance)
    p_class_array[1] = no_utterance/float(yes_utterance + no_utterance)

    probability_array = np.array([0,0])
    row_number = 25
    col_number = 10
    for i in range(2):
        if i == 0:
            occurence = yes_utterance
        else:
            occurence = no_utterance
        for j in range(row_number):
            for h in range(col_number):
                if h == 0 and sound_image[j][h] == "\n":
                    probability_array[i] += np.sum(np.log((training_result[i, j, :, 1]+k)/(float (occurence+2*k))))
                    break
                elif sound_image[j][h] == ' ':
                    probability_array[i] += math.log((training_result[i, j, h, 1]+k)/(float (occurence+2*k)))
                elif sound_image[j][h] == '%':
                    probability_array[i] += math.log((training_result[i, j, h, 0]+k)/(float (occurence+2*k)))
        probability_array[i] += math.log(p_class_array[i])

    index = np.argmax(probability_array)
    if offset == 0:
        if index == 0:
            yes_test_results.append("yes")
        else:
            yes_test_results.append("no")
    else:
        if index == 0:
            no_test_results.append("yes")
        else:
            no_test_results.append("no")



def map_test(test_sound_file, training_result, yes_utterance, no_utterance, k_value, offset):
    line_counter = 0
    with open(test_sound_file) as f:
        sound_image = []
        for line in f:
            if line_counter == 25:
                analyze_sound_image(sound_image, training_result, yes_utterance, no_utterance, k_value, offset)
                sound_image = []
            elif line_counter == 28:
                line_counter = 0
                sound_image.append(list(line))
            elif line_counter < 25:
                sound_image.append(list(line))
            line_counter += 1
        if len(sound_image) == 25:
            analyze_sound_image(sound_image, training_result, yes_utterance, no_utterance, k_value, offset)


complete_txt("yes_test.txt", "our_yes_test.txt")
complete_txt("no_test.txt", "our_no_test.txt")
complete_txt("yes_train.txt", "our_yes_train.txt")
complete_txt("no_train.txt", "our_no_train.txt")

yes_matrix, yes_utterance = train_to_3dmatrix("our_yes_train.txt")
no_matrix, no_utterance = train_to_3dmatrix("our_no_train.txt")
training_result = np.zeros((2,25,10,2))
training_result[0,:,:,:] = yes_matrix
training_result[1] = no_matrix

#begin test
yes_test_results = [] #offset 0
no_test_results = [] #offset 1
confusion_matrix = np.zeros((2,2))

map_test("our_yes_test.txt", training_result, yes_utterance, no_utterance, 5, 0)
map_test("our_no_test.txt", training_result, yes_utterance, no_utterance, 5, 1)

#write results to a result.txt
results_file = open("part2_yes_result.txt", "w+")
for res in yes_test_results:
    results_file.write(res)
    results_file.write("\n")
results_file.close

results_file1 = open("part2_no_result.txt", "w+")
for res in no_test_results:
    results_file1.write(res)
    results_file1.write("\n")
results_file1.close

yes_count = 0
no_count = 0
for i in range(len(yes_test_results)):
    if yes_test_results[i] == "yes":
        yes_count += 1
    else:
        no_count += 1

confusion_matrix[0][0] = float (yes_count)/50
confusion_matrix[0][1] = float (no_count)/50

yes_count = 0
no_count = 0
for i in range(len(no_test_results)):
    if no_test_results[i] == "yes":
        yes_count += 1
    else:
        no_count += 1

confusion_matrix[1][0] = float (yes_count)/50
confusion_matrix[1][1] = float (no_count)/50

print yes_test_results
print no_test_results
print confusion_matrix
