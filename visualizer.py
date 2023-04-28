from base       import *
from lib        import *

class Visualizer(Thread):

    def __init__(self, DB):

        self.DB     = DB

        super().__init__()
        self.daemon = True


    def run(self):

        fig = plt.figure(figsize=(10,10))
        viz = fig.add_subplot(1,1,1,projection="3d")

        traj = zeros(3)

        moon_u = linspace(0, 2 * pi, 10)
        moon_v = linspace(0, pi, 10)
        moon_x = outer(1.737e6*cos(moon_u), sin(moon_v))
        moon_y = outer(1.737e6*sin(moon_u), sin(moon_v))
        moon_z = outer(1.737e6*ones(size(moon_u)), cos(moon_v))
        
        while True:

            C_i2e = C_I2E(self.DB.t,self.DB.lon)
            C_e2w = C_E2W(self.DB.lat)
            C_i2b = C_W2B(self.DB.x[6],self.DB.x[7],self.DB.x[8])

            C_i2w = C_e2w@C_i2e

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

            r_w = C_i2w.T @ array([0,0,1.737e6])
            r_b = self.DB.x[:3]
            
            traj = vstack((traj,r_b))

            viz.cla()

            viz.plot_surface(moon_x, moon_y, moon_z, rstride=1, cstride=1, color="gray",alpha=0.3)

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

            viz.plot(traj[1:,0],traj[1:,1],traj[1:,2],'k-')

            viz.set_xlim(-3e6,3e6)
            viz.set_ylim(-3e6,3e6)
            viz.set_zlim(-3e6,3e6)
            viz.axis("off")

            plt.pause(0.01)
