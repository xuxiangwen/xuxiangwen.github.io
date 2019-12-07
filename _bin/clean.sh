# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

file_or_folder=$1
jekyll_image_path=$script_path/../assets/images
mkdir -p $jekyll_image_path

if [ "$file_or_folder" = ""  ]
then
  echo please assign a folder or a markdown file
fi

generate_one(){
  filepath=$1
  file_folder=$(dirname "$filepath")
  file_name=$(basename "$filepath")

  echo -------------------------------------------------------
  echo start generate blogs on $filepath



#  # convert one dollar sign to two-dollar sign
  sed -i 's/\$/\$\$/g' $filepath
  sed -i 's/\$\$\$\$/\$\$/g' $filepath
  sed -i 's/\\\$\$/\\\$/g' $filepath

}


if [ -d "$file_or_folder" ]; then
  echo start to generate folder: $file_or_folder
  for filepath in $(find $file_or_folder  -name '*.md' | grep -Ev '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  do
    generate_one $filepath
  done
  echo finish to generate folder: $file_or_folder
elif [ -f "$file_or_folder" ]; then
  echo start to generate file: $file_or_folder
  generate_one $file_or_folder
  echo finish to generate file: $file_or_folder
else
  echo $file_or_folder does not exist
fi

