# (copy)pasta

upload and comment on images

## getting started

0. Run the installer from the project base path, as root. Python
dependencies are installed in a virtualenv (venv).
```
# ./scripts/install.sh
```

1. A setup script is used to build out some of the postgresql databases
(which are just for dev/test), as well as create a user for management.
```
# ./scripts/setup.sh
```

2. You will be prompted for a username and password, which will then be stored
into the `db_login` json-file. Rename `db_json.dist` to `db_json` and fill
out the correct information.

WARNING: Mind the permissions of the `db_login` file (chmod 0600).

3. Once that is set, running the webapp requires the creation of a secret key.
```
export SECRET_KEY="_LONG_SECURE_RANDOM_STRING_GOES_HERE_"

-or-

export SECRET_KEY="$(python -c 'import os,binascii;print binascii.hexlify(os.urandom(32))')"
```

## running
pasta will be listening on http://0.0.0.0:8080
```
./pasta.py start
```

## login
pasta requires the user to login before use
