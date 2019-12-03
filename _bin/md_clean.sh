# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

file_or_folder=$1

if [ "$file_or_folder" = ""  ]
then
  echo please assign a folder or a markdown file
fi 

clean_one(){
  filepath=$1
  echo clean $filepath
  sed  's/\$\$/\n\$\$\n/g' $filepath  > $script_path/temp.md
  cat -s $script_path/temp.md > $filepath
  rm -rf $script_path/temp.md
}

if [ -d "$file_or_folder" ]; then
  echo start clean $file_or_folder
  for filepath in $(find $file_or_folder  -name '*.md')
  do
    clean_one $filepath
  done
elif [ -f "$file_or_folder" ]; then
  clean_one $file_or_folder
else
  echo $file_or_folder does not exist
fi


