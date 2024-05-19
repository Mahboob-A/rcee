#!/bin/bash

user_files_dir="/user-codes/cpp/result"

echo "script run" 

g++ $user_files_dir/main.cpp -o $user_files_dir/main
compile_status=$?

if [ $compile_status -ne 0 ]; then
    echo "Compilation failed"
    exit $compile_status
fi

# Run the compiled executable
$user_files_dir/main < $user_files_dir/input.txt > $user_files_dir/output.txt