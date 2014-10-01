#Training classifier (first argument to the script) against a train_path (second argument)

from my_fun import *
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sys

train_path = sys.argv[1]

clfRandom = RandomForestClassifier(n_estimators=95)
print "clfRandom created"

clfRandom = train_obj(train_path, clfRandom)
#9 stands for maximum compression
joblib.dump(clfRandom, "forest.xml", 9)
