# !/bin/bash
markdown_file=$1
jekyll_image_path=$2

file_folder=$(dirname "$markdown_file")
file_name=$(basename "$markdown_file")

markdown_file_clean=$file_folder/$file_name.markdown
cp $markdown_file  $markdown_file_clean
# 修改图片的引用路径
sed -i 's/\](images\//\](\/assets\/images\//g'  $markdown_file_clean

# 把图片拷贝到Jekyll的图片目录
if [ -d /images ]; then
  mkdir -p $jekyll_image_path
  cp $file_folder/images/* $jekyll_image_path
fi

# Tex/LaTex Display Math换行居中
awk '{
if ($0 ~ /^\s*\$\$\s{0,10}$/)
print "\n"$0"\n"
else 
  print $0
}' $markdown_file_clean > temp.md
cat -s temp.md > $markdown_file_clean
rm -rf temp.md

# 避免\{\{被Jekyll当作Liquid
sed -i 's/{\s*{/{ \n {/g' $markdown_file_clean

echo generate $markdown_file_clean, please check if the file is correct or not
echo if yes, run \"cp $markdown_file_clean $markdown_file\" to replace.
  
