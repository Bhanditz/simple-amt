import csv, sys, json, random
from scipy.io import loadmat
import scrape


imgpat = ('http://people.csail.mit.edu/davidbau/dissection' +
  '/reference_places205/image/conv5-5-%04d.jpg')

iccv_file = '/home/davidbau/interp/iccv/caffe_reference_places205/conv5-result.csv'
rng = random.Random(1)

all_labels = False
batch_size = 20

with open(iccv_file) as f:
    reader = csv.DictReader(f)
    cases = []
    for row in reader:
        # TODO: consider evaluating cases
        cases.append({
            'method': 'iccv',
            'unit': int(row['unit']),
            'image': imgpat % (int(row['unit']) - 1),
            'phrase': row['label']
        })

# TODO: add CVPR data from scrape.py
cvpr = scrape.cvpr_data()
for unit, row in enumerate(cvpr):
    cases.append({
        'method': 'cvpr',
        'unit': row['unit'],
        'image': imgpat % (row['unit'] - 1),
        'phrase': row['score'][0][1].lower()
        })

# TODO: add human data from import.py
human = loadmat('iclr/neuronAnnotation_places205_afterICLR.mat',
        squeeze_me=True)['layerAnnotation'][4,0]
for unit, labels in enumerate(human):
    alternatives = []
    for j in range(0, len(labels), 3):
        alternatives.append((-labels[j + 2], labels[j]))
    alternatives.sort()
    cases.append({
        'method': 'human',
        'unit': (unit + 1),
        'image': imgpat % unit,
        'phrase': alternatives[0][1]
    })

# Complicated shuffling to avoid duplicate unit in the same HIT batch
units = [[] for _ in range(256)]
for c in cases:
    units[c['unit'] - 1].append(c)

for u in units:
    rng.shuffle(u)

for b in range(0, 3):
    cases = [u[b] for u in units]
    rng.shuffle(cases)
    batch_count = (len(cases) + batch_size - 1) // batch_size
    batches = []
    for index in range(batch_count):
        batch = cases[index::batch_count]
        assert len(set([b['unit'] for b in batch])) == len(batch)
        print json.dumps({ 'cases': batch })

