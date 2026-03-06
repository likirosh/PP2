1.
import re
print(re.findall(r'ab*', 'ac abbc abbbc'))

2.
import re
print(re.findall(r'ab{2,3}', 'ab abbc abbbc abbbbc'))

3.
import re
print(re.findall(r'[a-z]+_[a-z]+', 'hello_world foo_bar ABC')) 

4.
import re
print(re.findall(r'[A-Z][a-z]+', 'Hello World foo Bar')) 

5.
import re
print(re.findall(r'a.*b', 'aXYZb acb ab a_b'))

6.
import re
print(re.sub(r'[ ,.]', ':', 'one two,three.four')) 

7.
import re
s = 'hello_world_foo'
print(re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)) 

8.
import re
print(re.split(r'(?=[A-Z])', 'HelloWorldFoo'))

9.
import re
print(re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', 'HelloWorldFoo'))

10.import re
s = 'helloWorldFoo'
print(re.sub(r'(?<=[a-z])([A-Z])', lambda m: '_' + m.group(1).lower(), s))