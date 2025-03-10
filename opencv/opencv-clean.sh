#!/bin/bash

VERSION=$1

wget -c https://github.com/opencv/opencv/archive/${VERSION}/opencv-${VERSION}.tar.gz
wget -c https://github.com/opencv/opencv_contrib/archive/${VERSION}/opencv_contrib-${VERSION}.tar.gz
wget -c https://github.com/opencv/opencv_extra/archive/${VERSION}/opencv_extra-${VERSION}.tar.gz

rm -rf opencv-${VERSION}/
tar xf opencv-${VERSION}.tar.gz
find opencv-${VERSION}/ -iname "*lena*" -exec rm {} ';' -print
find opencv-${VERSION}/ -iname "*lenna*" -exec rm {} ';' -print
rm -r opencv-${VERSION}/modules/xfeatures2d/
tar zcf opencv-clean-${VERSION}.tar.gz opencv-${VERSION}/
rm -r opencv-${VERSION}/

rm -rf opencv_contrib-${VERSION}/
tar xf opencv_contrib-${VERSION}.tar.gz
find opencv_contrib-${VERSION}/ -iname "*lena*" -exec rm {} ';' -print
find opencv_contrib-${VERSION}/ -iname "*lenna*" -exec rm {} ';' -print
rm -r opencv_contrib-${VERSION}/modules/xfeatures2d/
tar zcf opencv_contrib-clean-${VERSION}.tar.gz opencv_contrib-${VERSION}/
rm -r opencv_contrib-${VERSION}/

rm -rf opencv_extra-${VERSION}/
tar xf opencv_extra-${VERSION}.tar.gz
find opencv_extra-${VERSION} -iname "*lena*" -exec rm {} ';' -print
find opencv_extra-${VERSION} -iname "*lenna*" -exec rm {} ';' -print
find opencv_extra-${VERSION} \( -iname "len*.*" -o -iname "*lena*.png" -o -iname "*lena*.jpg" \) -exec rm {} ';' -print
tar zcf opencv_extra-clean-${VERSION}.tar.gz opencv_extra-${VERSION}/
rm -r opencv_extra-${VERSION}/


#echo fedpkg new-sources $(spectool -l --sources opencv.spec | sed 's/.*: //;s/.*\///')
