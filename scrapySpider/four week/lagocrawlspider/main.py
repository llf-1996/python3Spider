from scrapy.cmdline import execute

import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
# print(path)
sys.path.append(path)
execute(["scrapy","crawl","lago"])

