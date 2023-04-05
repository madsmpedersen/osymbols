#!/bin/bash
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.py .
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.kv .
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.spec .

buildozer -v android debug
cp bin/*.apk /mnt/c/mmpe/Privat/okr/OSymbols/bin
