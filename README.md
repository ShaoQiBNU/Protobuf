Protobuf
========

# 一. Protobuf简介

> Google Protocol Buffer( 简称 Protobuf) 是 Google 公司内部的混合语言数据标准，目前已经正在使用的有超过 48,162 种报文格式定义和超过 12,183 个 .proto 文件，主要用于 RPC 系统和持续数据存储系统。
>
> Protocol Buffers 是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。它很适合做数据存储或 RPC 数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式。目前提供了 C++、Java、Python 三种语言的 API。
>
> protobuf很适合用做数据存储和作为不同应用，不同语言之间相互通信的数据交换格式，只要实现相同的协议格式即同一proto文件被编译成不同的语言版本，加入到各自的工程中去。这样不同语言就可以解析其他语言通过protobuf序列化的数据。

# 二. 定义消息

## (一) 简单消息

### 1. proto文件
> 要想使用protobuf必须得先定义proto文件，定义程序中需要处理的结构化数据，在 protobuf 的术语中，结构化数据被称为 Message。proto 文件非常类似 java 或者 C 语言的数据定义，下面是这个.proto文件所定义的消息类型，如下：

```protobuf
syntax = "proto3";

message Article {
int32 article_id=1;
string article_excerpt=2;
string article_picture=3;
}
```

### 2. 语法解读

```protobuf
syntax = "proto3";
```
> 这句表示指示正在使用proto3语法，默认是proto2

```protobuf
message Article 
```
> 这句表示消息定义的关键字

```protobuf
int32 article_id=1;
string article_excerpt=2;
string article_picture=3;
```
> 这里定义了3个字段，名称/值对，每一条Article消息类型的数据都包含这三个字段定义的数据，每个字段包含一个名称和类型。string，int32表示字段类型。.proto文件中消息结构里用于定义字段的标准数据类型如下表所示，后面几列是.proto文件中定义的标准类型编译转换后在编程语言中的类型对照。具体可到官网查阅：https://developers.google.com/protocol-buffers/docs/proto3#scalar. 

![image](https://github.com/ShaoQiBNU/Protobuf/blob/master/image/1.png)

> 另外，每个字段都定义了一个唯一的数值标签，这些唯一的数值标签用来标识二进制消息中所定义的字段，一旦定义了编译后就无法修改。需要特别提醒的是标签1–15标识的字段编码仅占用1个字节（包括字段类型和标识标签），更多详细的信息请参考ProtoBuf编码。数值标签16–2047标识的字段编码占用2个字节。因此，实际应用中应该将标签1–15留给那些在消息类型中使用频率高的字段，记得预留一些空间（标签1–15）给将来可能添加的高频率字段，此外不能使用protobuf系统预留的编号标签（19000－19999）。

### 3. 保留字段
> 如果我们通过直接删除或注释一个字段的方式 更新 了一个消息结构，将来别人在更新这个消息的时候可能会重复使用标签。如果他们以后加载旧版本的相同的.proto 文件，可能会导致严重的问题。包括数据冲突、 隐秘的 bug 等等。为了保证这种情况不会发生，当我们想删除一个字段的时候，可以使用 reserved 关键字来申明该字段的标签（和/或名字，这在 JSON 序列化的时候也会产生问题）。 将来如果有人使用了我们使用 reserved关键字定义的标签或名字，编译器就好报错，如下：
```protobuf
message Foo {
  reserved 2, 15, 9 to 11;
  reserved "foo", "bar";
}
```

### 4. 枚举
> 当定义一个消息的时候，可能会希望某个字段在预定的取值列表里面取值。 例如，假设想为 SearchRequest 消息定义一个 corpus字段，它的取值可能是 UNIVERSAL，WEB，IMAGES，LOCAL，NEWS，PRODUCTS 或者 VIDEO，这样我们只需要简单的利用 enum 关键字定义一个枚举类型，它的每一个可能的取值都是常量，枚举类型的第一个常量被设置为0，代码如下：

```protobuf
message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;

  enum Corpus {
      UNIVERSAL = 0;
      WEB = 1;
      IMAGES = 2;
      LOCAL = 3;
      NEWS = 4;
      PRODUCTS = 5;
      VIDEO = 6;
  }

  Corpus corpus = 4;
}
```

### 5. Oneof
> 如果消息中定义了很多字段，而且最多每次只能有一个字段被设置赋值，那么可以利用 Oneof 特性来实现这种行为并能节省内存。Oneof 字段除了拥有常规字段的特性之外，所有字段共享一片 oneof 内存，而且每次最多只能有一个字段被设置赋值。设置 oneof组中的任意一个成员的值时，其它成员的值被自动清除。 可以用 case()或 WhickOneof()方法检查 oneof 组中哪个成员的值被设置了，具体选择哪个方法取决于所使用的编程语言。在.proto 文件中定义 oneof 需要用到 oneof 关键字，其后紧跟的是 oneof 的名字。下例中的 oneof 名字是 test_oneof：
```protobuf
message SampleMessage {
    oneof test_oneof {
          string name = 4;
          SubMessage sub_message = 9;
      }
}
```
> 设置 oneof 组中某一个成员的值时，其它成员的值被自动清除。因此，当 oneof 组中有多个成员的时候，只有最后一个被赋值的字段拥有自己的值。oneof 字段不能是 repeated 可重复的，可以使用反射函数。

## (二) 复杂消息
### 1. 多个消息
> 同一个.proto 文件中可以定义多个消息类型，这在定义多个相关的消息时非常有用。例如，如果想针对用于搜索查询的 SearchRequest 消息定义一个保存查找结果的 SearchResponse 消息，可以把它们放在同一个.proto 文件中：

```protobuf
syntax = "proto3";

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}

message SearchResponse {
  ...
}
```

### 2. 消息嵌套和复用

> 可以在一个消息结构内部定义另外一个消息类型，如下例所示：Result 消息类型定义在 SearchResponse 消息体内部
```protobuf
message SearchResponse {

    message Result {
        string url = 1;
        string title = 2;
        repeated string snippets = 3;
    }

    repeated Result result = 1;
}
```

> 如果想在它的父消息外部复用这个内部定义的消息类型，可以采用 Parent.Type 语法格式：

```protobuf
message SomeOtherMessage {
    SearchResponse.Result result = 1;
}
```

### 3. 使用其他消息类型
> 可以使用其它消息类型来定义字段，假如想在每一个 SearchResponse 消息里面定义一个 Result 消息类型的字段，只需要同一个.proto文件中定义 Result 消息，并用它来定义 SearchResponse 中的一个字段即可，代码如下：

```protobuf
message SearchResponse {
    repeated Result result = 1;
}

message Result {
    string url = 1;
    string title = 2;
    repeated string snippets = 3;
}
```

### 4. 导入定义
> 在上面的例子中，Result 消息类型和 SearchResponse 消息类型是定义在同一个文件中的，如果想用另外一个.proto 文件中定义的消息类型来定义字段，则可以导入其它.proto 文件中已经定义的消息，来定义该消息类型的字段。为了导入其它.proto 文件中的定义，需要在.proto 文件头部申明import 语句：

```protobuf
import "myproject/other_protos.proto";
```
# 三. 编译文件

## 1. 定义文件
> 定义如下的proto文件：

```protobuf
syntax = "proto3";

message Article {
   int32 article_id = 1; // ------article id
   string article_excerpt = 2; // ------article id
   repeated string article_picture = 3; // ------article id
   int32 article_pagecount = 4; // ------article id

  enum ArticleType {
    NOVEL = 0;
    PROSE = 1;
    PAPER = 2;
    POETRY = 3;
  }

   ArticleType article_type = 5; // -------article type

   message Author {
     string name = 1; //作者的名字
     string phone = 2; // 作者电话
  }

   Author author = 6; // ------article id
   reserved  9, 10, 12 to 15; // ------保留标签
}

message Other {
   string other_info = 1; // ------other info

   oneof test_oneof {
    string code1 = 2;
    string code2 = 3;
  }
}
```

## 2. 编译文件
> 有了proto文件后，需要把它编译成我们需要的语言，这里以python为例，通过以下命令生成我们需要的python代码，然后会发现目录多了一个article_pb2.py的文件，编译命令如下：
```linux
protoc -I=.  --python_out=.  article.proto
```

> 生成的article_pb2.py代码如下：

```python
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: article.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='article.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\rarticle.proto\"\xac\x02\n\x07\x41rticle\x12\x12\n\narticle_id\x18\x01 \x01(\x05\x12\x17\n\x0f\x61rticle_excerpt\x18\x02 \x01(\t\x12\x17\n\x0f\x61rticle_picture\x18\x03 \x03(\t\x12\x19\n\x11\x61rticle_pagecount\x18\x04 \x01(\x05\x12*\n\x0c\x61rticle_type\x18\x05 \x01(\x0e\x32\x14.Article.ArticleType\x12\x1f\n\x06\x61uthor\x18\x06 \x01(\x0b\x32\x0f.Article.Author\x1a%\n\x06\x41uthor\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05phone\x18\x02 \x01(\t\":\n\x0b\x41rticleType\x12\t\n\x05NOVEL\x10\x00\x12\t\n\x05PROSE\x10\x01\x12\t\n\x05PAPER\x10\x02\x12\n\n\x06POETRY\x10\x03J\x04\x08\t\x10\nJ\x04\x08\n\x10\x0bJ\x04\x08\x0c\x10\x10\"K\n\x05Other\x12\x12\n\nother_info\x18\x01 \x01(\t\x12\x0f\n\x05\x63ode1\x18\x02 \x01(\tH\x00\x12\x0f\n\x05\x63ode2\x18\x03 \x01(\tH\x00\x42\x0c\n\ntest_oneofb\x06proto3')
)



_ARTICLE_ARTICLETYPE = _descriptor.EnumDescriptor(
  name='ArticleType',
  full_name='Article.ArticleType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NOVEL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROSE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PAPER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POETRY', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=242,
  serialized_end=300,
)
_sym_db.RegisterEnumDescriptor(_ARTICLE_ARTICLETYPE)


_ARTICLE_AUTHOR = _descriptor.Descriptor(
  name='Author',
  full_name='Article.Author',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Article.Author.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='phone', full_name='Article.Author.phone', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=203,
  serialized_end=240,
)

_ARTICLE = _descriptor.Descriptor(
  name='Article',
  full_name='Article',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='article_id', full_name='Article.article_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='article_excerpt', full_name='Article.article_excerpt', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='article_picture', full_name='Article.article_picture', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='article_pagecount', full_name='Article.article_pagecount', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='article_type', full_name='Article.article_type', index=4,
      number=5, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='author', full_name='Article.author', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_ARTICLE_AUTHOR, ],
  enum_types=[
    _ARTICLE_ARTICLETYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=318,
)


_OTHER = _descriptor.Descriptor(
  name='Other',
  full_name='Other',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='other_info', full_name='Other.other_info', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='code1', full_name='Other.code1', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='code2', full_name='Other.code2', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='test_oneof', full_name='Other.test_oneof',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=320,
  serialized_end=395,
)

_ARTICLE_AUTHOR.containing_type = _ARTICLE
_ARTICLE.fields_by_name['article_type'].enum_type = _ARTICLE_ARTICLETYPE
_ARTICLE.fields_by_name['author'].message_type = _ARTICLE_AUTHOR
_ARTICLE_ARTICLETYPE.containing_type = _ARTICLE
_OTHER.oneofs_by_name['test_oneof'].fields.append(
  _OTHER.fields_by_name['code1'])
_OTHER.fields_by_name['code1'].containing_oneof = _OTHER.oneofs_by_name['test_oneof']
_OTHER.oneofs_by_name['test_oneof'].fields.append(
  _OTHER.fields_by_name['code2'])
_OTHER.fields_by_name['code2'].containing_oneof = _OTHER.oneofs_by_name['test_oneof']
DESCRIPTOR.message_types_by_name['Article'] = _ARTICLE
DESCRIPTOR.message_types_by_name['Other'] = _OTHER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Article = _reflection.GeneratedProtocolMessageType('Article', (_message.Message,), dict(

  Author = _reflection.GeneratedProtocolMessageType('Author', (_message.Message,), dict(
    DESCRIPTOR = _ARTICLE_AUTHOR,
    __module__ = 'article_pb2'
    # @@protoc_insertion_point(class_scope:Article.Author)
    ))
  ,
  DESCRIPTOR = _ARTICLE,
  __module__ = 'article_pb2'
  # @@protoc_insertion_point(class_scope:Article)
  ))
_sym_db.RegisterMessage(Article)
_sym_db.RegisterMessage(Article.Author)

Other = _reflection.GeneratedProtocolMessageType('Other', (_message.Message,), dict(
  DESCRIPTOR = _OTHER,
  __module__ = 'article_pb2'
  # @@protoc_insertion_point(class_scope:Other)
  ))
_sym_db.RegisterMessage(Other)


# @@protoc_insertion_point(module_scope)
```
## 3. 序列化
> 采用SerializeToStrin方法做序列化，代码如下：

```python
# -*- coding: utf-8 -*-
 
import article_pb2
from google.protobuf import json_format
from google.protobuf import text_format
 
article = article_pb2.Article()
article.article_id = 1  # 必须赋值，不然在序列化得时候会报异常
article.article_excerpt = "文章简介"
article.article_type = 2
 
# 内嵌消息操作
author = article.author
author.name = "oliver"
author.phone = "11343234"
 
# repeated类型的字段添加
article_picture = article.article_picture
article_picture.append("1.jpg")
article_picture.append("2.jpg")

# oneof操作,会发现当执行 oneof.code2 = "code2"之后，输出的结果中没有code1.自动被清除了。
oneof = article_pb2.Other()
oneof.code1 = "code1"
print(oneof)
"""
code1: "code1"
"""
oneof.code2 = "code2"
print(oneof)
"""
code2: "code2"
"""
 
print(article.IsInitialized())  # 检查required字段是否全部被赋值
 
print(article.ListFields())  # 列出所有字段得一个元组列表
 
article_binary = article.SerializeToString()  # 序列化API
# article.SerializePartialToString()  # 也可以序列化消息，只不过它不会检查required是否被设置，也就是说可以序列化required字段没有被赋值的情况
 
with open("article.binary.txt", "wb+") as f:  # 保存到文件
    f.write(article_binary)
```

## 4. 反序列化

> 采用ParseFromString方法做反序列化，代码如下：

```python
# -*- coding: utf-8 -*-
 
import article_pb2
from google.protobuf import json_format
from google.protobuf import text_format
 
article = article_pb2.Article()
article.article_id = 1  # 必须赋值，不然在序列化得时候会报异常
article.article_excerpt = "文章简介"
article.article_type = 2
 
# 内嵌消息操作
author = article.author
author.name = "oliver"
author.phone = "11343234"
 
# repeated类型的字段添加
article_picture = article.article_picture
article_picture.append("1.jpg")
article_picture.append("2.jpg")
 
print(article.IsInitialized())  # 检查required字段是否全部被赋值

 
print(article.ListFields())  # 列出所有字段得一个元组列表
 
article_binary = article.SerializeToString()  # 序列化API
# article.SerializePartialToString()  # 也可以序列化消息，只不过它不会检查required是否被设置，也就是说可以序列化required字段没有被赋值的情况
 
with open("article.binary.txt", "wb+") as f:  # 保存到文件
    f.write(article_binary)
 
# 反序列化API ParseFromString 此外将ParseFromString换成MergeFromString这个接口来反序列化也可以
another_article = article_pb2.Article()
another_article.ParseFromString(article_binary)
print(another_article)
```

