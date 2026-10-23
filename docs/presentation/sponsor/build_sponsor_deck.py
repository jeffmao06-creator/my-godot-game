#!/usr/bin/env python3
"""A PDF-only, art-led Traditional Chinese sponsorship concept presentation.

python3 build_sponsor_deck.py --content sponsor_content.json --output pitch.pdf

Images are placed from their original PNGs without changing the source artwork.
The renderer keeps all art visible; it does not make production game sprites.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

from reportlab import rl_config
from reportlab.pdfgen import canvas

# Flate-compressed original pixels; omitting ASCII85 is lossless and reduces PDF size.
rl_config.useA85 = False
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

sys.dont_write_bytecode = True

PREVIOUS_RENDERER = Path(__file__).resolve().parent.parent / 'build_deck.py'
spec = importlib.util.spec_from_file_location('lawfirm_font_helpers', PREVIOUS_RENDERER)
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)

W, H = 1280, 720
FONT, BOLD = helpers.FONT, helpers.BOLD
STYLE_SOURCE = Path(__file__).resolve().parents[2] / 'art' / 'visual_style.json'
STYLE = json.loads(STYLE_SOURCE.read_text(encoding='utf-8'))
STYLE_COLORS = {entry['name']: entry['hex'] for entry in STYLE['palette']}
PALETTE = {
    'paper': STYLE_COLORS['暖紙色'], 'navy': STYLE_COLORS['深藍'],
    'teal': STYLE_COLORS['玉綠'], 'amber': STYLE_COLORS['琥珀'],
    'coral': STYLE_COLORS['警示紅'], 'ink': STYLE_COLORS['深藍'],
    'wood': STYLE_COLORS['木棕'],
    'muted':'#93A7A8', 'white':'#FFFFFF', 'line':'#CBD5CC',
    'soft':'#DFE9E2', 'dark':'#0D222C',
}


def color(name):
    return HexColor(PALETTE.get(name, name))


def rect(c,x,y,w,h,fill='paper',stroke=None,r=0):
    c.setFillColor(color(fill))
    c.setStrokeColor(color(stroke or fill))
    if r:
        c.roundRect(x,y,w,h,r,fill=1,stroke=bool(stroke))
    else:
        c.rect(x,y,w,h,fill=1,stroke=bool(stroke))


def text(c,value,x,top,w,h,size=24,fill='ink',bold=False,min_size=None,leading=None,align='left'):
    return helpers.textbox(c,str(value or ''),x,top,w,h,size=size,fill=PALETTE.get(fill,fill),
        font=BOLD if bold else FONT,min_size=min_size or size,leading=leading,align=align)


def resolve_image(value,base):
    if not value: return None
    if isinstance(value,dict): value=value.get('image') or value.get('path')
    p=Path(value)
    if not p.is_absolute():p=base/p
    if not p.is_file():raise FileNotFoundError(p)
    return p


def artwork(c,value,base,x,y,w,h,background='navy',border=False):
    """Fit the whole original image inside its window, preserving aspect ratio."""
    if background:rect(c,x,y,w,h,background,stroke='line' if border else None)
    p=resolve_image(value,base)
    if p is None:
        text(c,'概念圖',x,y+h/2+16,w,40,size=26,fill='muted',align='center')
        return
    reader=ImageReader(str(p))
    iw,ih=reader.getSize()
    ratio=min(w/iw,h/ih)
    dw,dh=iw*ratio,ih*ratio
    c.drawImage(reader,x+(w-dw)/2,y+(h-dh)/2,dw,dh,mask='auto')


def body_list(value):
    if value is None:return []
    return value if isinstance(value,list) else [value]


def bullets(c,items,x,top,w,h,size=22,fill='ink',gap=15):
    items=body_list(items)
    if not items:return
    size0=size
    while size>=16:
        rows=[helpers.lines_for(i,w-24,size,FONT) for i in items]
        required=sum(len(r)*size*1.40+gap for r in rows)
        if required<=h:break
        size-=.5
    if size<16:raise ValueError('Sponsor slide copy is too long: '+str(items)[:120])
    y=top
    for item in items:
        rect(c,x,y-size+3,6,6,'amber')
        used=text(c,item,x+22,y,w-22,h,size=size,fill=fill,leading=size*1.40)
        y-=used+gap


def brand_mark(c,x=1190,y=679,dark=False):
    colors=['amber','teal','paper' if dark else 'ink']
    for i,(dx,dy) in enumerate([(0,0),(16,0),(32,0),(32,16)]):
        rect(c,x+dx,y+dy,11,11,colors[i%3])


def folio(c,index,total,dark=False,note=None):
    ink='muted' if dark else '#6D8082'
    text(c,'訴訟之神之路｜遊戲概念提案',40,23,960,16,size=9.5,fill=ink)
    text(c,f'{index:02d} / {total:02d}',1150,25,90,20,size=11,fill=ink,align='right')
    if note:
        text(c,note,40,40,1160,19,size=10,fill=ink,min_size=9)


def eyebrow(c,slide,dark=False,x=48,top=694,w=1100):
    text(c,slide.get('eyebrow','訴訟之神之路'),x,top,w,24,size=11,fill='amber' if dark else 'teal',bold=True)


def short_header(c,slide,dark=False):
    eyebrow(c,slide,dark)
    text(c,slide.get('title','').replace('\n',' '),48,668,1160,52,size=34,fill='paper' if dark else 'ink',bold=True,min_size=29)
    brand_mark(c,dark=dark)


def cinematic(c,s,base,index,total,closing=False):
    rect(c,0,0,W,H,'navy')
    # A separate paper title column protects the artwork's faces and silhouettes.
    artwork(c,s.get('image'),base,404,55,836,610,background='navy')
    rect(c,0,0,380,H,'paper')
    rect(c,0,0,12,H,'teal')
    eyebrow(c,s,x=42,top=674,w=308)
    title=s.get('title','')
    title_used=text(c,title,40,598,312,212,size=45,fill='ink',bold=True,min_size=38,leading=64)
    subtitle_top=min(480,598-title_used-26)
    subtitle_used=0
    if s.get('subtitle'):
        subtitle_used=text(c,s['subtitle'],43,subtitle_top,306,135,size=23,fill='teal',min_size=19,leading=34)
    if s.get('body'):
        body_top=min(340,subtitle_top-subtitle_used-30)
        bullets(c,s['body'],43,body_top,303,114,size=17,fill='ink',gap=9)
    text(c,'CONCEPT VISUALS · NOT GAMEPLAY CAPTURE',424,675,800,21,size=10.5,fill='muted')
    text(c,f'{index:02d} / {total:02d}',1150,27,90,20,size=11,fill='muted',align='right')
    if s.get('note'):
        text(c,s['note'],424,50,790,24,size=10,fill='muted',min_size=9)


def spread(c,s,base,index,total):
    rect(c,0,0,W,H,'navy')
    text(c,s.get('eyebrow','訴訟之神之路'),42,711,1120,15,size=9.5,fill='amber',bold=True)
    text(c,s.get('title','').replace('\n',' '),42,691,1172,48,size=30,fill='paper',bold=True,min_size=28)
    artwork(c,s.get('image'),base,8,54,1264,600,background='navy')
    supporting=' · '.join([str(s.get('subtitle',''))]+body_list(s.get('body'))).strip(' ·')
    if supporting:text(c,supporting,42,49,1152,26,size=15.5,fill='paper',min_size=13)
    note=s.get('note') or '訴訟之神之路｜遊戲概念提案'
    text(c,note,42,20,1080,15,size=9,fill='muted',min_size=8)
    text(c,f'{index:02d} / {total:02d}',1150,22,90,18,size=10,fill='muted',align='right')


def editorial(c,s,base,index,total):
    rect(c,0,0,W,H,'paper')
    eyebrow(c,s,x=42,top=690,w=340)
    title=s.get('title','')
    text(c,title,40,628,346,165,size=39,fill='ink',bold=True,min_size=32,leading=56)
    if s.get('subtitle'):
        text(c,s['subtitle'],43,427,336,114,size=23,fill='teal',min_size=20,leading=34)
    bullets(c,s.get('body'),43,277,333,183,size=19,fill='ink',gap=13)
    rect(c,414,72,830,590,'soft')
    artwork(c,s.get('image'),base,426,84,806,566,background='soft')
    brand_mark(c,x=1187,y=674)
    folio(c,index,total,note=s.get('note'))


def gallery(c,s,base,index,total):
    rect(c,0,0,W,H,'paper')
    short_header(c,s)
    entries=s.get('images') or []
    n=len(entries)
    if n not in (2,3):raise ValueError('gallery requires two or three images')
    gap=18; x=42; width=(1196-gap*(n-1))/n
    for i,item in enumerate(entries):
        data={'image':item} if isinstance(item,str) else item
        xx=x+i*(width+gap)
        rect(c,xx,142,width,453,'white')
        artwork(c,data.get('image'),base,xx,236,width,359,background='white')
        text(c,data.get('title',''),xx+15,222,width-30,34,size=22,fill='ink',bold=True,min_size=18)
        if data.get('caption'):
            text(c,data['caption'],xx+15,185,width-30,66,size=15,fill='teal',min_size=13)
    supporting=' · '.join([str(s.get('subtitle',''))]+body_list(s.get('body'))).strip(' ·')
    if supporting:text(c,supporting,43,107,1194,45,size=20,fill='teal',min_size=18)
    folio(c,index,total,note=s.get('note'))


def quote(c,s,base,index,total):
    rect(c,0,0,W,H,'navy')
    if s.get('image'):
        artwork(c,s['image'],base,505,73,739,567,background='navy')
        rect(c,0,0,466,H,'paper')
        eyebrow(c,s,x=45,top=683,w=371)
        rect(c,45,574,54,5,'amber')
        text(c,s.get('title',''),43,540,379,233,size=39,fill='ink',bold=True,min_size=32,leading=56)
        text(c,s.get('subtitle',''),46,262,365,116,size=23,fill='teal',min_size=20,leading=34)
        if s.get('body'):text(c,'\n'.join(body_list(s['body'])),46,122,366,66,size=17,fill='ink',min_size=15)
        text(c,f'{index:02d} / {total:02d}',1150,26,90,19,size=11,fill='muted',align='right')
        if s.get('note'):text(c,s['note'],502,49,733,23,size=10,fill='muted',min_size=9)
    else:
        eyebrow(c,s,dark=True)
        text(c,'「',51,593,100,100,size=88,fill='amber',bold=True)
        text(c,s.get('title',''),137,528,1003,245,size=56,fill='paper',bold=True,min_size=44,leading=80)
        text(c,s.get('subtitle',''),142,236,990,90,size=25,fill='muted',min_size=21,leading=38)
        if s.get('body'):text(c,' · '.join(body_list(s['body'])),142,122,990,44,size=18,fill='paper',min_size=16)
        folio(c,index,total,dark=True,note=s.get('note'))


def cards(c,s,base,index,total):
    dark=bool(s.get('dark',False))
    rect(c,0,0,W,H,'navy' if dark else 'paper')
    short_header(c,s,dark=dark)
    entries=s.get('cards') or []
    n=len(entries)
    if n<1 or n>4:raise ValueError('cards supports one to four concise cards')
    gap=20;width=(1196-gap*(n-1))/n
    accents=['teal','amber','coral','navy']
    for i,item in enumerate(entries):
        x=42+i*(width+gap)
        rect(c,x,145,width,418,'white')
        rect(c,x,555,width,8,accents[i%4])
        if item.get('tag'):text(c,item['tag'],x+24,531,width-48,30,size=14,fill='teal',bold=True,min_size=12)
        title_top=477 if item.get('tag') else 520
        text(c,item.get('title',''),x+24,title_top,width-48,110,size=29,fill='ink',bold=True,min_size=24,leading=40)
        body=item.get('body','')
        if isinstance(body,list):body='\n'.join(body)
        text(c,body,x+24,333,width-48,164,size=21,fill='ink',min_size=18,leading=31)
    supporting=' · '.join([str(s.get('subtitle',''))]+body_list(s.get('body'))).strip(' ·')
    if supporting:text(c,supporting,45,112,1189,42,size=20,fill='muted' if dark else 'teal',min_size=18)
    folio(c,index,total,dark=dark,note=s.get('note'))


def render(content,source,output):
    if not content.get('slides'):raise ValueError('Empty presentation')
    registration={'content':content,'renderer_labels':Path(__file__).read_text(encoding='utf-8')}
    helpers.register_fonts(registration,Path('/tmp/lawfirm-sponsor-fonts'))
    output.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(output),pagesize=(W,H),pageCompression=1)
    c.setTitle(content.get('title','訴訟之神之路｜贊助合作概念提案'))
    c.setAuthor('')
    c.setSubject('2D pixel-art game concept presentation; concept-stage sponsorship discussion')
    total=len(content['slides'])
    dispatch={'cinematic':cinematic,'spread':spread,'editorial':editorial,'gallery':gallery,'quote':quote,'cards':cards,'closing':cinematic}
    for index,s in enumerate(content['slides'],1):
        layout=s.get('layout','spread')
        if layout not in dispatch:raise ValueError('Unknown sponsor layout '+layout)
        try:dispatch[layout](c,s,source.parent,index,total)
        except Exception as e:raise ValueError(f'Slide {index} ({s.get("title")}): {e}') from e
        key=f'slide-{index}'
        c.bookmarkPage(key)
        c.addOutlineEntry(s.get('title','').replace('\n',' '),key,level=0,closed=False)
        c.showPage()
    c.save()
    return {'pages':total,'pdf':str(output),'bytes':output.stat().st_size,'warnings':helpers._WARNINGS}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--content',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    content=json.loads(args.content.read_text(encoding='utf-8'))
    print(json.dumps(render(content,args.content,args.output),ensure_ascii=False))


if __name__=='__main__':main()
