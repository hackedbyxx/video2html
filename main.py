#!/usr/bin/env python
# encoding=utf-8

from __future__ import print_function, unicode_literals

import os
import cv2
import argparse
import codecs
import json
from converter import Img2HTMLConverter

def mkdir(path):
    # 引入模块
    import os
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def main():
    parser = argparse.ArgumentParser(description='img2html : Convert image to HTML')
    parser.add_argument('-b', '--background', default='000000', metavar='#RRGGBB',
                        help='background color (#RRGGBB format)')
    parser.add_argument('-s', '--size', default=10, type=int, metavar='(4~30)',
                        help='font size (int)')
    parser.add_argument('-c', '--char', default='淘汰制作', metavar='CHAR',
                        help='characters')
    parser.add_argument('-t', '--title', default='create by xx', metavar='TITLE',
                        help='html title')
    parser.add_argument('-f', '--font', default='monospace', metavar='FONT',
                        help='html font')
    parser.add_argument('-i', '--in', metavar='IN', help='image to convert', required=True)
    parser.add_argument('-o', '--out', default="test.html", metavar='OUT',
                        help='output file')

    args, text = parser.parse_known_args()

    converter = Img2HTMLConverter(
        font_size=args.size,
        char=args.char,
        background=args.background,
        title=args.title,
        font_family=args.font,
    )
    file = getattr(args, 'in')
    mkdir('image')

    #每帧视频间隔
    density = 10
    cap = cv2.VideoCapture(file)  #返回一个capture对象
    frames = cap.get(7)#获取所有的帧数
    colors = json.loads('[]')
    length = int(frames/density)
    for i in range(0,length):
        cap.set(cv2.CAP_PROP_POS_FRAMES,i*density)  #设置要获取的帧号
        a,b=cap.read()  #read方法返回一个布尔值和一个视频帧。若帧读取成功，则返回True
        cv2.imshow('b', b)
        cv2.waitKey(1000)
        if cv2.imwrite('image/'+str(i)+'.jpg',b):       #存储为图像
            
            
            color = converter.convertColors('image/'+str(i)+'.jpg')
            colors.append(json.loads(color))
            
            if i==(length-1):#最后一张时输出JSON
                filename = os.path.splitext(file)[0]
                html = converter.convert('image/0.jpg',json.dumps(colors))
                if args.out:
                    with codecs.open(args.out, 'wb', encoding='utf-8') as fp:
                        fp.write(html)
                else:
                    with codecs.open(filename+'.html', 'wb', encoding='utf-8') as fp:
                        fp.write(html)
                        pass
    
    
if __name__ == "__main__":
    main()


