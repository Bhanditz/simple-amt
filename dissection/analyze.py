import json

all_results = []
with open('results.json') as f:
    for line in f.readlines():
        hit = json.loads(line)
        all_results.extend(
                zip(hit['output']['cases'], hit['output']['evaluations']))
exp = dict((k, [0 for _ in range(256)])
        for k in ['human', 'iccv', 'cvpr'])
dat = dict((k, [None for _ in range(256)])
        for k in ['human', 'iccv', 'cvpr'])
for c, e in all_results:
    exp[c['method']][c['unit'] - 1] = (e == True or e == None)
    dat[c['method']][c['unit'] - 1] = c

for m in exp:
    print m, sum(exp[m])
for m in exp:
    print m, sum(a & b for a, b in zip(exp[m], exp['human']))
for i in range(len(exp['human'])):
    if exp['human'][i]:
        print i+1, dat['human'][i]['phrase'], dat['iccv'][i]['phrase'], exp['iccv'][i], dat['cvpr'][i]['phrase'], exp['cvpr'][i]
