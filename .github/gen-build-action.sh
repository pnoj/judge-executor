#!/bin/bash
for file in runtimes/*
do
    langcode="$(basename $file)"
    sed -e "s/LANG/$langcode/g" .github/build-template.yml > .github/workflows/build-$langcode.yml
done
