# !/bin/bash
script=$(readlink -f "$0")
script_path=$(dirname "$script")

git pull
$script_path/generate.sh _posts
cd $script_path/..
bundle exec jekyll serve --host 0.0.0.0 --port 4000  
