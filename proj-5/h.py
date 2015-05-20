t1 = open('clickstream/trainfeat.csv', 'r')
t2 = open('clickstream/trainlabs.csv', 'r')
e1 = open('clickstream/testfeat.csv', 'r')
e2 = open('clickstream/testlabs.csv', 'r')

a1 = t1.read().strip().split('\n')
a2 = t2.read().strip().split('\n')
b1 = e1.read().strip().split('\n')
b2 = e2.read().strip().split('\n')
# print a1[0], a2[0], len(a1[0].split(' '))
# print b1[0], b2[0]

t1.close()
t2.close()
e1.close()
e2.close()

f = open('all.csv', 'w')
for i in range(len(a1)):
    print >> f, a1[i], a2[i]
for i in range(len(b1)):
    print >> f, b1[i], b2[i]

f.close()
