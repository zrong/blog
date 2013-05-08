[在PHP中读取二进制文件](http://zengrong.net/post/1715.htm)

很多时候，数据并不是用文本的方式保存的，这就需要将二进制数据读取出来，还原成我们需要的格式。PHP在二进制处理方面也提供了强大的支持。

## 任务

下面以读取并分析一个PNG图像的文件头为例，讲解如何使用PHP读取和分析二进制文件。

## 涉及函数

* [fopen](http://www.php.net/manual/zh/function.fopen.php)
* [fread](http://www.php.net/manual/zh/function.fread.php)
* [unpack](http://www.php.net/manual/zh/function.unpack.php)
* [bin2hex](http://www.php.net/manual/zh/function.bin2hex.php)

## PNG格式简介

为了完成任务，下面简单介绍一下PNG文件格式。
PNG是一种无损压缩的图像文件格式，该格式的第1-8字节保存着PNG署名域，内容如下：

* 十进制：		137	80	78	71	13	10	26	10
* 十六进制：	89	50	4e	47	0d	0a	1a	0a

我们的任务就是将这个文件头读取出来。

更详细的关于PNG格式的介绍：
* <http://www.w3.org/TR/2003/REC-PNG-20031110/>
* <http://www.libpng.org/pub/png/>

## 读取文件

<pre lang="PHP">
$filePath = "icon.png";
//必须使用rb来读取文件，这样能保证跨平台二进制数据的读取安全
$fh = fopen($filePath, "rb");
//仅读取前面的8个字节
$head = fread($fh, 8);
fclose($fh);
</pre>

上面的代码已经把我们需要的8个字节读入变量head中了。head是一个保存二进制数据的数组，我们还需要对它做一些操作才能得到我们需要的数据。

## unpack

unpack可以将二进制数据解析成关系数组，它接受2个参数，第一个提供解析方式字符串（见下方），第二个参数就提供我们前面读出的head变量就可以了。

* a：NULL填充的字节串
* A：空格填充的字节串
* h：十六进制数，低四位字节优先
* H：十六进制数，高四位字节优先
* c：有符号字符
* C：无符号字符
* s：有符号短整型(总是16位，机器字节序)
* S：无符号短整型(总是16位，机器字节序)
* n：无符号短整型(总是16位，大尾字节序)
* v：无符号短整型(总是16位，小尾字节序)
* I：有符号整型(机器相关大小和字节序)
* I：无符号整型(机器相关大小和字节序)
* l：有符号长整型(总是32位，机器字节序)
* L：无符号长整型(总是32位，机器字节序)
* N：无符号长整型(总是32位，大尾字节序)
* V：无符号长整型(总是32位，小尾字节序)
* f：浮点数(机器相关大小和表示)
* d：双精度数(机器相关大小和表示)
* x：空字节
* X：倒退一个字节
* @：用NULL填充绝对位置

unpack的第一个参数在在使用上有一点点小技巧，下面是范例：

* C 读取1个字符，返回的数组索引为1
* C4 读取4个字节，每个字节一个字符，返回的数组索引为1，2，3，4
* C4head 读取4个字符，每个字节一个字符，返回的数组索引为head1，head2，head3，head4
* Chead 读取1个字符，返回的数组索引为head

现在试着读取第1个字节：

<pre lang="PHP">
$arr = unpack("Chead", $head);
print_r($arr);
//Array ( [head] => 137 )
</pre>

读取所有的8个字节，用斜杠可以分隔：

<pre lang="PHP">
$arr = unpack("Chead/C3string/C4number", $head);
print_r($arr);
//Array ( [head] => 137 [string1] => 80 [string2] => 78 [string3] => 71 [number1] => 13 [number2] => 10 [number3] => 26 [number4] => 10 )
</pre>

把string开头的键拼成字符串：

<pre lang="PHP">
$arr = unpack("Chead/C3string/C4number", $head);
for($i=1;$i<=3;$i++)
{
	$type.=chr($arr['string'.$i]);
}
echo $type;
//PNG
</pre>

## bin2hex

上面使用print_r打印出来的内容，都是十进制数字，如果希望直接得到十六进制值，可以使用bin2hex函数。

<pre lang="PHP">
echo bin2hex($head[0]);
//89
</pre>

注意，使用这种方法得到的是字符串，并不是数字。因此下面的条件是不成立的：

<pre lang="PHP">
if(bin2hex($head[0]) == 0x89)
{
	echo 'match!';
}
</pre>
