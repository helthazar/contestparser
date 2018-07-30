#!/usr/bin/env bash

GCC='g++-8 -std=c++11 -pthread -fopenmp -O2 -Wl,-stack_size -Wl,40000000'
IN='in'
OUT='out'
ANS='ans'

function compile {
    compile=$GCC" -o $1 $dir/$task.cpp"
    if ! $compile 2> compile.log; then
        echo [1m[31mCompilation Error[0m
        cat compile.log
        rm compile.log
        exit
    fi
    rm compile.log
}

function outputStarted {
    echo [1m[32mTest $test_case: Started[0m
}

function outputAccepted {
    echo [1m[32mTest $test_case: Accepted[0m `cat time.log`
    if [ $full -eq 1 ]; then
        echo [1m[32mInput $test_case[0m
        cat $testdir/$test_case.$IN
        echo [1m[32mOutput $test_case[0m
        cat $dir/$test_case.$ANS
        echo ""
    fi
}

function outputFailed {
    echo [1m[31mTest $test_case: $1[0m `cat time.log`
    if [ $full -eq 1 ]; then
        echo [1m[31mInput $test_case[0m
        cat $testdir/$test_case.$IN
        echo [1m[31mOutput $test_case[0m
        cat $dir/$test_case.$ANS
        echo ""
    fi
}

function localtest {
    test_case=$1
    if [ -f $testdir/$test_case.$ANS ]; then
        return
    fi
    outputStarted
    if ! gtime -o time.log -f "(%es)" ./$dir/$task < $testdir/$test_case.$IN > $dir/$test_case.$ANS; then
        outputFailed 'Runtime Error'
    else
        outputAccepted
    fi
    rm *.log
}

function localtests {
    tests=$1
    for test_file in ${tests[@]}; do
        test_case=${test_file##*/}
        test_case=${test_case%.*}
        localtest $test_case
    done
}

function localalltests {
    for test_file in $testdir/*.in; do
        test_case=${test_file##*/}
        test_case=${test_case%.*}
        localtest $test_case
    done
}

function hashcode {
    compile $dir/$task
    tests=$1
    if [ -z "$tests" ]; then
        localalltests
    else
        localtests $tests
    fi
    rm $dir/$task
}

if [ "$#" -lt 1 ]; then
    echo [1m[31m'Error usage: ./run.sh contest/problem.cpp [-s] [testcases]'[0m
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

full=0
tests=()
for i in "${@:2}"
do
    if [ $i = "-f" ]; then
        full=1
    else
        if [ -f "$i" ]; then
            tests+=($i)
        fi
    fi
done

hashcode $tests
