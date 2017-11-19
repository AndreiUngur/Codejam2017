import pandas as pd
import sqlalchemy
import pickle
from sklearn import tree

CONN = sqlalchemy.create_engine('sqlite:///data.db')
shot_charts = pd.read_sql('select * from shot_charts',CONN)



def load_classifier():
    try:
        shot_classifier = pickle.load(open('shot_position_classifier.dump','rb'))
    except Exception as e:
        print(e)
        shot_classifier = tree.DecisionTreeClassifier()
        training = list(zip(list(shot_charts['LOC_X']),list(shot_charts['LOC_Y'])))
        shot_classifier.fit(training, shot_charts['SHOT_ZONE_BASIC'])

    pickle.dump(shot_classifier,open('shot_position_classifier.dump','wb'))
    return shot_classifier

shot_classifier = load_classifier()





def classify_shot(x,y):
    '''
    Will classify the shot using a decision tree. Pass the X and Y
    value here.
    '''
    return shot_classifier.predict([[x,y]])
