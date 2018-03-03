
# coding: utf-8

# In[6]:


print(__doc__)

import numpy as np
from sklearn import linear_model, svm, tree, ensemble, datasets
from sklearn.model_selection import cross_val_predict, GridSearchCV
import pandas as pd
import graphviz 

func_list = [tree.DecisionTreeClassifier,              ensemble.RandomForestClassifier,              svm.SVC,              linear_model.LinearRegression,              linear_model.LogisticRegression]

func_param = [{'max_depth':9},               {},               #{'max_depth':20, 'n_estimators':30, 'criterion':"entropy", 'max_features':None, 'min_samples_split':17}, \
              {'kernel':'rbf', 'C':2, 'gamma': 0.1}, \
              {}, \
              {'C':1e5}]

folder_path = 'Documents/UW_Madison/Course/2nd_Semester/CS839/stage1/features/'

def training(X, Y, cv_type):
    best_F1 = 0;
    best_classifier = []
    best_idx = None
    
    for idx in [1]:
    #for idx in [0, 1, 2, 3, 4]:
        l = func_list[idx]
        print("{}. {}".format(idx, l.__name__))
        
        if cv_type == 0:
            # Without Cross-Validation
            classifier = l()
            classifier.fit(X, Y)
            Y_pred = classifier.predict(X)
        elif cv_type == 1:
            # With Cross-Validation
            classifier = l(**func_param[idx])
            Y_pred = cross_val_predict(classifier, X, Y, cv=5)
            classifier.fit(X, Y)

        print("best_param = {}".format(classifier))
        F1 = calPR(Y, Y_pred)
        
        if F1 > best_F1:
            best_F1 = F1
            best_classifier = classifier
            best_idx = idx

    return best_classifier, best_idx

def pq_test(X, Y, cv_type, best_idx):
    l = func_list[best_idx]
    print("{}. {}".format(best_idx, l.__name__))

    if cv_type == 0:
        # Without Cross-Validation
        classifier = l()
        classifier.fit(X, Y)
        Y_pred = classifier.predict(X)
    elif cv_type == 1:
        # With Cross-Validation
        classifier = l(**func_param[best_idx])
        Y_pred = cross_val_predict(classifier, X, Y, cv=2)
        classifier.fit(X, Y)
        
    print("best_param = {}".format(classifier))
    print("[Before rule-based postprocessing step]")
    calPR(Y, Y_pred)

    #saveAnalysis(Y, Y_pred, "_pq", 0)
    
    # Rule-based postprocessing step
    print("[After rule-based postprocessing step]")
    Y_pred_new = post_processing(Y_pred, 0)
    calPR(Y, Y_pred_new)
    
    saveAnalysis(Y, Y_pred_new, "_pq", 0)
    
def saveAnalysis(Y, Y_pred, special_name, train_type):
    if train_type == 0:
        df = pd.read_csv(folder_path + 'train_index.csv')
    else:
        df = pd.read_csv(folder_path + 'test_index.csv')  
    train_index = df.values
    df = pd.read_csv(folder_path + 'X_train.csv')
    feature_title = list(df)
    
    # Check false negative to increase R
    print("False Negative generating...")
    
    false_neg_list = []
    false_neg = []    
    false_neg.append("[doc name]")
    for d in feature_title:
        false_neg.append(d)
    false_neg_list.append(false_neg)
    
    for i in range(len(Y)):
        if Y[i] == 1 and Y_pred[i] != 1:
            false_neg = []
            false_neg.append(train_index[i])
            for x in X[i]:
                false_neg.append(x)
            false_neg_list.append(false_neg)
    df = pd.DataFrame(false_neg_list)
    df.to_csv(folder_path + '/false_neg' + special_name + '.csv')
    
    # Check false positive to increase P
    print("False Positive generating...\n")
    
    false_pos_list = []
    false_pos = []    
    false_pos.append("[doc name]")
    for d in feature_title:
        false_pos.append(d)
    false_pos_list.append(false_pos)
    
    for i in range(len(Y)):
        if Y[i] != 1 and Y_pred[i] == 1:
            false_pos = []
            false_pos.append(train_index[i])
            for x in X[i]:
                false_pos.append(x)
            false_pos_list.append(false_pos)
    df = pd.DataFrame(false_pos_list)
    df.to_csv(folder_path + '/false_pos' + special_name + '.csv')
    
def calPR(Y, Y_pred):
    true_pred_num = 0
    total_pos_label_num = 0
    pred_pos_label_num = 0
    for i in range(len(Y)):
        if Y_pred[i] >= 0.5:
            Y_pred[i] = 1
        else:
            Y_pred[i] = 0

        if Y[i] == 1 and Y_pred[i] == 1:
            true_pred_num = true_pred_num + 1
        if Y[i] == 1:
            total_pos_label_num = total_pos_label_num + 1
        if Y_pred[i] == 1:
            pred_pos_label_num = pred_pos_label_num + 1

    assert (true_pred_num > 0),"true_pred_num = 0!"
    assert (pred_pos_label_num > 0),"pred_pos_label_num = 0!"
    P = float(true_pred_num)/pred_pos_label_num
    assert (total_pos_label_num > 0),"total_pos_label_num = 0!"
    R = float(true_pred_num)/total_pos_label_num
    F1 = (2 * P * R)/(P + R)
    
    print("- Precision(P) = {}/{} = {:.6f}".format(true_pred_num, pred_pos_label_num, P)) 
    print("- Recall(R) = {}/{} = {:.6f}".format(true_pred_num, total_pos_label_num, R)) 
    print("- F1 = {:.6f}\n".format(F1))
    
    return F1

def testing(best_classifier):
    print("{}. {}".format(best_idx, func_list[best_idx].__name__))
    print("best_param = {}".format(best_classifier))
    
    df = pd.read_csv(folder_path + '/X_test.csv')
    X_test = df.values
    df = pd.read_csv(folder_path + '/y_test.csv')
    Y_test = df.values
    
    print("[Before rule-based postprocessing step]")
    Y_pred = best_classifier.predict(X_test)
    calPR(Y_test, Y_pred)
    
    #saveAnalysis(Y_test, Y_pred, "_test", 1)
    
    # Rule-based postprocessing step
    print("[After rule-based postprocessing step]")
    Y_pred_new = post_processing(Y_pred, 1)
    calPR(Y_test, Y_pred_new)
    
    saveAnalysis(Y_test, Y_pred_new, "_test", 1)
    
# post processing
def post_processing(y_test_pred, train_type):
    # removing words in prefix dict
    input_file = open(folder_path + 'prefix_dict.txt', 'rb')
    lines = input_file.read().lower().splitlines()
    prefix_dict = list(set([ l.strip().lower() for l in lines ]))
    input_file.close()

    if train_type == 0:
        doc = pd.read_csv(folder_path + 'train_index.csv')
    else:
        doc = pd.read_csv(folder_path + 'test_index.csv')

    all_strings = doc.candidate_str.values
    y_test_pred_new = np.zeros(len(y_test_pred))
    for i, one_y in enumerate(y_test_pred):
        y_test_pred_new[i] = one_y
        if one_y == 1:
            myStr = all_strings[i]
            if myStr.isupper():
                y_test_pred_new[i] = 0
                continue

            elif len(myStr) == 1:
                y_val_pred_new[i] = 0
                continue

            for w in prefix_dict:
                if w in myStr.lower().split():
                    y_test_pred_new[i] = 0
                    break

    # remove words that contains country names
    country_name = pd.read_csv(folder_path + 'country_name.csv')
    all_names = country_name.Name.values
    for i in range(len(y_test_pred)):
        if y_test_pred_new[i] == 1:
            for cname in all_names:
                cname = cname.replace('"', '')
                if cname.lower() in all_strings[i].lower().split():
                    y_test_pred_new[i] = 0
                    break

    # add words in celebrity names
    input_file = open(folder_path + 'celebrity.txt', 'rb')
    celeb_names = input_file.read().lower().splitlines()

    for i in range(len(y_test_pred)):
        if y_test_pred_new[i] == 0:
            for cname in celeb_names:
                if all_strings[i].lower() == cname.lower():
                    y_test_pred_new[i] = 1
                    break
    
    return y_test_pred_new

if __name__ == "__main__":
    # Parse data
    df = pd.read_csv(folder_path + '/X_train.csv')
    X = df.values
    df = pd.read_csv(folder_path + '/y_train.csv')
    #Y = df.values
    Y = np.ravel(df.values)
    cv_type = 1

    # Training
    print("\n**************")
    print("** Training **")
    print("**************\n")

    best_classifier, best_idx = training(X, Y, cv_type)

    print("=======================================")

    # P/Q Test
    print("\n**************")
    print("** P/Q Test **")
    print("**************\n")

    pq_test(X, Y, cv_type, best_idx)

    print("=======================================")

    # Testing
    print("\n**************")
    print("** Testing **")
    print("**************\n")

    testing(best_classifier)

