import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

airbnbData = pd.read_csv('../finalizedData/finalizedData.csv')
print(airbnbData.columns)

airbnbData_randomized = airbnbData.sample(frac=1, random_state=42)
airbnbData_randomized = airbnbData_randomized.reset_index(drop=True)
print(airbnbData_randomized.columns)

X = airbnbData_randomized.drop(columns="price_category")
print(X.columns)
y = airbnbData_randomized["price_category"]


################################################################################
cat_cols = X.select_dtypes(include=['object']).columns.tolist()


bool_cols = X.select_dtypes(include=['bool']).columns.tolist()
if bool_cols:
    X[bool_cols] = X[bool_cols].astype(int)


X_enc = pd.get_dummies(X, columns=cat_cols, drop_first=True)
############################################################



print(X.head())
print(y.head())

X_train, X_test, y_train, y_test = train_test_split(X_enc, y, test_size=0.20, random_state=12, shuffle=True)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

model = GaussianNB()
model.fit(X_train, y_train)
modelPrediction = model.predict(X_test)

print(modelPrediction)

print(np.sum(modelPrediction == y_test))
accuracy = np.sum(y_test == modelPrediction) / modelPrediction.size
print(accuracy)


# majority_class = y_test.value_counts().idxmax()
# baseline_accuracy = y_test.value_counts(normalize=True).max()
#
# print("Majority class:", majority_class)
# print("Baseline (majority class) accuracy:", baseline_accuracy)
