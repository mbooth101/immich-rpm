#!/bin/bash

set -e

VERSION=$1

if [ ! -f "v$VERSION-bundled.tar.xz" ] ; then
	wget https://github.com/immich-app/immich/archive/refs/tags/v$VERSION.tar.gz
	tar xf v$VERSION.tar.gz
	rm v$VERSION.tar.gz

	pushd immich-$VERSION
	cp LICENSE machine-learning/
	mv machine-learning immich_ml-$VERSION
	tar caf ../v$VERSION.tar.xz immich_ml-$VERSION
	popd
	rm -rf immich-$VERSION/
fi
