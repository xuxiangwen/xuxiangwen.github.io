## Github Pages配置

### 配置_config.yml

~~~
cat << EOF >> _config.yml
theme: jekyll-theme-architect
title: 欢迎来到eipi10!
description: 记录了学习的经历和所得，分享给所有的朋友i
defaults:
  - scope:
      path: ""
      type: "posts"
    values:
      layout: "default"
  - scope:
      path: ""
    values:
      layout: "default"
      
EOF
~~~

### 配置Gemfile

~~~
cat << EOF >> Gemfile
# frozen_string_literal: true

source "https://rubygems.org"

git_source(:github) {|repo_name| "https://github.com/#{repo_name}" }

# gem "rails"

gem "jekyll"
gem "jekyll-theme-architect"
gem "github-pages"
EOF

cat Gemfile
~~~

### 安装依赖包

#### 第一次

~~~
bundle install
~~~

#### 更新

~~~
bundle update
~~~



### 运行

##### 本地开发

~~~
bundle exec jekyll serve --host 0.0.0.0 --port 4000
~~~



