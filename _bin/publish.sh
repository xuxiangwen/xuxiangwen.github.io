# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

publish_path=${1:-$script_path/../_posts}
message=${2:-publish blogs}

echo start to publish
echo ===========================================================
echo git pull 
git pull
echo ===========================================================
echo $script_path/generate.sh $publish_path
$script_path/generate.sh $publish_path
echo ===========================================================
echo push to github
echo git add $publish_path
if [ -d "$publish_path" ]; then
  git add $publish_path/*
elif [ -f "$publish_path" ]; then
  git add $publish_path
fi

echo git add $script_path/../_posts/*
git add $script_path/../_posts/* 
echo git add $script_path/../assets/*
git add $script_path/../assets/*
echo git commit -m "$message"
git commit -m "$message"
echo git push
git push
echo ===========================================================
echo finish to publish







