import os, sys
import math
import random
import chi2
from decimal import Decimal, getcontext

NODE_TYPE = ['DS', 'LS', 'ES', 'MIG'] # all data same, all label same, early stopped, maximum information gain

class TreeNode():
    def __init__(self):
        self.feature_id = None
        self.children = []
        self.end_node = False
        self.node_type = None
        self.split = [0, 0]
        self.label = None
        self.value = None

    def __str__(self):
        return str({'feature_id': self.feature_id,
                'children': self.children,
                'node_type': self.node_type,
                'split': self.split,
                'label': self.label,
                'value': self.value})

class DecisionTree():
    '''
    Decision Tree Class
    '''
    def __init__(self, p_thre, deb):
        '''
        init tree with threshold and debug option
        '''
        self.train_data = [] # training data
        self.size = None # size of tree nodes
        self.dimension = None # size of features of training data
        self.root = None # root of the tree
        self.p_threshold = p_thre # threshold for chi-square test
        self.debug = deb # debug or not

    def build(self):
        '''
        wrapper for training procedure
        '''
        self.root = self._build(self.train_data)

    def _build(self, train_data):
        '''
        recursive training procedure, splitting nodes based on conditions
        '''

        data = map(lambda x: x[0], train_data)
        label = map(lambda x: x[1], train_data)

        node_end = False 
        node_type = None
        node = TreeNode()

        label_set = set(label)
        node.split[0] = len(filter(lambda x: x == bool(0), label))
        node.split[1] = len(filter(lambda x: x == bool(1), label))

        if len(label_set) == 1: # all labels are the same
            node_end = True
            node.node_type = NODE_TYPE[1]
            node.label = list(label_set)[0]
            node.end_node = True
            return node

        # count data on different features
        feature_count = [None] * self.dimension # dict for the number of data as for different features
        for i in range(len(data)):
            for j in range(self.dimension): 
                if feature_count[j] == None:
                    feature_count[j] = {data[i][j]: [0, 0]} # list(label_set)}# [0, 0]}
                elif data[i][j] not in feature_count[j]:
                    feature_count[j][data[i][j]] = [0, 0] # list(label_set)
                feature_count[j][data[i][j]][int(label[i])] += 1

        all_feature_same = filter(lambda x: len(x) > 1, feature_count)
        if len(all_feature_same) == 0:
            node.end_node = True
            node.node_type = NODE_TYPE[0]
            return node

        # calculate information gain by calculating entropy
        # well, this is somehow redundant calculation, need improvement

        # H(X) = -sum(p(x) * log(p(x))), x belongs to X
        h_x = sum(map(lambda x: - (x * 1. / len(label)) * math.log(x * 1. / len(label)) if x != 0 else 0., node.split))
        # print 'h_x: {0}'.format(h_x), [len(filter(lambda x: x == i, label)) for i in label_set]

        # IG(X, Y) = H(X) - sigma( C(Y) / C(X) * H(Y))
        ig_x_y = [None] * self.dimension
        for i in range(self.dimension):
            if len(feature_count[i]) == 1:
                ig_x_y[i] = 0.
                continue

            h_y = 0
            for j in feature_count[i].keys():
                num_example = sum(feature_count[i][j])
                h_x_y = 0
                for l in label_set:
                    if feature_count[i][j][l] > 0:
                        p = feature_count[i][j][l] * 1. / num_example
                        h_x_y += -p * math.log(p)
                h_y += num_example * 1. / len(label) * h_x_y
            ig_x_y[i] = h_x - h_y
            # print feature_count[i], ig_x_y[i]
        # print max(ig_x_y), ig_x_y.index(max(ig_x_y)), feature_count[ig_x_y.index(max(ig_x_y))]

        if max(ig_x_y) < 1e-6: # feature impossible to be divided
            node.end_node = True
            node.node_type = NODE_TYPE[0]
            return node

        node.feature_id = ig_x_y.index(max(ig_x_y))
        for j in feature_count[node.feature_id]:
            sub_data = filter(lambda x: x[0][node.feature_id] == j, train_data)
            # print 'sub_data: {0}'.format(sub_data)
            node.children.append(self._build(sub_data))
            node.children[-1].value = j

        node.node_type = NODE_TYPE[3]
        return node

    def chi(self):
        if self.root == None:
            raise Exception('No tree trained yet!')

        result = None
        if self.root.node_type == 'MIG' and self._chi(self.root) == True:
            self.root.node_type = 'ES'
            self.root.label = False if self.root.split[0] > self.root.split[1] else True
            self.root.children = None

    def _chi(self, node):
        if node.children != None:
            for i in range(len(node.children)):
                if node.children[i].node_type == 'MIG' and self._chi(node.children[i]) == True:
                    node.children[i].node_type = 'ES'
                    node.children[i].label = False if node.children[i].split[0] > node.children[i].split[1] else True
                    node.children[i].children = None

            n = node.split[0] * 1.
            p = node.split[1] * 1.
            N = n + p
            s = Decimal('0.')
            for i in range(len(node.children)):
                _p = Decimal(sum(node.children[i].split) * p / N)
                _n = Decimal(sum(node.children[i].split) * n / N)
                s += Decimal(getcontext().power((_p - node.children[i].split[1]), 2) / _p)
                s += Decimal(getcontext().power((_n - node.children[i].split[0]), 2) / _n)
            if chi2.chisqr(len(node.children) - 1, s) > Decimal(self.p_threshold):
                return True
        else:
            return False

    def traverse(self):
        queue = []
        queue.append((self.root, 0))
        cur = 0
        pt = 0
        internal_cnt = 0
        leaf_cnt = 0
        while pt < len(queue):
            head = queue[pt]
            if head[0].node_type == 'MIG':
                internal_cnt += 1
            else:
                leaf_cnt += 1
                
            if (head[0].split[0] == 0 or head[0].split[1] == 0) and head[0].node_type == 'MIG':
                print '({0}, ({1}, {2}), {3}, {4}, {5})'.format(head[0].feature_id, head[0].split[0], head[0].split[1], head[0].node_type, head[0].value, head[0].label),
            if head[1] != cur:
                cur = head[1]
                # print '\n'
            # else:
                # print '({0}, ({1}, {2}), {3}, {4}, {5})'.format(head[0].feature_id, head[0].split[0], head[0].split[1], head[0].node_type, head[0].value, head[0].label),
            pt += 1
            if head[0].children != None:
                for i in head[0].children:
                    queue.append((i, head[1] + 1))
        # print '\n'
        print 'internal node: {0}, leaf node: {1}'.format(internal_cnt, leaf_cnt)

    def test(self, test_data):
        if self.root == None:
            raise Exception('No tree trained yet!')

        result = None
        cur_node = self.root
        cnt = 0
        while result == None:
            cnt += 1
            next_node = None
            if cur_node.label != None: # early stopping
                result = cur_node.label
                break

            if cur_node.node_type == 'LS':
                result = cur_node.label
                break

            if cur_node.node_type == 'DS':
                break

            if cur_node.children == None:
                break

            for i in cur_node.children:
                if test_data[cur_node.feature_id] == i.value:
                    next_node = i
                    break
                # if no hit, then missing value for one feature
            if next_node != None:
                cur_node = next_node
            else: # missing value (value of feature in the test data doesn't show in the tree node's feature domain)
                break

        if result == None and cur_node.children != None: # when can not be divided, (missing value?)
            result = False if cur_node.split[0] > cur_node.split[1] else True # this way, split[0] == split[1] then True

        # if result == None: # DS, meaning noisy data
        #     result = bool(random.randint(0, 1))

        return result

    def __str__(self):
        if self.size == None:
            return 'tree not built'
        else:
            # if False and self.debug:
            if self.debug:
                for i in self.train_data:
                    print "data {{{0}}}: {1}".format(i[0], i[1])
            return 'tree size: {0}, feature dimension: {1}'.format(self.size, self.dimension)

def unit_test(dt, data_set, data_label):
    cnt = 0
    t = 0
    f = 0
    n = 0
    for i in range(len(data_set)):
        r = dt.test(data_set[i])
        if r == True:
            t += 1
        elif r == False:
            f += 1
        else:
            n += 1
        if r == data_label[i]:
            cnt += 1
    print ''
    print f, t, n
    print [len(filter(lambda x: x == i, data_label)) for i in set(data_label)]
    print cnt, len(data_set), cnt * 1. / len(data_set) 

def load(f_d, f_l):
    f_d = open(f_d, 'r')
    f_l = open(f_l, 'r')
    data = [map(int, i) for i in map(lambda x: x.strip().split(' '), f_d.read().strip().split('\n'))] # turn data line into feature list
    label = map(bool, map(int, f_l.read().strip().split())) # turn label line into bool label
    size = len(data)
    dimension = None
    parsed_data = []
    for i in range(size):
        if dimension == None: # init dimensionality
            dimension = len(data[i])
        if len(data[i]) != dimension: # check missing features
            raise Exception('data dimension not match: {0} (dimension) and {1} (new data item dimension)'.format(dimension, len(data[i])))
        parsed_data.append((data[i], label[i]))
    f_d.close()
    f_l.close()
    return size, parsed_data, dimension

if __name__ == '__main__':
    # print chi2.chisqr(Decimal('255'), Decimal('290.285192'))
    f_train_data = 'clickstream/trainfeat.csv'
    f_train_label = 'clickstream/trainlabs.csv'
    f_test_data = 'clickstream/testfeat.csv'
    f_test_label = 'clickstream/testlabs.csv'

    dt = DecisionTree(0.05, False)
    dt.size, dt.train_data, dt.dimension = load(f_train_data, f_train_label)
    print 'load done'
    print dt
    dt.build()
    print 'train done'
    dt.traverse()
    dt.chi()
    print 'chi square test done'
    dt.traverse()

    # test on train set
    print '\ntest on train data'
    unit_test(dt, map(lambda y: y[0], dt.train_data), map(lambda y: y[1], dt.train_data))

    # test on test set
    print '\ntest on test data'
    test_data = load(f_test_data, f_test_label)[1]

    # test data distribution
    # _test_data = []
    # _cnt = 0
    # for i in test_data:
    #     if i[1] == False: 
    #         _cnt += 1
    #         if _cnt > 10000:
    #             _test_data.append(i)
    #     else:
    #         _test_data.append(i)
    # test_data = _test_data

    unit_test(dt, map(lambda y: y[0], test_data), map(lambda y: y[1], test_data))
