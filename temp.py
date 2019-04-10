import shlex

s = 'echo sdfsdfsf&&echo sdfs"DSf&&sd"||echo "fddfg&&dgdfg"'
s = shlex.shlex(s)
s.whitespace = '&& ||'
print(s.whitespace)


print(list(s))