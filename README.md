user_management 
===============


## Setting up development environment

The development environment can be setup either like a pythonista
with the usual python module setup, or like a docker user.

### The pythonista way

Ensure that you have an updated version of pip

```
pip --version
```
Should atleast be 1.5.4

If pip version is less than 1.5.4 upgrade it
```
pip install -U pip
```

This will install latest pip

Ensure that you are in virtualenv
if not install virtual env
```
sudo pip install virtualenv
```
This will make install all dependencies to the virtualenv
not on your root

From the module folder install the dependencies. This also installs
the module itself in a very pythonic way.

```
pip install -r requirements.txt
```
##NOTE
Postgresql must be installed.
if not install postgres and its server-side extensions

Run app by 
```
python app.py
```
### 
