# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 16:50:50 2026

@author: Harsh
"""

# p_global.py
# program used to defines module settings
# variables, it can be used while calling savedata function.
# Written by V. K. Panchal
# Modified on 2-Jan-2017 for PXI & SBC addition, 19-2-2021 added sbc4

# -------------------------------------------
#   Modules name   id   header      data
# -------------------------------------------
#   LS8212_32      1    lheader     l
#   LS8212_8       2    l8head      l8_
#   CA5548         3    header      inch
#   LS8210         4    h8210       l810
#   IPRMOD_B       5    hctd        ctd8
#   IPRMOD_U       6    huctd       uctd8
#   VMEVTR812      7    v812h       v812
#   VMEALPHI       8    ''          ''
#   PXI6133        9    h6133       p6133
#   SBC64          10   hsbc64      sbc64
#   SBC4           11   hsbc4       sbc4
# -------------------------------------------

import warnings
warnings.filterwarnings("ignore")

# Equivalent of MATLAB global variables
shot_no = None
dir_name = None
shot_return_status = None
OS_ID = None
deli_style = None
home_new = None

log_struct = None

server_string = ['adserver', 'old']

server_path_string = [
    'aditya','aditya','aditya','aditya','aditya',
    'aditya','aditya','aditya','pxi','sbc','sbc'
]

module_string = [
    'LS8212_32','LS8212_8','CA5548','LS8210',
    'IPRMOD_B','IPRMOD_U','VMEVTR812','VMEALPHI',
    'PXI6133','SBC64','SBC4'
]

head_string = [
    'lheader','l8head','header','h8210',
    'hctd','huctd','v812h','',
    'h6133','hsbc64','hsbc4'
]

data_string = [
    'l','l8_','inch','l810',
    'ctd8','uctd8','v812','',
    'p6133','sbc64','sbc4'
]

# MATLAB equivalent:
# [dirname '' char(head_string(1)) '.bin']
# sprintf('%s%s.bin',dirname,char(head_string(1)))

def build_filename(dirname, index):
    return f"{dirname}{head_string[index]}.bin"
