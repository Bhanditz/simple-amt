import csv, sys, json

imgpat = ('http://people.csail.mit.edu/davidbau/dissection' +
  '/reference_places205/image/conv5-%04d.jpg')

all_labels = False
with open(sys.argv[1]) as f:
    reader = csv.DictReader(f)
    for row in reader:
        result = {
            'unit': int(row['unit']),
            'image': imgpat % (int(row['unit']) - 1),
            'phrase': row['label']
        }
        print json.dumps(result)

