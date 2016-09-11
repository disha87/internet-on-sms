ps auxww | egrep -i 'SimpleHTTPServer|python reply.py' | awk '{print $2}' |\
xargs kill -9
