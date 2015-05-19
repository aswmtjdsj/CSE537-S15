import os, sys

class DecisionTree():
    '''
    Decision Tree Class
    '''
    def __init__(self):
        self.train_data = []

        self.tree = None
        self.size = None

        self.dimension = None
        self.feature_sets = []

        self.debug = True

    def load(self, f_d, f_l):
        f_d = open(f_d, 'r')
        f_l = open(f_l, 'r')
        data = [map(int, i) for i in map(lambda x: x.strip().split(' '), f_d.read().strip().split('\n'))] # turn data line into feature list
        label = map(bool, map(int, f_l.read().strip().split())) # turn label line into bool label
        # print len(data), len(label)
        self.size = len(data)
        for i in range(self.size):
            if self.dimension == None: # init dimensionality
                self.dimension = len(data[i])
                self.feature_sets = [None] * self.dimension
            for j in range(self.dimension): 
                if self.feature_sets[j] == None:
                    self.feature_sets[j] = set([data[i][j]])
                elif data[i][j] not in self.feature_sets[j]:
                    self.feature_sets[j].add(data[i][j])
            if len(data[i]) != self.dimension: # check missing features
                raise Exception('data dimension not match: {0} (dimension) and {1} (new data item dimension)'.format(self.dimension, len(data[i])))
            self.train_data.append((data[i], label[i]))
        f_d.close()
        f_l.close()

    def build(self):
        pass

    def test(self, test_data):
        if self.tree == None:
            raise Exception('No tree trained yet!')

    def __str__(self):
        if self.size == None:
            return 'tree not built'
        else:
            if False and self.debug:
            # if self.debug:
                for i in self.train_data:
                    print "data {{{0}}}: {1}".format(i[0], i[1])
            return 'tree size: {0}, dimension: {1}\nfeature set: {2}'.format(self.size, self.dimension, self.feature_sets)

if __name__ == '__main__':
    f_train_data = 'clickstream/trainfeat.csv'
    f_train_label = 'clickstream/trainlabs.csv'
    f_test_data = 'clickstream/testfeat.csv'
    f_test_label = 'clickstream/testlabs.csv'

    dt = DecisionTree()
    dt.load(f_train_data, f_train_label)
    print dt
