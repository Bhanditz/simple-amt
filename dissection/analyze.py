import json, re

all_results = []
with open('all_results.json') as f:
    for line in f.readlines():
        hit = json.loads(line)
        all_results.extend(
                zip(hit['output']['cases'], hit['output']['evaluations']))

with open('results-human.json') as f:
    for line in f.readlines():
        hit = json.loads(line)
        for c in hit['output']['cases']:
            if c['method'] == 'human':
                c['method'] = 'human2'
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
methods = ['human', 'iccv', 'cvpr', 'human2']

for layer, unitcount in layers:
    exp = {}
    print layer, 'raw'
    for method in methods:
        exp[method] = [keyed_results[(method, layer, u)][1]
                for u in range(unitcount)]
    for m in exp:
        print m, sum(exp[m]), float(sum(exp[m])) / unitcount
    humansum = sum(exp['human'])
    print layer, 'filtered where human was righti (%d)' % humansum
    for m in exp:
        print m, sum(a & b for a, b in zip(exp[m], exp['human'])), float(
                 sum(a & b for a, b in zip(exp[m], exp['human']))) / humansum

# Considering conv5 only
layer = 'conv5'
unitcount = 256

def check(values, layer, unit):
    """ Check if all methods come out the way specified """
    for method, expect in values:
        if keyed_results[(method, layer, unit)][1] != expect:
            return False
    return True


# Cases where both iccv and cvpr fail
print 'BOTH ICCV AND CVPR FAIL'
count = 0
for u in range(unitcount):
    if check([('human', True), ('iccv', False), ('cvpr', False)], layer, u):
        count += 1
        print "%d: h:%s / cvpr:%s / iccv:%s" % (
                u+1, keyed_results[('human', layer, u)][0]['phrase'],
              keyed_results[('cvpr', layer, u)][0]['phrase'],
              keyed_results[('iccv', layer, u)][0]['phrase'])
print 'Count', count

print
print 'ICCV SUCCEEDS AND CVPR FAILS'
count = 0
for u in range(unitcount):
    if check([('human', True), ('iccv', True), ('cvpr', False)], layer, u):
        count += 1
        print "%d: h:%s / cvpr:%s / iccv:%s" % (
                u+1, keyed_results[('human', layer, u)][0]['phrase'],
              keyed_results[('cvpr', layer, u)][0]['phrase'],
              keyed_results[('iccv', layer, u)][0]['phrase'])
print 'Count', count

print
print 'CVPR SUCCEEDS AND ICCV FAILS'
count = 0
for u in range(unitcount):
    if check([('human', True), ('iccv', False), ('cvpr', True)], layer, u):
        count += 1
        print "%d: h:%s / cvpr:%s / iccv:%s" % (
                u+1, keyed_results[('human', layer, u)][0]['phrase'],
              keyed_results[('cvpr', layer, u)][0]['phrase'],
              keyed_results[('iccv', layer, u)][0]['phrase'])
print 'Count', count

print
print 'BOTH CVPR SUCCEEDS AND ICCV SUCCEEDS'
count = 0
for u in range(unitcount):
    if check([('human', True), ('iccv', True), ('cvpr', True)], layer, u):
        count += 1
        if (keyed_results[('cvpr', layer, u)][0]['phrase'].lower() !=
                keyed_results[('iccv', layer, u)][0]['phrase'].lower()):
            print "%d: h:%s / cvpr:%s / iccv:%s" % (
                    u+1, keyed_results[('human', layer, u)][0]['phrase'],
                  keyed_results[('cvpr', layer, u)][0]['phrase'],
                  keyed_results[('iccv', layer, u)][0]['phrase'])
print 'Count', count


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
