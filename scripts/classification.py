import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

seed = 7
np.random.seed(seed)

dataframe = pd.read_csv("/Users/karola/PycharmProjects/ZPI/data/dataset_QL.csv")
X = dataframe.loc[:, 'T':'pR2']
Y = dataframe.loc[:, 'label']


def create_baseline():
    model = Sequential()
    model.add(Dense(30, input_dim=7, kernel_initializer='normal', activation='relu'))
    model.add(Dense())
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


estimator = KerasClassifier(build_fn=create_baseline, epochs=1000, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(estimator, X, Y, cv=kfold)

print("Results: %.2f%% (%.2f%%)" % (results.mean() * 100, results.std() * 100))
