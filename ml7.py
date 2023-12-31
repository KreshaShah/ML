# -*- coding: utf-8 -*-
"""ml7.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14CJ7cg6bm0RfVTDhWF170wH-z-S0u5V3
"""

from sklearn.datasets import make_classification
import pandas as pd
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold, cross_val_score

n_samples = 1000
n_features = 4
n_classes = 2
random_state = 20

X, y = make_classification(n_samples=n_samples, n_features=n_features, n_classes=n_classes, random_state=random_state)

df = pd.DataFrame(X)
df['target'] = y

df.head()

# Create a Decision Tree classifier object
dt = DecisionTreeClassifier()

# Create a Logistic Regression object
lr = LogisticRegression()

# Set the number of folds for KFold cross validation
k = 10

# Perform KFold cross validation on the Decision Tree classifier
dt_scores = cross_val_score(dt, X, y, cv=k)

# Perform KFold cross validation on the Logistic Regression classifier
lr_scores = cross_val_score(lr, X, y, cv=k)

# Print the average accuracy of the Decision Tree classifier
print("Decision Tree classifier accuracy:", dt_scores.mean())

# Print the average accuracy of the Logistic Regression classifier
print("Logistic Regression classifier accuracy:", lr_scores.mean())

from sklearn.ensemble import AdaBoostClassifier

# Create an AdaBoost classifier with Decision Tree as base learner
dt_ab = AdaBoostClassifier(estimator=dt)

# Create an AdaBoost classifier with Logistic Regression as base learner
lr_ab = AdaBoostClassifier(estimator=lr)

# Perform KFold cross validation on the AdaBoost classifier with Decision Tree as base learner
dt_ab_scores = cross_val_score(dt_ab, X, y, cv=k)

# Perform KFold cross validation on the AdaBoost classifier with Logistic Regression as base learner
lr_ab_scores = cross_val_score(lr_ab, X, y, cv=k)

# Print the average accuracy of the AdaBoost classifier with Decision Tree as base learner
print("AdaBoost classifier with Decision Tree base learner accuracy:", dt_ab_scores.mean())

# Print the average accuracy of the AdaBoost classifier with Logistic Regression base learner
print("AdaBoost classifier with Logistic Regression base learner accuracy:", lr_ab_scores.mean())

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load the credit card dataset
df = pd.read_csv("/content/drive/MyDrive/creditcard.csv")

# Check for class imbalance
class_counts = df['Class'].value_counts()
print("Class counts:\n", class_counts)
print("Class imbalance ratio:", class_counts[1] / class_counts[0])

# Split the dataset into training and testing sets
X = df.drop('Class', axis=1)
y = df['Class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate the Decision Tree Classifier
dtc = DecisionTreeClassifier(random_state=42)
dtc.fit(X_train, y_train)
y_pred = dtc.predict(X_test)
print("Decision Tree Classifier results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Train and evaluate the AdaBoost Classifier with base estimator as Decision Tree
ada_boost = AdaBoostClassifier(base_estimator=dtc, n_estimators=50, random_state=42)
ada_boost.fit(X_train, y_train)
y_pred = ada_boost.predict(X_test)
print("AdaBoost Classifier with Decision Tree base estimator results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# explore adaboost ensemble tree depth effect on performance
from numpy import mean
from numpy import std
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot

# get the dataset
def get_dataset():
	X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=6)
	return X, y

# get a list of models to evaluate
def get_models():
	models = dict()
	# explore depths from 1 to 10
	for i in range(1,11):
		# define base model
		base = DecisionTreeClassifier(max_depth=i)
		# define ensemble model
		models[str(i)] = AdaBoostClassifier(base_estimator=base)
	return models

# evaluate a given model using cross-validation
def evaluate_model(model, X, y):
	# define the evaluation procedure
	cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
	# evaluate the model and collect the results
	scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
	return scores

# define dataset
X, y = get_dataset()
# get the models to evaluate
models = get_models()
# evaluate the models and store results
results, names = list(), list()
for name, model in models.items():
	# evaluate the model
	scores = evaluate_model(model, X, y)
	# store the results
	results.append(scores)
	names.append(name)
	# summarize the performance along the way
	print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))
# plot model performance for comparison
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.show()

# explore adaboost ensemble learning rate effect on performance
from numpy import mean
from numpy import std
from numpy import arange
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.ensemble import AdaBoostClassifier
from matplotlib import pyplot

# get the dataset
def get_dataset():
	X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=6)
	return X, y

# get a list of models to evaluate
def get_models():
	models = dict()
	# explore learning rates from 0.1 to 2 in 0.1 increments
	for i in arange(0.1, 2.1, 0.1):
		key = '%.3f' % i
		models[key] = AdaBoostClassifier(learning_rate=i)
	return models

# evaluate a given model using cross-validation
def evaluate_model(model, X, y):
	# define the evaluation procedure
	cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
	# evaluate the model and collect the results
	scores = cross_val_score(model, X, y, scoring='accuracy', cv=cv, n_jobs=-1)
	return scores

# define dataset
X, y = get_dataset()
# get the models to evaluate
models = get_models()
# evaluate the models and store results
results, names = list(), list()
for name, model in models.items():
	# evaluate the model
	scores = evaluate_model(model, X, y)
	# store the results
	results.append(scores)
	names.append(name)
	# summarize the performance along the way
	print('>%s %.3f (%.3f)' % (name, mean(scores), std(scores)))
# plot model performance for comparison
pyplot.boxplot(results, labels=names, showmeans=True)
pyplot.xticks(rotation=45)
pyplot.show()

# example of grid searching key hyperparameters for adaboost on a classification dataset
from sklearn.datasets import make_classification
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import AdaBoostClassifier
# define dataset
X, y = make_classification(n_samples=1000, n_features=20, n_informative=15, n_redundant=5, random_state=6)
# define the model with default hyperparameters
model = AdaBoostClassifier()
# define the grid of values to search
grid = dict()
grid['n_estimators'] = [10, 50, 100, 500]
grid['learning_rate'] = [0.0001, 0.001, 0.01, 0.1, 1.0]
# define the evaluation procedure
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
# define the grid search procedure
grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy')
# execute the grid search
grid_result = grid_search.fit(X, y)
# summarize the best score and configuration
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# summarize all scores that were evaluated
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))