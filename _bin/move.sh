# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

md_path=$1
new_folder=$2

new_image_folder=$new_folder/images
$script_path/copy_image.sh $md_path $new_image_folder

echo move $md_path to $new_folder
mv $md_path $new_folder







