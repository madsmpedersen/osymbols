#!/bin/bash
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.py .
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.kv .
cp /mnt/c/mmpe/Privat/okr/OSymbols/*.spec .
cp /mnt/c/mmpe/Privat/okr/OSymbols/graphics/*.png ./graphics/

buildozer -v android release
cd ~
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./keystores/net-clusterbleep-osignatur.keystore ./osymbols/bin/osymbols-0.4-arm64-v8a_armeabi-v7a-release.aab cb-play
cd osymbols

cp bin/*.aab /mnt/c/mmpe/Privat/okr/OSymbols/bin
