import urllib2, urllib, urlparse
import re, math, os

'''
Example:

<h2>256. unit 208 confidence:0.058 (object)</h2>
<p>predicted labels:</p><strong>    object</strong>: tree (0.058) windowpane (0.038) house (0.036) mountain (0.034) grass (0.029)<br>
<strong>      part</strong>: pane (0.046) wheel (0.024) hair (0.010) windowpane (0.009) chimney (0.008)<br>
<strong>   texture</strong>: crosshatched (-0.017) porous (-0.018) potholed (-0.019) crystalline (-0.019) braided (-0.019)<br>
<strong>  material</strong>: glass (-0.017) wallpaper (-0.020) granite (-0.024) concrete (-0.027) food (-0.028)<br>
<strong>     color</strong>: white-c (-0.077) grey-c (-0.078) blue-c (-0.080) brown-c (-0.081) yellow-c (-0.083)<br>
<p><img src="unit_segmentation_singlelayer/places205_baseline/unitID208.jpg" /></p>
'''

def read_listing_page(url):
    '''
    returns an array of dicts.
    Each dict has a u
    '''
    webpage = urllib2.urlopen(url)
    records = []
    record = None
    for line in webpage.readlines():
        m = re.search(r'<h2>(?:\d+\. )?unit (\d+).*', line)
        if m:
            record = {'unit': int(m.group(1)), 'score': []}
        m = re.search(r'''(?x)
            <strong>\s*(object|part|texture|material|color)</strong>:
            \s*([^\(\)]+)\s\((-?[\d\.]+)\)
            ''', line)
        if m:
            record['score'].append((m.group(1), m.group(2),float(m.group(3))))
        m = re.search(r'''(?x)
            <img\s+src="([^"]*)"
            ''', line)
        if m and not 'validation set' in line:
            record['img'] = urllib.unquote(m.group(1))
            records.append(record)
            record = None
    return records


# Old url - was overwritten by a different approach
url = 'http://places.csail.mit.edu/deepscene/hybercolumn/plot_cvpr/precision_unit2label_places205_baseline.html'

# New url - same data
url = 'http://places.csail.mit.edu/deepscene/hybercolumn/plot_cvpr/precision_unit2label_places1_caffenet_unisegV4/%s.html'

def cvpr_data(layer):
    return read_listing_page(url % layer)
