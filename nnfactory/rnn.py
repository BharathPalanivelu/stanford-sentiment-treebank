#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.07.09
Description: a factory for building the Recurrent Neural Network layer
'''

import numpy as np
import theano
import theano.tensor as T
floatX = theano.config.floatX

def ortho_weight(nrow, ncol = None, dtype = floatX):
	"""
	initialization of a matrix [nrow x ncol] with orthogonal weight
	"""
	dim = nrow if ncol is None else max(nrow, ncol)

	W = np.random.randn(dim, dim)
	u, s, v = np.linalg.svd(W)

	return u[:nrow, :ncol].astype(dtype)

def init_param(prefix, dim, odim = None):
	if odim is None:
		odim = dim

	params = []
	params.append(('%s_W'%(prefix), ortho_weight(dim, odim)))
	params.append(('%s_U'%(prefix), ortho_weight(odim, odim)))
	params.append(('%s_b'%(prefix), np.zeros((odim,)).astype(floatX)))

	return params

def build_layer(
		# data access
		tparams,
		prefix,

		# params of the network
		state_below,
		mask,
	):

	nsteps = state_below.shape[0]
	dim_output = tparams['%s_b'%(prefix)].shape[0]

	if state_below.ndim == 3:
		# for parallel computation
		n_samples = state_below.shape[1]
	else:
		n_samples = 1

	def _step(m_, x_, h_):
		"""
		m_: mask
		x_: main input x
		h_: hidden output from the last loop
		"""

		h = T.tanh(x_ + T.dot(h_, tparams['%s_U'%(prefix)]))
		h = m_[:, None] * h + (1. - m_)[:, None] * h_ # cover h if m == 1

		return h

	state_below = T.dot(state_below, tparams['%s_W'%(prefix)]) + tparams['%s_b'%(prefix)]

	rval, updates = theano.scan(
				_step,
				sequences = [mask, state_below],
				outputs_info = [
					T.alloc(np.asarray(0., dtype = floatX), n_samples, dim_output),
					],
				name = '%s_layers'%(prefix),
				n_steps = nsteps
			)

	# hidden state output, memory states
	return rval

def postprocess_avg(proj, mask):
	"""
	mean pooling
	
	proj: a matrix of size [n_step, n_samples, dim_proj]
	mask: a matrix of size [n_step, n_samples]
	"""

	proj = (proj * mask[:, :, None]).sum(axis=0)
	proj = proj / mask.sum(axis=0)[:, None]

	return proj

def postprocess_last(proj):
	"""
	keep only the last hidden state
	
	proj: a matrix of size [n_step, n_samples, dim_proj]
	"""

	return proj[-1]
