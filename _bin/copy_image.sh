# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

md_path=$1
new_image_folder=$2

md_folder=$(dirname "$md_path")
md_file=$(basename "$md_path")

num=0
for img in `grep -P '!\[.*\]\(.*\)' $md_path`
do
  img_file=`echo $img | sed 's/.*](\(.*\))/\1/g'`
  old_image_path=$md_folder/$img_file
  echo copy $old_image_path to $new_image_folder
  cp $old_image_path $new_image_folder
  num=$((num + 1))
done

echo copy $num files to $new_image_folder
