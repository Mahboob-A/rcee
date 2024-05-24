#!/bin/bash 

# Judge container volume mount and Sibling container volume mount is same. Hence, 
# the full filepath in Judge container is the filepath for the  Sibling container too. 

g++ $user_file_parent_dir/main.cpp -o $user_file_parent_dir/main 
compile_status=$?

if [ $compile_status -ne 0 ]; then 
    echo "Compile Failed"
    exit $compile_status 
fi

# run the binary 
$user_file_parent_dir/main < $user_file_parent_dir/input.txt > $user_file_parent_dir/output.txt 