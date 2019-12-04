
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl                                                          #packages imported
import matplotlib.pyplot as plt
import random
import math


# In[2]:


def spheref(x,y):                                                                 #sphere function for distance
    d = float(x**2+y**2)
    return d


# In[3]:


def light(d):                                                                     #light intensity function
    l=1/d
    return l


# In[4]:


def roulette_wheel(total):                                                        #roulette wheel function
    global c
    leader=-1
    r = random.uniform(0,1)
    for n in range(c):
        if r<total[n]:
            leader=n
            break
    return leader 


# In[5]:


def probability_func(values,prob):                                                #calculating probability (max)
    global c
    for j in range(c):
        prob.append(values[j]/sum(values))
    return prob    


# In[6]:


def slope(x1, y1, x2, y2):                                                        #slope function
    if(x1==x2):
        t=math.pi
    else:    
        m = (float)(y2-y1)/(x2-x1)
        t = math.atan(m)
    return(t)


# In[7]:


def checkarea(rect,xc,yc):                                                        #checking position of point wrt obstacle
    flag=True
    for j in rect:
        if (xc>=j[0]) and (xc<=(j[0]+j[2])) and (yc>=j[1]) and (yc<=(j[1]+j[3])):
            flag=False
            print("Hey Obstacle!")            
            break
    return flag,j
        


# In[8]:


def generate_obs(rectangle):                                                      #creating obstacles
    global l,b        
    rectangle.append([-l,-b,2*l,b])
    rectangle.append([-l,-b,l,2*b])


# In[9]:


def new_path(newx,newy,rect):                                                     #candidate on obstacle edge
    d1=rect[1]+rect[3]-newy
    d2=rect[0]+rect[2]-newx
    d3=newy-rect[1]
    d4=newx-rect[0]
    m=min(d1,d2,d3,d4)
    if(m==d1):
        (px,py)=(newx,newy+d1)
    elif(m==d2):
        (px,py)=(newx+d2,newy)
    elif(m==d3):
        (px,py)=(newx,newy-d3)
    elif(m==d4):
        (px,py)=(newx-d4,newy)
    
    print("edge pt=",px,py)
    return px,py


# In[10]:


def new_inputf(new_input,matrix,c_follow,rect):                                    #new matrix acc to following 
    m=t=0
    global c,step
    for i in range(c):
        xn=matrix[i][0]
        yn=matrix[i][1]
        xf=matrix[c_follow[i]][0]
        yf=matrix[c_follow[i]][1]
        
        if (c_follow[i]==i):
            t=random.uniform(-math.pi,math.pi)
            cos=abs(math.cos(t))*step
            sin=abs(math.sin(t))*step
            ai=xn-cos
            bi=yn-sin
            flag,j=checkarea(rect,ai,bi)
            if(flag):
                new_input[i].append(ai)
                new_input[i].append(bi)
            else:
                px,py=new_path(ai,bi,j)
                new_input[i].append(px)
                new_input[i].append(py)    
        else:
            t=slope(xn,yn,xf,yf)
            cos=abs(math.cos(t))*step
            sin=abs(math.sin(t))*step
            ci=xn+cos
            di=yn+sin
            ei=xn-cos
            fi=yn-sin
            if (xn<=xf and yn<=yf):
                flag,j=checkarea(rect,ci,di)
                if(flag):
                    new_input[i].append(ci)
                    new_input[i].append(di)
                else:
                    px,py=new_path(ci,di,j)
                    new_input[i].append(px)
                    new_input[i].append(py)    
                    
            elif (xn>=xf and yn>=yf):
                flag,j=checkarea(rect,ei,fi)
                if(flag):
                    new_input[i].append(ei)
                    new_input[i].append(fi)
                else:
                    px,py=new_path(ei,fi,j)
                    new_input[i].append(px)
                    new_input[i].append(py)

            elif (xn>=xf and yn<=yf):
                flag,j=checkarea(rect,ei,di)
                if(flag):
                    new_input[i].append(ei)
                    new_input[i].append(di)
                else: 
                    px,py=new_path(ei,di,j)
                    new_input[i].append(px)
                    new_input[i].append(py)
               
            elif (xn<=xf and yn>=yf):
                flag,j=checkarea(rect,ci,fi)
                if(flag):
                    new_input[i].append(ci)
                    new_input[i].append(fi)
                else: 
                    px,py=new_path(ci,fi,j)
                    new_input[i].append(px)
                    new_input[i].append(py)

    return new_input


# In[11]:


def main_func(matrix,rect,n):  
    global frange,l,b,c,step,x,y              
   
    for i in range(c):                                                            #storing for plot
        x[i].append(matrix[i][0])
        y[i].append(matrix[i][1])
        
    distance_sq=[]                                                                #distance and light intensity
    distance=[]
    for i in range(c):
        distance_sq.append(float(spheref(matrix[i][0],matrix[i][1])))
        distance.append(float(math.sqrt(distance_sq[i])))
    print("Distance from light source: ", distance)
    
    light_int=[]
    for j in range(c):
        light_int.append(float(light(distance_sq[j])))
    #print("Light intensity: ",light_int)
    
    prob=[]
    probability_func(light_int,prob)
    #print("Probabilities: ",prob)
    
    total=[]                                                                      #creating the roulette scale
    for i in range(c):
        total.append(sum(prob[0:i+1]))
    #print("Roulette Wheel: ",total)
    
    c_follow=[]                                                                   #determining who follows whom
    for i in range(c):
        c_follow.append(int(roulette_wheel(total)))
    #print("Following: ",c_follow)
    
    new_input=[[] for _ in range(c)]                                              #new coordinates
    new_inputf(new_input,matrix,c_follow,rectangle)
    print("Next Learning attempt: ",new_input)
    
    print("Learning attempt no= ",n)
    n=n+1
    if n==100:
        step=0.5*step
    if all(val<0.1 for val in distance):
        return(x,y)
    else:
        main_func(new_input,rect,n)    


# In[12]:


c=int(input("Enter number of candidates:"))                                      #taking input 
l=float(input("Enter length of arena:"))
b=float(input("Enter breadth of arena:"))
step=float(math.sqrt(l*b)/100)
#step=float(0.1)
print("Step=",step)

rectangle=[]
generate_obs(rectangle)                                                           #creating obstacles
print("Obstacle coordinates:",rectangle)

matrix=[[] for _ in range(c)]                                                     #matrix to store values of x,y
cnt=0
while cnt<c:
    xc=random.uniform(0,l)
    yc=random.uniform(0,b)
    flag,j=checkarea(rectangle,xc,yc)
    if (flag):
        matrix[cnt].append(xc)
        matrix[cnt].append(yc)
        cnt=cnt+1
    
print("Start positions: ",matrix)


# In[13]:


x=[[] for _ in range(c)]
y=[[] for _ in range(c)]
main_func(matrix,rectangle,1)


# In[14]:


fig,ax=plt.subplots(figsize=(8, 8))
for p in range(c):
    ax.plot(x[p],y[p],".",linewidth=2,)
    
ax.set_title("Arena")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_xlim((0,l))
ax.set_ylim((0,b))
x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
ax.set_aspect(abs(x1-x0)/abs(y1-y0))
ax.grid(b=True, which='major', color='k', linestyle='--')

for q in rectangle:
    patch=plt.Rectangle((q[0],q[1]),q[2],q[3],color='lightpink')
    ax.add_patch(patch)

plt.show()


# #### 
