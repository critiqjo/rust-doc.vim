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

def new_surround(tag, end_with='', skip_tags=[], ret_end=True):
  return { 'tag': tag,
           'stack_len': 1,
           'end_with': end_with,
           'skip_tags': skip_tags,
           'ret_end': ret_end }

surround = {}

def rust_tag_handle(parser, tag, attrs, start):
  global surround

  if len(surround) > 0:
    if start:
      surround['stack_len'] += 1
    else:
      surround['stack_len'] -= 1

    if surround['stack_len'] == 0:
      parser.o(surround['end_with'])
      ret = surround['ret_end']
      surround = {}
      return ret

    if tag in surround['skip_tags']:
      return True

  if tag == 'em' and 'class' in attrs and 'stab' in attrs['class'] and start:
    parser.o("[notice] ")
    surround = new_surround(tag, ' [/notice]', 'p')
    return True

  if ((tag == 'span' and 'class' in attrs and 'rusttest' in attrs['class']) or \
      ('id' in attrs and attrs['id'] == 'help')) and start:
    parser.o("[ignore] ")
    surround = new_surround(tag, ' [/ignore]', 'p')
    return True

  if tag == 'td' and 'class' in attrs and 'docblock' in attrs['class'] and start:
    surround = new_surround(tag, '', ['p', 'em'], False)

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
