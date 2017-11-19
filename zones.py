import pandas as pd
import sqlalchemy
from sklearn import tree

CONN = sqlalchemy.create_engine('sqlite:///data.db')
shot_charts = pd.read_sql('select * from shot_charts',CONN)

shot_classifier = tree.DecisionTreeClassifier()

training = list(zip(list(shot_charts['LOC_X']),list(shot_charts['LOC_Y'])))
shot_classifier.fit(training, shot_charts['SHOT_ZONE_BASIC'])



def classify_shot(x,y):
    '''
    Will classify the shot using a decision tree. Pass the X and Y
    value here.
    '''
    return shot_classifier.predict([[x,y]])
