import re
l = []
ip = '8.8.8.8'
s = " 11.|-- 8.8.8.8                    0.0%     4   60.0  60.3  59.9  61.2   0.0"
a = s.split(' ')
for i in range(len(a)):
    if a[i] != '':
        l.append(a[i])
print(l)

o = lambda a: l.append(a[i])