


import sys
import getopt
import json
from src import xmlReader
from src import cite
from src import coordshift

import numpy as np

if __name__ == '__main__':

    cite.head()

    opts,args = getopt.getopt(
        sys.argv[1:], '-h', [ \
            'help', \
            'xml_i=','xml_o=', \
            'coord_k_i=', 'coord_k_check', 'coord_k_o=', 'coord_k_old=', 'coord_k_new='])

    tag_xml_reader = False
    xml_input_path = ''
    xml_output_path = 'xml'

    tag_coord_k = False
    coord_k_i = ''
    coord_k_check = False
    coord_k_o = 'coord'    
    coord_k_old = [[0,1],[0,1],[0,1]]
    coord_k_new = [[0,1],[0,1],[0,1]]

    for opt_name, opt_value in opts:
        # print(opt_name)
        if opt_name in ('-h', '--help'):
            
            print('| --xml_i="path_xml_file"  read the xml file')
            print('| [--xml_o="saved_file_name"]  read the xml file')
            print(cite.hbar+cite.dashbar)
            print('| example : ')
            print('| $ python main.py --xml_i="./example/testPY/Transmission_PC.xml" --xml_o="test/PC."')
            print(cite.hbar+cite.lbar)
            print('| --coord_k_i="path_coord_file"  read the coord file, like "transm.coordinatesOfKPoints.dat"')
            print('| [--coord_k_check]  check the coord range. ')
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

    if tag_xml_reader:
        xmlReader.readXML(xml_input_path, xml_output_path)
    
    if tag_coord_k:
        if coord_k_check:
            coordshift.coord_k_check(coord_k_i)
        else:
            coordshift.coord_k_transform(coord_k_i, coord_k_o, coord_k_old, coord_k_new)