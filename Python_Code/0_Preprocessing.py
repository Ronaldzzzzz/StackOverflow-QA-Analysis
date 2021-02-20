#!/usr/bin/env python
# coding: utf-8

# ---------------------------------------------
# Library
# ---------------------------------------------
import sqlite3, pandas, dask.dataframe as dd, datetime

# ---------------------------------------------
# Preprocess 1. Raw to database 
# ---------------------------------------------
# Remove some useless columns and store the date 
# in a Database format, which will be more effieient.


## Load data
print("Loading data ... ", end = '')
rawAnswer = pandas.read_csv("data/Answers.csv", encoding="latin1")
rawQuestions = pandas.read_csv("data/Questions.csv",encoding="latin1")
rawTags = pandas.read_csv("data/Tags.csv", encoding="latin1")
print("done!")

## Drop useless columns
print("Drop useless columns ... ", end = '')
rawAnswer.drop(columns = ["OwnerUserId"])
rawQuestions.drop(columns = ["ClosedDate", "ClosedDate"])
print("done!")

## Count contents
print("Count contents ... ", end = '')
for i in range(len(rawAnswer)):
    rawAnswer.at[i, "Body"] = len(str(rawAnswer.loc[i]["Body"]).split(" "))

for i in range(len(rawQuestions)):
    rawQuestions.at[i, "Body"] = len(str(rawQuestions.loc[i]["Body"]).split(" "))
    rawQuestions.at[i, "Title"] = len(str(rawQuestions.loc[i]["Title"]).split(" "))
print("done!")

## Store data in a DB
cnx = sqlite3.connect('data/QAT.db')
print("Store data into a DB ... ", end = '')
rawAnswer.to_sql(name='Answer', con=cnx,  if_exists = "replace")
rawQuestions.to_sql(name='Question', con=cnx,  if_exists = "replace")
rawTags.to_sql(name='Tag', con=cnx,  if_exists = "replace")
print("done!")
# ---------------------------------------------

# ---------------------------------------------
# Preprocess 2. Remove redundancy
# ---------------------------------------------
# Some of the Question has no answer, should be removed

print("Loading data ... ", end = '')
Answer = dd.read_sql_table('Answer', "sqlite:///data/QAT.db", index_col='index')
Tag = dd.read_sql_table('Tag', "sqlite:///data/QAT.db", index_col='index')
Question = dd.read_sql_table('Question', "sqlite:///data/QAT.db", index_col='index')
print("done!")

print('Remove unanswered questions ... ', end = '')
## Get Parent Id from Answers
pid = list(Answer["ParentId"])
pid = set(pid)
## Checking the existence
Question = Question[Question.Id.isin(pid)]
Question = Question.compute()
Answer = Answer.compute()
print("done!")

## Change the time format from text to float timestamp
print("Change time text to float timestamp ... ", end = '')
def column_time_text_to_datetime(df,label):
    to_datetime = []
    for idx, row_data in df.iterrows():
        date_time_obj = datetime.datetime.strptime(row_data[label], '%Y-%m-%dT%H:%M:%SZ')
        to_datetime.append(date_time_obj.timestamp())
    df = df.drop(columns=[label])
    df.insert(len(df.columns),label+'_to_datetime',to_datetime, True)
    return df

Answer = column_time_text_to_datetime(Answer,"CreationDate")
Question = column_time_text_to_datetime(Question,"CreationDate")
print("done!")

## Store data in a new DB
print("Store data into a new DB ... ", end = '')
Question.to_sql("Question_trimmed", "sqlite:///data/QAT_trimmed.db", if_exists = "replace")
Answer.to_sql("Answer_trimmed", "sqlite:///data/QAT_trimmed.db", if_exists = "replace")
print("done!")
# ---------------------------------------------

# ---------------------------------------------
# Preprocess 3. Select Interested Data By Question Id
# ---------------------------------------------
# Since the dataset is very large, we should only select
# the data we interested in

## Load trimmed data
print("Load Data ... ", end = '')
Answer = pandas.read_sql('Answer_trimmed', "sqlite:///data/QAT_trimmed.db", index_col='index')
Question = pandas.read_sql('Question_trimmed', "sqlite:///data/QAT_trimmed.db", index_col='index')
print("done!")

## Sort data by CreationDate_to_datetime & Score
print("Sort data ... ", end = '')
Answer_sorted_score = Answer.sort_values(by=['ParentId','Score','CreationDate_to_datetime'],ascending=[1,0,1])
Answer_sorted_time = Answer.sort_values(by=['ParentId','CreationDate_to_datetime'])
Question_sorted_Id = Question.sort_values(by=['Id'])
print("done!")

## Select interested data, and put into Question dataframe
### Create iterator
time_gen = Answer_sorted_time.iterrows()
score_gen = Answer_sorted_score.iterrows()
count = 0
next_score_data = next(score_gen)
next_time_data = next(time_gen)

print("Select data ", end = '')
for idx, row in Question_sorted_Id.iterrows():
    ### Put first data into Question dataframe by row
    Question_sorted_Id.at[idx,'BestAnsTime'] = next_score_data[1]['CreationDate_to_datetime']
    Question_sorted_Id.at[idx,'FirstAnsTime'] = next_time_data[1]['CreationDate_to_datetime']
    next_score_data = next(score_gen)
    next_time_data = next(time_gen)

    ### Skip other data
    while(next_score_data[1]['ParentId'] == row['Id']):
        try:
            next_score_data = next(score_gen)
            next_time_data = next(time_gen)
        except StopIteration:
            print('\ndone!')
            break
    if count % 10000 == 0:
        print('.', end='')
    count+=1

## Store data to a final DB
print("Store Final Data to DB ... ", end = '')
Answer.to_sql('Answer', "sqlite:///data/QAT_final.db",  if_exists = "replace")
Question_sorted_Id = Question_sorted_Id.drop(columns=['OwnerUserId','ClosedDate'])
Question_sorted_Id.to_sql('Question', "sqlite:///data/QAT_final.db",  if_exists = "replace")
print("done!")
# ---------------------------------------------
