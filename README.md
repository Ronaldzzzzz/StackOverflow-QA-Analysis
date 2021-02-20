# Stack Overflow Q&A Analysis

This project analyzes the `Answer` and the `Question` from Stack Overflow and trying to find some relationship between them, especially `Post Time` and `Response Time`.
This is a final project for the course Knowledge Discovery and Data Mining ACS 577.

## Data

### Data source

The data we used is [StackSample: 10% of Stack Overflow Q&A](https://www.kaggle.com/stackoverflow/stacksample) from [Kaggle](https://www.kaggle.com/), which contains 10% QA in Stack Overflow.

### Data size and attribute

The size is 3.35GB, contains 3 table:

* Answers

| Attribute   | Description                  | Data Format | Example                                                                  |
| ----------- | ---------------------------- | ----------- | ------------------------------------------------------------------------ |
| ID          | *ID of This Post*            | `Numeric`   | `92`                                                                     |
| OwnerUserID | *ID of This Poster*          | `Numeric`   | `61`                                                                     |
| CreateDate  | *Post Time*                  | `UTC`       | `2008-08-01T14:45:37Z`                                                   |
| ParentID    | *Question ID of this Answer* | `Numeric`   | `90`                                                                     |
| Score       | *Rating of this Post*        | `Numeric`   | `13`                                                                     |
| Body        | *Content of this Post*       | `Character` | `"<p><a href=""http://svnbook.red-bean.com/" ... specific, though.</p>"` |

* Questions

| Attribute   | Description              | Data Format         | Example                                                                                   |
| ----------- | ------------------------ | ------------------- | ----------------------------------------------------------------------------------------- |
| ID          | *ID of This Post*        | `Numeric`           | `80`                                                                                      |
| OwnerUserID | *ID of This Poster*      | `Numeric`           | `26`                                                                                      |
| CreateDate  | *Post Time*              | `UTC`               | `2008-08-01T13:57:07Z`                                                                    |
| CloseDate   | *Closed Time*            | `UTC (Default N/A)` | `NA`                                                                                      |
| Score       | *Rating of this Post*    | `Numeric`           | `26`                                                                                      |
| Title       | *Title of this Question* | `Character`         | `SQLStatement.execute() - multiple queries in one statement`                              |
| Body        | *Content of this Post*   | `Character`         | `<p>I've written a database generation script ... multiple queries in one statement?</p>` |

* Tags (Each post might have multiple tags)

| Attribute | Description         | Data Format | Example |
| --------- | ------------------- | ----------- | ------- |
| ID        | *ID of This Post*   | `Numeric`   | `80`    |
| Tag       | *Tags for the Post* | `Character` | `flex`  |

## Problem Statement

These problems are what we are focus on:

* What time does a user post a question that will get the quickest response?*
* What time does a user posts a question that will get the highest rating?*
* Does a tag or the other feature affect the response time?*

We are trying to find some relationship based on these problems.

## Content

* [Preprocessing](https://github.com/Ronaldzzzzz/StackOverflow-QA-Analysis/blob/main/0_Preprocessing.ipynb)
* [Visualization](https://github.com/Ronaldzzzzz/StackOverflow-QA-Analysis/blob/main/1_visualization.ipynb)
* [Decision Tree](https://github.com/Ronaldzzzzz/StackOverflow-QA-Analysis/blob/main/2_decision_tree.ipynb)
* [Deep learning](https://github.com/Ronaldzzzzz/StackOverflow-QA-Analysis/blob/main/3_deepLearning.ipynb)

## Usage

### Jupyter Notebook

We are using `Python` to do the analysis.
Access each `jupyter` file in the order to see each step.

### Source code

*Not recommend to execute as a normal `python` progeam.*

#### Prerequisites / Libraries

* Install the following `python` libiaires.

  ```python
  pip install sqlite3 pandas "dask[complete]" matplotlib scikit-learn tensorflow
  ```

* Run each files
  
## Conclusion

In the visualization, we can get a very first step result.
We can see that the data is very dispersed.
The response times are various, from few seconds to several years.
The density of questions is various.
The number of questions of the highest posting hour is 2 times the lowest posting number.

In the decision tree part and deep learning part, we get a failure.
We figure out several reasons and improvements.
First, the labels we use are not iconic, this dataset is not suitable for the task we set.
One of the possible ways is to transfer timestamps into day hours or weekday.
The other possible way is labeling the text content of the body and title.
If we can label the text content, we can use the meaning in the body and title and train a better model.
To archive this, we can use RNN or LSTM, or manually label them. However, no matter which way is very expansive.

## Reference

1. Tak-Chung Fu, “A review on time series data mining”, in Sciencedirect, 2010
2. Vasudev Bhat, Adheesh Gokhale, Ravi Jadhav, Jagat Pudipeddi, Leman Akoglu, “Min(e)d your tags: Analysis of Question response time in StackOverflow”, in IEEE, 2014
3. Seyed Mehdi Nasehi, Jonathan Sillito, Frank Maurer, Chris Burns, “What makes a good code example?: A study of programming Q&A in StackOverflow”, in IEEE, 2012
4. Dana Movshovitz-Attias, Yair Movshovitz-Attias, Peter Steenkiste, Christos Faloutsos, “Analysis of the reputation system and user contributions on a question answering website: StackOverflow”, in IEEE, 2013
5. Saraj Singh Manes, Olga Baysal, “How Often and What StackOverflow Posts Do Developers Reference in Their GitHub Projects?”, in IEEE, 2019
6. StackSample: 10% of Stack Overflow Q&A, Kaggle, Oct 28, 2020, [https://www.kaggle.com/stackoverflow/stacksample](https://www.kaggle.com/stackoverflow/stacksample)

## Contributors

1. Lin, Kun-Jung
2. [Chang, Li-Chi](https://github.com/Li-Chi-Chang)
