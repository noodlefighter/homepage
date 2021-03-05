
import sys
import re
import os.path
import shutil
from functools import reduce

src_file = sys.argv[1] # example: ./嵌入式软件/MQTT协议快速入门.md
dst_dir  = sys.argv[2]
src_dir  = os.path.dirname(src_file)

# name_list, like: ['嵌入式软件','MQTT协议快速入门.md']
name_list = src_file.split('/')
name_list = list(filter(lambda x: x != '.', name_list))

categorys = name_list[0:-1]

src_basename = name_list[-1]
dst_basename = reduce(lambda x,y: x + "-" + y , name_list)

dst_file = dst_dir + '/' + dst_basename

src_title = src_basename.split('.')[0]
dst_title = dst_basename.split('.')[0]

# copy images
img_src_dir = '%s/_assets/%s' % (src_dir, src_title)
img_dst_dir = dst_dir + '/' + dst_title
if os.path.exists(img_src_dir):
    shutil.copytree(img_src_dir, img_dst_dir)

# create target file
with open(dst_file, mode='w', encoding='utf-8') as f:
    f.write('title: ' + src_title + '\n')

    if len(categorys) != 0:
        f.write('categories:\n')
        for c in categorys:
            f.write('  - ' + c + '\n')

    with open(src_file, 'r') as sf:
        pattern = re.compile(r'!\[(?P<desc>.+)\]\(_assets\/.+\/(?P<file>.+)\)')
        for l in sf.readlines():
            def newstr(matched):
                desc = str(matched.group('desc'))
                name = str(matched.group('file'))
                return '{% asset_img ' + name + ' ' + desc + ' %}'
            new_l = re.sub(pattern, newstr, l)
            f.write(new_l)



