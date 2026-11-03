#!/bin/bash

echo "Stopping Flask applications on ports 8001 and 8002..."

# Kill processes on ports 8001 and 8002
fuser -k 8001/tcp 2>/dev/null
fuser -k 8002/tcp 2>/dev/null

echo "Applications stopped."