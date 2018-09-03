#!/usr/bin/env python
# encoding=utf-8
from __future__ import print_function, unicode_literals

import os
import sys
import time
import json
from collections import namedtuple
from itertools import cycle
import jinja2
from PIL import Image

Point = namedtuple('Point', ['x', 'y'])
Pixel = namedtuple('Pixel', ['r', 'g', 'b'])
RenderItem = namedtuple('RenderItem', ['color', 'char'])
RenderGroup = list
HTMLImage = list

TEMPLATE = '''
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <style type="text/css">
        body {
            margin: 0px; padding: 0px; line-height:100%; letter-spacing:0px; text-align: center;
            min-width: {{width}}px;
            width: auto !important;
            font-size: {{size}}px;
            background-color: #{{background}};
            font-family: {{font_family}};
        }
    </style>
</head>
<body>
<div>
{% for group in html_image %}
    {% for item in group %}<font color="#{{ item.color }}">{{ item.char }}</font>{% endfor %}
    <br>
{% endfor %}
</div>
<script>
    var colors = {{colors}}
    let i =-1;
    var fonts = document.getElementsByTagName('font')
    console.log('fonts.length:'+fonts.length);
    var int = setInterval(function(){
        if(i==colors.length-1){
            i=-1;
            console.log('播放完成');
        }
        i++;
        let color = colors[i];
        //console.log('color.type'+typeof(color));
        //console.log('color.length'+color.length)
        for(var j=0;j<color.length;j++){
            fonts[j].color = color[j];
        }
    },300)
</script>
</body>
</html>'''


_c = cycle(r'/-\|')


def _progress_callback(percent):
    if percent == 100:
        os.system("cls")
        print("100%完成！")  
    else:
        lca = getattr(_progress_callback, '_last_call_at', 0)
        if time.time() - lca > 0.5:
            _progress_callback._last_call_at = time.time()
            #sys.stdout.write('\r{} progress: {:.2f}%'.format(_c.next(), percent))
            
            Img2HTMLConverter.showprogress(percent)


class Img2HTMLConverter(object):
    def __init__(self,
                 font_size=10,
                 char='䦗',
                 background='#000000',
                 title='by xx',
                 font_family='monospace',
                 progress_callback=None):
        self.font_size = font_size
        self.background = background
        self.title = title
        self.font_family = font_family
        if isinstance(char, str):
            #char = char.encode('utf-8')
            pass
        self.char = cycle(char)
        self._prg_cb = progress_callback or _progress_callback

    def convert(self, source ,colors):
        image = Image.open(source)
        width, height = image.size

        #按比例缩高
        if width>1200 and height<width:
            height = int(1200/width*height)
            width = 1200
        #按比例缩宽
        elif height>800:
            width = int(800/height*width)
            height = 800

        size = width,height
        image.thumbnail(size, Image.ANTIALIAS)
        print(width,height)
        width,height = image.size
        row_blocks = int(round(float(width) / self.font_size))
        col_blocks = int(round(float(height) / self.font_size))
        html_image = HTMLImage()
        progress = 0.0
        step = 1. / (col_blocks * row_blocks)

        for col in range(col_blocks):
            render_group = RenderGroup()
            for row in range(row_blocks):
                pixels = []
                for y in range(self.font_size):
                    for x in range(self.font_size):
                        point = Point(row * self.font_size + x, col * self.font_size + y)
                        if point.x >= width or point.y >= height:
                            continue
                        pixels.append(Pixel(*image.getpixel(point)[:3]))
                average = self.get_average(pixels=pixels)
                color = self.rgb2hex(average)
                render_item = RenderItem(color=color, char=next(self.char))
                render_group.append(render_item)

                progress += step
                self._prg_cb(int(progress * 100))

            html_image.append(render_group)

        self._prg_cb(100)
        return self.render(html_image,colors)

    def convertColors(self, source):

        colors = []
        
        image = Image.open(source)
        width, height = image.size

        #按比例缩高
        if width>1200 and height<width:
            height = int(1200/width*height)
            width = 1200
        #按比例缩宽
        elif height>800:
            width = int(800/height*width)
            height = 800

        size = width,height
        image.thumbnail(size, Image.ANTIALIAS)
        print(width,height)
        width,height = image.size
        row_blocks = int(round(float(width) / self.font_size))
        col_blocks = int(round(float(height) / self.font_size))
        html_image = HTMLImage()
        progress = 0.0
        step = 1. / (col_blocks * row_blocks)

        for col in range(col_blocks):
            render_group = RenderGroup()
            for row in range(row_blocks):
                pixels = []
                for y in range(self.font_size):
                    for x in range(self.font_size):
                        point = Point(row * self.font_size + x, col * self.font_size + y)
                        if point.x >= width or point.y >= height:
                            continue
                        pixels.append(Pixel(*image.getpixel(point)[:3]))
                average = self.get_average(pixels=pixels)
                color = self.rgb2hex(average)
                colors.append('#'+color)#将color存入数组里
                render_item = RenderItem(color=color, char=next(self.char))
                render_group.append(render_item)
    
                progress += step
                self._prg_cb(int(progress * 100))

            #html_image.append(render_group)

        self._prg_cb(100)
        return json.dumps(colors)
        #return self.render(html_image),'null'   

    def showprogress(progress):
        os.system("cls")
        #打印一个#号，这种方法打印不会自动换行  
        sys.stdout.write("转换中："+str(progress)+'%')  
        #实时刷新一下，否则上面这一条语句，会等#号全部写入到缓存中后才一次性打印出来  
        sys.stdout.flush()  
        #每个#号等待0.1秒的时间打印  
        #time.sleep(0.1)  

    def render(self, html_image,colors):
        template = jinja2.Template(TEMPLATE)
        return template.render(
            html_image=html_image,
            colors =colors,
            size=self.font_size,
            background=self.background,
            title=self.title,
            font_family=self.font_family,
            width=self.font_size * len(html_image[0])
        )

    @staticmethod
    def rgb2hex(pixel):
        return '{:02x}{:02x}{:02x}'.format(*pixel)

    @staticmethod
    def get_average(pixels):
        r, g, b = 0, 0, 0
        for pixel in pixels:
            r += pixel.r
            g += pixel.g
            b += pixel.b
        base = float(len(pixels))
        return Pixel(
            r=int(round(r / base)),
            g=int(round(g / base)),
            b=int(round(b / base)),
        )
