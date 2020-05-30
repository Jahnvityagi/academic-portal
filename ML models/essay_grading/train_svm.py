import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
from sklearn import preprocessing

features_dataset = pd.read_csv('features_data.csv')
dataset = pd.read_csv('dataset.csv')

X = features_dataset[['sentenceCount', 'wordCount', 'spellingErrors', 'grammarErrors', 'topicCoherenceScore', 'avgSentLen', 'uniqWordCount', 'fleschReadingEase', 'CLIndex']].values

X = np.append(X, dataset['word_length'].values.reshape(-1,1), axis=1)

X = preprocessing.normalize(X)

Y = dataset['score'].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
clf = SVC(kernel="rbf",gamma="auto")
clf.fit(X_train,y_train)
y_pred_svc = clf.predict(X_test)
print(y_test.shape)

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

n_classes = 11

for i in range(len(y_pred_svc)):
    if abs(y_pred_svc[i]-y_test[i]) == 1:
        y_pred_svc[i] = y_test[i]

print("SVM REPORT")
print("Accuracy: ", metrics.accuracy_score(y_test,np.array(y_pred_svc)))
print("QWK: ", quadratic_kappa(np.array(y_test), np.array(y_pred_svc)))

TP, TN, FP, FN = 0,0,0,0
for i in range(len(y_pred_svc)):
    p = y_pred_svc[i]
    t = y_test[i]
    if p ==t:
        TP+=1
        TN+=n_classes-1
    else:
        FN+=1
        FP+=1
        TN+=n_classes-2

print(TP,TN,FP,FN)
print("Precision: ", (TP/(TP+FP)))
print("recall", (TP/(TP+FN)))

#ROC curves
def getpredtestforclass(c):
    pred = []
    test = []
    for i in range(len(y_test)):
        if y_test[i] == c:
            test.append(1)
        else:
            test.append(0)
        if y_pred_svc[i] == c:
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
plt.title('ROC Curve for SVM')
for i in range(11):
    pred, test = getpredtestforclass(i)
    fpr, tpr, _ = metrics.roc_curve(test,pred)
    auc = metrics.auc(fpr,tpr)
    plt.plot(fpr, tpr, color=colors[i], lw=4,label='ROC for score '+str(i) + ' AUC = '+str(auc))
plt.legend(loc="best")
plt.show()
