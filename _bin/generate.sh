# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

file_or_folder=$1
jekyll_post_path=$script_path/../_posts
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

  # check if the file_name contains date
  if [[ $file_name =~ [0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
    echo can not generate $filepath because it is already generated.
    return
  fi

  md_date=`head -n 10 $filepath | grep 'date:' |awk '{print $2}' | head -n 1 | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"`
  if [[ "${md_date}" = "" ]]; then
    echo can not find correct date as blog date in $filepath
    return
  fi

  # delete previous published file
  for old_file in $(ls $jekyll_post_path | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}-$file_name")
  do
    rm -rf $jekyll_post_path/$old_file
  done

  publish_path=$jekyll_post_path/${md_date}-$file_name
  echo cp $filepath $publish_path
  cp $filepath $publish_path
  sed -i 's/\](images\//\](\/assets\/images\//g'  $publish_path
   
  # add line break when find $$
  awk '{
if ($0 ~ /^\s*\$\$\s{0,10}$/)
	print "\n"$0"\n"
else 
  print $0
}'  $publish_path  > $script_path/temp.md
  cat -s $script_path/temp.md > $publish_path
  rm -rf $script_path/temp.md


  # add line break between { and {
  sed -i 's/{{/{ \n {/g' $publish_path
  sed -i 's/{ {/{ \n {/g' $publish_path

  # copy image
  if [ -d $file_folder/images ]; then
    echo cp $file_folder/images/ to $jekyll_image_path
    cp $file_folder/images/* $jekyll_image_path
  fi

  #add sourcepath
  sed -i "1,3 s|---|---\n# generated from $filepath\n|"  $publish_path

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

