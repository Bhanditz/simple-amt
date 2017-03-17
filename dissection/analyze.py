import json

all_results = []
with open('results.json') as f:
    for line in f.readlines():
        hit = json.loads(line)
        all_results.extend(
                zip(hit['output']['cases'], hit['output']['evaluations']))
exp = dict((k, [0 for _ in range(256)])
        for k in ['human', 'iccv', 'cvpr'])
for c, e in all_results:
    exp[c['method']][c['unit'] - 1] = (e == True or e == None)
for m in exp:
    print m, sum(exp[m])
