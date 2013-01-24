[在bash中替换屏幕上显示的行](http://zengrong.net/post/1799.htm)

在编写一些比较耗时的程序时，我经常需要在屏幕上显示一些进度信息。默认的echo在输出的时候，会将每一条进度信息换行显示，就像下面这样：

<pre lang="BASH">
for i in {1..3};do
	sleep 1
	echo "第$i次"
done
# 输出
第1次
第2次
第3次
</pre>

如果希望每次显示替换掉前一次显示，可以这样处理：

<pre lang="BASH">
for i in {1..3};do
	sleep 1
	echo -en "\r第$i次"
done
</pre>

`-n` 参数的作用是不在echo的结尾自动加入换行符，`-e` 参数的作用是对反斜杠字符进行转义。把它们用在一起，对输出文本中的 `\r` 进行了转义，相当于在上一行内容之后输入了一次回车，清空了当前行的显示。

下面的代码运行后，“倒计时完毕”字样会紧接在“第3次”之后，这个应该如何处理呢？

<pre lang="BASH">
for i in {1..3};do
	sleep 1
	echo -en "\r第$i次"
done
echo '倒计时完毕'
</pre>
