#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Xihao Liang
Created: 2016.05.16
'''

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import cPickle
from optparse import OptionParser

def main():
	optparser = OptionParser()
	optparser.add_option('-i', '--input', action = 'store', dest = 'input', type = 'str')
	optparser.add_option('-n', '--topN', action = 'store', dest = 'topN', type = 'int', default = 10)
	opts, args = optparser.parse_args()

	prec = cPickle.load(open('data/test/%s_prec.pkl'%(opts.input), 'r'))
	if len(prec) > opts.topN:
		prec = prec[:opts.topN]

	print '  '.join(['(%d)%.4f'%(i + 1, p) for i, p in enumerate(prec)])

if __name__ == '__main__':
	main()
