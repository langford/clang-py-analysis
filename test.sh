#!/bin/sh

./clang_shim.py xcodebuild -project Sample/Sample.xcodeproj -sdk iphonesimulator7.1 -jobs 1 clean build
./clang_analyze.py
