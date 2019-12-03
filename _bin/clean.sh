# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

echo start replace \$\$ to \\n\$\$\\n 
for filepath in $(find $script_path/../_notes  -name '*.md')
do 
  echo $filepath
  sed  's/\$\$/\n\$\$\n/g' $filepath  > $script_path/temp.md
  cat -s $script_path/temp.md > $filepath  
done

for filepath in $(find $script_path/../_posts  -name '*.md')
do
  echo $filepath
  sed  's/\$\$/\n\$\$\n/g' $filepath >  $script_path/temp.md
  cat -s $script_path/temp.md > $filepath  
done

rm -rf temp.md
