import pandas as pd
import os
from mjol.base import *
from mjol.gan import *
from mjol.tools import *

chm13 = GAn(
    file_name = 'data/chm13v2.0_RefSeq_Liftoff_v5.2.gff3',
    file_fmt = 'gff'
)
chm13.build_db()
chm13.save_as_gix("output/chm13_original.pkl")

# checked that outputs all features