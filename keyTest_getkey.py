from getkey import getkey, keys

# Use this one, it works, the other ones didn't work like this... if
# want to use others then do more research on them.

buffer = ''
while True:
    key = getkey()
    if key == keys.UP:
        print "keys.UP"  # Handle the UP key
    elif key == keys.DOWN:
        print "keys.DOWN"  # Handle the DOWN key
    elif key == 'a':
        print "letter a"  # Handle the `a` key
    elif key == 'q':
        print "letter q"  # Handle `shift-y`
        break
    else:
        # Handle other text characters
        buffer += key
        print(buffer)
