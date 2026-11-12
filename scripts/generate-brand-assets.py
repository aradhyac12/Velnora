#!/usr/bin/env python3
"""Regenerates the VELNORA logo assets (seal, icons, favicons, OG image, Android icons/splash). Needs Pillow."""
from PIL import Image, ImageDraw, ImageFont
import glob, os
NAVY=(0,26,57); IVORY=(252,249,242); GOLD=(176,141,87)
SS=4
def mark(d, cx, cy, s, ink=IVORY, dot=GOLD):
    # Balanced geometric "V" with a short gold base bar; unit square 100x100, optically centred.
    def P(pts): return [(cx+(x-50)*s, cy+(y-53)*s) for x,y in pts]
    d.polygon(P([(20,24),(33.5,24),(50,60),(66.5,24),(80,24),(55.5,76),(44.5,76)]), fill=ink)
    d.rectangle(P([(41,83),(59,86)]) [0]+P([(41,83),(59,86)])[1], fill=dot)
def canvas(w,h,bg=None):
    im=Image.new("RGBA",(w*SS,h*SS),bg or (0,0,0,0)); return im, ImageDraw.Draw(im)
def done(im,w,h): return im.resize((w,h),Image.LANCZOS)
def seal(n):
    im,d=canvas(n,n); S=n*SS
    d.ellipse([0,0,S-1,S-1],fill=NAVY)
    rr=S*0.455; w=max(1,int(S*0.008)); d.ellipse([S/2-rr,S/2-rr,S/2+rr,S/2+rr],outline=GOLD,width=w)
    mark(d,S/2,S/2,S/100*0.88); return done(im,n,n)
def icon(n,round_=False,bg=NAVY):
    im,d=canvas(n,n); S=n*SS
    if round_: d.ellipse([0,0,S-1,S-1],fill=bg)
    else: d.rectangle([0,0,S,S],fill=bg)
    mark(d,S/2,S/2,S/100*0.62); return done(im,n,n)
def foreground(n):
    im,d=canvas(n,n); S=n*SS; mark(d,S/2,S/2,S/100*0.5); return done(im,n,n)
def splash(w,h):
    im,d=canvas(w,h,IVORY+(255,)); m=int(min(w,h)*0.3)
    s=seal(m*1); im=done(im,w,h); im.alpha_composite(s,((w-m)//2,(h-m)//2)); return im
def font(sz,bold=True):
    return ImageFont.truetype("/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf" if bold else "/usr/share/fonts/opentype/inter/InterDisplay-Light.otf",sz)
def spaced(d,xy,text,f,fill,track):
    x,y=xy
    for ch in text:
        d.text((x,y),ch,font=f,fill=fill); x+=d.textlength(ch,font=f)+track
    return x
def lockup(W,H,bg=IVORY):
    im=Image.new("RGB",(W,H),bg); n=int(H*0.5); s=seal(n); im.paste(s,(int(W*0.09),(H-n)//2),s)
    d=ImageDraw.Draw(im); x=int(W*0.09)+n+int(H*0.1)
    f=font(int(H*0.16)); spaced(d,(x,int(H*0.31)),"VELNORA",f,NAVY,int(H*0.035))
    d.line([x,int(H*0.56),x+int(H*0.2),int(H*0.56)],fill=GOLD,width=max(2,H//200))
    spaced(d,(x,int(H*0.6)),"INTERNATIONAL JOURNAL OF MEDICAL INNOVATION",font(int(H*0.036),False),(95,95,90),int(H*0.006)); return im
def og(): return lockup(1200,630)
pub=lambda f:"public/"+f
seal(512).save(pub("velnora-seal.png")); seal(1200).save(pub("velnora-seal-hd.png"))
for n,f in [(192,"icon-192.png"),(512,"icon-512.png"),(180,"apple-touch-icon.png"),(32,"favicon-32.png"),(48,"favicon-48.png")]: icon(n).save(pub(f))
icon(48).save(pub("favicon.ico"),sizes=[(16,16),(32,32),(48,48)])
og().save(pub("og-image.jpg"),quality=92); lockup(2400,1000).save(pub("velnora-logo-horizontal.png"))
res="android/app/src/main/res/"
for f in glob.glob(res+"mipmap-*/ic_launcher*.png"):
    n=Image.open(f).size[0]; b=os.path.basename(f)
    (foreground(n) if "foreground" in b else icon(n,round_="round" in b)).save(f)
for f in glob.glob(res+"drawable*/splash.png"):
    w,h=Image.open(f).size; splash(w,h).convert("RGB").save(f)
open(res+"values/ic_launcher_background.xml","w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#001A39</color>\n</resources>\n')
print("ok")
