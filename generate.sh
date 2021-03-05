#!/bin/bash

set -e

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
SOURCE_FOLDER=$SHELL_FOLDER/post
BUILD_FOLDER=$SHELL_FOLDER/build
TARGET_FOLDER=$SHELL_FOLDER/hexo/source/_posts

rm -rf $BUILD_FOLDER
mkdir -p $BUILD_FOLDER

echo "=============================="
echo " generate file"
echo "=============================="
cd $SOURCE_FOLDER
find -name "*.md" -print0|xargs -0 -i python $SHELL_FOLDER/scripts/do_copy.py "{}" "$BUILD_FOLDER"

echo "=============================="
echo " copy to _post"
echo "=============================="
mkdir -p $TARGET_FOLDER
rm -vrf $TARGET_FOLDER/*
cp -vr $BUILD_FOLDER/* $TARGET_FOLDER

# call hexo
cd $SHELL_FOLDER/hexo
yarn install
yarn run hexo clean
yarn run hexo g
yarn run hexo g # quick fix for image-asset bug "undefined"
