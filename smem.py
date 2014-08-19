#!/usr/bin/env python
#coding=utf-8

import os
import sys

if len(sys.argv) < 2:
    print 'using %s pid' % sys.argv[0]
    sys.exit(1)

pid = sys.argv[1]
path = '/proc/%s/smaps' % pid
if not os.path.exists(path):
    print '%s not exists' % path

# read smap lines
with open(path) as fp:
    lines = fp.readlines()


class SmapUnit(object):

    def __init__(self):
        self.name = ''
        self.size = ''
        self.rss = ''
        self.sclean = ''
        self.sdirty = ''
        self.pclean = ''
        self.pdirty = ''


def make_unit(unit_lines):
    unit_lines = [line.strip('\n') for line in unit_lines]
    line= lines[0].split()
    if len(line) == 6:
        name = line[5]
    else:
        name = ''

    size = unit_lines[1].split(':')[1].rstrip('kB')
    rss = unit_lines[2].split(':')[1].rstrip('kB')
    sclean = unit_lines[3].split(':')[1].rstrip('kB')
    sdirty = unit_lines[4].split(':')[1].rstrip('kB')
    pclean = unit_lines[5].split(':')[1].rstrip('kB')
    pdirty = unit_lines[6].split(':')[1].rstrip('kB')

    unit = SmapUnit()
    unit.name = name
    unit.size = int(size)
    unit.rss = int(rss)
    unit.sclean = int(sclean)
    unit.sdirty = int(sdirty)
    unit.pclean = int(pclean)
    unit.pdirty = int(pdirty)

    return unit


def parse(lines):
    line_length = len(lines)

    units = []
    for i in xrange(0, line_length, 7):
        unit_lines = lines[i: i+7]
        unit = make_unit(unit_lines)
        units.append(unit)

    return units


units = parse(lines)

vmsize = sum([unit.size for unit in units])
rss = sum([unit.rss for unit in units])
shared = sum([unit.sclean + unit.sdirty for unit in units])
pclean = sum([unit.pclean for unit in units])
pdirty = sum([unit.pdirty for unit in units])

print 'VMSIZE: %s kb' % vmsize
print 'RSS: %s kb total' % rss
print '%s kb shard' % shared
print '%s kb private clean' % pclean
print '%s kb private dirty' % pdirty

print 'private mappings'
print 'vmsize rss clean rss dirty file'
#for unit in units:
#    print '%s kb %s kb %s kb %s ' % (unit.size, unit.pclean, unit.pdirty, unit.name)



