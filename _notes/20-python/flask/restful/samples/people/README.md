# Python REST APIs With Flask, Connexion, and SQLAlchemy

## The People REST API

下面例子将会实现对于people的CRUD。

| Action | HTTP Verb | URL Path              | Description                                                  |
| ------ | --------- | --------------------- | ------------------------------------------------------------ |
| Create | `POST`    | `/api/people`         | Defines a unique URL to create a new person                  |
| Read   | `GET`     | `/api/people`         | Defines a unique URL to read a collection of people          |
| Read   | `GET`     | `/api/people/Farrell` | Defines a unique URL to read a particular person in the people collection |
| Update | `PUT`     | `/api/people/Farrell` | Defines a unique URL to update an existing order             |
| Delete | `DELETE`  | `/api/orders/Farrell` | Defines a unique URL to delete an existing person            |

## Getting Started

```
cat << EOF > server.py
from flask import (
    Flask,
    render_template
)

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)

EOF

cat << EOF > home.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Application Home Page</title>
</head>
<body>
    <h2>
        Hello World!
    </h2>
</body>
</html>

EOF
```

运行

```
python server.py
```

