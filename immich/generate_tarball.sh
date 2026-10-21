#!/bin/bash

set -e

VERSION=$1

if [ ! -f "v$VERSION.tar.xz" ] ; then
	wget https://github.com/immich-app/immich/archive/refs/tags/v$VERSION.tar.gz
	tar xf v$VERSION.tar.gz
	rm v$VERSION.tar.gz

	pushd immich-$VERSION
	# Unneeded for RPM build
	rm -r .github/
	rm -r design/
	rm -r docs/
	rm -r mobile/
	# Packaged separately
	rm -r machine-learning/
	# Big language translations that we don't need
	rm i18n/{ta,ml,hi,el,th,mr,uk,kn,ru,bg,ar,he,ja,vi,ko,sr_Cyrl,sr_Latn,yue_Hant,zh_Hans,zh_Hant}.json
	# End to end tests we can't run
	rm -r e2e/ e2e-auth-server/
	popd

	tar caf v$VERSION.tar.xz immich-$VERSION
	rm -rf immich-$VERSION/
fi
