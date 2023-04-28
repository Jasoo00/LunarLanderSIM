from base    import *
from lib     import *

t = 0
i = 0

lam = deg2rad(20)
nu  = deg2rad(45)

fig = plt.figure(figsize=(10,10))
viz = fig.add_subplot(1,1,1,projection="3d")


u = linspace(0, 2 * pi, 10)
v = linspace(0, pi, 10)
x = outer(2*cos(u), sin(v))
y = outer(2*sin(u), sin(v))
z = outer(2*ones(size(u)), cos(v))



while True:

    t += 3600*1
    i += 0.1

    r_b = array([0.5*cos(i), 0.5*sin(i), 0.5])

    roll = 0
    pitch = 0
    yaw = i

    C_i2e = C_I2E(t,lam)
    C_e2w = C_E2W(nu)
    C_w2b = C_W2B(roll,pitch,yaw)

    C_i2w = C_e2w@C_i2e
    C_i2b = C_w2b@C_e2w@C_i2e

    x_i = array([1,0,0])
    y_i = array([0,1,0])
    z_i = array([0,0,1])

    x_e = C_i2e.T @ x_i
    y_e = C_i2e.T @ y_i
    z_e = C_i2e.T @ z_i

    x_w = C_i2w.T @ x_i
    y_w = C_i2w.T @ y_i
    z_w = C_i2w.T @ z_i

    x_b = C_i2b.T @ x_i
    y_b = C_i2b.T @ y_i
    z_b = C_i2b.T @ z_i

    r_w = C_i2w.T @ array([0,0,2])
    r_b = C_i2w.T @ r_b + r_w
    
    viz.cla()

    viz.plot_surface(x, y, z, rstride=1, cstride=1, color="gray",alpha=0.3)

    viz.quiver(0,0,0,x_i[0],x_i[1],x_i[2],color="black",arrow_length_ratio=0.1)
    viz.quiver(0,0,0,y_i[0],y_i[1],y_i[2],color="black",arrow_length_ratio=0.1)
    viz.quiver(0,0,0,z_i[0],z_i[1],z_i[2],color="black",arrow_length_ratio=0.1)
    viz.text(x_i[0]+0.05,x_i[1],x_i[2],r"$x_I$",color="black")
    viz.text(y_i[0],y_i[1]+0.05,y_i[2],r"$y_I$",color="black")
    viz.text(z_i[0],z_i[1],z_i[2]+0.05,r"$z_I$",color="black")

    viz.quiver(0,0,0,x_e[0],x_e[1],x_e[2],color="red",arrow_length_ratio=0.1)
    viz.quiver(0,0,0,y_e[0],y_e[1],y_e[2],color="red",arrow_length_ratio=0.1)
    viz.quiver(0,0,0,z_e[0],z_e[1],z_e[2],color="red",arrow_length_ratio=0.1)
    viz.text(x_e[0]+0.05,x_e[1],x_e[2],r"$x_e$",color="red")
    viz.text(y_e[0],y_e[1]+0.05,y_e[2],r"$y_e$",color="red")
    viz.text(z_e[0],z_e[1],z_e[2]+0.05,r"$z_e$",color="red")

    viz.quiver(r_w[0],r_w[1],r_w[2],x_w[0],x_w[1],x_w[2],color="blue",arrow_length_ratio=0.1,length=0.5)
    viz.quiver(r_w[0],r_w[1],r_w[2],y_w[0],y_w[1],y_w[2],color="blue",arrow_length_ratio=0.1,length=0.5)
    viz.quiver(r_w[0],r_w[1],r_w[2],z_w[0],z_w[1],z_w[2],color="blue",arrow_length_ratio=0.1,length=0.5)
    viz.text(r_w[0]+x_w[0]/2+0.01,r_w[1]+x_w[1]/2,r_w[2]+x_w[2]/2,r"$x_w$",color="blue")
    viz.text(r_w[0]+y_w[0]/2,r_w[1]+y_w[1]/2+0.01,r_w[2]+y_w[2]/2,r"$y_w$",color="blue")
    viz.text(r_w[0]+z_w[0]/2,r_w[1]+z_w[1]/2,r_w[2]+z_w[2]/2+0.01,r"$z_w$",color="blue")

    viz.quiver(r_b[0],r_b[1],r_b[2],x_b[0],x_b[1],x_b[2],color="green",arrow_length_ratio=0.1,length=0.5)
    viz.quiver(r_b[0],r_b[1],r_b[2],y_b[0],y_b[1],y_b[2],color="green",arrow_length_ratio=0.1,length=0.5)
    viz.quiver(r_b[0],r_b[1],r_b[2],z_b[0],z_b[1],z_b[2],color="green",arrow_length_ratio=0.1,length=0.5)
    viz.text(r_b[0]+x_b[0]/2+0.01,r_b[1]+x_b[1]/2,r_b[2]+x_b[2]/2,r"$x_b$",color="green")
    viz.text(r_b[0]+y_b[0]/2,r_b[1]+y_b[1]/2+0.01,r_b[2]+y_b[2]/2,r"$y_b$",color="green")
    viz.text(r_b[0]+z_b[0]/2,r_b[1]+z_b[1]/2,r_b[2]+z_b[2]/2+0.01,r"$z_b$",color="green")

    viz.set_xlim(-3,3)
    viz.set_ylim(-3,3)
    viz.set_zlim(-3,3)
    viz.axis("off")

    plt.pause(0.1)

plt.show()