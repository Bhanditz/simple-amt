import csv, sys, json, random

imgpat = ('http://people.csail.mit.edu/davidbau/dissection' +
  '/reference_places205/image/conv5-5-%04d.jpg')

rng = random.Random(1)

all_labels = False
batch_size = 64
with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    cases = []
    for row in reader:
        # TODO: consider evaluating cases
        cases.append({
            'unit': int(row['unit']),
            'image': imgpat % (int(row['unit']) - 1),
            'phrase': row['label']
        })

rng.shuffle(cases)
for index in range(0, len(cases), batch_size):
    batch = cases[index:index+batch_size]
    print json.dumps({ 'cases': batch })
