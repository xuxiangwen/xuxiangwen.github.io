[Tutorial: Create a web API with ASP.NET Core | Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api?view=aspnetcore-8.0&tabs=visual-studio-code)

## Overview

| API                          | Description             | Request body | Response body        |
| :--------------------------- | :---------------------- | :----------- | :------------------- |
| `GET /api/todoitems`         | Get all to-do items     | None         | Array of to-do items |
| `GET /api/todoitems/{id}`    | Get an item by ID       | None         | To-do item           |
| `POST /api/todoitems`        | Add a new item          | To-do item   | To-do item           |
| `PUT /api/todoitems/{id}`    | Update an existing item | To-do item   | None                 |
| `DELETE /api/todoitems/{id}` | Delete an item          | None         | None                 |

![The client is represented by a box on the left. It submits a request and receives a response from the application, a box drawn on the right. Within the application box, three boxes represent the controller, the model, and the data access layer. The request comes into the application's controller, and read/write operations occur between the controller and the data access layer. The model is serialized and returned to the client in the response.](images/architecture.pngview=aspnetcore-8.png)

## Create a web project

~~~powershell
dotnet new webapi --use-controllers -o TodoApi
cd TodoApi
dotnet add package Microsoft.EntityFrameworkCore.InMemory
code -r ../TodoApi
~~~

### Test the project

~~~
dotnet dev-certs https --trust
~~~

~~~
dotnet run --launch-profile https
~~~

