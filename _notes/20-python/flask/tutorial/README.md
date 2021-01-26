# [Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)

本文摘自[Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)。

本教程使用Flaskr创建一个基本的blog application。

![screenshot of index page](image/flaskr_index.png)

## [Project Layout](https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/)

~~~
mkdir flask-tutorial
cd flask-tutorial
~~~

在该目录下，在教程过程中，将会创建以下文件。

- `flaskr/`, a Python package containing your application code and files.
- `tests/`, a directory containing test modules.
- Installation files telling Python how to install your project.
- Version control config, such as [git](https://git-scm.com/).

具体的内容如下：

~~~
/home/grid/eipi10/flask/tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
~~~

创建.gitignore

~~~
cat << EOF > .gitignore
venv/

*.pyc
__pycache__/

instance/

.pytest_cache/
.coverage
htmlcov/

dist/
build/
*.egg-info/


EOF
~~~



## [Application Setup](https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/)

创建Flask实例的推荐方式是在*application factory*中创建。

### The Application Factory

~~~python
mkdir -p flaskr
cat << EOF > flaskr/__init__.py
import os

from flask import Flask
from . import db, auth, blog


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    	
    db.init_app(app)   
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

EOF


~~~

代码说明：

- `app = Flask(__name__, instance_relative_config=True)` 、

  - instance_relative_config=True： 知识app的配置文件是相对于instance folder的。

-  blog blueprint

  - 没有定义url_prefix，这意味着该blueprint是`/`开始路由的。
  - app.add_url_rule： 关联`index`和`/`。这使得`url_for('index')` or `url_for('blog.index')` 都能生成 `/` URL
  
  

### Run The Application

~~~
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --port 5002 --host 0.0.0.0
~~~

## [Define and Access the Database](https://flask.palletsprojects.com/en/1.1.x/tutorial/database/)

### Connect to the Database

~~~
cat << EOF > flaskr/db.py
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

EOF

~~~

- g： 是一个特殊的对象，对于每一次request来说，它是唯一的。通常它用于保存被多个函数访问的数据。
- current_app: 另外一个特殊对象，它指向Flask Application。
- [`open_resource()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.open_resource): 打开一个文件，相对于flaskr包的路径。
- [`click.command()`](https://click.palletsprojects.com/en/7.x/api/#click.command): 定义一个command line command. 
- [`app.teardown_appcontext()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.teardown_appcontext):  
- [`app.cli.add_command()`](https://click.palletsprojects.com/en/7.x/api/#click.Group.add_command) adds a new command that can be called with the `flask` command.

### Create the Tables

~~~sql
cat << EOF  > flaskr/schema.sql
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

EOF
  
~~~

### Register with the Application

上面的close_db和init_db_command需要被注册到application实例。详见上面db.py中的init_app函数，然后在\_\_init\_\_.py中添加对init_app的调用。

### Initialize the Database File

在instance目录下创建了数据库文件flaskr.sqlite。

~~~
export FLASK_APP=flaskr
flask init-db
~~~

## [Blueprints and Views](https://flask.palletsprojects.com/en/1.1.x/tutorial/views/)

一个蓝图（BluePrint）定义了可用于单个应用的视图，模板，静态文件等等的集合。蓝图使用起来就像应用当中的子应用一样，可以有自己的模板，静态目录，有自己的视图函数和URL规则，蓝图之间互相不影响。但是它们又属于应用中，可以共享应用的配置。

Flaskr有两种blueprint.

- authentication functions
- blog posts

~~~python
cat << EOF > flaskr/auth.py

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))  


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


EOF
~~~

- [`bp.before_app_request()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Blueprint.before_app_request) ： 注册一个函数在blue print被请求之前调用。

- load_logged_in_user ： 检查用户id是否保存在session中，如果yes，则得到用户的数据。g的生命周期是本次request.

- login_required:  由于创建，编辑，删除blog post要求用户必须处于登录状态。decorator 将包参数包装，然后返回一个新的view function. 

  

## [Templates](https://flask.palletsprojects.com/en/1.1.x/tutorial/templates/)

Flask使用Jinja2模板库来render tempaltes。Jinja2 是一个现代的，设计者友好的，仿照 Django 模板的 Python 模板语言。 它速度快，被广泛使用，并且提供了可选的沙箱模板执行环境保证安全:

### The  Base  Layout

~~~jinja2
mkdir -p flaskr/templates
cat << EOF > flaskr/templates/base.html
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>

EOF


~~~

其他页面都是从base'继承而来。

~~~
mkdir -p flaskr/templates/auth
cat << EOF > flaskr/templates/auth/register.html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
{% endblock %}

EOF

cat << EOF > flaskr/templates/auth/login.html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Log In{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Log In">
  </form>
{% endblock %}

EOF


~~~



## [Static Files](https://flask.palletsprojects.com/en/1.1.x/tutorial/static/)

增加css样式等静态文件。

~~~shell
mkdir -p flaskr/static
cat  << EOF > flaskr/static/style.css
html { font-family: sans-serif; background: #eee; padding: 1rem; }
body { max-width: 960px; margin: 0 auto; background: white; }
h1 { font-family: serif; color: #377ba8; margin: 1rem 0; }
a { color: #377ba8; }
hr { border: none; border-top: 1px solid lightgray; }
nav { background: lightgray; display: flex; align-items: center; padding: 0 0.5rem; }
nav h1 { flex: auto; margin: 0; }
nav h1 a { text-decoration: none; padding: 0.25rem 0.5rem; }
nav ul  { display: flex; list-style: none; margin: 0; padding: 0; }
nav ul li a, nav ul li span, header .action { display: block; padding: 0.5rem; }
.content { padding: 0 1rem 1rem; }
.content > header { border-bottom: 1px solid lightgray; display: flex; align-items: flex-end; }
.content > header h1 { flex: auto; margin: 1rem 0 0.25rem 0; }
.flash { margin: 1em 0; padding: 1em; background: #cae6f6; border: 1px solid #377ba8; }
.post > header { display: flex; align-items: flex-end; font-size: 0.85em; }
.post > header > div:first-of-type { flex: auto; }
.post > header h1 { font-size: 1.5em; margin-bottom: 0; }
.post .about { color: slategray; font-style: italic; }
.post .body { white-space: pre-line; }
.content:last-child { margin-bottom: 0; }
.content form { margin: 1em 0; display: flex; flex-direction: column; }
.content label { font-weight: bold; margin-bottom: 0.5em; }
.content input, .content textarea { margin-bottom: 1em; }
.content textarea { min-height: 12em; resize: vertical; }
input.danger { color: #cc2f2e; }
input[type=submit] { align-self: start; min-width: 10em; }

EOF
~~~

## [Blog Blueprint](https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/)

接下来，将使用相同的技术来编写blog blueprint. 

### The Blueprint

~~~python
cat << EOF > flaskr/blog.py
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

EOF

~~~

### Index

~~~python
mkdir -p flaskr/templates/blog
cat << EOF > flaskr/templates/blog/index.html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Posts{% endblock %}</h1>
  {% if g.user %}
    <a class="action" href="{{ url_for('blog.create') }}">New</a>
  {% endif %}
{% endblock %}

{% block content %}
  {% for post in posts %}
    <article class="post">
      <header>
        <div>
          <h1>{{ post['title'] }}</h1>
          <div class="about">by {{ post['username'] }} on {{ post['created'].strftime('%Y-%m-%d') }}</div>
        </div>
        {% if g.user['id'] == post['author_id'] %}
          <a class="action" href="{{ url_for('blog.update', id=post['id']) }}">Edit</a>
        {% endif %}
      </header>
      <p class="body">{{ post['body'] }}</p>
    </article>
    {% if not loop.last %}
      <hr>
    {% endif %}
  {% endfor %}
{% endblock %}

EOF

~~~

### Create

~~~
cat << EOF > flaskr/templates/blog/create.html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}New Post{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title" value="{{ request.form['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
{% endblock %}

EOF
~~~

### Update

~~~python
cat << EOF > flaskr/templates/blog/update.html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Edit "{{ post['title'] }}"{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="title">Title</label>
    <input name="title" id="title"
      value="{{ request.form['title'] or post['title'] }}" required>
    <label for="body">Body</label>
    <textarea name="body" id="body">{{ request.form['body'] or post['body'] }}</textarea>
    <input type="submit" value="Save">
  </form>
  <hr>
  <form action="{{ url_for('blog.delete', id=post['id']) }}" method="post">
    <input class="danger" type="submit" value="Delete" onclick="return confirm('Are you sure?');">
  </form>
{% endblock %}
     
EOF
~~~

### Delete

见blog.py。

## [Make the Project Installable](https://flask.palletsprojects.com/en/1.1.x/tutorial/install/)

### Describe the Project

~~~python
cat << EOF > setup.py
from setuptools import find_packages, setup

setup(
    name='eipi10flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

EOF

cat << EOF > MANIFEST.in 
include flaskr/schema.sql
graft flaskr/static
graft flaskr/templates
global-exclude *.pyc

EOF

~~~

- `include_package_data=True` : 设置包含其他的文件，比如静态目录， 模板目录等。同时需要生成MANIFEST.in文件，指定具体的文件和目录。

### Install the Project

~~~
pip install -e .
pip list | grep flaskr
~~~

pip命令将会在安装*editable* or *development* 模式下安装setup.py。



## [Test Coverage](https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/)

~~~
pip install pytest coverage
~~~

### Setup and Fixtures

数据准备

~~~
mkdir -p tests
cat << EOF > tests/data.sql
INSERT INTO user (username, password)
VALUES
  ('test', 'pbkdf2:sha256:50000\$TCI4GzcX\$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'pbkdf2:sha256:50000\$kJPKsz6N\$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (title, body, author_id, created)
VALUES
  ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
  
EOF
~~~

定义conftest.py

~~~python
cat << EOF > tests/conftest.py
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
    
    
class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)    
    
EOF

~~~

- [`tempfile.mkstemp()`](https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp) ： 创建临时文件，返回文件对象和其路径。
- [`TESTING`](https://flask.palletsprojects.com/en/1.1.x/config/#TESTING) : 告诉Flask应用处于test模式，Flask会改变一些内部的行为，使得更加容易测试。
-  [`app.test_client()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.test_client) ： Tests使用该函数返回的client来发送request.
-  [`app.test_cli_runner()`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.test_cli_runner) : 创建一个runner调用已经注册好的Click命令

### Factory

~~~python
cat << EOF > tests/test_factory.py
from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'
    
EOF

~~~

### Database

~~~python
cat << EOF > tests/test_db.py
import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
    
EOF
~~~

### Authentication

def auth(client):已添加到conftest.py

使用auth fixture, 我们可以调用auth.login()来以一个test用户登陆。

~~~python
cat << EOF > tests/test_auth.py
import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session    
    
EOF

pytest -v tests/test_auth.py
~~~



### Blog

~~~
cat << EOF > tests/test_blog.py
import pytest
from flaskr.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data
    
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data
    
def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

EOF

~~~

### Runnnig the Tests

Some extra configuration, which is not required but makes running tests with coverage less verbose, can be added to the project’s `setup.cfg` file.

~~~
cat << EOF > setup.cfg
[tool:pytest]
testpaths = tests

[coverage:run]
branch = True
source =
    flaskr

EOF

pytest -v 

~~~

代码覆盖测试（code coverage）

~~~
coverage run -m pytest
coverage report
~~~



## [Deploy to Production](https://flask.palletsprojects.com/en/1.1.x/tutorial/deploy/)

确保安装了wheel

~~~
pip install wheel
~~~

**打包**

~~~
rm -rf dist
python setup.py bdist_wheel
~~~

**安装**

在另外一个机器上安装

~~~
#安装方法一： 把flaskr-1.0.0-py3-none-any.whl 拷贝到另外一台机器。然后执行下面命令
##  pip install dist/flaskr-1.0.0-py3-none-any.whl 

#安装方法二：
# 上传
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# 安装
pip install -U -i https://test.pypi.org/simple/ eipi10flaskr
pip list | grep flaskr

# 初始化数据库
export FLASK_APP=flaskr
flask init-db

# flaskr.sqlite将会创建在下面的目录
ll venv/var/flaskr-instance
~~~

### 定义secret key

~~~
python -c 'import os; print(os.urandom(16))'
~~~

获取上面得到的随机密钥

~~~
cat << EOF > venv/var/flaskr-instance/config.py
SECRET_KEY = b'P.\r;7\xb28\x0c\xc8\x1f\rL\x8b4B\xae'
EOF

~~~

### 运行

production 必须使用WSGI server，这样更加高效，稳定和安全。 比如使用： [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)

~~~
pip install waitress
~~~

运行

~~~
waitress-serve --port=5003 --call 'flaskr:create_app' 
~~~



## [Keep Developing!](https://flask.palletsprojects.com/en/1.1.x/tutorial/next/)

本教程完整见 [example project](https://github.com/pallets/flask/tree/master/examples/tutorial)