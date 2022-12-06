
#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import os

from src import cite

def readNode(root, outfile_head='', out_print=cite.hbar):
    data_all ={}

    for nadata in root.findall('nadata'):
        nameEle = nadata.find('name')
        if nameEle is not None:
            print(out_print+cite.m2+' find '+nameEle.text)

            # grep data info

            ## size of data
            size = tuple(map(int, nadata.get('size').split()))
            axis = tuple(x for x in range(len(size)-1,-1,-1))
            print(out_print+cite.m2+cite.m1+' data shape', size)
            
            ## type of data 
            data_type = nadata.get('type')
            isComplex = None
            if nadata.get('isComplex'):
                isComplex = nadata.get('isComplex') == 'Y'

            if (data_type == 'double' and (not isComplex)):
                print(out_print+cite.m2+cite.m1+' data type', data_type, ' supported')
                # get all data
                raw_data_in_str = nameEle.tail
                # to array
                data = np.array([float(x) for x in raw_data_in_str.split()]).reshape(tuple(reversed(size))).transpose(axis)
                if 1 in size and len(size)>2:
                    size = tuple(x for x in size if x!=1)
                    if(len(size) == 0):
                        size = (1,1)
                    else:
                        data = data.reshape(size)

                if (len(size) <= 2):

                    save_name = outfile_head+nameEle.text+'.dat'
                    save_path = os.path.dirname(os.path.abspath(save_name))
                    os.makedirs(save_path, exist_ok=True)
                    print(out_print+cite.m2+cite.m1+ ' save data to '+save_name)
                    np.savetxt(save_name, data)

                data_all[nameEle.text] = data

                print(out_print+cite.dashbar)
            elif (data_type == 'cell'):
                print(out_print+cite.m2+cite.m1+' data type : '+ data_type, ' find deeper')
                print(out_print+cite.dashbar)
                data_all.update(readNode(nadata,outfile_head=outfile_head, out_print=out_print+cite.m1)) 
            else:
                print(out_print+cite.m2+cite.m1+' data type : '+ data_type, ' not supported!')
                print(out_print+cite.dashbar)
                
            return data_all

    # print(cite.hbar+cite.lbar)

# settings for files and tag name
def readXML(filePath, outfile_head=''):
    print(cite.hbar+cite.m1+' Getting data stored in the "'+filePath+'" file.')
    # start here
    root = ET.parse(filePath).getroot()

    print(cite.hbar+cite.lbar)
    print(cite.hbar+cite.m1+' Checking tags...')

    print(cite.hbar+cite.lbar)

    print(cite.hbar+cite.m1+ ' finding data ...')
    print(cite.hbar+cite.lbar)

    data_all = readNode(root, outfile_head=outfile_head, out_print=cite.m1)

    print(cite.hbar+cite.lbar)
    
    if len(data_all.keys())> 0:
        print(cite.hbar+cite.m2+ ' There are '+str(len(data_all.keys()))+" supported data sets.")
        save_name = outfile_head+'all.npz'
        print(cite.hbar+cite.m2+ ' save all these data to '+save_name)
        save_path = os.path.dirname(os.path.abspath(save_name))
        os.makedirs(save_path, exist_ok=True)
        np.savez(save_name,*data_all)
        print(cite.hbar+cite.lbar)