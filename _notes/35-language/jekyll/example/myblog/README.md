# 1. 入门

## 1.1 安装

### 1.11 Jekyll

#### [手动安装](https://www.jekyll.com.cn/docs/)

1. 安装一个完整的 [Ruby 开发环境](ruby.md) 

2. 安装 Jekyll 和[bundler](https://www.jekyll.com.cn/docs/ruby-101/#bundler) [gems](https://www.jekyll.com.cn/docs/ruby-101/#gems)

   ```
   gem install jekyll bundler  --http-proxy $http_proxy
   ```

3. 在./myblog目录下创建一个全新的 Jekyll 网站

   ```
   jekyll new myblog
   ```

   > 默认的路径在`/home/grid/eipi10/xuxiangwen.github.io/99-others/jekyll/myblog`

4. 进入新创建的目录

   ```
   cd myblog
   if [ ! -f _config.yml.template ]; then
     cp _config.yml _config.yml.template
   fi
   
   cp _config.yml.template _config.yml
   cat << EOF >> _config.yml
   host: 0.0.0.0 
   port: 4000 
   defaults:
     - 
       scope:
         path: ""
         type: "posts"
       values:
           layout: "post"
           title: "Default Title"
           
   EOF
   ```

5. 构建网站并启动一个本地 web服务

   ```
   bundle exec jekyll serve
   ```

6. 在浏览器中打开 [http://localhost:4000](http://localhost:4000/) 网址