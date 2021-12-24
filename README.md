# video2html
python将视频转换为网页字符动画，基于image2html

demo：https://hackedbyxx.github.io/my/demo/video2html.html

使用方法 <code>python main.py -i video.mp4 -d 10</code>

<code>-b', '--background', default='000000', metavar='#RRGGBB', help='background color (#RRGGBB format)'</code>

<code>-s', '--size', default=10, type=int, metavar='(4~30)', help='font size (int)'</code>

<code>-c', '--char', default='淘汰制作', metavar='CHAR', help='characters'</code>

<code>-t', '--title', default='create by xx', metavar='TITLE', help='html title'</code>

<code>-f', '--font', default='monospace', metavar='FONT', help='html font'</code>

<code>-i', '--in', metavar='IN', help='image to convert', required=True</code>

<code>-o', '--out', metavar='OUT', help='output file'</code>

<code>'-d', '--density', default=10, type=int, metavar='DENSITY', help='video frame density'</code>
