import re
from collections import Counter
import numpy as np
import os
import sys

class MarkovChain:
    def __init__(self,data):
        self.stopwords = {'', 'they', 'whom', 'will', 'don', 'here', 'an', 'out', 'then', 'same', 'again', 'most', 'him', 'his', 'can', 'be', 'you', 'have', 'from',
                     'if', 'nor', 'off', 'into', 'until', 'now', 'before', 'we', 'hers', 'itself', 'she', 'while', 'too', 'as', 'been', 'or', 'so', 'do', 'more',
                     'myself', 'with', 'what', 'but', 'above', 'has', 'down', 'why', 'yours', 't', 'ourselves', 'up', 'of', 'its', 'there', 'to', 'their', 'being',
                     'all', 'herself', 'further', 'through', 'once', 'am', 'who', 'he', 'for', 'on', 'very', 'your', 'under', 'the', 'in', 'me', 'between', 'over',
                     'her', 'having', 'other', 'are', 'where', 'below', 'each', 'than', 'should', 'these', 'a', 'own', 's', 'few', 'which', 'such', 'that', 'yourself',
                     'because', 'any', 'this', 'both', 'themselves', 'only', 'is', 'my', 'during', 'at', 'it', 'no', 'them', 'not', 'was', 'himself', 'those','i', 'just',
                     'and', 'about', 'theirs', 'when', 'after', 'how', 'ours', 'by', 'does', 'some', 'doing', 'were', 'against', 'yourselves', 'did', 'our', 'had'}

        self.unigram_probs = {}
        self.bigram_probs = {}
        self.trigram_probs = {}
        self.unigram_counts = {}
        self.bigram_counts = {}
        self.trigram_counts = {}
        self.unigrams = []
        self.bigrams = []
        self.trigrams = []
        for i in range(len(data)):
            data[i] = [x.lower() for x in re.findall(r'[a-zA-Z0-9]+',data[i]) if x not in self.stopwords]

        self.texts = data

        self.unigrams = self.ngrams(1,self.texts)
        self.bigrams = self.ngrams(2,self.texts)
        self.trigrams = self.ngrams(3,self.texts)

    def ngrams(self,n,data):
        ngrams = []
        for i in range(len(data)):
            for j in range(len(data[i])-n+1):
                ngrams.append([data[i][k] for k in range(j,j+n)])

        return ngrams

    def ngram_counts(self):
        self.unigram_counts = Counter([x[0] for x in self.unigrams])

        self.bigram_counts = Counter([x[0]+','+x[1] for x in self.bigrams])

        self.trigram_counts = Counter([x[0]+','+x[1]+','+x[2] for x in self.trigrams])

    def solve_unigrams(self):
        for i in self.unigrams:
            if str(i[0]) in self.unigram_probs.keys():
                continue

            self.unigram_probs[str(i[0])] = self.unigram_counts[i[0]]/len(self.unigrams)

    def solve_bigrams(self):
        total = {}
        for i in self.unigram_counts.keys():
            total[i] = 0

        for i in self.bigrams:
            total[i[0]] += 1
            
        for i in self.bigrams:
            if str(i) in self.bigram_probs.keys():
                continue

            self.bigram_probs[str(i)] = self.bigram_counts[i[0]+','+i[1]]/total[i[0]]

    def solve_trigrams(self):
        total = {}
        for i in self.bigram_counts.keys():
            total[i] = 0

        for i in self.trigrams:
            total[i[0]+','+i[1]] += 1
        
        for i in self.trigrams:
            if str(i) in self.trigram_probs.keys():
                continue

            self.trigram_probs[str(i)] = self.trigram_counts[i[0]+','+i[1]+','+i[2]]/total[i[0]+','+i[1]]

    def generate_sequence(self):
        num_sequences = 0
        all_sequences = []
        all_sequence_probs = []
        while(num_sequences<10):
            sequence = []
            sequence_probs = []
            random_unigram = np.random.choice(list(self.unigram_probs.keys()),p = [self.unigram_probs[x] for x in self.unigram_probs.keys()])

            sequence.append(random_unigram)
            sequence_probs.append(self.unigram_probs[random_unigram])

            available_bigrams = [x for x in self.bigram_counts.keys() if x.split(',')[0] == random_unigram]

            if available_bigrams == []:
                continue
            
            random_bigram = np.random.choice(available_bigrams,p = [self.bigram_probs["['"+x.split(',')[0]+"', '"+x.split(',')[1]+"']"] for x in available_bigrams]).split(',')

            sequence.append(random_bigram[-1])
            sequence_probs.append(self.bigram_probs["['"+random_bigram[0]+"', '"+random_bigram[1]+"']"])

            count = 0
            while count<18:
                count += 1
                available_trigrams = [x for x in self.trigram_counts.keys() if x.split(',')[0] == random_bigram[0] and x.split(',')[1] == random_bigram[1]]

                if available_trigrams == []:
                    break
                random_trigram = np.random.choice(available_trigrams,p = [self.trigram_probs["['"+x.split(',')[0]+"', '"+x.split(',')[1]+"', '"+x.split(',')[2]+"']"] for x in available_trigrams]).split(',')
                sequence.append(random_trigram[-1])
                sequence_probs.append(self.trigram_probs["['"+random_trigram[0]+"', '"+random_trigram[1]+"', '"+random_trigram[2]+"']"])

                random_bigram = random_trigram[1:]

            all_sequences.append(sequence)
            all_sequence_probs.append(sequence_probs)
            num_sequences += 1

        return all_sequences,all_sequence_probs

    def evaluate(self,author2,sequences):
        evaluation_probs = []
        for sequence in sequences:
            prob = []
            min_unigram_prob = min(author2.unigram_probs[x] for x in author2.unigram_probs.keys())/2
            min_bigram_prob = min(author2.bigram_probs[x] for x in author2.bigram_probs.keys())/2
            min_trigram_prob = min(author2.trigram_probs[x] for x in author2.trigram_probs.keys())/2
            
            if sequence[0] in author2.unigram_probs.keys():
                prob.append(author2.unigram_probs[sequence[0]])
            else:
                prob.append(min_unigram_prob)

            if len(sequence)>1:
                if "['"+sequence[0]+"', '"+sequence[1]+"']" in author2.bigram_probs.keys():
                    prob.append(author2.bigram_probs["['"+sequence[0]+"', '"+sequence[1]+"']"])
                else:
                    prob.append(min_bigram_prob)

                for i in range(2,len(sequence)-2):
                    if "['"+sequence[i]+"', '"+sequence[i+1]+"', '"+sequence[i+2]+"']" in author2.trigram_probs.keys():
                        prob.append(author2.trigram_probs["['"+sequence[i]+"', '"+sequence[i+1]+"', '"+sequence[i+2]+"']"])

                    else:
                        prob.append(min_trigram_prob)

            evaluation_probs.append(prob)
        return evaluation_probs

if __name__ == '__main__':
    path = sys.argv[1]
    path2 = sys.argv[2]

    books = os.listdir(path)
    books2 = os.listdir(path2)

    texts = []
    for book in books:
        with open(path+book,'r') as f:
            data = f.read().split('\n\n')

        texts = texts+data

    texts2 = []
    for book in books2:
        with open(path2+book,'r') as f:
            data = f.read().split('\n\n')

        texts2 = texts2+data

    author1 = MarkovChain(texts)
    author2 = MarkovChain(texts2)

    author1.ngram_counts()
    author1.solve_unigrams()
    author1.solve_bigrams()
    author1.solve_trigrams()

    author2.ngram_counts()
    author2.solve_unigrams()
    author2.solve_bigrams()
    author2.solve_trigrams()

    sequences,sequence_probs = author1.generate_sequence()
    sequences2,sequence_probs2 = author2.generate_sequence()

    evaluation_probs = author1.evaluate(author2,sequences)
    evaluation_probs2 = author2.evaluate(author1,sequences2)
    
    final_probs = []
    final_probs2 = []
    final_evaluation_probs = []
    final_evaluation_probs2 = []

    for i in range(len(sequences)):
        prob1 = 1
        prob2 = 1
        prob3 = 1
        prob4 = 1
        for j in sequence_probs[i]:
            prob1 *= j
        for j in sequence_probs2[i]:
            prob2 *= j
        for j in evaluation_probs[i]:
            prob3 *= j
        for j in evaluation_probs2[i]:
            prob4 *= j
        final_probs.append(prob1)
        final_probs2.append(prob2)
        final_evaluation_probs.append(prob3)
        final_evaluation_probs2.append(prob4)

    with open(sys.argv[3]+'.txt','w') as f:
        f.write('Unigram probabilities: \n')
        for i in author1.unigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')
        f.write('\n')
        f.write('Bigram probabilities: \n')
        for i in author1.bigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')
        f.write('\n')
        f.write('Trigram probabilities: \n')
        for i in author1.trigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')

    with open(sys.argv[4]+'.txt','w') as f:
        f.write('Unigram probabilities: \n')
        for i in author2.unigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')
        f.write('\n')
        f.write('Bigram probabilities: \n')
        for i in author2.bigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')
        f.write('\n')
        f.write('Trigram probabilities: \n')
        for i in author2.trigram_probs.items():
            f.write(str(i[0])+' : '+str(i[1])+'\n')

    with open(sys.argv[5]+'.txt','w') as f:
        f.write("Sequences of author 1:- \n")
        for i in range(len(sequences)):
            sequence = ''
            for j in sequences[i]:
                sequence = sequence+j+' '
            f.write('Sequence '+str(i+1)+':\n'+sequence+'\n')
            f.write("Probability of the sequence based on model of the same author is: "+str(final_probs[i])+'\n')
            f.write("Probability of the sequence based on model of author 2 is: "+str(final_evaluation_probs[i])+'\n\n')

        f.write('\n')
        f.write("Sequences of author 2:- \n")
        for i in range(len(sequences2)):
            sequence = ''
            for j in sequences2[i]:
                sequence = sequence+j+' '
            f.write('Sequence '+str(i+1)+':\n'+sequence+'\n')
            f.write("Probability of the sequence based on model of the same author is: "+str(final_probs2[i])+'\n')
            f.write("Probability of the sequence based on model of author 1 is: "+str(final_evaluation_probs2[i])+'\n\n')
