import os, sys

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
        return self.name + ": " + self.label + ", " + str(len(self.freq))

def parse_file(f):
    items = []
    with open(f) as data:
        for line in data:
            a = ITEM()
            line = line.split(' ')
            a.set_name(line[0])
            a.set_label(line[1])
            for i in zip(line[2::2], line[3::2]):
                a.add_occur(i[0], i[1])
            items.append(a)
    return items

if __name__ == '__main__':
    print 'This is a naive bayes spam filter!'
    train_data = 'spam/train'
    test_data = 'spam/test'
    print 'training data: ' + train_data
    print 'testing data: ' + test_data

    train_items = parse_file(train_data)
    test_items = parse_file(test_data)
    for i in train_items:
        print i
    print len(train_items)
