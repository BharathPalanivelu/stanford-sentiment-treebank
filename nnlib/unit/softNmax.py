
#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.07.08
Description: a factory for build Softmax layer
'''

import numpy as np
import theano
import theano.tensor as T
floatX = theano.config.floatX

import common

def build_layer(tparams, prefix, state_before, dim, odim = None, N = 2):
	if odim is None:
		odim = dim

	params = [
		('%s_U'%(prefix), common.ortho_weight(dim, odim * N, floatX)),
		('%s_b'%(prefix), common.rand_weight((odim * N, ), floatX)),
		]

	for name, value in params:
		tparams[name] = theano.shared(value, name = name)

	proj = T.dot(state_before, tparams['%s_U'%(prefix)]) + tparams['%s_b'%(prefix)]
	proj = proj.reshape([odim, N])
	proj = T.max(proj, axis = 1)

	return T.nnet.softmax(proj)
