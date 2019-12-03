本文来自[Pytest 使用手册](https://learning-pytest.readthedocs.io/zh/latest/index.html)

Pytest 是 Python 的一种单元测试框架，与 Python 自带的 unittest 测试框架类似，但是比 unittest 框架使用起来更简洁，效率更高。Pytest 是一个成熟的全功能的 Python 测试工具，可以帮助你写出更好的程序，让我们很方便的编写测试用例。

# 1. 快速入门

##  Install

~~~
pip install pytest
~~~

## First Function

下面是最简单的测试方法。其中一个是成功的，一个是失败的。

~~~
cat << EOF > test1.py

def test_passing():
    assert (1, 2, 3) == (1, 2, 3)
    
EOF

cat << EOF > test2.py
def test_failing():
    assert (1, 2, 3) == (3, 2, 1)
    
EOF

pytest test1.py
pytest test2.py
~~~

> pytest 使用 `.` 标识测试成功（`PASSED`）
>
> pytest 使用 `F` 标识测试失败（`FAILED`）

# 2. 测试函数

## 捕获异常

在测试过程中，经常需要测试是否如期抛出预期的异常，以确定异常处理模块生效。在 pytest 中使用 `pytest.raises()` 进行异常捕获：

~~~
cat << EOF > test_raises.py
import pytest

def connect(host, port):
    if not isinstance(port,int):
        raise TypeError('port type must be int')

def test_raises():
    with pytest.raises(TypeError) as e:
        connect('localhost', '6379')
    exec_msg = e.value.args[0]
    assert exec_msg == 'port type must be int'
    
    
EOF

pytest test_raises.py
~~~

## 标记函数

### Pytest 查找测试策略

默认情况下，pytest 会递归查找当前目录下所有以 `test` 开始的 Python 脚本，并执行文件内的所有以 `test` 开始或结束的函数和方法。

~~~
cat << EOF > test_no_mark.py

def test_func1():
    assert 1 == 1

def func2_test():
    assert 1 != 1
    
def test_func3():
    assert 1 != 1   
    
EOF

pytest -v test_no_mark.py
~~~

> 只有开头的test才能被识别。

### 标记测试函数

使用 mark，我们可以给每个函数打上不同的标记，测试时指定就可以允许所有被标记的函数。

~~~
cat << EOF > test_with_mark.py
import pytest

@pytest.mark.finished
def test_func1():
    assert 1 == 1

@pytest.mark.finished
def test_func2():
    assert 1 != 1

@pytest.mark.unfinished
def test_func3():
    assert 1 != 1   
    
EOF

pytest -m finished -v test_with_mark.py
~~~

## 跳过测试

如果我们事先知道测试函数会执行失败，但又不想直接跳过，而是希望显示的提示。

~~~
cat << EOF > test_skip.py
import pytest
@pytest.mark.skip(reason='out-of-date api')
def test_connect():
    pass
EOF

pytest test_skip.py    
~~~

> pytest 使用 `s` 表示测试被跳过（`SKIPPED`）。

Pytest 还支持使用 `pytest.mark.skipif` 为测试函数指定被忽略的条件。

~~~
@pytest.mark.skipif(conn.__version__ < '0.2.0',
                    reason='not supported until v0.2.0')
def test_api():
    pass
~~~

## 预见的错误

~~~
cat << EOF > test_xfail.py
import pytest

class Generator():
    def __init__(self, version='0.1.0'):
        self.__version__ = version
    def unique_id(self):
        return 1
        
gen = Generator('0.1.0')

@pytest.mark.xfail(gen.__version__ < '0.2.0',
                   reason='not supported until v0.2.0')
def test_api():
    id_1 = gen.unique_id()
    id_2 = gen.unique_id()
    assert id_1 != id_2

def test_api1():
    id_1 = gen.unique_id()
    id_2 = gen.unique_id()
    assert id_1 == id_2
    
EOF

pytest -v test_xfail.py
~~~

> pytest 使用 `x` 表示预见的失败（`XFAIL`）。
>
> 如果预见的是失败，但实际运行测试却成功通过，pytest 使用 `X` 进行标记（`XPASS`）

## 参数化

当对一个测试函数进行测试时，通常会给函数传递多组参数。比如测试账号登陆，我们需要模拟各种千奇百怪的账号密码。当然，我们可以把这些参数写在测试函数内部进行遍历。不过虽然参数众多，但仍然是一个测试，当某组参数导致断言失败，测试也就终止了。

通过异常捕获，我们可以保证程所有参数完整执行，但要分析测试结果就需要做不少额外的工作。

在 pytest 中，我们有更好的解决方法，就是参数化测试，即每组参数都独立执行一次测试。使用的工具就是 `pytest.mark.parametrize(argnames, argvalues)`。

~~~
cat << EOF > test_parametrize.py
import pytest
@pytest.mark.parametrize('passwd',
                      ['123456',
                       'abcdefdfs',
                       'as52345fasdf4'])
def test_passwd_length(passwd):
    assert len(passwd) >= 8
    
@pytest.mark.parametrize('user, passwd',
                         [('jack', 'abcdefgh'),
                          ('tom', 'a123456a')])
def test_passwd_md5(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }

    import hashlib

    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]    

@pytest.mark.parametrize('user, passwd',
                         [pytest.param('jack', 'abcdefgh', id='User<Jack>'),
                          pytest.param('tom', 'a123456a', id='User<Tom>')])
def test_passwd_md5_id(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }

    import hashlib

    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]

EOF

pytest -v test_parametrize.py
~~~

#  3. 固件fixture

固件（Fixture）是一些函数，pytest 会在执行测试函数之前（或之后）加载运行它们。我们可以利用固件做任何事情，其中最常见的可能就是数据库的初始连接和最后关闭操作。

~~~
# test_postcode.py

@pytest.fixture()
def postcode():
    return '010'

def test_postcode(postcode):
    assert postcode == '010'
~~~

固件可以直接定义在各测试脚本中，就像上面的例子。更多时候，我们希望一个固件可以在更大程度上复用，这就需要对固件进行集中管理。Pytest 使用文件 `conftest.py` 集中管理固件。不要自己显式调用 `conftest.py`，pytest 会自动调用，可以把 conftest 当做插件来理解。

## 预处理和后处理

~~~
cat << EOF > test_db.py 
import pytest
@pytest.fixture()
def db():
    print('Connection successful')

    yield

    print('Connection closed')

def search_user(user_id):
    d = {
        '001': 'xiaoming'
    }
    return d[user_id]

def test_search(db):
    assert search_user('001') == 'xiaoming'

EOF

pytest -s test_db.py             # 执行时使用 -s 阻止消息被吞：
pytest --setup-show  test_db.py  # 详细跟踪fixture的调用
~~~

## 作用域

固件的作用是为了抽离出重复的工作和方便复用，为了更精细化控制固件（比如只想对数据库访问测试脚本使用自动连接关闭的固件），pytest 使用作用域来进行指定固件的使用范围。

在定义固件时，通过 `scope` 参数声明作用域，可选项有：

- `function`: 函数级，每个测试函数都会执行一次固件；默认的作用域为 `function`。
- `class`: 类级别，每个测试类执行一次，所有方法都可以使用；
- `module`: 模块级，每个模块执行一次，模块内函数和方法都可使用；
- `session`: 会话级，一次测试只执行一次，所有被找到的函数和方法都可用。

~~~
cat << EOF > test_scope.py 
import pytest
@pytest.fixture(scope='function')
def func_scope():
    pass

@pytest.fixture(scope='module')
def mod_scope():
    pass

@pytest.fixture(scope='session')
def sess_scope():
    pass

@pytest.fixture(scope='class')
def class_scope():
    pass
    
@pytest.mark.usefixtures('class_scope')
class TestClassScope:
    def test_1(self):
        pass

    def test_2(self):
        pass    

def test_multi_scope(sess_scope, mod_scope, class_scope, func_scope):
    pass
    
def test_multi_scope1(sess_scope, mod_scope, class_scope, func_scope):
    pass    
EOF

pytest --setup-show test_scope.py 
~~~

## 自动执行

目前为止，所有固件的使用都是手动指定，或者作为参数，或者使用 `usefixtures`。如果我们想让固件自动执行，可以在定义时指定 `autouse` 参数。

~~~python
cat << EOF > test_autouse.py
import pytest
import time

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

@pytest.fixture(scope='session', autouse=True)
def timer_session_scope():
    start = time.time()
    print('\nstart: {}'.format(time.strftime(DATE_FORMAT, time.localtime(start))))

    yield

    finished = time.time()
    print('finished: {}'.format(time.strftime(DATE_FORMAT, time.localtime(finished))))
    print('Total time cost: {:.3f}s'.format(finished - start))

@pytest.fixture(autouse=True)
def timer_function_scope():
    start = time.time()
    yield
    print(' Time cost: {:.3f}s'.format(time.time() - start))
    

def test_1():
    time.sleep(1)

def test_2():
    time.sleep(2)
    
EOF

pytest -s test_autouse.py
~~~

### 重命名

固件的名称默认为定义时的函数名，如果不想使用默认，可以通过 `name` 选项指定名称：

~~~
# test_rename.py

@pytest.fixture(name='age')
def calculate_average_age():
    return 28

def test_age(age):
    assert age == 28
~~~

## 参数化

固件也是函数，我们同样可以对固件进行参数化。在什么情况下需要对固件参数化？

假设现在有一批 API 需要测试对不同数据库的支持情况（对所有数据库进行相同操作），最简单的方法就是针对每个数据库编写一个测试用例，但这包含大量重复代码，如数据库的连接、关闭，查询等。

进一步，可以使用固件抽离出数据库的通用操作，每个 API 都能复用这些数据库固件，同时可维护性也得到提升。

更进一步，可以继续将这些固件合并为一个，而通过参数控制连接到不同的数据库。这就需要使用固件参数化来实现。固件参数化需要使用 pytest 内置的固件 `request`，并通过 `request.param` 获取参数。

~~~
cat << EOF > test_parametrize.py
import pytest

@pytest.fixture(params=[
    ('redis', '6379'),
    ('elasticsearch', '9200')
])
def param(request):
    return request.param

@pytest.fixture(autouse=True)
def db(param):
    print('\nSucceed to connect %s:%s' % param)

    yield

    print('\nSucceed to close %s:%s' % param)

def test_api():
    assert 1 == 1
    
EOF

pytest -s test_parametrize.py
~~~

## 内置固件fixture

内置固件fixture，即pytest已经定义好的fixture， 可以直接使用。

### tmpdir & tmpdir_factory

用于临时文件和目录管理，默认会在测试结束时删除。

- `tmpdir` 只有 `function` 作用域，只能在函数内使用。
- `tmpdir_factory` 可以在所有作用域使用，包括 `function, class, module, session`

~~~
cat << EOF > test_tmpdir.py
import pytest

def test_tmpdir(tmpdir):
    a_dir = tmpdir.mkdir('mytmpdir')
    a_file = a_dir.join('tmpfile.txt')

    a_file.write('hello, pytest!')

    assert a_file.read() == 'hello, pytest!'

@pytest.fixture(scope='module')
def my_tmpdir_factory(tmpdir_factory):
    a_dir = tmpdir_factory.mktemp('mytmpdir')
    a_file = a_dir.join('tmpfile.txt')

    a_file.write('hello, pytest!')

    return a_file

def test_tmpdir_factory(my_tmpdir_factory):
    assert my_tmpdir_factory.read() == 'hello, pytest!'

EOF

pytest --setup-show test_tmpdir.py
~~~

### pytestconfig

用 `pytestconfig`，可以很方便的读取命令行参数和配置文件。`pytestconfig` 其实是 `request.config` 的快捷方式，所以也可以自定义固件实现命令行参数读取。

~~~
cat << EOF > conftest.py
import pytest
def pytest_addoption(parser):
    parser.addoption('--host', action='store',
                     help='host of db')
    parser.addoption('--port', action='store', default='8888',
                     help='port of db')

@pytest.fixture
def config(request):
    return request.config

EOF

cat << EOF > test_config.py
def test_option1(pytestconfig):
    print('host: %s' % pytestconfig.getoption('host'))
    print('port: %s' % pytestconfig.getoption('port'))

def test_option2(config):
    print('host: %s' % config.getoption('host'))
    print('port: %s' % config.getoption('port'))

EOF

pytest -s --host=localhost test_config.py
pytest -s --setup-show test_config.py
~~~

