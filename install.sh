#!/bin/bash

set -e

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)

npm install -g yarn
yarn global add hexo
