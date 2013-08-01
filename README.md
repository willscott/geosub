Geo Sub
=======

Initial work on subscription service for streaming geographic data.

Prerequisites
------

[Shapely](https://pypi.python.org/pypi/Shapely) is installed through ```setup.sh```,
but it does not automatically install its C dependency, [Geos](http://trac.osgeo.org/geos/).  Install that
library as is appropriate for your platform.

Installation
------

    git submodule init
    git submodule update
	bash setup.sh

Running
------

### Backend

    cd hub
    python daemon.py

### Frontend

* Currently needs a google project id saved as client_secrets.json.
* Make a project at https://code.google.com/apis/console
* In API Access create a client id for Web apps
* Set javascript origin to 'http://localhost:8080'
* In Services, enable 'Google+ API'
* Save a file 'client_secrets.json' that looks like:

```javascript
    { "web":
      { "client_id": "<yourid>.apps.googleusercontent.com",
        "client_secret": "<yoursecret>",
        "redirect_uris": [ "/user/redirect"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token"
      }
    }
```

* Setup additional libraries

```
    bash setup.sh
```

* Run the server

```
    python server.py
```
