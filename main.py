import cv2 as cv
import numpy as np

w, h = 600, 600
cs = 200
e = 0
px = 1
po = 2
bw, bh = 100, 50
rbx, rby = 10, 10
ebx, eby = w - bw - 10, 10

bd = [[e, e, e],
      [e, e, e],
      [e, e, e]]
cp = px
go = False
wn = None
run = True

bg = cv.resize(cv.imread("background.jpg"), (w, h))
x_img = cv.resize(cv.imread("x_img.png", cv.IMREAD_UNCHANGED), (100, 100))
o_img = cv.resize(cv.imread("o_img.png", cv.IMREAD_UNCHANGED), (100, 100))

def overlay_img(bg, fg, x, y):
    h_fg, w_fg = fg.shape[:2]
    for c in range(3):
        bg[y:y+h_fg, x:x+w_fg, c] = fg[:,:,c] * (fg[:,:,3]/255.0) + bg[y:y+h_fg, x:x+w_fg, c] * (1.0 - fg[:,:,3]/255.0)

def dr(img):
    img[:] = bg.copy()
    for i in range(1,3):
        cv.line(img,(0,cs*i),(w,cs*i),(0,0,0),3)
        cv.line(img,(cs*i,0),(cs*i,h),(0,0,0),3)
    for r in range(3):
        for c in range(3):
            x = c * cs + cs//2 - 50
            y = r * cs + cs//2 - 50
            if bd[r][c]==px:
                overlay_img(img, x_img, x, y)
            elif bd[r][c]==po:
                overlay_img(img, o_img, x, y)
    cv.rectangle(img,(rbx,rby),(rbx+bw,rby+bh),(200,200,200),-1)
    cv.rectangle(img,(ebx,eby),(ebx+bw,eby+bh),(200,200,200),-1)
    cv.putText(img,"Restart",(rbx+5,rby+30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)
    cv.putText(img,"Exit",(ebx+15,eby+30),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,0,0),2)
    if go:
        txt = "Draw!" if wn is None else f"Win {'X' if wn==px else 'O'}!"
        cv.putText(img,txt,(w//2-100,h//2),cv.FONT_HERSHEY_SIMPLEX,1.5,(0,0,0),3)

def cbc(x,y,bx,by,ww,hh):
    return (bx<=x<=bx+ww) and (by<=y<=by+hh)

def rg():
    global bd,cp,go,wn
    bd=[[e,e,e],[e,e,e],[e,e,e]]
    cp=px
    go=False
    wn=None

def cw(p):
    for rr in range(3):
        if bd[rr][0]==bd[rr][1]==bd[rr][2]==p: return True
    for cc in range(3):
        if bd[0][cc]==bd[1][cc]==bd[2][cc]==p: return True
    if bd[0][0]==bd[1][1]==bd[2][2]==p: return True
    if bd[0][2]==bd[1][1]==bd[2][0]==p: return True
    return False

def cd():
    for rr in bd:
        if e in rr: return False
    return True

def mouse_evt(event,x,y,flags,param):
    global cp,go,wn,run
    if event==cv.EVENT_LBUTTONDOWN:
        if cbc(x,y,rbx,rby,bw,bh):
            rg()
            return
        if cbc(x,y,ebx,eby,bw,bh):
            run=False
            return
        if go:
            return
        c=int(x//cs)
        r=int(y//cs)
        if 0<=r<3 and 0<=c<3:
            if bd[r][c]==e:
                bd[r][c]=cp
                if cw(cp):
                    go=True
                    wn=cp
                elif cd():
                    go=True
                    wn=None
                else:
                    cp=po if cp==px else px

def main():
    cv.namedWindow("XO")
    cv.setMouseCallback("XO",mouse_evt)
    img = np.ones((h,w,3),dtype=np.uint8)*255
    while True:
        dr(img)
        cv.imshow("XO",img)
        if cv.waitKey(10)==27 or not run:
            break
    cv.destroyAllWindows()

if __name__=="__main__":
    main()
