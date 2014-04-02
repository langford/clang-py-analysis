__author__ = 'schwa'

from clang import cindex

import os

cindex.Config.set_library_file(
    '/Applications/Xcode5-DP2.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib')

index = cindex.Index.create()

#print dir(index)

#clang -cc1 -ast-dump
f = 'example.m'

# theTranslationUnit = index.parse(f, args=['-F', '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/System/Library/Frameworks'])

args = [
        # "-triple", "x86_64-apple-macosx10.9.0", "-emit-obj", "-mrelax-all", "-disable-free", "-disable-llvm-verifier",
        "-main-file-name", "example.m", "-mrelocation-model", "pic", "-pic-level", "2", "-mdisable-fp-elim",
        # "-masm-verbose", "-munwind-tables", "-target-cpu", "core2", "-target-linker-version", "142", "-resource-dir",
        # "/Applications/Xcode5-DP2.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/clang/5.0",
        "-isysroot",
        "/Applications/Xcode5-DP2.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk",
        "-isysroot-implicit", "-fdebug-compilation-dir", "/Users/schwa/Desktop/clang_test", "-ferror-limit", "19",
        "-fmessage-length", "134", "-stack-protector", "1", "-mstackrealign", "-fblocks",
        "-fobjc-runtime=macosx-10.9.0", "-fobjc-dispatch-method=mixed", "-fobjc-default-synthesize-properties",
        "-fencode-extended-block-signature", "-fobjc-exceptions", "-fexceptions", "-fdiagnostics-show-option",
        "-fcolor-diagnostics", "-x",
        "objective-c",
        # "example.m",
        # "/Applications/Xcode5-DP2.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/ld", "-demangle",
        # "-dynamic", "-arch", "x86_64", "-macosx_version_min", "10.9.0", "-syslibroot",
        # "/Applications/Xcode5-DP2.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.9.sdk", "-o",
        # "a.out", "/var/folders/c9/pqvs14g940j9q5dxgh8njsnh0000gp/T/example-W3QDKE.o", "-lSystem",
        # "/Applications/Xcode5-DP2.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/../lib/clang/5.0/lib/darwin/libclang_rt.osx.a",
        # "-L", "/usr/local/lib", "-F", "/Library/Frameworks"
        ]

theTranslationUnit = index.parse(f, args = args)

#print dir(theTranslationUnit)

s = file(f).read()


def walk(c, depth=0):

    #print '\t' * depth, c.kind, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')
    #if c.location.file == f:
    if c.kind not in [ cindex.CursorKind.UNEXPOSED_EXPR ]:
        if depth == 0 or (c.location.file and c.location.file.name == f):
            print '\t' * depth, c.kind, c.displayname, s[c.extent.start.offset: c.extent.end.offset][:100].strip().replace('\n', ' ')

        depth += 1

    for child in c.get_children():
        walk(child, depth)


walk(theTranslationUnit.cursor)
