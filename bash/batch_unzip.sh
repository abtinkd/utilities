find . -name '*.zip' -exec sh -c 'unzip -d `dirname {}` {}' ';'
