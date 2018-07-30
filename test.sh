#!/usr/bin/env bash

GCC='g++-8 -std=c++11 -O2 -Wl,-stack_size -Wl,40000000 -m64'
IN='in'
OUT='out'
ANS='ans'

function compile {
    compile=$GCC" -o $1 $path"
    if ! $compile 2> compile.log; then
        echo [1m[31mCompilation Error[0m
        cat compile.log
        rm compile.log
        exit
    fi
    rm compile.log
}

function outputAccepted {
    echo [1m[32mSample test \#$test_case: Accepted[0m `cat time.log`
}

function outputFailed {
    echo [1m[31mSample test \#$test_case: $1[0m `cat time.log`
    echo [1m[31mSample input \#$test_case[0m
    cat $test_case.$IN
    echo [1m[31mSample output \#$test_case[0m
    cat $test_case.$ANS
    echo [1m[31mProgram output \#$test_case[0m
    cat $test_case.$OUT
    echo ""
}

function programtest {
    ./$task &> out.log
    sed -i -e 's/Test Case #\([0-9]\)...PASSED/[1m[32mSample Input #\1: Accepted[0m/g' out.log
    sed -i -e 's/Test Case #\([0-9]\)...FAILED/[1m[31mSample Input #\1: Wrong Answer[0m/g' out.log
    cat out.log
    rm *.log*
}

function localtest {
    test_case=$1
    if ! [ -f $test_case.$ANS ]; then
        return
    fi
    if ! gtime -o time.log -f "(%es)" ./$task < $test_case.$IN > $test_case.$OUT; then
        outputFailed 'Runtime Error'
    else
        if diff -b --brief $test_case.$OUT $test_case.$ANS > diff.log; then
            outputAccepted
        else
            outputFailed 'Wrong Answer'
        fi
    fi
    rm *.log
}

function localalltests {
    for test_file in *.$IN; do
        test_case=${test_file%.*}
        localtest $test_case
    done
}

function topcoder {
    if [ -d $testdir ]; then
        return 0
    fi
    compile $task
    programtest
    rm $task
    return 1
}

function codeforces {
    compile $testdir/$task
    cd $testdir
    if [ "$#" -eq 1 ]; then
        localtest $1
    else
        localalltests
    fi
    rm $task
}

if [ "$#" -lt 1 -o "$#" -gt 2 ]; then
    echo [1m[31m'Error usage: ./test.sh contest/problem.cpp [-l | testcase]'[0m
    exit
fi

path=$1
dir=${path%/*}
file=${path##*/}
task=${file%.*}

if [ -d "$dir/tests/$task" ]; then
    testdir=$dir/tests/$task
else
    testdir="in"
fi

if [ "$#" -eq 2 ]; then
    if [ "$2" = "-l" ]; then
        testdir="test"
        codeforces
    else
        codeforces $2
    fi
else
    if topcoder == 0; then
        codeforces
    fi
fi
