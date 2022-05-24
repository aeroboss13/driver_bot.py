#!/bin/sh
ret=$(ps aux | grep -v grep | grep bot.py | wc -l)
if [ "$ret" -eq 0 ]
then {
  echo "Running my bot" #output
  sleep 1  #delay
  cd /root/bot
  python3 bot.py
  exit 1
}
else 
{
  echo "EXIT. This bot is already running!"
  exit 1
}
fi;
