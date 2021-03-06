"""divide the data into left branch or right branch according to the split number"""
def split_data_set_left(data_set, axis, mean_value):
    # All the data in the left brach have a smaller value of the feature than the split number. 
    # All the value of that feature are deleted
    new_data_set_left = []
    
    for row in data_set:
        if row[axis] <= mean_value:
            split_vector = row[:axis]
            split_vector.extend(row[axis + 1:])
            new_data_set_left.append(split_vector)

    return new_data_set_left

def split_data_set_right(data_set, axis, mean_value):
    # All the data in the right brach have a larger value of the feature than the split number. 
    # All the value of that feature are deleted
    new_data_set_right = []
    
    for row in data_set:
        if row[axis] > mean_value:
            split_vector = row[:axis]
            split_vector.extend(row[axis + 1:])
            new_data_set_right.append(split_vector)

    return new_data_set_right

"""calculate gini of the data"""
def calc_gini(data_set):

    count = len(data_set)
    label_counts = {}

    # for data in each branch: calculate how many data has the lable ">6" and how many data has the lable "<=6"
    # put the number of data whose lable is ">6" and the number of data whose label is"<=6" into a dictionary
    for row in data_set:
        label = row[-1] # the lable of each piece of data is the last number of the list
        if label not in label_counts:
            label_counts[label] = 1
        else:
            label_counts[label] += 1

    # calculate gini
    gini = 1.0
    for key in label_counts:
        prob = label_counts[key] / count
        gini -= prob * prob
    return gini

def cal_mean(i, j):
    mean = (i+j)/2
    return mean 

"""find the best split feature according to gini of each feature"""
'''find the best split number of the best split feature'''
def choose_best_feature_and_split_gini(data_set):

    feature_count = len(data_set[0]) - 1 

    # store the minimum gini among all the feature  
    min_gini_index = 0.0
    # store in what feature we get the niminum gini
    best_feature = -1

    # calculate gini of each feature
    for i in range(feature_count):
        features = [example[i] for example in data_set]  # get all the value of the examples under that feature
        feature_value_set = list(set(features))
        means = []      # store (n-1) mean value

        for j in range(len(feature_value_set)-1):
            mean = cal_mean(feature_value_set[j], feature_value_set[j+1])
            means.append(mean)           

        # calculate gini of each split number 
        for mean_value in means:

            sub_data_set_left = split_data_set_left(data_set, i, mean_value)  
            sub_data_set_right = split_data_set_right(data_set, i, mean_value)
            prob_left = len(sub_data_set_left) / len(data_set)
            prob_right = len(sub_data_set_right) / len(data_set)
            gini_index = prob_left * calc_gini(sub_data_set_left) + prob_right * calc_gini(sub_data_set_right)

            # every single time after calculating gini, update the minimum gini
            if gini_index < min_gini_index or min_gini_index == 0.0:
                min_gini_index = gini_index
                best_feature = i
                best_split = mean_value

    return best_feature,best_split

"""find the majority label of a number of data"""
def get_top_class(class_labels):
    count_class_below = class_labels.count('<=6')
    count_class_above = class_labels.count('>6')

    # if most of the data have the label "<=6", return "<=6" as the top class, vice versa. 
    if count_class_below > count_class_above:
        top_class = '<=6'
    else:
        top_class = '>6'
    return top_class

def grow_tree(data_set):
    class_list = []
    for example in data_set:
        if example[-1] <= 6:
            class_list.append('<=6')
        else:
            class_list.append('>6')

    '''determine whether the process is complete'''
    # if all the features have been considered and split the data according to the best split of that feature,
    # then return the label of the majority
    if len(data_set[0]) == 1 :
        return get_top_class(class_list)

    # if all the data in that node have the same label, return that label
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    '''continue if the process is not complete'''
    # find the best feature and best split number to divide the data into two parts
    best_feature,best_split = choose_best_feature_and_split_gini(data_set)

    # use a dictionary to store the tree
    tree = {}

    tree['best_feature'] = best_feature
    tree['best_split'] = best_split
    
    # use recurtion to grow a tree
    left_set = split_data_set_left(data_set, best_feature, best_split)
    right_set = split_data_set_right(data_set, best_feature, best_split)

    tree["amount"] = len(left_set) + len(right_set)

    if len(left_set) != 0:
        tree['left'] = grow_tree(left_set)
    if len(right_set) != 0:
        tree['right'] = grow_tree(right_set)

    return tree   

"""use nested list to store each piece of data in the dataset."""
def load_data(file):
    data_set = []
    fr = open(file,"r")
    text = fr.readlines()[1:]
    for line in text:
        line = line.split('\n')[0].split(", ")
        float_line = []
        for i in line:
            float_line.append(eval(i))
        data_set.append(float_line)
    fr.close()
    return data_set

"""use the tree to predict the label of one piece of data in the test dataset"""
def classify(mytree, test_data):
    test_data_temp = eval(str(test_data))
    if not isinstance(mytree, dict):
        class_label = mytree
        return class_label
    else:
        best_feature = mytree['best_feature'] #int
        best_split = mytree['best_split']  #int
        if test_data_temp[best_feature] <= best_split:
            next_tree = mytree['left']
        elif test_data_temp[best_feature] > best_split:
            next_tree = mytree['right']
        del test_data_temp[best_feature]
        return classify(next_tree, test_data_temp)

"""for each piece of data, compare the predict label with the real label, get the accuracy of the whole tree"""
def calc_accuracy(mytree,test_data_set):
    classification_result = []
    for test_data in test_data_set:
        prediction = classify(mytree, test_data)
        if (test_data[-1] <= 6 and prediction == "<=6") or (test_data[-1] > 6 and prediction == ">6"):
            classification_result.append(True)
        else:
            classification_result.append(False)
    accuracy = classification_result.count(True)/len(classification_result)
    return accuracy

"""use Pessimistic-Error Pruning(PEP) to prune the tree"""
def prune(mytree,data_set):
    '''判断该节点是否为非叶节点'''
    if isinstance(mytree,dict):
        # number of datas under the tree
        N = mytree["amount"]

        # number of errors before pruning
        error_before = calc_error(mytree,data_set)
        # number of leaf nodes under the tree
        leaf = calc_leaf(mytree,0)
        # estimated error rate beforr pruning
        p = (error_before + 0.5*leaf)/N

        # expectation of the number of errors before pruning
        E1 = N * p
        # The standard deviation of the number of errors before pruning
        std = sqrt(N*p*(1-p))

        # number of errors after pruning
        class_list = []
        for example in data_set:
            if example[-1] <= 6:
                class_list.append('<=6')
            else:
                class_list.append('>6')
        if class_list.count("<=6") > class_list.count(">6"):
            error_after = class_list.count(">6")
        if class_list.count("<=6") <= class_list.count(">6"):
            error_after = class_list.count("<=6")
        # estimated error rate after pruning
        e = (error_after+0.5)/N
        # number of errors after pruning
        E2 = N * e

        '''if the expectation of the number of errors before pruning is larger than the number of errors after pruning, prune the tree'''
        if E1 + std > E2:
            mytree = get_top_class(class_list)
        else:
            best_feature = mytree["best_feature"]
            best_split = mytree["best_split"]
            data_set_left = split_data_set_left(data_set,best_feature,best_split)
            data_set_right = split_data_set_right(data_set,best_feature,best_split)
            mytree["left"] = prune(mytree["left"],data_set_left)
            mytree["right"] = prune(mytree["right"],data_set_right)
    
    return mytree

"""Find the square root of a number"""
def sqrt(n):
    #Find the square root of 0.
    if n == 0:
        return n
    #Find the square root of n when n is not equsl to 0.
    else:
        i = 1        #Specify an positive value i.
        j = 0        #introduce variable j.
        while i-j >= 0.000000001 or j-i >= 0.000000001:        #End up the loop when the difference between nextGuess and lastGuess is less than a very small number 0.000000001.
            j = (i+(n/i))/2         #Get the nextGuess j using the formula.
            i,j = j,i         #Exchange value. Let i be the lastGuess of the next loop.
        return i         #Return the approximated square root of n.

"""Find the number of leaf nodes under the subtree"""
def calc_leaf(mytree,leaf):
    # if the left subtree of the current node is not a leaf node, recursively find the leaf node
    if isinstance(mytree["left"],dict):
        leaf = calc_leaf(mytree["left"],leaf)
    # if the left subtree of the current node is a leaf node, increase the total number of leaf nodes
    else:
        leaf += 1

    # if the right subtree of the current node is not a leaf node, recursively find the leaf node
    if isinstance(mytree["right"],dict):
        leaf = calc_leaf(mytree["right"],leaf)
    # if the right subtree of the current node is a leaf node, increase the total number of leaf nodes
    else:
        leaf += 1
    
    return leaf

"""Find the total number of mispredictions under a tree"""
def calc_error(mytree,datas):
    error = 0
    for data in datas:
        prediction = classify(mytree, data)
        if (data[-1] <= 6 and prediction != "<=6") or (data[-1] > 6 and prediction != ">6"):
            error += 1
    return error


if __name__ == "__main__":
    data_set = load_data(r"train.csv")
    test_data_set = load_data(r"test.csv")

    # grow the tree
    Tree = grow_tree(data_set)
    accuracy_before = calc_accuracy(Tree,test_data_set)*100

    # prune the tree
    Tree = prune(Tree,data_set)

    # print the accuracy before and after pruning
    print("\naccuracy before pruning: ","%.2f"%accuracy_before,"%\n",sep = "")
    accuracy_after = calc_accuracy(Tree,test_data_set)*100
    print("accuracy after pruning: ","%.2f"%accuracy_after,"%\n",sep = "")
