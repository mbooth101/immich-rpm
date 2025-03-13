#!/bin/bash

set -e

VERSION=$1

if [ ! -f "v$VERSION-bundled.tar.xz" ] ; then
	wget https://github.com/immich-app/immich/archive/refs/tags/v$VERSION.tar.gz
	tar xf v$VERSION.tar.gz
	rm v$VERSION.tar.gz

	pushd immich-$VERSION/server
	npm ci
	rm -rf node_modules/@img/sharp-libvips*
	rm -rf node_modules/@img/sharp-linuxmusl-x64
	popd
	pushd immich-$VERSION/open-api/typescript-sdk
	npm ci
	popd
	pushd immich-$VERSION/web
	npm ci
	popd

	tar caf v$VERSION-bundled.tar.xz immich-$VERSION
	rm -rf immich-$VERSION/
fi

if [ ! -f "immich-cli.tar.xz" ] ; then
	OLD_PREFIX=$(npm get prefix)
	mkdir immich-cli
	pushd immich-cli
	npm set prefix $(pwd)
	npm install -g @immich/cli
	npm set prefix $OLD_PREFIX
	popd
	tar caf immich-cli.tar.xz immich-cli
	rm -rf immich-cli/
fi
