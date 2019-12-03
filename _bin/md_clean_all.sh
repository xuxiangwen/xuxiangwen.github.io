# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

echo start clean $script_path/../_notes 
echo ---------------------------------------------------
for filepath in $(find $script_path/../_notes  -name '*.md')
do 
  $script_path/md_clean.sh $filepath  
done
echo ---------------------------------------------------

echo
echo start clean $script_path/../_posts 
echo ---------------------------------------------------
for filepath in $(find $script_path/../_posts  -name '*.md')
do
  $script_path/md_clean.sh $filepath
done
echo ---------------------------------------------------

