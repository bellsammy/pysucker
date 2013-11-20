# -*- coding: utf-8 -*-
from robot import r

print 'Start with', r.scard('test_set')
values = ['1', '2', '3']
r.sadd('test_set', *values)
print 'After first insert', r.scard('test_set')
r.sadd('test_set', *values)
print 'After second insert', r.scard('test_set')
for v in values:
    r.sadd('test_set', v)
print 'After last inserts', r.scard('test_set')
r.delete('test_set')
print 'End with', r.scard('test_set')