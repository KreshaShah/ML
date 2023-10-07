# -*- coding: utf-8 -*-
"""ML-Exp2_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13TXJMxl_WI5zhLAJaskZj7znqgY02BkV
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import LabelEncoder

class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value

class DecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, min_impurity_decrease=0):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_impurity_decrease = min_impurity_decrease

    def fit(self, X, y):
      self.n_classes = len(set(y))
      self.n_features = 4
      self.tree = self._grow_tree(X, y)

    def predict(self, X):
        return [self._predict(inputs) for inputs in X]

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_labels = len(set(y))

        if (depth >= self.max_depth
            or n_samples < self.min_samples_split
            or n_labels == 1):
            return Node(value=self._most_common_label(y))

        best_feature, best_threshold = self._best_criteria(X, y)
        left_idx, right_idx = self._split(X[:, best_feature], best_threshold)
        left = self._grow_tree(X[left_idx, :], y[left_idx], depth+1)
        right = self._grow_tree(X[right_idx, :], y[right_idx], depth+1)

        return Node(feature=best_feature, threshold=best_threshold, left=left, right=right)

    def _best_criteria(self, X, y):
        best_gain = -1
        split_idx, split_threshold = None, None

        n_samples, n_features = X.shape
        entropy_parent = self._entropy(y)

        for feature_idx in range(n_features):
            feature_vals = X[:, feature_idx]
            thresholds = np.unique(feature_vals)

            for threshold in thresholds:
                left_idx, right_idx = self._split(feature_vals, threshold)
                if len(left_idx) == 0 or len(right_idx) == 0:
                    continue

                entropy_left = self._entropy(y[left_idx])
                entropy_right = self._entropy(y[right_idx])
                info_gain = entropy_parent - ((len(left_idx) / n_samples) * entropy_left
                                              + (len(right_idx) / n_samples) * entropy_right)

                if info_gain > best_gain:
                    best_gain = info_gain
                    split_idx = feature_idx
                    split_threshold = threshold

        if best_gain < self.min_impurity_decrease:
            return None, None

        return split_idx, split_threshold

    def _split(self, feature_vals, threshold):
        left_idx = np.argwhere(feature_vals <= threshold).flatten()
        right_idx = np.argwhere(feature_vals > threshold).flatten()
        return left_idx, right_idx

    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / np.sum(hist)
        return -np.sum([p * np.log2(p) for p in ps if p > 0])

    def _most_common_label(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common

    def _predict(self, inputs):
        node = self.tree
        while node.value is None:
            if inputs[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value

data = pd.read_csv('/content/drive/MyDrive/SEM 4/play_tennis.csv')
for col in data.columns:
    if data[col].dtype == 'object':
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTree(max_depth=5)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
for i in range(len(y_pred)):
    print(f"Prediction: {y_pred[i]}, Actual: {y_test[i]}")

from sklearn.tree import DecisionTreeClassifier, export_text

# Create a decision tree classifier
clf = DecisionTreeClassifier()

# Train the model using the training sets
clf.fit(X_train[:, :-1], y_train)

# Print the decision tree as text
tree_text = export_text(clf, feature_names=['outlook', 'temp', 'humidity', 'windy'])
print(tree_text)

from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

data = pd.read_csv('/content/drive/MyDrive/play_tennis.csv')
for col in data.columns:
    if data[col].dtype == 'object':
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Train decision tree model
clf = DecisionTreeClassifier(max_depth=6, random_state=42)
clf.fit(X_train[:, :-1], y_train)
# Plot the decision tree
plt.figure(figsize=(12,12))
plot_tree(clf, feature_names=['outlook', 'temp', 'humidity', 'windy'], filled=True)
plt.show()