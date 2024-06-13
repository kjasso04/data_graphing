import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler


df = pd.read_csv("./rowFilter.csv", encoding='latin-1')


df = df.drop(columns=['sample', 'monomer1', 'monomer2'])


y = df['crosslinkermol']


X = df.drop(['crosslinkermol'], axis=1)


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.20, random_state=101)


radForest_Model = RandomForestRegressor(random_state=101, oob_score=True)


param_grid = {
    'n_estimators': [int(x) for x in np.linspace(start=100, stop=500, num=10)],  
    'max_features': ['auto', 'sqrt', 'log2'], 
    'max_depth': [int(x) for x in np.linspace(10, 110, num=11)] + [None],  
    'min_samples_split': [2, 5, 10, 15, ],  
    'min_samples_leaf': [1, 2, 4, 6], 
    'bootstrap': [True, False], 
    'min_weight_fraction_leaf': [0.0, 0.01, 0.02],  
    'min_impurity_decrease': [0.0, 0.01, 0.02],  
    'max_samples': [None, 0.5, 0.75] 
}


rf_Grid = GridSearchCV(estimator=radForest_Model, param_grid=param_grid, cv=2, verbose=2, n_jobs=-1)


rf_Grid.fit(X_train, y_train)


print("Best Parameters Found: ", rf_Grid.best_params_)


best_params = rf_Grid.best_params_
best_radForest_Model = RandomForestRegressor(**best_params, random_state=101, oob_score=True)


best_radForest_Model.fit(X_train, y_train)


print(f'OOB Score - : {best_radForest_Model.oob_score_:.3f}')


print(f'Train R-squared - : {best_radForest_Model.score(X_train, y_train):.3f}')


print(f'Test R-squared - : {best_radForest_Model.score(X_test, y_test):.3f}')
