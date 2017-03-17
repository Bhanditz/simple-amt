import csv, sys, json, random
from scipy.io import loadmat
import scrape

layers = [('conv1', 96), ('conv2', 256), ('conv3', 384), ('conv4', 384)]

imgpat = ('http://people.csail.mit.edu/davidbau/dissection' +
  '/reference_places205/image/%s-5-%04d.jpg')

iccv_file = '/home/davidbau/interp/iccv/caffe_reference_places205/%s-result.csv'
rng = random.Random(1)

all_labels = False
batch_size = 20

cases = []
start = 0
for layer, s in layers:
    with open(iccv_file % layer) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # TODO: consider evaluating cases
            cases.append({
                'method': 'iccv',
                'unit': int(row['unit']),
                'index': int(row['unit']) - 1 + start,
                'image': imgpat % (layer, int(row['unit']) - 1),
                'phrase': row['label'].lower()
            })
    start += s

# TODO: add CVPR data from scrape.py
start = 0
for layer, s in layers:
    cvpr = scrape.cvpr_data(layer)
    for unit, row in enumerate(cvpr):
        cases.append({
            'method': 'cvpr',
            'unit': row['unit'],
            'index': int(row['unit']) - 1 + start,
            'image': imgpat % (layer, row['unit'] - 1),
            'phrase': row['score'][0][1].lower()
            })
    start += s

# TODO: add human data from import.py
start = 0
for i, (layer, s) in enumerate(layers):
    human = loadmat('iclr/neuronAnnotation_places205_afterICLR.mat',
            squeeze_me=True)['layerAnnotation'][i,0]
    for unit, labels in enumerate(human):
        alternatives = []
        for j in range(0, len(labels), 3):
            alternatives.append((-labels[j + 2], labels[j]))
        alternatives.sort()
        cases.append({
            'method': 'human',
            'unit': (unit + 1),
            'index': unit + start,
            'image': imgpat % (layer, unit),
            'phrase': alternatives[0][1].lower()
        })
    start += s

assert(len(cases) == 3 * (96 + 256 + 384 + 384))

# Complicated shuffling to avoid duplicate unit in the same HIT batch
units = [[] for _ in range(start)]
for c in cases:
    units[c['index']].append(c)

for u in units:
    rng.shuffle(u)

for b in range(0, 3):
    cases = [u[b] for u in units]
    rng.shuffle(cases)
    batch_count = (len(cases) + batch_size - 1) // batch_size
    batches = []
    for index in range(batch_count):
        batch = cases[index::batch_count]
        assert len(set([b['index'] for b in batch])) == len(batch)
        print json.dumps({ 'cases': batch })

#rng.shuffle(cases)
#batch_count = (len(cases) + batch_size - 1) // batch_size
#batches = []
#for index in range(batch_count):
#    batch = cases[index::batch_count]
#    if len(set([b['unit'] for b in batch])) < len(batch):
#       print 'OOPS'
#    else:
#        print 'OK'
#    # print json.dumps({ 'cases': batch })

