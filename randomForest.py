import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("./rowFilter.csv", encoding='latin-1')

df = df.drop(columns=['sample', 'monomer1', 'monomer2'])

y = df['crosslinkermol']
X = df.drop(['crosslinkermol'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

radForest_Model = RandomForestRegressor(random_state=25)
param_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=1, stop=400, num=30)],
    'max_depth': [int(x) for x in np.linspace(start=1, stop=40, num=20)] +[None],
    'min_samples_split': [int(x) for x in np.linspace(start=1, stop=40, num=20)],
    'min_samples_leaf': [1,2,3,4,5,6,7,8,9,10],
    'max_features': ['sqrt'],  
    'bootstrap': [True]
}

# {'bootstrap': True, 'max_depth': 9, 'max_features': 'sqrt', 'min_samples_leaf': 1, 'min_samples_split': 2, 'n_estimators': 297}

rf_Grid = GridSearchCV(estimator=radForest_Model, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)
rf_Grid.fit(X_train, y_train)
best_params = rf_Grid.best_params_

best_radForest_Model = RandomForestRegressor(**best_params,random_state=75, oob_score=True)

best_radForest_Model.fit(X_train, y_train)


oob_score = best_radForest_Model.oob_score_
train_r2 = best_radForest_Model.score(X_train, y_train)
test_r2 = best_radForest_Model.score(X_test, y_test)

print(f'OOB Score - : {best_radForest_Model.oob_score_:.3f}')
print(f'Train R-squared - : {best_radForest_Model.score(X_train, y_train):.3f}')
print(f'Test R-squared - : {best_radForest_Model.score(X_test, y_test):.3f}')
