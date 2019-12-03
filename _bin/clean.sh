# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

echo start replace \$\$ to \\n\$\$\\n 
for filepath in $(find $script_path/../_notes  -name '*.md')
do 
  echo $filepath
  sed -i 's/\$\$/\n\$\$\n/g' $filepath
done

for filepath in $(find $script_path/../_posts  -name '*.md')
do
  echo $filepath
  sed -i 's/\$\$/\n\$\$\n/g' $filepath
done
