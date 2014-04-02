#!/usr/bin/python

__author__ = 'schwa'

import sys
import subprocess
import os
from clang import cindex
import json

class Notice(object):
    NOTICE = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, level, location, message):
        self.level = level
        self.location = location
        self.message = message

    def __str__(self):
        return 'NOTICE: %s' % self.message

def test_NSLog(c, depth):
#    print '\t' * depth, c.kind, c.displayname, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
    if c.kind == cindex.CursorKind.CALL_EXPR and c.displayname == 'NSLog':
        #print '\t' * depth, c.kind, c.displayname, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
        #print '>', c.spelling
        notice = Notice(Notice.NOTICE, c.extent, 'Should not use NSLog use XXLog instead.')
        # print dir(c.extent.start)
        # print c.extent.start.line
        # print c.extent.start.file
        # print c.extent.start.column
        return notice

def test_viewDidAppear(c, depth):
    if c.kind == cindex.CursorKind.OBJC_INSTANCE_METHOD_DECL and c.displayname == 'viewDidAppear:':
        print 'MATCH'

def walk(c, depth = 0):
    yield c, depth
    for child in c.get_children():
        for node, depth_ in walk(child, depth + 1):
            yield node, depth_

# for child in self.children:
#     for path in child.paths([self.node]+acc):
#         yield path

# def node_recurse_generator(node):
#     yield node.value
#     for n in node.ChildElements:
#         for rn in node_recurse_generator(n):
#             yield rn

def walk_refactorme(c, depth=0):
#    print '\t' * depth, c.kind, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
    #if c.location.file == f:
    if not c.kind:
        return
    if c.kind not in [ cindex.CursorKind.UNEXPOSED_EXPR ]:
        if depth == 0 or (c.location.file and c.location.file.name == f):
#            print '\t' * depth, c.kind, c.displayname, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
            x = test_NSLog(c, depth)
            if x:
                print x
            x = test_viewDidAppear(c, depth)
            if x:
                print x

        depth += 1

    for child in c.get_children():
        walk_refactorme(child, depth)

argv = ['clang'] + sys.argv[1:]

###########################################

path = os.path.expanduser('clang_shim.json')
content = json.load(file(path))

###########################################

cindex.Config.set_library_file('/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib')

for d in content:
    args = d['args']
    #print args

    print '#' * 80

    if '-c' not in args:
        print 'Cannot find target. Skipping.'
        continue
    path = args[args.index('-c') + 1]
    if path == '/dev/null':
        print 'Cannot find target (target is /dev/null). Skipping.'
        continue
    if os.path.splitext(path)[1] == '.pch':
        print 'Skipping pch'
        continue
    print path
    index = cindex.Index.create()

#        args = args[:-4]

    theTranslationUnit = index.parse('', args = args)

    s = file(path).read()
    f = path

    for c, depth in walk(theTranslationUnit.cursor):
       print '\t' * depth, c.kind, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
    #walk_refactorme(theTranslationUnit.cursor)

    print 'Success'

    break
