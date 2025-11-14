#!/bin/bash

set -e

VERSION=$1

if [ ! -f "v$VERSION.tar.xz" ] ; then
	wget https://github.com/immich-app/immich/archive/refs/tags/v$VERSION.tar.gz
	tar xf v$VERSION.tar.gz
	rm v$VERSION.tar.gz

	pushd immich-$VERSION
	# Unneeded for RPM build
	rm -r mobile/
	rm -r docs/
	# Fonts already shipped in Fedora
	rm web/src/lib/assets/fonts/overpass/*.ttf
	# Pointless splashes for iOS
	rm web/src/lib/assets/apple/*.png
	popd

	tar caf v$VERSION.tar.xz immich-$VERSION
	rm -rf immich-$VERSION/
fi
