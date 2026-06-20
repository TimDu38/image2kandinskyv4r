from kandinsky import fill_rect
def show_image(pal,rects,pos=(0,0),s=1):
 d=fill_rect;o=ord;p=pal
 f,x,y,w,h,c=0,0,0,0,0,(0,0,0)
 a,b=pos;a-=35*s;b-=35*s
 for i in rects:
  v=o(i)
  if f==4:
   if v<35:f=5;continue
   else:d(x*s+a,y*s+b,(w-35)*s,(h-35)*s,c);f=1;x=v;continue
  if f==1:y=v;f=2;continue
  if f==2:w=v;f=3;continue
  if f==3:h=v;f=4;continue
  if f==5:
   q=v*3-105
   z=p[q:q+3]
   c=((o(z[0])*255-8910)//31,(o(z[1])*255-8894)//63,(o(z[2])*255-8910)//31)
   d(x*s+a,y*s+b,(w-35)*s,(h-35)*s,c);f=0;continue
  if f==0:x=v;f=1;continue
 if f==4:d(x*s+a,y*s+b,(w-35)*s,(h-35)*s,c)