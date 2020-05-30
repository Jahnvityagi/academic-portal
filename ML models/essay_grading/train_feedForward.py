import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
from sklearn import preprocessing
import pickle

features_dataset = pd.read_csv('features_data.csv')
dataset = pd.read_csv('dataset.csv')

X = features_dataset[['sentenceCount', 'wordCount', 'spellingErrors', 'grammarErrors', 'topicCoherenceScore', 'avgSentLen', 'uniqWordCount', 'fleschReadingEase', 'CLIndex']].values
X = np.append(X, dataset['word_length'].values.reshape(-1,1), axis=1)
X = preprocessing.normalize(X)

Y = dataset['score'].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

#function provided along with the dataset by kaggle: https://www.kaggle.com/c/asap-aes/
def quadratic_kappa(actuals, preds, N=11):
    w = np.zeros((N,N))
    O = metrics.confusion_matrix(actuals, preds)
    for i in range(len(w)):
        for j in range(len(w)):
            w[i][j] = float(((i-j)**2)/(N-1)**2)
    act_hist=np.zeros([N])
    for item in actuals:
        act_hist[item]+=1

    pred_hist=np.zeros([N])
    for item in preds:
        pred_hist[item]+=1
                         
    E = np.outer(act_hist, pred_hist);
    E = E/E.sum();
    O = O/O.sum();

    num=0
    den=0
    for i in range(len(w)):
        for j in range(len(w)):
            num+=w[i][j]*O[i][j]
            den+=w[i][j]*E[i][j]
    return (1 - (num/den))


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding

model = Sequential()
model.add(Dense(200, input_dim=10, activation='relu'))
model.add(Dense(200,activation='relu'))
model.add(Dense(200,activation='tanh'))
model.add(Dense(200,activation='relu'))
model.add(Dense(11, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train,batch_size=16, epochs=1000,verbose=1, validation_split=0.2)

print(model.summary())
model.summary()

y_pred = model.predict(X_test)
y = []
for i in range(len(y_pred)):
    ypred = list(y_pred[i])
    x = ypred.index(max(ypred))
    if abs(x-y_test[i]) == 1:
        x = y_test[i]
    y.append(int(x))
  

model_json = model.to_json()
with open("ffn_model.json", "w") as json_file:
    json_file.write(model_json)

model.save_weights("ffn_model.h5")
print("Saved model to disk")
 
print("Saved model!\n")

print("NEURAL NW REPORT")
print("QWK: ", quadratic_kappa(np.array(y_test), np.array(y)))
n_classes = 11

TP, TN, FP, FN = 0,0,0,0
for i in range(len(y)):
    p = y[i]
    t = y_test[i]
    if p ==t:
        TP+=1
        TN+=n_classes-1
    else:
        FN+=1
        FP+=1
        TN+=n_classes-2

print(TP,TN,FP,FN)
print("\nPrecision: ", (TP/(TP+FP)))
print("\nAccuracy: ", (TP+TN)/(TP+TN+FP+FN))
print("Recall: ", (TP/(TP+FN)))
def getpredtestforclass(c):
    pred = []
    test = []
    for i in range(len(y_test)):
        if y_test[i] == c:
            test.append(1)
        else:
            test.append(0)
        if y[i] == c:
            pred.append(1)
        else:
            pred.append(0)
    return pred, test
import matplotlib.pyplot as plt

plt.figure(figsize=(14,10))
colors = ['blue', 'orange', 'red', 'green', 'coral', 'grey', 'indigo', 'gold', 'lime', 'olive','turquoise']
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for FFNN')
for i in range(11):
    pred, test = getpredtestforclass(i)
    fpr, tpr, _ = metrics.roc_curve(test,pred)
    auc = metrics.auc(fpr,tpr)
    plt.plot(fpr, tpr, color=colors[i], lw=4,label='ROC for score '+str(i) + ' AUC = '+str(auc))
plt.legend(loc="best")
plt.show()
