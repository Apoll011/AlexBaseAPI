#!/bin/bash

# Define constants
export HOME_LOCATION="/home/$USER"
export PID_FILE="$HOME_LOCATION/.alex"
export LOCATION="/bin/alex"

install() {
  echo "Installing Alex..."
  mkdir /tmp/alex
  echo "Downloading Alex..."
  wget "http://$1:1178/version_control/main/get" -O /tmp/alex/alex.zip -t 5 -q
  echo "Downloaded Alex..."
  echo "Building Alex..."
  unzip -qq /tmp/alex/alex.zip -d /tmp/alex/
  echo "Linking..."
  cp /tmp/alex/main $HOME_LOCATION/alex
  sudo ln -s $HOME_LOCATION/alex /bin/alex -f
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
        install $2
        ;;
    uninstall)
        uninstall
        ;;
    *)
        echo "$1" is not a valid command.
        ;;
esac

