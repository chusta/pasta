#!/bin/bash
# database setup script

DATABASE="pasta"

[ $(id -u) -ne 0 ] && echo "! run as root." && exit

echo -n "Username: "
read owner

[ -z "$owner" ] && echo "! missing username." && exit

echo "creating database owner ..."
sudo -u postgres createuser "$owner" --interactive -P 2>/dev/null
[ $? -ne 0 ] && echo "+ user created: $owner" || echo "- $owner already exists."

#echo "dropping database ..."
#sudo -u postgres dropdb "$DATABASE" 2>/dev/null

echo "creating database ..."
sudo -u postgres createdb "$DATABASE" -O "$owner" && echo "+ db created: $i";
