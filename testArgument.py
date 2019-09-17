import sys

print('Number of arguments: {}'.format(len(sys.argv)))
print('Argument(s) passed: {}'.format(str(sys.argv)))

print("Listed individually")
for theArg in sys.argv:
    print theArg