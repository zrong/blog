Lua中的字节流序列化

Lua语言并没有为我们提供封装好的字节流序列化库。我们需要动手封装一个类似 JAVA 的 `java.nio.ByteBuffer` 或 Actionscript 的 `flash.utils.ByteArray` 的库，方便自己使用。

下面是封装的要点。

1. 依赖库；
1. byte 与 char；
1. 数字；
1. 字符串与中文

这个封装本身的技术难度并不大，因为我们可以依赖极好的库。但实现这个封装，有助于梳理字节流和序列化的相关知识，更帮我复习了一遍 Actionscript 和 JAVA。

	local __ba = ByteArrayVarint.new()
	__ba:writeByte(0x59)
	__ba:writeByte(0x7a)
	__ba:writeByte(0)
	__ba:writeInt(11)
	__ba:writeShort(1101)
	__ba:writeByte(0)
	__ba:writeByte(3)
	__ba:writeByte(bit.bor(0,0))
	__ba:writeByte(bit.bor(bit.lshift(1,3), 0))
	__ba:writeByte(bit.bor(bit.lshift(2,3), 0))
	__ba:writeUVInt(1000)
	__ba:writeUVInt(1)
	__ba:writeUVInt(1)
	__ba:writeStringUVInt("English")
	__ba:writeStringUVInt("中文")
	__ba:setPos(1)
	print(__ba:toString())

	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readInt())
	print(__ba:readShort())
	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readByte())
	print(__ba:readUVInt())
	print(__ba:readUVInt())
	print(__ba:readUVInt())
	print(__ba:readStringUVInt())
	print(__ba:readStringUVInt())
	print(__ba:getAvailable())


	local __ba = ByteArray.new()
	__ba:writeUByte(66666)
	__ba:setPos(1)
	print(__ba:getLen())
	print(__ba:readByte())
	--print(__ba:readByte())
	--print(__ba:readByte())
	--print(__ba:readByte())

	--local __cn = "我是中文我"
	--print(__cn)
	--print('cn len:', #__cn)
	--print("sting.byte cn:", string.byte(__cn, 1, #__cn))
	--local __bits = string.pack("<a", __cn)
	--print('bits len:', #__bits)
	--local __len, __val = string.unpack(__bits, "<a")
	--print("unpack bits:", __len, __val)
	--print("string.byte bits:", string.byte(__bits, 1, #__bits))
	--print("hex bits:", hex(__bits))

	local __bits = string.pack("d", 333.666)
	local __bits2 = string.pack("f", 333.666)
	print("double:" ,string.byte(__bits, 1, #__bits))
	print("float:" ,string.byte(__bits2, 1, #__bits2))
	print(string.unpack(__bits, "d"))
	print(string.unpack( __bits2, "f"))

	local __dlong = string.pack("d", 99999999.99)
	local __long = string.pack("l", 99999999)
	local __ulong = string.pack("L", 99999999)
	local __nlong = string.pack("n", 99999999.99)

	print("dlong:", #__dlong)
	print("dlong:" ,string.byte(__dlong, 1, #__dlong))

	print("long:", #__long)
	print("long:" ,string.byte(__long, 1, #__long))

	print("ulong:", #__ulong)
	print("ulong:" ,string.byte(__ulong, 1, #__ulong))

	print("nlong:", #__nlong)
	print("nlong:" ,string.byte(__nlong, 1, #__nlong))

	print("hex", hex(__nlong))
	print("hex", hex(__nlong))

	local __str = "ABC"
	print(#__str)
