#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from hashlib import md5

try:
    from .config import username, password, soft_id
except Exception as im_err:
    try:
        from config import username, password, soft_id
    except Exception as im_err:
        print("image_code 包导入失败：{}".format(im_err))


# 验证码识别 封装
class CClient(object):
    def __init__(self, user_name, pass_word, u_soft_id):
        self.username = user_name
        self.password = md5(pass_word.encode("utf-8")).hexdigest()
        self.soft_id = u_soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    # 提交验证码
    def post_pic(self, im, code_type):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': code_type,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()


def get_code(image_name):
    c_ji_y = CClient(str(username), str(password), soft_id)
    im = open(image_name, 'rb').read()
    image_info = c_ji_y.post_pic(im, 1006)
    pic_code = image_info["pic_str"]
    return pic_code


if __name__ == '__main__':
    pass
