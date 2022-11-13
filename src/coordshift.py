#!/usr/bin/env python
# coding: utf-8

import xml.etree.ElementTree as ET
import numpy as np
import os
import math

from src import cite

def coord_k_transform(coord_k_i, coord_k_o, coord_k_old, coord_k_new):
    print(cite.hbar+cite.m1+' transformed data stored in the "'+coord_k_i+'" file.')

    save_path = os.path.dirname(os.path.abspath(coord_k_o))
    os.makedirs(save_path, exist_ok=True)

    array = np.loadtxt(coord_k_i)
    if len(array.shape) == 1:
        print(cite.hbar+cite.m2+" transforming colum:", 1, ' of ', 1, ' ...')

        f_old = coord_k_old[0]
        t_old = coord_k_old[1]

        f_new = coord_k_new[1]
        t_new = coord_k_new[1]

        d = f_new - f_old
        p = t_old - f_old

        if p == 0. :
            n_p_dn = 0
            n_p_up = 0
            f_new_dn_map = f_new
            t_new_dn_map = t_new
            f_new_up_map = f_new
            t_new_up_map = t_new

            shift_dn = f_new - f_old
            shift_up = f_new - f_old
        else:
            n_p_dn = math.floor(d/p)
            n_p_up = math.ceil(d/p)

            f_new_dn_map = f_new - n_p_dn * p
            t_new_dn_map = t_new - n_p_dn * p

            shift_dn = n_p_dn * p

            f_new_up_map = f_new - n_p_up * p
            t_new_up_map = t_new - n_p_up * p

            shift_up = n_p_up * p

        print(cite.hbar+cite.m2+" [", f_old, ',', t_old, ']->[',f_new,',',t_new,']')

        array_r = np.array([])
        for x in array[:]:
            if x>= f_new and x <= t_new :
                array_r = np.append(array_r, x)
            elif x >= f_new_dn_map  and x <= t_new_dn_map :
                array_r = np.append(array_r,x + shift_dn)
            elif x >= f_new_up_map  and x  <= t_new_up_map :
                array_r = np.append(array_r,x + shift_up)
            else:
                print(cite.hbar+cite.m2+' unknown x:',x , f_new, t_new, f_new+shift_dn, t_new+shift_dn, f_new+shift_up, t_new+shift_up)
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

            if p == 0. :
                n_p_dn = 0
                n_p_up = 0
                f_new_dn_map = f_new
                t_new_dn_map = t_new
                f_new_up_map = f_new
                t_new_up_map = t_new

                shift_dn = f_new - f_old
                shift_up = f_new - f_old
            else:
                n_p_dn = math.floor(d/p)
                n_p_up = math.ceil(d/p)

                f_new_dn_map = f_new - n_p_dn * p
                t_new_dn_map = t_new - n_p_dn * p

                shift_dn = n_p_dn * p

                f_new_up_map = f_new - n_p_up * p
                t_new_up_map = t_new - n_p_up * p

                shift_up = n_p_up * p


            print(cite.hbar+cite.m2+" [", f_old, ',', t_old, ']->[',f_new,',',t_new,']')

            array_r = np.array([])
            for x in array[:,c]:
                if x>= f_new and x <= t_new :
                    array_r = np.append(array_r, x)
                elif x >= f_new_dn_map  and x <= t_new_dn_map :
                    array_r = np.append(array_r,x + shift_dn)
                elif x >= f_new_up_map  and x  <= t_new_up_map :
                    array_r = np.append(array_r,x + shift_up)
                else:
                    print(cite.hbar+cite.m2+' unknown x:',x , f_new, t_new, f_new+shift_dn, t_new+shift_dn, f_new+shift_up, t_new+shift_up)
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

def transpose_matrix_dat(transpose_i, transpose_o):
    print(cite.hbar+cite.m1+' matrix data stored in the "'+transpose_i+'" file.')

    save_path = os.path.dirname(os.path.abspath(transpose_o))
    os.makedirs(save_path, exist_ok=True)

    array = np.loadtxt(transpose_i)
    print(cite.hbar+cite.m1+' the shape of the matrix : ', array.shape)
    # print(array)
    np.savetxt(transpose_o, array.T)
    print(cite.hbar+cite.m1+' the shape of the transposed matrix : ', array.T.shape)
    print(cite.hbar+cite.m1+' transposed matrix data stored in the "'+transpose_o+'" file.')
    print(cite.hbar+cite.lbar)