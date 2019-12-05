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
  
  # check if the file_name contains date
  if [[ $file_name =~ [0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
    echo can not generate $filepath because it is already generated.    
    return
  fi
  
  
  md_date=`cat $filepath | grep 'date:' |awk '{print $2}' | head -n 1 | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"`
  if [[ "${md_date}" = "" ]]; then
    echo can not find correct date as blog date in $filepath     
    return    
  fi
  
  # delete previous published file
  for old_file in $(ls $file_folder | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}-$file_name")
  do
    rm -rf $file_folder/$old_file
  done
  
  publish_path=$file_folder/${md_date}-$file_name
  echo cp $filepath $publish_path
  cp $filepath $publish_path
  sed -i 's/(images\//(\/assets\/images\//g'  $publish_path  

  # add line break 
  sed  's/\$\$/\n\$\$\n/g' $publish_path  > $script_path/temp.md
  cat -s $script_path/temp.md > $publish_path
  rm -rf $script_path/temp.md 

  # convert one dollar sign to two-dollar sign
  sed -i 's/\$/\$\$/g' $publish_path  
  sed -i 's/\$\$\$\$/\$\$/g' $publish_path

  # copy image
  echo cp $file_folder/images/* $jekyll_image_path
  cp $file_folder/images/* $jekyll_image_path
}

if [ -d "$file_or_folder" ]; then
  echo start publish $file_or_folder
  for filepath in $(find $file_or_folder  -name '*.md' | grep -Ev '[0-9]{4}-[0-9]{2}-[0-9]{2}')
  do
    generate_one $filepath
  done
elif [ -f "$file_or_folder" ]; then
  generate_one $file_or_folder
else
  echo $file_or_folder does not exist
fi






