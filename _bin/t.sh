# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

message=${1:-publish blogs}

echo start to publish
echo ===========================================================
echo git pull 
git pull
echo ===========================================================
echo $script_path/generate.sh $script_path/../_posts
$script_path/generate.sh $script_path/../_posts
echo ===========================================================
echo push to github
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







