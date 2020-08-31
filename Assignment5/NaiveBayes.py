import csv
import re
import sys

class NaiveBayes:
    feature_prior_probs = []
    feature_likelihood_probs = []
    
    def train_model(self,training_dataset):
        feature_values = []
        index = 0
        while(index<len(training_dataset[0])):
            feature_values.append(list(set([training_dataset[i][index] for i in range(1,len(training_dataset))])))
            index += 1

        feature_prior_probs = []
        feature_likelihood_probs = []
        feature = 0
        while(feature<len(training_dataset[0])):
            temp = {}
            temp1 = {}
            for i in feature_values[feature]:
                temp[i] = 0
                temp1[i+'|'+'0'] = 0
                temp1[i+'|'+'1'] = 0
                
            feature_prior_probs.append(temp)
            feature_likelihood_probs.append(temp1)
            feature += 1

        feature_likelihood_probs = feature_likelihood_probs[:-1]

        feature = 0
        while(feature<len(feature_prior_probs)):
            count = 0
            for i in range(1,len(training_dataset)):
                feature_prior_probs[feature][training_dataset[i][feature]] += 1
                count += 1

            for key in feature_prior_probs[feature].keys():
                feature_prior_probs[feature][key] = round(feature_prior_probs[feature][key]/count,3)
            feature += 1

        feature = 0
        while(feature<len(feature_likelihood_probs)):
            count = {'0':0,'1':0}
            for i in range(1,len(training_dataset)):
                feature_likelihood_probs[feature][training_dataset[i][feature]+'|'+training_dataset[i][-1]] += 1
                count[training_dataset[i][-1]] += 1

            for key in feature_likelihood_probs[feature].keys():
                label = key.split('|')[1]
                feature_likelihood_probs[feature][key] = round(feature_likelihood_probs[feature][key]/count[label],3)
            feature += 1

        self.feature_prior_probs = feature_prior_probs
        self.feature_likelihood_probs = feature_likelihood_probs

    def predict(self,data):
        prediction = []
        for i in range(1,len(data)):
            positive_prob = self.feature_prior_probs[-1]['1']
            negative_prob = self.feature_prior_probs[-1]['0']
            for feature in range(len(data[i])-1):
                positive_prob = positive_prob * self.feature_likelihood_probs[feature][data[i][feature]+'|1']
                negative_prob = negative_prob * self.feature_likelihood_probs[feature][data[i][feature]+'|0']

            prob = round(positive_prob/(positive_prob+negative_prob),2)
            if prob >= 0.50:
                prediction.append(1)
            else:
                prediction.append(0)
                    
        return prediction

    def evaluate(self,X,y):
        count = 0
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(len(X)):
            if X[i]==y[i]:
                count += 1
            if X[i]==y[i] == 1:
                TP += 1
            elif X[i] != y[i] and y[i]==1:
                FP += 1
            elif X[i] != y[i] and y[i]==0:
                FN +=1
            else:
                TN += 1

        accuracy = count/len(X)
        matrix = []
        matrix.append(['TP = '+str(TP),'FN = '+str(FN)])
        matrix.append(['FP = '+str(FP),'TN = '+str(TN)])
        return accuracy,matrix

    def test(self,test_dataset):
        predictions = self.predict(test_dataset)
        X = [int(test_dataset[x][-1]) for x in range(1,len(test_dataset))]
        accuracy,confusion_matrix = self.evaluate(X,predictions)

        print("Model Accuracy: ",accuracy)
        print("Confusion Matrix: ")
        for i in confusion_matrix:
            print(i)
            
        return accuracy,confusion_matrix,X,predictions

if __name__ == '__main__':
    training_dataset = []
    test_dataset = []
    with open(sys.argv[1]+'.csv',newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            training_dataset.append(row)

    with open(sys.argv[2]+'.csv',newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in reader:
            test_dataset.append(row)

    bayes = NaiveBayes()
    bayes.train_model(training_dataset)
    accuracy,confusion_matrix,actual_values,predictions = bayes.test(test_dataset)

    with open(sys.argv[3]+'.txt','w') as f:
        f.write('Prior probabilities of each feature are: \n')
        for i in range(len(bayes.feature_prior_probs) - 1):
            f.write("Feature '"+training_dataset[0][i]+"' = \n"+str(bayes.feature_prior_probs[i])+'\n')
        f.write('\n')
        f.write('Output prior probabilities: \n')
        f.write(str(bayes.feature_prior_probs[-1])+'\n\n')
        f.write('Likelihood probabilities of each feature are: \n')
        for i in range(len(bayes.feature_likelihood_probs)):
            f.write("Feature '"+training_dataset[0][i]+"' = \n"+str(bayes.feature_likelihood_probs[i])+'\n')

    with open(sys.argv[4]+'.txt','w') as f:
        f.write('Actual values are: \n'+str(actual_values)+'\n\nPrediced values are: \n'+str(predictions)+'\n\n')
        f.write('Model Accuracy : '+str(accuracy)+'\n\n')
        f.write('Confusion matrix : \n')
        for i in confusion_matrix:
            f.write(str(i)+'\n')
