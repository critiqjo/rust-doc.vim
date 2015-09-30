#!/bin/env python
import os, sys

if len(sys.argv) < 2:
  print("Usage: {0} <path-to-html-page>".format(sys.argv[0]))
  sys.exit(1)

plugpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'html2text')
sys.path.append(plugpath)
import html2text

with open(sys.argv[1]) as f:
  html = f.read()

surround = {'active': False, 'tag': None, 'stack_len': 0, 'end_with': ''}

def rust_tag_handle(parser, tag, attrs, start):
  global surround

  if surround['active']:
    if start:
      surround['stack_len'] += 1
    else:
      surround['stack_len'] -= 1
    if surround['stack_len'] == 0:
      parser.o(surround['end_with'])
      surround['active'] = False
    return True

  if tag == 'em' and 'class' in attrs and 'stab' in attrs['class'] and start:
    parser.o("[notice] ")
    surround['active'] = True
    surround['tag'] = tag
    surround['stack_len'] = 1
    surround['end_with'] = '[/notice]'
    return True

  if ((tag == 'span' and 'class' in attrs and 'rusttest' in attrs['class']) or \
      (tag == 'div' and 'id' in attrs and attrs['id'] == 'help')) and start:
    parser.o("[ignore] ")
    surround['active'] = True
    surround['tag'] = tag
    surround['stack_len'] = 1
    surround['end_with'] = ' [/ignore]'
    return True

parser = html2text.HTML2Text()
parser.tag_callback = rust_tag_handle
parser.ignore_links = True
parser.ignore_images = True
parser.mark_code = True
text = parser.handle(html)

import re
text = re.sub(r'\n\[ignore\].*?\[/ignore\]\n', '', text, flags=re.S)
text = re.sub(r'\[code\]\n', '[code]', text)

print(text)
