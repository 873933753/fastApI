""" 
基础数据类型：
Number：int, float
string：str
bool：bool - True, False
空类型：None
集合类型：set
元组类型：tuple
字典类型：dict
"""

# 1、数字类型：int, float
""" 
* 乘法
/ 浮点数除法，结果是float
// 整除，结果是int  
% 取模运算，结果是int
** 幂运算，结果是int
"""
print(type(1)) # <class 'int'>
print(type(1.1)) # <class 'float'>
print(type(1+1.1)) # <class 'float'>
print(type(1*1.0)) # <class 'float'>
print(type(1/1.0)) # <class 'float'>
print(type(1/1)) # <class 'float'> - 这里两个int相除，结果是float
print(type(1//1)) # <class 'int'> - 这里两个int相除，结果是int
print(1//2) # 0 - 整数除法，结果是整数
print(1%3) # 1 - 取模运算

# 进制表示
""" 
0bxx 二进制
0oxx 八进制
0xxx 十六进制

进制转换：
bin(int) 十进制转二进制
oct(int) 十进制转八进制
hex(int) 十进制转十六进制
""" 
print(0b11) # 3
print(0o11) # 9
print(0x11) # 17

# 十进制转二进制、八进制、十六进制
print(bin(10)) # 0b1010
print(oct(10)) # 0o12
print(hex(10)) # 0xa

# 2、布尔类型：bool
print('---bool---')
print(type(True)) # <class 'bool'>
print(type(False)) # <class 'bool'>
print(bool('2')) # True
print(bool('0')) # True
# 空字符串、空列表、空字典、空元组、空集合、空None都是False
print(bool('')) # False
print(bool(0)) # False
print(bool([])) # False
print(bool({})) # False
print(bool(None)) # False

# 3、文本类型：str
""" 
+ 字符串拼接
* 字符串重复
[] 字符串索引
[:] 字符串切片
len(str) 字符串长度
str.upper() 字符串大写
str.lower() 字符串小写
"""
print('---str---')
print(type('1')) # <class 'str'>
print('a'+'b') # ab
print('a'*3) # aaa
print('abc'[1]) # b
print('abcdefg'[1:-1]) # bcd - 从1到-1，不包括-1
print(len('abc')) # 3
print('abc'.upper()) # ABC
print('AbC'.lower()) # abc
# 转义字符和原始字符串
print(r'a\nb') # a\nb - 这里\n不会被转义为换行符 
print('a\nb') # a 换行 b - 这里\n会被转义为换行符

