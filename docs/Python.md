# Python 基础 常用高级特性 模块

---


## 基础

### and or not
- not运算是非运算 相当于js !
```buildoutcfg
>>> not True
False
```

###  str
- str是不变对象，而list是可变对象

```
>>> a = ['c', 'b', 'a']
>>> a.sort()
>>> a
['a', 'b', 'c']

>>> a = 'abc'
>>> a.replace('a', 'A')
'Abc'
>>> a
'abc'
```

### list
 - 查找和插入的时间随着元素的增加而增加；
 - 占用空间小，浪费内存很少。
 - len(list) 长度
 - list.append('XX')追加元素到末尾
 - list.insert(1,'XX)插入到指定的位置
 - list.pop(i)删除list末尾的元素,i可选 指定位置
 
 ### tuple
 - 另一种有序列表叫元组：tuple
 - tuple和list非常类似，但是tuple一旦初始化就不能修改
 - 当你定义一个tuple时，在定义的时候，tuple的元素就必须被确定下来，比如：
 ```
>>> t = (1, 2)
>>> t
(1, 2)
```

### dict
- dict全称dictionary，在其他语言中也称为map，使用键-值（key-value）存储，具有极快的查找速度。
- 查找和插入的速度极快，不会随着key的增加而变慢；
- 需要占用大量的内存，内存浪费多。
```
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```
- 判断不存在、取值、删除
```
>>> 'Thomas' in d
False
>>> d.get('Thomas')
None
>>> d.get('Thomas', -1)
-1
>>> d.pop('Bob')
75
>>> d
{'Michael': 95, 'Tracy': 85}
```


### set
- set和dict类似，也是一组key的集合，但不存储value。由于key不能重复，所以，在set中，没有重复的key。
```
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}
```
- set.add('XX')添加
- set.remove('XX')删除
```
>>> s.add(4)
>>> s
{1, 2, 3, 4}
>>> s.remove(4)
>>> s
{1, 2, 3}
```




## 高级特性

### 判断一个对象是可迭代对象呢？方法是通过collections模块的Iterable类型判断
```
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance([1,2,3], Iterable) # list是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```

### 下标循环 内置的enumerate函数可以把一个list变成索引-元素对
```
>>> for i, value in enumerate(['A', 'B', 'C']):
...     print(i, value)
...
0 A
1 B
2 C
```

###  列表生成式
```
>>> list(range(1, 11))
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
>>> [x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]
```

