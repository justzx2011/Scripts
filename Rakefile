#!/bin/bash
LANG=zh
dir=~/works/maplebeats.github.com/_posts
cd $dir
temp=/tmp/post.$$
editor=gedit

date +%F >$temp
echo $*.textile >>$temp
xargs <$temp |tee $temp
cat $temp|sed '/ \+/s//-/g' |tee $temp
touch `cat $temp`
#generate_filename ()
#{
#    echo -n `LANG=C date +%F`-"$1".textile
#}
#touch "`generate_filename miku`"
echo "输入文章title"
read post_title
echo "输入文章summary"
read post_summary
echo "---
layout: post
title: $post_title
summary: $post_summary
---
" >`cat $temp`
$editor `cat $temp`
exit 0
