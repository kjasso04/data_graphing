import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import matplotlib.pyplot as plt

print("Loading CSV file...")
df = pd.read_csv("./rowFilter.csv", encoding='latin-1')
print("CSV file loaded successfully.")

df = df.drop(columns=['sample', 'monomer1', 'monomer2'])

y = df['crosslinkermol']
X = df.drop(['crosslinkermol'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsRegressor(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Initial model performance:")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)


k_values = list(range(1, 31))
scores = []


X_scaled = scaler.fit_transform(X)

for k in k_values:
    knn = KNeighborsRegressor(n_neighbors=k)
    score = cross_val_score(knn, X_scaled, y, cv=5, scoring='r2')
    scores.append(np.mean(score))


sns.lineplot(x=k_values, y=scores, marker='o')
plt.xlabel("K Values")
plt.ylabel("R2 Score")
plt.title("KNN Regressor Performance")
plt.show()


best_index = np.argmax(scores)
best_k = k_values[best_index]


knn = KNeighborsRegressor(n_neighbors=best_k)
knn.fit(X_train, y_train)


y_pred = knn.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Final model performance with best K value:")
print("Best K:", best_k)
print("Mean Squared Error:", mse)
print("R2 Score:", r2)
print("")

y_train_pred = knn.predict(X_train)


train_mse = mean_squared_error(y_train, y_train_pred)
train_r2 = r2_score(y_train, y_train_pred)

print("Training data performance:")
print("Mean Squared Error:", train_mse)
print("R2 Score:", train_r2)

print("")

print("Test data performance:")
print("Mean Squared Error:", mse)
print("R2 Score:", r2)
