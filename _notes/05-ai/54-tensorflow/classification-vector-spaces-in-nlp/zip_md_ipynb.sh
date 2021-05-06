# !/bin/bash

script=$(readlink -f "$0")
script_path=$(dirname "$script")

zip_file=$1
file_name=$(basename "$zip_file")
file_name=${file_name%.*}
zip_path=$script_path/$file_name
md_file=$zip_path/$file_name.md
notebook_file=$zip_path/$file_name.ipynb
mkdir -p $zip_path

target_path=${2:-$script_path}
mkdir -p $target_path

echo unzip $zip_file -d $zip_path
unzip $zip_file -d $zip_path

echo notedown $md_file \> $notebook_file
notedown $md_file > $notebook_file

echo mv $notebook_file $target_path
mv $notebook_file $target_path

