# -*- coding：utf-8 -*-

from django.shortcuts import HttpResponse
from Crypto.Cipher import AES
import json
import hashlib
import time

# 以下大写变量都可以写入配置文件中
EXPIRE = 10         # 令牌生命期，单位为秒
AUTH_KEY = 'ThisIsAnAuthKeyForApiAccess'    # api访问密匙
DATA_KEY = b'ThisKeyMustBeSix'  # 数据通信密匙，由于选择了AES的MODE_CBC模式，长度必须为16位

api_auth_record = {}    # api访问记录，形如："e05eec4bf729b80e6d60cfec01ff0e30|1501474102.8840663":"1501474112.8840663"}


def api_access(func):
    def wrapper(requset, *args, **kwargs):
        """
        api权限验证
        :param requset:
        :param args:
        :param kwargs:
        :return:
        """
        client_openkey = requset.META.get('HTTP_OPENKEY')       # 获取请求端密匙
        client_key, client_time = client_openkey.split('|')     # 拆分密匙：动态令牌+请求端时间
        client_time = float(client_time)
        server_time = time.time()
        # 若动态令牌超时，认证失败
        if server_time - client_time > EXPIRE:
            return HttpResponse('接口超时')
        # 根据请求端的时间及api端令牌，计算动态令牌
        temp = "%s|%s" % (AUTH_KEY, client_time)
        m = hashlib.md5()
        m.update(bytes(temp, encoding='utf-8'))
        server_openkey = m.hexdigest()
        # 若动态令牌不符，认证失败
        if server_openkey != client_key:
            return HttpResponse('接口验证失败')
        # 维护api访问记录，删除已过期的密匙
        for openkey in list(api_auth_record):
            overtime = api_auth_record[openkey]
            if server_time > overtime:
                del api_auth_record[openkey]
        # 若密匙已被使用过，认证失败，否则加入api访问记录内
        if client_openkey in api_auth_record:
            return HttpResponse('该接口已被请求过')
        else:
            api_auth_record[client_openkey] = client_time + EXPIRE
            ret = func(requset)         # 执行被装饰方法
            return ret
    return wrapper


def encrypt(data):
    """
    数据加密
    要加密的字符串，必须是16个字节或16个字节的倍数
    :param data:
    :return:
    """
    cipher = AES.new(DATA_KEY, AES.MODE_CBC, DATA_KEY)
    ba_data = bytearray(data, encoding='utf-8')         # bytearray可变对象
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    # 补齐数据长度为16的倍数
    for i in range(v3):
        ba_data.append(v3)
    final_data = ba_data.decode('utf-8')        # 解码为字符串
    msg = cipher.encrypt(bytes(final_data, encoding='utf-8'))        # 编码为byte数据
    return msg


def decrypt(data):
    """
    数据解密
    :param data:
    :return:
    """
    cipher = AES.new(DATA_KEY, AES.MODE_CBC, DATA_KEY)
    result = cipher.decrypt(data)
    data = result[0: -result[-1]]       # -result[-1]代表加密时补位的数字的个数
    return str(data, encoding='utf-8')