本文摘自[Flask  RESTful User’s Guide](https://flask-restful.readthedocs.io/en/latest/index.html)

[TOC]

# 1.  Installation

~~~shell
pip install flask-restful
~~~

# 2. Quickstart

## A Minimal API

### Resourceful Routing

~~~
cat << EOF > api.py
from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        # Default to 200 OK
        return {'hello': 'world'}
        
todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')        
api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

EOF

~~~

启动

~~~
python api.py
~~~

测试

~~~
curl http://127.0.0.1:5004/
curl http://localhost:5004/todo1 -d "data=Remember the milk" -X PUT
curl http://localhost:5004/todo1
curl http://localhost:5004/todo2 -d "data=Change my brakepads" -X PUT
curl http://localhost:5004/todo2
~~~

在python端的测试

~~~
pip install requests
~~~

~~~
cat << EOF > test_api.py
from requests import put, get
print(put('http://localhost:5004/todo1', data={'data': 'Remember the milk'}).json())
print(get('http://localhost:5004/todo1').json())
print(put('http://localhost:5004/todo2', data={'data': 'Change my brakepads'}).json())
print(get('http://localhost:5004/todo2').json())
EOF

python test_api.py
~~~

Flask-RESTful 支持设置

- response code
- response header

~~~python
class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self):
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}
~~~

## Full Example

~~~python
cat << EOF > api.py
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)

EOF
~~~

重启

~~~
python api.py
~~~

测试

~~~
curl http://localhost:5004/todos
curl http://localhost:5004/todos/todo3
curl http://localhost:5004/todos/todo2 -X DELETE -v
curl http://localhost:5004/todos -d "task=something new" -X POST -v
curl http://localhost:5004/todos/todo3 -d "task=something different" -X PUT -v

~~~

# 3. [Request Parsing](https://flask-restful.readthedocs.io/en/latest/reqparse.html#request-parsing)

当前的 request parser部分准备被移除，这意味着当前的版本只会被维护。

## Basic Arguments

~~~
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=int, help='Rate cannot be converted')
parser.add_argument('name')
parser.add_argument('name', required=True, help="Name cannot be blank!")   # Required Arguments
args = parser.parse_args()
~~~

- help： 类型解析错误信息。当解析过程中如果发生类型错误，显示help的内容。
- require=True: 必要参数

## Multiple Values & Lists

action='append'： 多个值。

~~~
parser.add_argument('name', action='append')
~~~

测试

~~~
curl http://api.example.com -d "name=bob" -d "name=sue" -d "name=joe"
~~~

参数将是：

~~~
args = parser.parse_args()
args['name']    # ['bob', 'sue', 'joe']
~~~

## Argument Locations

默认情况下，[`RequestParser`](https://flask-restful.readthedocs.io/en/latest/api.html#reqparse.RequestParser)从[`flask.Request.values`](http://flask.pocoo.org/docs/api/#flask.Request.values), and [`flask.Request.json`](http://flask.pocoo.org/docs/api/#flask.Request.json)中来解析value。

~~~python
# Look only in the POST body
parser.add_argument('name', type=int, location='form')

# Look only in the querystring
parser.add_argument('PageSize', type=int, location='args')

# From the request headers
parser.add_argument('User-Agent', location='headers')

# From http cookies
parser.add_argument('session_id', location='cookies')

# From file uploads
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')

parser.add_argument('text', location=['headers', 'values'])
~~~

- Only use `type=list` when `location='json'`. [See this issue for more details](https://github.com/flask-restful/flask-restful/issues/380)  这个目前还不能理解。
- 如果指定多个location, 这些location获取的值将会合并到单个的 [`MultiDict`](http://werkzeug.pocoo.org/docs/datastructures/#werkzeug.datastructures.MultiDict)中，其中location中最后一个值，会有优先权。

## Parser Inheritance

重用参数解析

~~~python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('foo', type=int)

parser_copy = parser.copy()
parser_copy.add_argument('bar', type=int)

# parser_copy has both 'foo' and 'bar'

parser_copy.replace_argument('foo', required=True, location='json')
# 'foo' is now a required str located in json, not an int as defined
#  by original parser

parser_copy.remove_argument('foo')
# parser_copy no longer has 'foo' argument
~~~

## Error Handling

默认情况下， RequestParser碰到去第一个错误就会退出。如果我们需要把参数中所有的错误一次返回给客户端，可以定义bundle_errors

~~~
from flask_restful import reqparse

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('foo', type=int, required=True)
parser.add_argument('bar', type=int, required=True)

# If a request comes in not containing both 'foo' and 'bar', the error that
# will come back will look something like this.

{
    "message":  {
        "foo": "foo error message",
        "bar": "bar error message"
    }
}

# The default behavior would only return the first error

parser = RequestParser()
parser.add_argument('foo', type=int, required=True)
parser.add_argument('bar', type=int, required=True)

{
    "message":  {
        "foo": "foo error message"
    }
}
~~~

也可以在Flask applicaton级别来定义BUNDLE_ERRORS，这是一个全局变量，将会覆盖[`RequestParser`](https://flask-restful.readthedocs.io/en/latest/api.html#reqparse.RequestParser) instances中的定义。

~~~
from flask import Flask

app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True
~~~

## Error Messages

`help` 中可以包含一个interpolation token, `{error_msg}`,

~~~
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument(
    'foo',
    choices=('one', 'two'),
    help='Bad choice: {error_msg}'
)

# If a request comes in with a value of "three" for `foo`:

{
    "message":  {
        "foo": "Bad choice: three is not a valid choice",
    }
}
~~~

# 4. Output Fields

Flask-RESTful提供一种容易的方式来控制哪些数据被render到response. 使用 [`fields`](https://flask-restful.readthedocs.io/en/latest/api.html#module-fields)  moduel，可以使用任何的对象（ORM models/custom classes等等）

## Basic Usage

~~~
from flask_restful import Resource, fields, marshal_with

# 定义一个dict或者OrderedDict
resource_fields = {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
}

class Todo(Resource):
    @marshal_with(resource_fields, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()  # Some function that queries the db
~~~

- db_get_todo： 返回一个自定义的对象，这个对象包含attributes `name`, `address`, and `date_updated`，其他的字段在output中将会被忽略。
- ecorator [`marshal_with`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.marshal_with) ：从对象中获取所需要的字段，进行marchalling。

## Renaming Attributes

~~~
fields = {
    'name': fields.String(attribute='private_name'),
    'address': fields.String,
}

fields = {
    'name': fields.String(attribute=lambda x: x._private_name),
    'address': fields.String,
}

# Nested properties can also be accessed with attribute 如何理解呢
fields = {
    'name': fields.String(attribute='people_list.0.person_dictionary.name'),
    'address': fields.String,
}
~~~

## Default Values

~~~
fields = {
    'name': fields.String(default='Anonymous User'),
    'address': fields.String,
}
~~~

## Custom Fields & Multiple Values

```
class UrgentItem(fields.Raw):
    def format(self, value):
        return "Urgent" if value & 0x01 else "Normal"

class UnreadItem(fields.Raw):
    def format(self, value):
        return "Unread" if value & 0x02 else "Read"

fields = {
    'name': fields.String,
    'priority': UrgentItem(attribute='flags'),
    'status': UnreadItem(attribute='flags'),
}
```

## Url & Other Concrete Fields

~~~
class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()

fields = {
    'name': fields.String,
    # todo_resource is the endpoint name when you called api.add_resource()
    'uri': fields.Url('todo_resource'),
    'random': RandomNumber,
}

fields = {
    'uri': fields.Url('todo_resource', absolute=True)
    'https_uri': fields.Url('todo_resource', absolute=True, scheme='https')
}
~~~

- 默认情况下fields.Url返回的是相对uri。

## Complex Structures

 [`marshal()`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.marshal) 可以把一个平面的结构转化成一个嵌套的结构。

~~~
from flask_restful import fields, marshal
import json

resource_fields = {'name': fields.String}
resource_fields['address'] = {}
resource_fields['address']['line 1'] = fields.String(attribute='addr1')
resource_fields['address']['line 2'] = fields.String(attribute='addr2')
resource_fields['address']['city'] = fields.String
resource_fields['address']['state'] = fields.String
resource_fields['address']['zip'] = fields.String
data = {'name': 'bob', 'addr1': '123 fake street', 'addr2': '', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
json.dumps(marshal(data, resource_fields))
~~~

返回

~~~
'{"name": "bob", "address": {"line 1": "123 fake street", "line 2": "", "state": "NY", "zip": "10468", "city": "New York"}}'
~~~

## List Field

~~~
from flask_restful import fields, marshal
import json

resource_fields = {'name': fields.String, 'first_names': fields.List(fields.String)}
data = {'name': 'Bougnazal', 'first_names' : ['Emile', 'Raoul']}
json.dumps(marshal(data, resource_fields))
~~~

返回

~~~
'{"name": "Bougnazal", "first_names": ["Emile", "Raoul"]}'
~~~

## Advanced : Nested Field

~~~
from flask_restful import fields, marshal, marshal_with
import json

address_fields = {}
address_fields['line 1'] = fields.String(attribute='addr1')
address_fields['line 2'] = fields.String(attribute='addr2')
address_fields['city'] = fields.String(attribute='city')
address_fields['state'] = fields.String(attribute='state')
address_fields['zip'] = fields.String(attribute='zip')

resource_fields = {}
resource_fields['name'] = fields.String
resource_fields['billing_address'] = fields.Nested(address_fields)
resource_fields['shipping_address'] = fields.Nested(address_fields)
address1 = {'addr1': '123 fake street', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
address2 = {'addr1': '555 nowhere', 'city': 'New York', 'state': 'NY', 'zip': '10468'}
data = { 'name': 'bob', 'billing_address': address1, 'shipping_address': address2}

json.dumps(marshal(data, resource_fields))
~~~

返回

~~~
'{"name": "bob", "billing_address": {"line 1": "123 fake street", "line 2": null, "city": "New York", "state": "NY", "zip": "10468"}, "shipping_address": {"line 1": "555 nowhere", "line 2": null, "city": "New York", "state": "NY", "zip": "10468"}}'
~~~

可以嵌套使用[`Nested`](https://flask-restful.readthedocs.io/en/latest/api.html#fields.Nested) with [`List`](https://flask-restful.readthedocs.io/en/latest/api.html#fields.List) 

~~~
user_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

user_list_fields = {
    fields.List(fields.Nested(user_fields)),
}
~~~

# 5. [Extending Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/extending.html)

当我们发现内置的函数功能不能满足需要，可以对 Flask-RESTful进行一些扩展。

## Content Negotiation(谈判)

如果我们希望 Flask-RESTful仅仅支持support JSON.

~~~
app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
~~~

定义默认的Flask-RESTful JSON representation

~~~
class MyConfig(object):
    RESTFUL_JSON = {'separators': (', ', ': '),
                    'indent': 2,
                    'cls': MyCustomEncoder}
~~~



## Custom Fields & Inputs

### Fields

~~~
class AllCapsString(fields.Raw):
    def format(self, value):
        return value.upper()


# example usage
fields = {
    'name': fields.String,
    'all_caps_name': AllCapsString(attribute=name),
}
~~~

### Inputs

自定义参数验证

```
def odd_number(value):
    if value % 2 == 0:
        raise ValueError("Value is not odd")

    return value

# 如果你想访问参数名，可以增加一个参数
def odd_number(value, name):
    if value % 2 == 0:
        raise ValueError("The parameter '{}' is not odd. You gave us the value: {}".format(name, value))

    return value
    
# maps the strings to their internal integer representation
# 'init' => 0
# 'in-progress' => 1
# 'completed' => 2

def task_status(value):
    statuses = [u"init", u"in-progress", u"completed"]
    return statuses.index(value)
    
parser = reqparse.RequestParser()
parser.add_argument('OddNumber', type=odd_number)
parser.add_argument('Status', type=task_status)
args = parser.parse_args()
```

## Response Formats

为了支持其他representations (xml, csv, html)，使用[`representation()`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Api.representation) decorator。

~~~
api = Api(app)

@api.representation('text/csv')
def output_csv(data, code, headers=None):
    pass
    # implement csv output!
~~~

These output functions有三个参数：`data`, `code`, and `headers`

- data ： the object you return from your resource method
- code：the HTTP status code that it expects
- headers ： any HTTP headers to set in the response

而output function必须返回一个[`flask.Response`](http://flask.pocoo.org/docs/api/#flask.Response) object. 示例如下：

~~~
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    return resp
~~~

另外一种实现的方法是，继承[`Api`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Api) class 。

~~~python
class Api(restful.Api):
    def __init__(self, *args, **kwargs):
        super(Api, self).__init__(*args, **kwargs)
        self.representations = {
            'application/xml': output_xml,
            'text/html': output_html,
            'text/csv': output_csv,
            'application/json': output_json,
        }
~~~

## Resource Method Decorators

 [`Resource`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Resource) class中有一个属性method_decorators。我们可以增加自己的decorator导这个属性中。比如，下面添加自定义的认证。

~~~
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = basic_authentication()  # custom account lookup function

        if acct:
            return func(*args, **kwargs)

        flask_restful.abort(401)
    return wrapper


class Resource(flask_restful.Resource):
    method_decorators = [authenticate]   # applies to all inherited resources
~~~

而且，可以定义一个dictionary来把HTTP methods和decorator关联起来。

~~~
def cache(f):
    @wraps(f)
    def cacher(*args, **kwargs):
        # caching stuff
    return cacher

class MyResource(restful.Resource):
    method_decorators = {'get': [cache]}

     def get(self, *args, **kwargs):
        return something_interesting(*args, **kwargs)

     def post(self, *args, **kwargs):
        return create_something(*args, **kwargs)
~~~

## Custom Error Handlers

Flask-RESTful调用 [`handle_error()`](https://flask-restful.readthedocs.io/en/latest/api.html#flask_restful.Api.handle_error)函数来处理400或500错误。当发生404 Not Found错误时，返回一个错误消息，可以使用 catch_all_404s参数。

~~~
app = Flask(__name__)
api = flask_restful.Api(app, catch_all_404s=True)
~~~

有时，如果需要对于错误做一些特别处理，比如：log到文件，发送邮件等等，可以使用**got_request_exception()**方法

```
def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)

from flask import got_request_exception
got_request_exception.connect(log_exception, app)
```

### Define Custom Error Messages

~~~
errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

app = Flask(__name__)
api = flask_restful.Api(app, errors=errors)
~~~

默认的status是500

# 6. Intermediate Usage

下面将建立一个与哦一点复杂的 Flask-RESTful app，其中包含了建立Flask-RESTful-based API的一些最佳实践。

## Project Structure

基本的思路是把app分成：

- route
- resource
- common infrastructure

目录结构如下：

```
myapi/
    __init__.py
    app.py          # this file contains your app and routes
    resources/
        __init__.py
        foo.py      # contains logic for /Foo
        bar.py      # contains logic for /Bar
    common/
        __init__.py
        util.py     # just some common infrastructure
```

~~~
cat << EOF > app.py
from flask import Flask
from flask_restful import Api
from myapi.resources.foo import Foo
from myapi.resources.bar import Bar
from myapi.resources.baz import Baz

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(app)

api.add_resource(Foo, '/Foo', '/Foo/<str:id>')
api.add_resource(Bar, '/Bar', '/Bar/<str:id>')
api.add_resource(Baz, '/Baz', '/Baz/<str:id>')

class TodoItem(Resource):
    def get(self, id):
        return {'task': 'Say "Hello, World!"'}

api.add_resource(TodoItem, '/todos/<int:id>')
app.register_blueprint(api_bp)

EOF

cat << EOF > foo.py
from flask_restful import Resource

class Foo(Resource):
    def get(self):
        pass
    def post(self):
        pass
        
EOF

~~~

## Full Parameter Parsing Example

~~~python
from flask_restful import fields, marshal_with, reqparse, Resource

def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if valid_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))

post_parser = reqparse.RequestParser()
post_parser.add_argument(
    'username', dest='username',
    location='form', required=True,
    help='The user\'s username',
)
post_parser.add_argument(
    'email', dest='email',
    type=email, location='form',
    required=True, help='The user\'s email',
)
post_parser.add_argument(
    'user_priority', dest='user_priority',
    type=int, location='form',
    default=1, choices=range(5), help='The user\'s priority',
)

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'user_priority': fields.Integer,
    'custom_greeting': fields.FormattedString('Hey there {username}!'),
    'date_created': fields.DateTime,
    'date_updated': fields.DateTime,
    'links': fields.Nested({
        'friends': fields.Url('user_friends'),
        'posts': fields.Url('user_posts'),
    }),
}

class User(Resource):

    @marshal_with(user_fields)
    def post(self):
        args = post_parser.parse_args()
        user = create_user(args.username, args.email, args.user_priority)
        return user

    @marshal_with(user_fields)
    def get(self, id):
        args = post_parser.parse_args()
        user = fetch_user(id)
        return user
~~~

## Passing Constructor Parameters Into Resources

把Constructor Parameter参数传给Resource

~~~
from flask_restful import Resource

class TodoNext(Resource):
    def __init__(self, **kwargs):
        # smart_engine is a black box dependency
        self.smart_engine = kwargs['smart_engine']

    def get(self):
        return self.smart_engine.next_todo()
~~~

~~~
smart_engine = SmartEngine()

api.add_resource(TodoNext, '/next',
    resource_class_kwargs={ 'smart_engine': smart_engine })
~~~

