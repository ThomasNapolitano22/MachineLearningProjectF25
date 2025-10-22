import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split

airbnbData = pd.read_csv('../finalizedData/finalizedData.csv')


airbnbData_randomized = airbnbData.sample(frac=1, random_state=42)
airbnbData_randomized = airbnbData_randomized.reset_index(drop=True)


X = airbnbData_randomized.drop(columns="price_category")

y = airbnbData_randomized["price_category"]


################################################################################
cat_cols = X.select_dtypes(include=['object']).columns.tolist()


bool_cols = X.select_dtypes(include=['bool']).columns.tolist()
if bool_cols:
    X[bool_cols] = X[bool_cols].astype(int)


X_enc = pd.get_dummies(X, columns=cat_cols, drop_first=True)
############################################################





X_train, X_test, y_train, y_test = train_test_split(X_enc, y, test_size=0.20, random_state=12, shuffle=True)


model = GaussianNB()
model.fit(X_train, y_train)
modelPrediction = model.predict(X_test)

amountCorrect = np.sum(modelPrediction == y_test)
print("Out of " + str (len(y_test)) + " tests. Naive Bayes correctly predicted " + str(amountCorrect) + " of them.")
accuracy = np.sum(y_test == modelPrediction) / modelPrediction.size
print(f"Accuracy of our Naive Bayes Model: {accuracy * 100:.2f}%")


# majority_class = y_test.value_counts().idxmax()
# baseline_accuracy = y_test.value_counts(normalize=True).max()
#
# print("Majority class:", majority_class)
# print("Baseline (majority class) accuracy:", baseline_accuracy)
