#### [Docker安装](https://github.com/envygeeks/jekyll-docker/blob/master/README.md)

~~~
mkdir -p docker-myblog
mkdir -p docker-myblog/vendor/bundle
cd docker-myblog
rm _config.yml
echo host: 0.0.0.0 >> _config.yml
echo port: 4000    >> _config.yml
 
docker run  \
  --volume="$PWD:/srv/jekyll" \
  --volume="$PWD/vendor/bundle:/usr/local/bundle" \
  -p 14000:4000 \
  -it jekyll/jekyll:latest \
  jekyll serve  
~~~

