使用说明

1.	文件夹：
a)	bin执行文件夹（这里为空）
b)	conf 配置文件夹（这里没有任何配置）
c)	lib 转码功能依赖包（必须加到classpath里面）
d)	example 实例程序文件夹
2.	实例
如example/ExampleTester.java所示
只需要初始化实例SilentSimpler则可以通过实例的方法getPageContent()拿到转码内容。

实例化方法为
SilentSimpler(content,imgStr)

参数：
content：网页内容
imgStr:  图片json字符串，格式应该为
{
	"www.baidu.com/a.jpg": {"width": "620px", "height": "620px"}, 
	"www.baidu.com/b.jpg": {"width": "220px", "height": "220px"}
}

3.	有问题请联系
冯炜（fengwei04@baidu.com）
