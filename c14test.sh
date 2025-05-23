#!/bin/bash

# make sure the server in c14-accesscontrol is running

# Check if method is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <-register | -login>"
  exit 1
fi

# Test registration
if [ "$1" == "-register" ]; then
  curl -X POST http://localhost:5000/register \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"123","role":"admin"}'
fi

# Test login
if [ "$1" == "-login" ]; then
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","password":"123"}'
fi
