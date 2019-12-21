
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib as mpl                                                      #packages imported
import matplotlib.pyplot as plt
import random
import math


# In[2]:


def spheref(x,y):                                                             #sphere function for distance
    d = float(x**2+y**2)
    return d


# In[3]:


def light(d):                                                                 #light intensity function
    if (d==0):
        l=999
    else:    
        l=1/d
    return l


# In[4]:


def roulette_wheel(total):                                                    #roulette wheel function
    global c
    leader=-1
    r = random.uniform(0,1)
    for n in range(c):
        if r<total[n]:
            leader=n
            break
    return leader 


# In[5]:


def probability_func(values,prob):                                           #probability (max) func
    global c
    for j in range(c):
        prob.append(values[j]/sum(values))
    return prob    


# In[6]:


def slope(x1, y1, x2, y2):                                                   #slope function
    if(x1==x2):
        t=math.pi
    else:    
        m = (float)(y2-y1)/(x2-x1)
        t = math.atan(m)
    return(t)


# In[7]:


def generate_obs():                                                          #creating obstacles
    global l,b,rectangle
    
    rectangle.append([-l,-b,2*l,b])
    rectangle.append([-l,-b,l,2*b])
    for i in range(0,10):
        xr=random.uniform(0,l)
        yr=random.uniform(0,b)
        wr=random.uniform(0.5,1)
        hr=random.uniform(0.5,1)
        rectangle.append([xr,yr,wr,hr])
        


# In[8]:


def checkarea(xc,yc):                                                        #checking position of point wrt obstacle
    global rectangle
    flag=True
    for j in rectangle:
        if (xc>j[0]) and (xc<(j[0]+j[2])) and (yc>j[1]) and (yc<(j[1]+j[3])):
            flag=False
            print("Hey Obstacle!")            
            break
    return flag,j                                                            #false if obstacle hit, j=rectangle sublist
        


# In[9]:


def new_path(newx,newy,j):                                                   #put candidate on obstacle edge
    d1=j[1]+j[3]-newy
    d2=j[0]+j[2]-newx
    d3=newy-j[1]
    d4=newx-j[0]
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


def position(new_input,n,m,i):                                              #loop & multi check
    global rectangle
    flag,j=checkarea(n,m)
    while(flag==False and (math.sqrt(spheref(n,m)))>0.1):
        k,l=new_path(n,m,j)
        flag,j=checkarea(k,l)
        (n,m)=(k,l)
    new_input[i].append(n)
    new_input[i].append(m)
    return(new_input)


# In[11]:


def new_inputf(new_input,matrix,c_follow):                                  #new matrix acc to following list
    m=t=0
    global c,step
    for i in range(c):
        xn=matrix[i][0]
        yn=matrix[i][1]
        xf=matrix[c_follow[i]][0]
        yf=matrix[c_follow[i]][1]
        
        if (c_follow[i]==i):                                                #if candidate follows itself                                              
            t=random.uniform(0,2*math.pi)
            cos=abs(math.cos(t))*step
            sin=abs(math.sin(t))*step
            a=xn-cos
            b=yn-sin
            position(new_input,a,b,i)
                     
        else:                                                               #following other candidate
            t=slope(xn,yn,xf,yf)
            cos=abs(math.cos(t))*step
            sin=abs(math.sin(t))*step
            ci=xn+cos
            di=yn+sin
            ei=xn-cos
            fi=yn-sin
            if (xn<=xf and yn<=yf):
                position(new_input,ci,di,i)
                
            elif (xn>=xf and yn>=yf):
                position(new_input,ei,fi,i)
                
            elif (xn>=xf and yn<=yf):
                position(new_input,ei,di,i)
               
            elif (xn<=xf and yn>=yf):
                position(new_input,ci,fi,i)

    return new_input


# In[12]:


def main_func(matrix,n):  
    global frange,l,b,c,step,x,y,rectangle              
   
    for i in range(c):                                                          #storing values for plotting
        x[i].append(matrix[i][0])
        y[i].append(matrix[i][1])
        
    distance_sq=[]                                                              #calculating distance from light source
    distance=[]
    for i in range(c):
        distance_sq.append(float(spheref(matrix[i][0],matrix[i][1])))
        distance.append(float(math.sqrt(distance_sq[i])))
    #print("Distance from light source: ", distance)
    
    light_int=[]
    for j in range(c):
        light_int.append(float(light(distance_sq[j])))                          #calculating light intensity
    #print("Light intensity: ",light_int)
    
    prob=[]
    probability_func(light_int,prob)                                            #calculating probability
    #print("Probabilities: ",prob)
    
    total=[]                                                                    #creating the roulette scale
    for i in range(c):
        total.append(sum(prob[0:i+1]))
    #print("Roulette Wheel: ",total)
    
    c_follow=[]                                                                 #determining who follows whom
    for i in range(c):
        c_follow.append(int(roulette_wheel(total)))
    print("Following: ",c_follow)
    
    new_input=[[] for _ in range(c)]                                            #new positions of candidates
    new_inputf(new_input,matrix,c_follow)
    #print("Next Learning attempt: ",new_input)
    
    print("Learning attempt no= ",n)
    n=n+1
    if n==100:
        step=0.5*step                                                           #halving step after 100th iteration
    if all(val<0.1 for val in distance):
        return(x,y)
    else:
        main_func(new_input,n)                                                  #recursive function


# In[13]:


c=int(input("Enter number of candidates:"))                                     #taking input 
l=float(input("Enter length of arena:"))
b=float(input("Enter breadth of arena:"))

step=float(math.sqrt(l**2+b**2)/100)                                            #step=diagonal/100

print("Step=",step)

rectangle=[]
generate_obs()                                                                  #creating obstacles
print("Obstacle coordinates:",rectangle)

matrix=[[] for _ in range(c)]                                                   #matrix to store values of x,y
cnt=0

while cnt<c:                                                                    #random initial positions of candidates
    xc=random.uniform(0,l)
    yc=random.uniform(0,b)
    flag,j=checkarea(xc,yc)
    if (flag):
        matrix[cnt].append(xc)
        matrix[cnt].append(yc)
        cnt=cnt+1
    
print("Start positions: ",matrix)


# In[14]:


x=[[] for _ in range(c)]
y=[[] for _ in range(c)]
main_func(matrix,1)


# In[15]:


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


# In[16]:


fig,ax=plt.subplots(figsize=(8, 8))
for p in range(c):
    ax.plot(x[p],y[p],".",linewidth=2,)
for q in rectangle:
    pat=plt.Rectangle((q[0],q[1]),q[2],q[3],color='lightpink')
    ax.add_patch(pat)    
ax.set_title("Arena")
ax.set_xlabel("X")
ax.set_ylabel("Y")
plt.show()

