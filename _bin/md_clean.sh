# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

filepath=$1

if [ "$filepath" = ""  ]
then
  echo please assign a markdown file
fi 

echo clean $filepath
sed  's/\$\$/\n\$\$\n/g' $filepath  > $script_path/temp.md
cat -s $script_path/temp.md > $filepath
rm -rf temp.md
