import os
import sys
from psd_tools import PSDImage

"""

https://psd-tools.readthedocs.io/en/latest/

psd-tools 1.8.30

"""

psdpath = os.path.dirname(__file__) + '/test.psd'
output_path = os.path.dirname(__file__) + '/output'

psd = PSDImage.open(psdpath)
for layer in psd:
    layer.visible = True
    print(layer)

psd.compose().save(output_path + '/example.png')
