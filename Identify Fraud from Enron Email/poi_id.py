import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
import enron
import tester

import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC




### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".


features_list = ['poi',
                 'bonus',
                 'deferral_payments',
                 'deferred_income',
                 'director_fees',
                 'exercised_stock_options',
                 'expenses',
                 'loan_advances',
                 'long_term_incentive',
                 'other',
                 'restricted_stock',
                 'restricted_stock_deferred',
                 'salary',
                 'total_payments',
                 'total_stock_value',
                 'from_messages',
                 'from_poi_to_this_person',
                 'from_this_person_to_poi',
                 'shared_receipt_with_poi',
                 'to_messages']



### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
def PlotOutlier(data_dict, feature_x, feature_y):
    """ Plot with flag = True in Red """
    data = featureFormat(data_dict, [feature_x, feature_y, 'poi'])
    for point in data:
        x = point[0]
        y = point[1]
        poi = point[2]
        if poi:
            color = 'red'
        else:
            color = 'blue'
        plt.scatter(x, y, color=color)
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.show()
    
print(PlotOutlier(data_dict, 'total_payments', 'total_stock_value'))
print(PlotOutlier(data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi'))
print(PlotOutlier(data_dict, 'salary', 'total_stock_value'))
outliers = ['TOTAL', 'LOCKHART EUGENE E', 'THE TRAVEL AGENCY IN THE PARK']
enron.remove_outliers(data_dict, outliers)


### Task 3: Create new feature(s)
enron.poi_communication(data_dict)
enron.total_wealth(data_dict)

features_list += ['poi_communication', 'total_wealth']


### Store to my_dataset for easy export below.
my_dataset = data_dict



# The Top 10 best features using SelectKBest().

best_features_list = ['poi',
                      'exercised_stock_options',
                      'total_stock_value',
                      'bonus',
                      'salary',
                      'total_wealth',
                      'deferred_income',
                      'long_term_incentive',
                      'restricted_stock',
                      'total_payments',
                      ]


### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys=True)
labels, features = targetFeatureSplit(data)


### Task 4: Try a varity of classifiers



def tune_svc():

    skb = SelectKBest()
    pca = PCA()
    svc_clf = SVC()

    pipe_svc = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("SVC", svc_clf)])

    svc_k = {"SKB__k": range(8, 10)}
    svc_params = {'SVC__C': [1000], 'SVC__gamma': [0.001], 'SVC__kernel': ['rbf']}
    svc_pca = {"PCA__n_components": range(3, 8), "PCA__whiten": [True, False]}

    svc_k.update(svc_params)
    svc_k.update(svc_pca)

    enron.get_best_parameters_reports(pipe_svc, svc_k, features, labels)


def tune_decision_tree():

    skb = SelectKBest()
    pca = PCA()
    dt_clf = DecisionTreeClassifier()

    pipe = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("DecisionTreeClassifier", dt_clf)])

    dt_k = {"SKB__k": range(8, 10)}
    dt_params = {"DecisionTreeClassifier__min_samples_leaf": [2, 6, 10, 12],
                 "DecisionTreeClassifier__min_samples_split": [2, 6, 10, 12],
                 "DecisionTreeClassifier__criterion": ["entropy", "gini"],
                 "DecisionTreeClassifier__max_depth": [None, 5],
                 "DecisionTreeClassifier__random_state": [42, 46, 60]}
    dt_pca = {"PCA__n_components": range(4, 7), "PCA__whiten": [True, False]}

    dt_k.update(dt_params)
    dt_k.update(dt_pca)

    enron.get_best_parameters_reports(pipe, dt_k, features, labels)

def tune_logistic_regression():

    skb = SelectKBest()
    pca = PCA()
    lr_clf = LogisticRegression()

    pipe_lr = Pipeline(steps=[("SKB", skb), ("PCA", pca), ("LogisticRegression", lr_clf)])

    lr_k = {"SKB__k": range(9, 10)}
    lr_params = {'LogisticRegression__C': [1e-08, 1e-07, 1e-06],
                 'LogisticRegression__penalty': ['l1', 'l2'],
                 'LogisticRegression__random_state': [42, 46, 60]}
    lr_pca = {"PCA__n_components": range(3, 8), "PCA__whiten": [True, False]}

    lr_k.update(lr_params)
    lr_k.update(lr_pca)

    enron.get_best_parameters_reports(pipe_lr, lr_k, features, labels)

### Task 5: Tune your classifier

if __name__ == '__main__':

    '''SUPPORT VECTOR CLASSIFIER  '''

    #tune_svc()

    best_features_list_svc = enron.get_k_best(my_dataset, features_list, 7)

    clf_svc = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=6, whiten=True)),
        ('classifier', SVC(C=1000, gamma=.001, kernel='rbf'))])

    print "Support Vector Classifier :", tester.test_classifier(clf_svc, my_dataset, best_features_list_svc)



    '''DECISION TREE CLASSIFIER '''

    #tune_decision_tree()

    best_features_list_dt = enron.get_k_best(my_dataset, features_list, 8)

    clf_dt = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=5, whiten=True)),
        ('classifier', DecisionTreeClassifier(criterion='entropy',
                                              min_samples_leaf=2,
                                              min_samples_split=2,
                                              random_state=46,
                                              max_depth=None))
    ])

    print "Decision Tree Classifier :",tester.test_classifier(clf_dt, my_dataset, best_features_list_dt)
    
    
        
    '''LOGISTIC REGRESSION'''

    #tune_logistic_regression()

    best_features_list_lr = enron.get_k_best(my_dataset, features_list, 7)

    clf_lr = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=4, whiten=False)),
        ('classifier', LogisticRegression(tol=0.01, C=1e-08, penalty='l2', random_state=42))])

    print "Logistic Regression :", tester.test_classifier(clf_lr, my_dataset, best_features_list_lr)


    

    


    



  
dump_classifier_and_data(clf_lr, my_dataset, best_features_list_lr)