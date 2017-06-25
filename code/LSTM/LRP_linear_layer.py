'''
@author: Leila Arras
@maintainer: Leila Arras
@date: 21.06.2017
@version: 1.0
@copyright: Copyright (c) 2017, Leila Arras, Gregoire Montavon, Klaus-Robert Mueller, Wojciech Samek
@license : BSD-2-Clause
'''


import numpy as np
from numpy import newaxis as na


def lrp_linear(hin, w, b, hout, Rout, bias_nb_units, eps, bias_factor, debug=False):
    """
    LRP for a linear layer with input dim D and output dim M.
    Args:
    - hin:            forward pass input, of shape (D,)
    - w:              connection weights, of shape (D, M)
    - b:              biases, of shape (M,)
    - hout:           forward pass, of shape output (M,) (unequal to np.dot(w.T,hin)+b if more than one incoming layer!)
    - Rout:           relevance at layer output, of shape (M,)
    - bias_nb_units:  number of lower-layer units onto which the bias/stabilizer contribution is redistributed
    - eps:            stabilizer 
    - bias_factor:    for global relevance conservation set to 1.0, otherwise 0.0 to ignore bias redistribution
    Returns:
    - Rin:            relevance at layer input, of shape (D,)
    """
    sign_out = np.where(hout[na,:]>=0, 1., -1.) # shape (1, M)
    
    numer    = (w * hin[:,na]) + ( (bias_factor*b[na,:]*1. + eps*sign_out*1.) * 1./bias_nb_units ) # shape (D, M)
    
    denom    = hout[na,:] + (eps*sign_out*1.)   # shape (1, M)
    
    message  = (numer/denom) * Rout[na,:]       # shape (D, M)
    
    Rin      = message.sum(axis=1)              # shape (D,)
    
    # Note: local  layer   relevance conservation if bias_factor==1.0 and bias_nb_units==D
    #       global network relevance conservation if bias_factor==1.0 (can be used for sanity check)
    if debug:
        print("local diff: ", Rout.sum() - Rin.sum())
    
    return Rin
