# KetcherSVC

Backend Service to render molfiles to SVG using Ketcher implemented in Python.

## Usage

Simply send a HTTP POST request to the service with the molfile as body.

Request:

```
POST http://service/render
<molfile as body>
```

Reply:

```
<svg data>
```

# Note

`service.spec` is a spec file for pyinstaller. Use like this:

```
pyinstaller service.spec ; docker build . -t ketchersvc:py
```
