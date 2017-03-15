import csv, sys, json, random

imgpat = ('http://people.csail.mit.edu/davidbau/dissection' +
  '/reference_places205/image/conv5-5-%04d.jpg')

rng = random.Random(1)

all_labels = False
batch_size = 20
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
# Rount up the number of batches so that the size of batches is no
# more than batch_size.  Batches will be evenly distributed.
batch_count = (len(cases) + batch_size - 1) // batch_size
for index in range(batch_count):
    batch = cases[index::batch_count]
    print json.dumps({ 'cases': batch })
