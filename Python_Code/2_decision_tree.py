#!/usr/bin/env python
# coding: utf-8

# ---------------------------------------------
# Library
# ---------------------------------------------
import pandas, datetime 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import graphviz

from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree
from sklearn.model_selection import train_test_split 
from sklearn import metrics 
from sklearn.utils import shuffle

# ---------------------------------------------
# Applied functions
# ---------------------------------------------
# To manipulate the dataframe more efficient, 
# using dataframe.apply instead of iterrows

def timestamp_to_class(x):
    in30min = 30*60
    in60min = 2*in30min
    in6hour = 6*in60min
    in12hour = 2*in6hour
    in1day = 2*in12hour
    in1week = 7*in1day
    in1month = 4*in1week
    inhalfyear = (366/2)*in1day
    in1year = 366*in1day

    if x <= in30min:
        return 0
    elif x <= in60min:
        return 1
    elif x <= in6hour:
        return 2
    elif x <= in12hour:
        return 3
    elif x <= in1day:
        return 4
    elif x <= in1week:
        return 5
    elif x <= in1month:
        return 6
    elif x <= inhalfyear:
        return 7
    elif x <= in1year:
        return 8
    else :
        return 9

# Load data form DB
print("Load Data ... ", end = '')
Answer = pandas.read_sql('Answer', "sqlite:///data/QAT_final.db", index_col='index')
Question = pandas.read_sql('Question', "sqlite:///data/QAT_final.db", index_col='index')
Tags = pandas.read_csv("data/Tags.csv")
print("done!")

# Marge tags count
Tags = Tags.groupby("Id").count()
Question = pandas.merge(Question, Tags, on=["Id"])

# Calculate the response time of the first/best answer
Question['FirstAnsTime_timestamp'] = Question['FirstAnsTime'] - Question['CreationDate_to_datetime']
Question['BestAnsTime_timestamp'] = Question['BestAnsTime'] - Question['CreationDate_to_datetime']

# Remove outlier
Question = Question[Question['FirstAnsTime_timestamp'] > 0]
Question = Question[Question['BestAnsTime_timestamp'] > 0]

# Create a subset
df = Question[['Score', 'Title', 'Body', 'Tag', 'FirstAnsTime_timestamp']]

# Convert timestamp to class
df['label'] = df['FirstAnsTime_timestamp'].apply(timestamp_to_class)

df.head()

# Split data into features and label
mydata = pandas.DataFrame()

for i in range(0, 10):
    mydata = mydata.append(df[df['label'] == i].sample(n=3000))
mydata = shuffle(mydata)

feature_cols = ['Score', 'Title', 'Body', 'Tag']

X = df[feature_cols] 
y = df["label"] 

# Split into training data and test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) 

# Decision Tree classifer
clf = DecisionTreeClassifier(max_depth=5)
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# Display the pplot
text_representation = tree.export_text(clf)

## Text
print(text_representation)

## Graph
tree.plot_tree(clf, filled = True)
