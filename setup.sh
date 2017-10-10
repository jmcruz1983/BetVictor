#!/bin/bash

echo '--> Running setup!'

BASEDIR="$(pwd)"

# PYTHON
PYTHON_BIN=$(which python)

# Workspace
# Bins dir
BINS_PATH=$BASEDIR/bins
mkdir -p $BINS_PATH
# Downlads dir
DOW_PATH=$BASEDIR/downloads
mkdir -p $DOW_PATH

# Ant
ANT_URL=http://apache.uvigo.es/ant/binaries/apache-ant-1.10.1-bin.zip
ANT_DOW=$DOW_PATH/ant
mkdir -p $ANT_DOW
ANT_WS=$BINS_PATH/ant
mkdir -p $ANT_WS
ANT_BIN=$(find $ANT_WS -type f  -name 'ant' | head -1)

# Check if Python is installed
if ! which python > /dev/null; then
    echo '--> Error : Python exec is missing'
fi

# Check if PIP is installed
if ! which pip > /dev/null; then
    echo '--> Error : PIP is missing'
fi

# Downloading and extracting the ANT
if [ -z $ANT_BIN ]; then
    echo '--> Setting up ANT'
    # Download ANT
    if [ ! -f $ANT_DOW/apache-ant.zip ]; then
        echo '        Downloading ANT'
        curl -o $ANT_DOW/apache-ant.zip $ANT_URL &> /dev/null
    fi
    # Extract SDK
    if [ -f $ANT_DOW/apache-ant.zip ]; then
        echo '        Extracting ANT'
        unzip -qq -o $ANT_DOW/apache-ant.zip -d $ANT_WS
    fi
fi

ANT_BIN=$(find $ANT_WS -type f  -name 'ant' | head -1)

# Setting PATH
if [ -f $ANT_BIN ];then
    ANT_HOME="$(dirname "$ANT_BIN")"
    if [ -d $ANT_HOME ];then
        if ! echo $PATH | grep ant &> /dev/null ;then
        export PATH=$ANT_HOME:$PATH
        echo '--> Exported ANT to path'
        fi
    fi
fi

# Check if ant is set
if ! which ant > /dev/null; then
    echo '--> Error : ant exec is missing'
fi

echo '--> Setup DONE!'