
#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import os

from src import cite

# settings for files and tag name
def readXML(filePath, outfile_head=''):
    print(cite.hbar+cite.m1+' Getting data stored in the "'+filePath+'" file.')
    # start here
    root = ET.parse(filePath).getroot()

    print(cite.hbar+cite.lbar)
    print(cite.hbar+cite.m1+' Checking tags...')

    # tags = ['transm.energyPoints', 'transm.averagedTransmissionCoefficients', 'transm.coordinatesOfKPoints','transm.transmissionCoefficients']
    # tags = ['transm.coordinatesOfKPoints']
    tags = ['transm.transmissionCoefficients']

    print(cite.hbar+cite.m2+' find tags:')
    for t in tags:
        print(cite.hbar+cite.m2+cite.m1+' '+ t)

    print(cite.hbar+cite.lbar)

    print(cite.hbar+cite.m1+ ' finding data ...')
    print(cite.hbar+cite.lbar)

    data_all ={}

    for nadata in root.findall('nadata'):
        nameEle = nadata.find('name')
        if nameEle is not None:
            print(cite.hbar+cite.m2+' find '+nameEle.text)

            # grep data info

            ## size of data
            size = tuple(map(int, nadata.get('size').split()))
            axis = tuple(x for x in range(len(size)-1,-1,-1))
            print(cite.hbar+cite.m2+cite.m1+' data shape', size)
            
            ## type of data 
            data_type = nadata.get('type')
            isComplex = None
            if nadata.get('isComplex'):
                isComplex = nadata.get('isComplex') == 'Y'

            if (data_type == 'double' and (not isComplex)):
                print(cite.hbar+cite.m2+cite.m1+' data type', data_type, ' supported')
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
                    print(cite.hbar+cite.m2+cite.m1+ ' save data to '+save_name)

                    data_all[nameEle.text] = data
                    np.savetxt(save_name, data)
                else:
                    data_all[nameEle.text] = data
                    
            else:
                print(cite.hbar+cite.m2+cite.m1+' data type : '+ data_type, ' not supported!')
            print(cite.hbar+cite.dashbar)

    print(cite.hbar+cite.lbar)
    if len(data_all.keys())> 0:
        print(cite.hbar+cite.m2+ ' There are '+str(len(data_all.keys()))+" supported data sets.")
        save_name = outfile_head+'all.npz'
        print(cite.hbar+cite.m2+ ' save all these data to '+save_name)
        save_path = os.path.dirname(os.path.abspath(save_name))
        os.makedirs(save_path, exist_ok=True)
        np.savez(save_name,*data_all)
        print(cite.hbar+cite.lbar)