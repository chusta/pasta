#!/bin/bash
# database setup script

DATABASE=(pasta pasta-test)

[ $(id -u) -ne 0 ] && echo "! run as root." && exit

echo -n "Username: "
read owner

[ -z "$owner" ] && echo "! missing username." && exit

echo "creating database owner ..."
sudo -u postgres createuser "$owner" --interactive -P 2>/dev/null
[ $? -ne 0 ] && echo "+ user created: $owner" || echo "- $owner already exists."

service postgresql restart

echo "creating database ..."
for db in ${DATABASE[@]}; do
    sudo -u postgres dropdb "$db" 2>/dev/null
    sudo -u postgres createdb "$db" -O "$owner" && echo "+ db created: $db"
done
