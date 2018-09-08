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