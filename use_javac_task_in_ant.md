在ANT中使用javac任务

好吧，这篇文章要完成这个任务：

一个Android项目
让我们从一个小例子开始吧。这个例子只需要3个类


<target name="packJAR">
	<javac srcdir="${basedir}/src"
		destdir="${basedir}/bin"
		encoding="UTF-8"
		includeAntRuntime="false">
		<exclude name="us/sanguo/uc/**" />
		<classpath>
			  <fileset dir="${basedir}/libs">
				 <include name="**/*.jar"/>
			  </fileset>
			  <pathelement location="${ANDROID8}/android.jar"/>
		</classpath>
	</javac>
</target>
