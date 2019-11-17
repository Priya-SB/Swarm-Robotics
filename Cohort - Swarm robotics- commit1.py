
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
    m = (float)(y2-y1)/(x2-x1)
    t = math.atan(m)
    return(t)


# In[7]:


def new_inputf(new_input,matrix,c_follow,t):                                         #new matrix acc to following                                                              
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
            new_input[i].append(xn-cos)
            new_input[i].append(yn-sin)
        else:
            t=slope(xn,yn,xf,yf)
            cos=abs(math.cos(t))*step
            sin=abs(math.sin(t))*step
            #print("Theta= ",t)
            
            if (xn<xf and yn<yf):
                new_input[i].append(xn+cos)
                new_input[i].append(yn+sin)
            elif (xn>xf and yn>yf):
                new_input[i].append(xn-cos)
                new_input[i].append(yn-sin)
            elif (xn>xf and yn<yf):
                new_input[i].append(xn-cos)
                new_input[i].append(yn+sin)
            elif (xn<xf and yn>yf):
                new_input[i].append(xn+cos)
                new_input[i].append(yn-sin)

    return new_input


# In[13]:


def main_func(matrix,n,x,y):   
    global frange,l,b,c              
   
    for i in range(c):                                                            #storing for plot
        x[i].append(matrix[i][0])
        y[i].append(matrix[i][1])
        
    distance_sq=[]                                                               #distance and light intensity
    distance=[]
    for i in range(c):
        distance_sq.append(float(spheref(matrix[i][0],matrix[i][1])))
        distance.append(float(math.sqrt(distance_sq[i])))
    #print("Distance from light source: ", distance)
    
    light_int=[]
    for j in range(c):
        light_int.append(float(light(distance_sq[j])))
    print("Light intensity: ",light_int)
    
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
    
    m=t=0
    new_input=[[] for _ in range(c)]                                              #new coordinates
    new_inputf(new_input,matrix,c_follow,t)
    print("Next Learning attempt: ",new_input)
    
    print("Learning attempt no= ",n)
    n=n+1
    #if n>200:

    if all(val>4 for val in light_int):
        return(x,y)
    else:
        main_func(new_input,n,x,y)    


# In[14]:


c=int(input("Enter number of candidates:"))                                      #taking input 
l=float(input("Enter length of arena:"))
b=float(input("Enter breadth of arena:"))
step=float(((l*b)**(0.5))/100)
print("Step=",step)

matrix=[[] for _ in range(c)]                                                    #matrix to store values of x,y
for i in range(c):
    matrix[i].append(random.uniform(0,l))
    matrix[i].append(random.uniform(0,b))
    
print("Start positions: ",matrix)


# In[15]:


x=[[] for _ in range(c)]
y=[[] for _ in range(c)]
main_func(matrix,1,x,y)


# In[16]:


fig,ax=plt.subplots()
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
plt.show()


# In[17]:


fig,ax=plt.subplots()
for p in range(c):
    ax.plot(x[p],y[p],".",linewidth=2,)
    
ax.set_title("Arena")
ax.set_xlabel("X")
ax.set_ylabel("Y")

