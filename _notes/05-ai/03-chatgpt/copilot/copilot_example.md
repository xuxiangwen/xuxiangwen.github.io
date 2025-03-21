## Fetch outlook mails

1. create the project folder

   ```
   mkdir OutlookMail
   cd OutlookMail
   code .
   ```

2. Create a console project refer to  [Create a Hello World app](https://code.visualstudio.com/docs/csharp/get-started#_create-a-hello-world-app).

3. Open Copilot Chat

   ~~~
   create a hello program
   ~~~

   ~~~
   // fetch emails from Outlook app, meeting the following requirements:
   // 1. Filter emails whose title is "New Authentication Request".
   // 2. Read the latest email from the filtered list.
   ~~~

   

## Chinese

~~~
用c#写一段outlook收取邮件的代码，具体要求如下：
1. 按照邮件的title过滤邮件
2. 过滤的邮件列表中，读取最新那一封
3. 按照正则表达式提取其中的某一段内容
4. 把邮件删除
~~~



~~~
上面的代码中，library的引用有问题，修正一下
~~~



~~~
用c#写一段outlook收取邮件的代码，具体要求如下：
1. 按照邮件的title过滤邮件
2. 过滤的邮件列表中，读取最新那一封
3. 按照正则表达式提取其中的某一段内容
4. 把邮件删除
5. 命名空间要引用正确
~~~



~~~
Microsoft.Office.Interop.Outlook 对应的library是哪一个，如何加到c#项目中
~~~



~~~
用c#写一段outlook收取邮件的代码，具体要求如下：
1. 按照邮件的title过滤收件箱未读邮件，且邮件必须是最近一分钟收取的邮件
2. 过滤的邮件列表中，读取最新那一封
3. 按照正则表达式提取其中的某一段内容
4. 把邮件删除
5. 命名空间要引用正确
~~~



~~~
用c#写一段outlook收取邮件的代码，具体要求如下：
1. 按照条件 title=New Authentication Request 过滤收件箱未读邮件，且邮件必须是当前时间后收取的邮件。如果邮件列表为空，等待5秒后再试，如果不为空，执行如下步骤
2. 过滤的邮件列表中，读取最新那一封
3. 按照正则表达式\d{6}提取其中的某一段内容
4. 把邮件删除
5. 命名空间要引用正确
~~~

~~~
上面代码中Outlook找不到
~~~

~~~
修正了，另外也找不到Regex和Match
~~~

~~~
上面代码中，outlookApp.Session.Accounts找不到IsOpen这个属性
~~~

~~~
用c#写一个类，它所属命名空间是IGSONumber_Test，它有一个静态方法名为GetPasscode，该方法收取outlook邮件，具体要求如下：
1. 按照条件 title=New Authentication Request 过滤收件箱未读邮件，且邮件必须是最近一分钟收取的邮件。如果邮件列表为空，等待5秒后再试，如果不为空，执行如下步骤
2. 过滤的邮件列表中，读取最新那一封
3. 按照正则表达式\d{6}提取其中的某一段内容
4. 把邮件删除
5. 命名空间要引用正确
~~~

~~~

~~~

## English

~~~

~~~

