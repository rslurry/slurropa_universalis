#! /usr/bin/env bash

source .env

yes | cp game/* "${SLURROPA_FOLDER}/."

for foo in *.py
do
  python $foo
done
