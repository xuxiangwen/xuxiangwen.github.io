PowerShell 是一种命令行 shell 和脚本语言一体化工具。 它被设计为任务引擎，使用 cmdlet 来包装用户需要执行的任务。 在 PowerShell 中，可以在本地或远程计算机上运行命令。 可以执行管理用户和自动执行工作流等任务。

PowerShell 由命令行 shell 和脚本语言两部分组成。 它最初是一种框架，用于在 Windows 中自动执行管理任务。 PowerShell 现已发展为一种跨平台工具，用于执行多种任务。

## Skills

### Enable Running Scripts

~~~powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
~~~

![image-20240229214057161](images/image-20240229214057161.png)

### 验证PowerShell安装情况

~~~powershell
$PSVersionTable
~~~

![image-20240229205804413](images/image-20240229205804413.png)

~~~powershell
$PSVersionTable.PSVersion
~~~

![image-20240229205853363](images/image-20240229205853363.png)

### 使用 Get-Command 查找命令

~~~powershell
Get-Command -Noun e*
~~~

![image-20240229211338463](images/image-20240229211338463.png)

~~~powershell
Get-Command -Verb Get -Noun e*
~~~

![image-20240229211325914](images/image-20240229211325914.png)

### 创建文件

~~~powershell
new-item helloworld.ps1
~~~

![image-20240229214535099](images/image-20240229214535099.png)

