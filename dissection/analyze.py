import json, re

all_results = []
with open('all_results.json') as f:
    for line in f.readlines():
        hit = json.loads(line)
        all_results.extend(
                zip(hit['output']['cases'], hit['output']['evaluations']))
keyed_results = {}
for c, e in all_results:
    # Oops, the AMT data does not have the layer.  We can recover it
    # from the image filename.
    layer = re.search(r'/(conv\d+)-', c['image']).group(1)
    unit = c['unit'] - 1
    method = c['method']
    keyed_results[(method, layer, unit)] = (c, e == True)

layers = [
        ('conv1', 96), ('conv2', 256), ('conv3', 384),
        ('conv4', 384), ('conv5', 256) ]
methods = ['human', 'iccv', 'cvpr']

for layer, unitcount in layers:
    exp = {}
    print layer, 'raw'
    for method in methods:
        exp[method] = [keyed_results[(method, layer, u)][1]
                for u in range(unitcount)]
    for m in exp:
        print m, sum(exp[m]), float(sum(exp[m])) / unitcount
    print layer, 'filtered where human was right'
    humansum = sum(exp['human'])
    for m in exp:
        print m, sum(a & b for a, b in zip(exp[m], exp['human'])), float(
                 sum(a & b for a, b in zip(exp[m], exp['human']))) / humansum

#exp = dict((k, [0 for _ in range(256)])
#        for k in ['human', 'iccv', 'cvpr'])
#dat = dict((k, [None for _ in range(256)])
#        for k in ['human', 'iccv', 'cvpr'])
#for c, e in all_results:
#    exp[c['method']][c['unit'] - 1] = (e == True or e == None)
#    dat[c['method']][c['unit'] - 1] = c
#
#for m in exp:
#    print m, sum(exp[m])
#for m in exp:
#    print m, sum(a & b for a, b in zip(exp[m], exp['human']))


#for i in range(len(exp['human'])):
#    if exp['human'][i]:
#        print i+1, dat['human'][i]['phrase'], dat['iccv'][i]['phrase'], exp['iccv'][i], dat['cvpr'][i]['phrase'], exp['cvpr'][i]
