[使用bash从SVN和Git中获取顺序版本号](http://zengrong.net/post/1798.htm)

在进行自动部署的时候，经常需要用脚本获取程序的最新版本号，下面是我的两个解决方案。

## for SVN
<pre lang="BASH">
# 获取XML版本的svn信息，这样可以避免不同语言的问题
__xml=`svn info --xml --incremental`
# 我们可以获取到2个版本号，一个是最新版本库版本号，一个是自己的提交版本号。删除自己提交的版本号。
__revision=`echo "$__xml"|sed '/revision/!d'|sed '$d'`
# 提取出版本号的数字部分
echo $__revision|sed 's/revision="\([0-9]\+\)">\?/\1/'
</pre>

## for Git

Git采用的是SHA散列码作为版本号，因此它没有顺序的版本号。但我们可以通过统计Git版本库的提交次数来获得一个顺序版本号。

<pre lang="BASH">
# 基准版本号默认是1，可以通过传递一个参数修改
get_version()
{
	local __base=${1:-1}
	echo $((`git rev-list --all|wc -l` + $__base))
}
get_version 7000
</pre>

这个版本对网上搜到的那个被普遍转载的版本做了简化和调整。网上那个版本写得比较复杂，例如awk的使用没有必要，而且要统计所有提交，应该用 `git rev-list --all` 参数，而不是用 `git rev-list HEAD`。
