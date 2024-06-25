import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


def plot_grid_search(cv_results, best_params, name_param_1, name_param_2):
    scores_mean = cv_results['mean_test_score']
    scores_sd = cv_results['std_test_score']
    
    best_param_value = best_params[name_param_2]
    
    _, ax = plt.subplots(1, 1)
    ax.errorbar(cv_results[name_param_1], scores_mean, yerr=scores_sd, fmt='-o', label=f'{name_param_2}: {best_param_value}')
    
    ax.set_title("Grid Search Scores", fontsize=20, fontweight='bold')
    ax.set_xlabel(name_param_1, fontsize=16)
    ax.set_ylabel('CV Average Score', fontsize=16)
    ax.legend(loc="best", fontsize=15)
    ax.grid(True)  

    plt.show()


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
    'n_estimators': [int(x) for x in np.linspace(start=1, stop=400, num=20)],
    'max_depth': [int(x) for x in np.linspace(start=1, stop=40, num=5)] +[None],
    'min_samples_split': [int(x) for x in np.linspace(start=1, stop=40, num=5)],
    'min_samples_leaf': [7],
    'max_features': ['sqrt'], 
    'bootstrap': [True]
}

rf_Grid = GridSearchCV(estimator=radForest_Model, param_grid=param_grid, cv=3, verbose=2, n_jobs=-1)
rf_Grid.fit(X_train, y_train)
best_params = rf_Grid.best_params_


best_radForest_Model = RandomForestRegressor(**best_params, random_state=75, oob_score=True)


best_radForest_Model.fit(X_train, y_train)


print(f'OOB Score - : {best_radForest_Model.oob_score_:.3f}')
print(f'Train R-squared - : {best_radForest_Model.score(X_train, y_train):.3f}')
print(f'Test R-squared - : {best_radForest_Model.score(X_test, y_test):.3f}')


plot_grid_search(rf_Grid.cv_results_, best_params, 'n_estimators', 'max_features')
