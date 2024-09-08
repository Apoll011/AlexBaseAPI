#!/bin/bash

# Define constants
PID_FILE="/home/pegasus/.alex_server"
ALEX_PID_FILE="/home/pegasus/.alex"
SCRIPT_DIR="/home/pegasus/development/AlexBaseAPI/"
LOG_FILE="output.log"

# Function to display usage information
usage() {
    echo "Usage: alex-server [command] [options]"
    echo
    echo "Commands:"
    echo "  start              Start the Alex server if it's not running."
    echo "  stop               Stop the Alex server if it's running."
    echo "  reload             Reload the Alex server (stop and then start)."
    echo "  show               Will show the Alex Server if Its Active."
    echo "  --help, -h         Display this help message."
    echo
    echo "Options for start and reload:"
    echo "  [args]             Arguments to pass to the server's main.py script."
    echo
    echo "The Alex server listens on port 1178 of 0.0.0.0."
    echo "Logs are saved to $LOG_FILE."
    exit 0
}

# Function to kill the server
killit() {
    if [ ! -f "$PID_FILE" ]; then
        echo "The server is not running."
        exit 1
    fi

    PID=$(cat "$PID_FILE")
    if ! [[ "$PID" =~ ^[0-9]+$ ]]; then
        echo "PID is not valid: $PID"
        exit 1
    fi

    kill "$PID"

    if [ $? -eq 0 ]; then
        echo "Alex Server ($PID) terminated successfully."
        rm "$PID_FILE"
    else
        echo "Failed to terminate Alex Server ($PID)."
    fi
}

# Function to start the server
startit() {
    if [ -f "$PID_FILE" ]; then
        echo "The server is already running"
    else
        shift
        echo "Starting server"
        cd "$SCRIPT_DIR"
        source .venv/bin/activate
        nohup python main.py "$@" > "$LOG_FILE" 2>&1 &
        sleep 4
        echo "Alex Server started with PID $(cat $PID_FILE)."
    fi
}

show() {
    if [ ! -f "$PID_FILE" ]; then
        echo "The server is not running."
        exit 1
    fi

    if [ -f "$ALEX_PID_FILE" ]; then
        echo "Alex"
        top -p $(cat "$PID_FILE"),$(cat "$ALEX_PID_FILE") -d 0.2 -E g -e m -H
    else
        top -p $(cat "$PID_FILE") -d 0.1 -E g -e m -H
    fi
}

clear() {
    rm "$PID_FILE"
    rm "$ALEX_PID_FILE"
}

# Main script logic
case "$1" in
    reload)
        echo "Reloading the server."
        killit
        startit
        ;;
    stop)
        killit
        ;;
    show)
        show
        ;;
    clear)
        clear
        ;;
    --help|-h)
        usage
        ;;
    start)
        startit
        ;;
    *)
        echo "$1" is not a valid command. See -h/--help for help
        ;;
esac
