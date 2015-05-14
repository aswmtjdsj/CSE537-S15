import os, sys, math

class ITEM:
    def __init__(self):
        self.freq = {}

    def set_name(self, name):
        self.name = name

    def set_label(self, label):
        self.label = label

    def add_occur(self, word, freq):
        if word not in self.freq:
            self.freq[word] = freq
        else:
            self.freq[word] += freq

    def __str__(self):
        return self.name + ": " + self.label + ", " + str(len(self.freq))# + ", " + str(self.freq)

def parse_file(f):
    items = []
    with open(f) as data:
        for line in data:
            a = ITEM()
            line = line.strip().split(' ')
            a.set_name(line[0])
            a.set_label(line[1])
            for i in zip(line[2::2], line[3::2]):
                a.add_occur(i[0], int(i[1]))
            items.append(a)
    return items

if __name__ == '__main__':
    print 'This is a naive bayes spam filter!'
    train_data = 'spam/train'
    test_data = 'spam/test'
    print 'training data: ' + train_data
    print 'testing data: ' + test_data

    # parse data
    train_items = parse_file(train_data)
    test_items = parse_file(test_data)

    # train stage
    occur = {}
    for i in train_items:
        for j in i.freq:
            if j not in occur:
                occur[j] = i.freq[j]
            else:
                occur[j] += i.freq[j]
    # print occur
    # print sum([sum(i.values()) for i in map(lambda x: x.freq, train_items)])
    # print sum([occur[i] for i in occur])

    # P(W)
    prior_word_count = {} # word occurrence
    prior_word = {} # word freq 
    prior_tot = sum(occur.values())
    for i in occur:
        prior_word_count[i] = occur[i]
        prior_word[i] = occur[i] * 1. / prior_tot
    print prior_word 

    # P(C)
    prior_class_count = {} # spam/ham class occurrence
    prior_class = {} # spam/ham class frequency
    train_labels = map(lambda x: x.label, train_items)
    for i in set(train_labels):
        prior_class_count[i] = train_labels.count(i)
        prior_class[i] = train_labels.count(i) * 1. / len(train_labels)
    print prior_class

    # P(W|C)
    prior_word_in_class_count = {} # given class, the occurrence of word
    prior_word_in_class = {} # given class, the frequency of word
    for i in prior_class:
        prior_word_in_class_count[i] = {}
        prior_word_in_class[i] = {}

    for i in train_items:
        for j in i.freq:
            if j not in prior_word_in_class_count[i.label]:
                prior_word_in_class_count[i.label][j] = 1
            else:
                prior_word_in_class_count[i.label][j] += 1

    for i in prior_word_in_class_count:
        # prior_i_tot = sum(prior_word_in_class_count[i].values())
        prior_i_tot = prior_class_count[i]
        for j in prior_word_in_class_count[i]:
            prior_word_in_class[i][j] = prior_word_in_class_count[i][j] * 1. / prior_i_tot
        print prior_word_in_class[i]

    # test stage
    # calc P(C|W) = P(W|C) * P(C) / P(W)
    # P(W|C) = PI(P(Wi|C)), P(W) = PI(P(Wi))
    correct = 0
    for i in test_items:
        p_w_c = 1.
        log_p_w_c = math.log(p_w_c)
        p_c = prior_class['spam']
        p_w = 1.
        log_p_w = math.log(p_w)
        cnt = 0
        for j in i.freq:
            if j in prior_word and j in prior_word_in_class['spam']:
                cnt += 1
                #p_w_c *= prior_word_in_class['spam'][j]
                # log_p_w_c += math.log(prior_word_in_class['spam'][j])
                log_p_w_c += math.log(prior_word_in_class['spam'][j] * p_c)
                #p_w *= prior_word[j]
                # log_p_w += math.log(prior_word[j])
                log_p_w += math.log(prior_word_in_class['spam'][j] * prior_class['spam'] + prior_word_in_class['ham'][j] * prior_class['ham'])
        #prob = p_w_c * p_c / p_w
        # prob = math.exp(log_p_w_c + math.log(p_c) - log_p_w)
        prob = math.exp(log_p_w_c - log_p_w)
        if prob > 0.9:
            if i.label == 'spam':
                correct += 1
        else:
            if i.label == 'ham':
                correct += 1
        print i.label, math.exp(log_p_w_c), math.exp(log_p_w), prob
    print 'correct rate: ' + str(correct * 1. / len(test_items))

    pass
    correct = 0
    for i in test_items:
        log_p_w_c = math.log(p_w_c)
        p_c = prior_class['spam']
        log_p_w = math.log(p_w)
        cnt = 0
        a = 0.
        b = 0.
        for j in i.freq:
            if j in prior_word and j in prior_word_in_class['spam']:
                cnt += 1
                log_p_w_c += math.log(prior_word_in_class['spam'][j])
                log_p_w += math.log(prior_word[j])
                log_p_c_w = math.log(prior_word_in_class['spam'][j] * p_c / prior_word[j])
                a += log_p_c_w
                if math.exp(log_p_c_w) > 1:
                    print prior_word_in_class_count['spam'][j]
                    print p_c
                    print prior_word_in_class['spam'][j]
                    print prior_word_count[j]
                    print prior_word[j]
                    print math.exp(log_p_c_w)
                b += math.log((1 - math.exp(log_p_c_w)))
        a += math.log(p_c)
        b += math.log(1 - p_c)
        prob = math.exp(a) / (math.exp(a) + math.exp(b))
        # prob = math.exp(log_p_w_c + math.log(p_c) - log_p_w)
        if prob > 0.9:
            if i.label == 'spam':
                correct += 1
        else:
            if i.label == 'ham':
                correct += 1
    print correct * 1. / len(test_items)
