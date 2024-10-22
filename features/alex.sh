#!/bin/bash

# Define constants
HOME_LOCATION = "/home/$USER"
PID_FILE="$HOME_LOCATION/.alex"
LOCATION="/bin/alex"

install() {
  echo "Installing Alex..."
  mkdir /tmp/alex
  echo "Downloading Alex..."
  wget "http://$2:1178/version_control/main/get" -O /tmp/alex/alex.zip -t 5 -q
  echo "Downloaded Alex..."
  echo "Building Alex..."
  unzip -qq /tmp/alex/alex.zip -d /tmp/alex/
  echo "Linking..."
  cp /tmp/alex/main $HOME_LOCATION/alex
  sudo ln -s $HOME_LOCATION/alex /bin/alex
  rm -r /tmp/alex
  echo "Alex Installed..."
}

uninstall(){
  sudo rm -f /bin/alex
  rm -f $HOME_LOCATION/alex
  rm -r -f $HOME_LOCATION/.alex_resources/
}

case "$1" in
    install)
        install
        ;;
    uninstall)
        uninstall
        ;;
    *)
        echo "$1" is not a valid command.
        ;;
esac

