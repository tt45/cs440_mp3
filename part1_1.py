import numpy as np
import math

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

def analyze_number(number_image, training_result, occurence, k):
    print number_image
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

    index = np.argmax(probability_array)
    print index
    f = open("result.txt", 'w+')
    f.write(str(index))
    f.close


def map_test(test_image_file, training_result, occurence, k_value):
    line_counter = 0
    with open(test_image_file) as f:
        number_image = []
        for line in f:
            if line_counter % 28 == 0 and line_counter != 0:
                analyze_number(number_image, training_result, occurence, k_value)
                number_image = []
                number_image.append(list(line))
            else:
                number_image.append(list(line))
            line_counter += 1


training_results, occurence = read_file("traininglabels", "trainingimages")
print "training_finished"
map_test("testimages_small.txt", training_results, occurence, 5)
# np.set_printoptions(linewidth=200)
# print np.array(training_results[8,:,:,1])
# print occurence
#def training_fun():
