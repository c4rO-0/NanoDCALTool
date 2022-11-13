


import sys
import getopt
import json
from src import xmlReader
from src import cite
from src import coordshift
import os
import math

from datetime import datetime

import numpy as np

if __name__ == '__main__':

    cite.head()

    opts,args = getopt.getopt(
        sys.argv[1:], '-h', [ \
            'help', \
            'xml_i=','xml_o=', \
            'coord_k_i=', 'coord_k_check', 'coord_k_o=', 'coord_k_old=', 'coord_k_new=',
            't_i=','t_o=', 'auto'])

    tag_xml_reader = False
    tag_auto = False
    xml_input_path = ''
    xml_output_path = 'auto'

    tag_coord_k = False
    coord_k_i = ''
    coord_k_check = False
    coord_k_o = 'coord.dat'    
    coord_k_old = [[0,1],[0,1],[0,1]]
    coord_k_new = [[0,1],[0,1],[0,1]]

    tag_transpose = False
    transpose_i = ''
    transpose_o = 'transpose.dat'   

    for opt_name, opt_value in opts:
        # print(opt_name)
        if opt_name in ('-h', '--help'):
            
            print('| --xml_i="path_xml_file"  read the xml file')
            print('| --auto write data automatically')
            print(cite.hbar+cite.dashbar)
            print('| [--xml_o="saved_file_name"]  read the xml file')
            print(cite.hbar+cite.dashbar)
            print('| example : ')
            print('| $ python main.py --xml_i="./example/testPY/Transmission_PC.xml" --xml_o="test/PC."')
            print(cite.hbar+cite.lbar)
            print('| --t_i="path_matrix_file"  read the matrix file to be transposed, like "transm.coordinatesOfKPoints.dat"')
            print('| --t_o="path_matrix_file"  write the transposed matrix fil, like "transm.coordinatesOfKPoints_T.dat"')
            print(cite.hbar+cite.lbar)
            print('| --coord_k_i="path_coord_file"  read the coord file, like "transm.coordinatesOfKPoints.dat"')
            print('| --coord_k_check  check the coord range. ')
            print('|    Run this tag before really transforming coords')
            print('| --coord_k_o="path_coord_file"  path for storing the transformed coords. ')
            print('|    If --coord_k_check exists, this tag will be blocked.')
            print('| --coord_k_old="coord_range"  range of the old coord, which are stored as arrays. ')
            print('|    i.e., [[0,1],[0,1], [0,1]] for the range of the 1st, 2nd and 3rd column. ')
            print('| --coord_k_new="coord_range"  range of the old coord, which are stored as arrays.')
            print('|    i.e., [[0,1],[0,1], [0,1]] for the range of the 1st, 2nd and 3rd column. ')
            print(cite.hbar+cite.dashbar)
            print('| example : ')
            print('| $ python main.py -h --coord_k_i="test/PC.transm.coordinatesOfKPoints.dat"')
            print('| >                   --coord_k_o="test/PC.transm.coordinatesOfKPoints_t.dat"')
            print('| >                   --coord_k_old="[[0,1],[0,1],[0,1]]"')
            print('| >                   --coord_k_new="[[1,2],[1,2],[1,2]]"')
            print(cite.hbar+cite.lbar)

            sys.exit()

        if opt_name == '--xml_i':
            tag_xml_reader = True
            xml_input_path = opt_value
        if opt_name == '--xml_o':
            xml_output_path = opt_value
        if opt_name == '--coord_k_i':
            tag_coord_k = True
            coord_k_i = opt_value        
        if opt_name == '--coord_k_check':
            coord_k_check = True   
        if opt_name == '--coord_k_o':
            coord_k_o = opt_value    
        if opt_name == '--coord_k_old':
            coord_k_old = np.array(json.loads(opt_value))
        if opt_name == '--coord_k_new':
            coord_k_new = np.array(json.loads(opt_value))
        if opt_name == '--t_i':
            tag_transpose = True
            transpose_i = opt_value
        if opt_name == '--t_o':
            transpose_o = opt_value
        if opt_name == '--auto' :
            tag_auto = True

    if (not tag_auto) and tag_xml_reader:
        xmlReader.readXML(xml_input_path, xml_output_path)
    
    if (not tag_auto) and tag_coord_k:
        if coord_k_check:
            coordshift.coord_k_check(coord_k_i)
        else:
            coordshift.coord_k_transform(coord_k_i, coord_k_o, coord_k_old, coord_k_new)

    if (not tag_auto) and tag_transpose:
        coordshift.transpose_matrix_dat(transpose_i,transpose_o)

    if tag_auto and tag_xml_reader:

        print(cite.hbar+cite.m1+' auto mod is on...')

        now = datetime.now()

        save_path = os.path.dirname(os.path.abspath(xml_input_path))
        save_path = os.path.join(save_path,'auto_xml', now.strftime("%y%m%d_%H%M%S") ) 
        os.makedirs(save_path, exist_ok=True)
        xml_output_path = os.path.join(save_path, '')

        xmlReader.readXML(xml_input_path, xml_output_path+'/')

        coord_name = "transm.coordinatesOfKPoints"
        # transpose
        transpose_i = os.path.join(save_path , coord_name+".dat")
        transpose_o = os.path.join(save_path , coord_name+"_transpose.dat")
        coord_k_o = os.path.join(save_path   , coord_name+"_transpose_shift.dat")


        coordshift.transpose_matrix_dat(transpose_i,transpose_o)

        # shift - range
        v_range = coordshift.coord_k_check(transpose_o)

        v_range_smooth = np.zeros((len(v_range),2))
        v_range_shift = np.zeros((len(v_range),2))
        for i in range(len(v_range)):
            v = v_range[i]
            s = v[0]
            e = v[1]

            if s >=0.:
                s = float(math.ceil(s))
            else:
                s = -1.*float(math.ceil(-1.*s))

            if e >=0.:
                e = float(math.ceil(e))
            else:
                e = -1.*float(math.ceil(-1.*e))

            s_shift = s - (e-s)/2.
            e_shift = s + (e-s)/2. 

            v_range_smooth[i] = [s, e]
            v_range_shift[i] = [s_shift, e_shift]

        coordshift.coord_k_transform(transpose_o, coord_k_o, v_range_smooth, v_range_shift)
        
