#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import os
import math

from src import cite

def coord_k_transform(coord_k_i, coord_k_o, coord_k_old, coord_k_new):
    print(cite.hbar+cite.m1+' transformed data stored in the "'+coord_k_i+'" file.')

    array = np.loadtxt(coord_k_i)
    if len(array.shape) == 1:
        print(cite.hbar+cite.m2+" transforming colum:", 1, ' of ', 1, ' ...')

        f_old = coord_k_old[0]
        t_old = coord_k_old[1]

        f_new = coord_k_new[1]
        t_new = coord_k_new[1]

        d = f_new - f_old
        p = t_old - f_old
        n_p_dn = int(d/p)
        n_p_up = int(d/p)

        f_new_dn_map = f_new - n_p_dn * p
        t_new_dn_map = t_new - n_p_dn * p

        f_new_up_map = f_new - n_p_up * p
        t_new_up_map = t_new - n_p_up * p

        print(cite.hbar+cite.m2+" [", f_old, ',', t_old, ']->[',f_new,',',t_new,']')
        
        array_r = np.array([])
        for x in array[:]:
            if x>= f_new and x <= t_new :
                array_r = np.append(array_r, x)
            elif x >= f_new_dn_map  and x <= t_new_dn_map :
                array_r = np.append(array_r,x + n_p_dn * p)
            elif x >= f_new_up_map  and x  <= t_new_up_map :
                array_r = np.append(array_r,x + n_p_up * p)
            else:
                print(cite.hbar+cite.m2+' unknown x:',x , f_new, t_new, f_new+n_p_dn * p, t_new+n_p_dn * p, f_new+n_p_up * p, t_new+n_p_up * p)
                return
        np.savetxt(coord_k_o, array_r)

    else:
        for c in range(len(array[0,:])):
            print(cite.hbar+cite.m2+" transforming colum:", c+1, ' of ', len(array[0,:]), ' ...')
            

            f_old = coord_k_old[c,0]
            t_old = coord_k_old[c,1]

            f_new = coord_k_new[c,0]
            t_new = coord_k_new[c,1]

            d = f_new - f_old
            p = t_old - f_old
            n_p_dn = int(d/p)
            n_p_up = math.ceil(d/p)

            f_new_dn_map = f_new - n_p_dn * p
            t_new_dn_map = t_new - n_p_dn * p

            f_new_up_map = f_new - n_p_up * p
            t_new_up_map = t_new - n_p_up * p

            print(cite.hbar+cite.m2+" [", f_old, ',', t_old, ']->[',f_new,',',t_new,']')

            array_r = np.array([])
            for x in array[:,c]:
                if x>= f_new and x <= t_new :
                    array_r = np.append(array_r, x)
                elif x >= f_new_dn_map  and x <= t_new_dn_map :
                    array_r = np.append(array_r,x + n_p_dn * p)
                elif x >= f_new_up_map  and x  <= t_new_up_map :
                    array_r = np.append(array_r,x + n_p_up * p)
                else:
                    print(cite.hbar+cite.m2+' unknown x:',x , f_new, t_new, f_new+n_p_dn * p, t_new+n_p_dn * p, f_new+n_p_up * p, t_new+n_p_up * p)
                    return
            array[:,c] = array_r
        
        np.savetxt(coord_k_o, array)
    print(cite.hbar+cite.lbar)

def coord_k_check(coord_k_i):
    print(cite.hbar+cite.m1+' transform stored in the "'+coord_k_i+'" file.')

    array = np.loadtxt(coord_k_i)

    if len(array.shape) == 1:
        print(cite.hbar+cite.m2+' There are ' , len(array[:]), ' elements in the column.')
        print(cite.hbar+cite.m2+' The column 1 range is [' , np.min(array[:]) , np.max(array[:]) , ']')
    else:
        print(cite.hbar+cite.m2+' There are ' , len(array[:,0]), ' elements in the column.')
        for c in range(len(array[0,:])):
            print(cite.hbar+cite.m2+' The column '+str(c+1)+' range is [' , np.min(array[:,c]) , np.max(array[:,c]) , ']')
    
    print(cite.hbar+cite.lbar)