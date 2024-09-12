#!/bin/bash

if curl -sk http://nginx1 > /dev/null; then
  # Nginx is running and responding
  echo "Nginx is running"
  exit 0
else
  # Nginx is not responding
  echo "Nginx is not responding"
  exit 1
fi
