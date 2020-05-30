actuals = [100,100,100,100,100,92,96,93,98,94,91,95,91,97,95,0,0,0,0,0]

seq = [100,100,100,100,100,92.87,97.07,92.89,98.74,84.53,86.91,86.59,75.82,79.02,80.68,0.66,0.8,0.9,1.5,1.47]

jac = [100,100,100,100,100,93.45,96.33,93.29,97.53,94.44,93.28,96.50,93.12,97.35,94.44,10.21,10.84,11.93,10.72,10.86]

cos = [99.99,99.99,99.99,99.99,99.99,99.94,99.96,99.94,99.97,99.96,99.93,99.96,99.94,99.97,99.96,93.3,92.3,92.9,92.8,93.8]


from sklearn import metrics

print(metrics.mean_absolute_error(actuals, seq))
print(metrics.mean_absolute_error(actuals, jac))
print(metrics.mean_absolute_error(actuals, cos))

print(metrics.mean_squared_error(actuals, seq))
print(metrics.mean_squared_error(actuals, jac))
print(metrics.mean_squared_error(actuals, cos))

def regression_to_classification(arr):
    for i in range(len(arr)):
        if arr[i]>75:
            arr[i] = 1
        else:
            arr[i]=0


regression_to_classification(seq)
regression_to_classification(jac)
regression_to_classification(cos)
regression_to_classification(actuals)
print(metrics.accuracy_score(actuals, seq))
print(metrics.accuracy_score(actuals, jac))
print(metrics.accuracy_score(actuals, cos))
print(metrics.precision_score(actuals, seq))
print(metrics.precision_score(actuals, jac))
print(metrics.precision_score(actuals, cos))
print(metrics.recall_score(actuals, seq))
print(metrics.recall_score(actuals, jac))
print(metrics.recall_score(actuals, cos))
print(metrics.f1_score(actuals, seq))
print(metrics.f1_score(actuals, jac))
print(metrics.f1_score(actuals, cos))
print(metrics.confusion_matrix(actuals, seq))
print(metrics.confusion_matrix(actuals, jac))
print(metrics.confusion_matrix(actuals, cos))
print(metrics.roc_auc_score(actuals, seq))
print(metrics.roc_auc_score(actuals, jac))
print(metrics.roc_auc_score(actuals, cos))

import matplotlib.pyplot as plt

fpr,tpr, _ = metrics.roc_curve(actuals,seq)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=5,label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy',  linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve - SEQUENCE MATCHER')
plt.legend(loc="lower right")
plt.show()

fpr,tpr, _ = metrics.roc_curve(actuals,jac)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=5,label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy',  linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve - JACCARD')
plt.legend(loc="lower right")
plt.show()


fpr,tpr, _ = metrics.roc_curve(actuals,cos)
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=5,label='ROC curve')
plt.plot([0, 1], [0, 1], color='navy',  linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve - COSINE')
plt.legend(loc="lower right")
plt.show()
