from base       import *
from lib        import *


class Visualizer:

    def __init__(self, DB):

        self.DB     = DB

        ### init figures ###
        fig = plt.figure(figsize=(15,15))
        self.viz = fig.add_subplot(1,2,1,projection="3d")
        self.viz2 = fig.add_subplot(1,2,2,projection="3d")
        
        self.cubes  = self.generate_cubes()

        moon_u = linspace(0, 2 * pi, 20)
        moon_v = linspace(0, pi, 10)
        self.moon_x = outer(1.737e6*cos(moon_u), sin(moon_v))
        self.moon_y = outer(1.737e6*sin(moon_u), sin(moon_v))
        self.moon_z = outer(1.737e6*ones(size(moon_u)), cos(moon_v))

        self.traj = zeros(3)


    def generate_cubes(self):

        cubelines = zeros((3,17*len(self.DB.components)))

        for idx,component in enumerate(self.DB.components):

            h, w = component.dim[0]/2,component.dim[1]/2

            center = component.p_cg
    
            cubelines[:,idx*17 + 0] = center + array([-w,-w,-h])
            cubelines[:,idx*17 + 1] = center + array([-w, w,-h])
            cubelines[:,idx*17 + 2] = center + array([ w, w,-h])
            cubelines[:,idx*17 + 3] = center + array([ w,-w,-h])
            cubelines[:,idx*17 + 4] = center + array([-w,-w,-h])

            cubelines[:,idx*17 + 5] = center + array([-w,-w, h])
            cubelines[:,idx*17 + 6] = center + array([-w, w, h])
            cubelines[:,idx*17 + 7] = center + array([ w, w, h])
            cubelines[:,idx*17 + 8] = center + array([ w,-w, h])
            cubelines[:,idx*17 + 9] = center + array([-w,-w, h])
            cubelines[:,idx*17 + 10] = center + array([-w, w,-h])
            cubelines[:,idx*17 + 11] = center + array([-w, w, h])
            cubelines[:,idx*17 + 12] = center + array([ w, w,-h])
            cubelines[:,idx*17 + 13] = center + array([ w, w, h])
            cubelines[:,idx*17 + 14] = center + array([ w,-w,-h])
            cubelines[:,idx*17 + 15] = center + array([ w,-w, h])
            cubelines[:,idx*17 + 16] = center + array([-w,-w,-h])

        return cubelines


    def run(self):

        ### state vector ###
        x       = self.DB.x        

        ### DCM matrices ###
        C_i2e = C_I2E(self.DB.t,self.DB.lon)
        C_e2w = C_E2W(self.DB.lat)
        C_i2b = C_W2B(x[6],x[7],x[8])
        C_i2w = C_e2w@C_i2e

        ### basis vectors ###
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

        ### ENU center location & Body center location ###
        r_w = C_i2w.T @ array([0,0,1.737e6])
        r_b = x[:3]

        self.traj = vstack((self.traj,r_b))

        self.viz.cla()

        self.viz.plot_surface(self.moon_x, self.moon_y, self.moon_z, rstride=1, cstride=1, color="gray",alpha=0.3)

        self.viz.quiver( 0,0,0,  x_i[0],x_i[1],x_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
        self.viz.quiver( 0,0,0,  y_i[0],y_i[1],y_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
        self.viz.quiver( 0,0,0,  z_i[0],z_i[1],z_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
        self.viz.text(2e6*x_i[0]+0.05,2e6*x_i[1],2e6*x_i[2],r"$x_I$",color="black")
        self.viz.text(2e6*y_i[0],2e6*y_i[1]+0.05,2e6*y_i[2],r"$y_I$",color="black")
        self.viz.text(2e6*z_i[0],2e6*z_i[1],2e6*z_i[2]+0.05,r"$z_I$",color="black")

        self.viz.quiver( 0,0,0,  x_e[0],x_e[1],x_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.viz.quiver( 0,0,0,  y_e[0],y_e[1],y_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.viz.quiver( 0,0,0,  z_e[0],z_e[1],z_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.viz.text(2e6*x_e[0]+0.05,2e6*x_e[1],2e6*x_e[2],r"$x_e$",color="red")
        self.viz.text(2e6*y_e[0],2e6*y_e[1]+0.05,2e6*y_e[2],r"$y_e$",color="red")
        self.viz.text(2e6*z_e[0],2e6*z_e[1],2e6*z_e[2]+0.05,r"$z_e$",color="red")

        self.viz.quiver( r_w[0],r_w[1],r_w[2],   x_w[0],x_w[1],x_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.viz.quiver( r_w[0],r_w[1],r_w[2],   y_w[0],y_w[1],y_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.viz.quiver( r_w[0],r_w[1],r_w[2],   z_w[0],z_w[1],z_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.viz.text(r_w[0]+5e5*x_w[0]/2+0.01,r_w[1]+5e5*x_w[1]/2,r_w[2]+5e5*x_w[2]/2,r"$x_w$",color="blue")
        self.viz.text(r_w[0]+5e5*y_w[0]/2,r_w[1]+5e5*y_w[1]/2+0.01,r_w[2]+5e5*y_w[2]/2,r"$y_w$",color="blue")
        self.viz.text(r_w[0]+5e5*z_w[0]/2,r_w[1]+5e5*z_w[1]/2,r_w[2]+5e5*z_w[2]/2+0.01,r"$z_w$",color="blue")

        self.viz.quiver( r_b[0],r_b[1],r_b[2],   x_b[0],x_b[1],x_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.viz.quiver( r_b[0],r_b[1],r_b[2],   y_b[0],y_b[1],y_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.viz.quiver( r_b[0],r_b[1],r_b[2],   z_b[0],z_b[1],z_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.viz.text(r_b[0]+5e5*x_b[0]/2+0.01,r_b[1]+5e5*x_b[1]/2,r_b[2]+5e5*x_b[2]/2,r"$x_b$",color="green")
        self.viz.text(r_b[0]+5e5*y_b[0]/2,r_b[1]+5e5*y_b[1]/2+0.01,r_b[2]+5e5*y_b[2]/2,r"$y_b$",color="green")
        self.viz.text(r_b[0]+5e5*z_b[0]/2,r_b[1]+5e5*z_b[1]/2,r_b[2]+5e5*z_b[2]/2+0.01,r"$z_b$",color="green")

        self.viz.plot(self.traj[1:,0],self.traj[1:,1],self.traj[1:,2],'k-')

        self.viz.set_xlim(-3.5e6,3.5e6)
        self.viz.set_ylim(-3.5e6,3.5e6)
        self.viz.set_zlim(-3.5e6,3.5e6)
        self.viz.axis("off")


        ### Lunar Module Detailed View ###

        self.viz2.cla()

        cubes   = C_i2b.T @ self.cubes

        for idx, component in enumerate(self.DB.components):

            uvec = C_i2b.T @ (-component.uvec)
            p_cg = C_i2b.T @ component.p_cg
            p_c = C_i2b.T @ component.p_c

            self.viz2.plot(cubes[0,idx*17:idx*17+17],cubes[1,idx*17:idx*17+17],cubes[2,idx*17:idx*17+17],"k-",alpha=0.1)                
            self.viz2.quiver(p_cg[0],p_cg[1],p_cg[2],uvec[0],uvec[1],uvec[2],color="red",arrow_length_ratio=0.2,length=10000,linewidth = 2)
        

        self.viz2.quiver(0,0,0,x_b[0],x_b[1],x_b[2],color="red",arrow_length_ratio=0.1,length=3)
        self.viz2.quiver(0,0,0,y_b[0],y_b[1],y_b[2],color="green",arrow_length_ratio=0.1,length=3)
        self.viz2.quiver(0,0,0,z_b[0],z_b[1],z_b[2],color="blue",arrow_length_ratio=0.1,length=3)
        self.viz2.text(3.2*x_b[0],3.2*x_b[1],3.2*x_b[2],r"$x_b$",color="red")
        self.viz2.text(3.2*y_b[0],3.2*y_b[1],3.2*y_b[2],r"$y_b$",color="green")
        self.viz2.text(3.2*z_b[0],3.2*z_b[1],3.2*z_b[2],r"$z_b$",color="blue")

        self.viz2.set_xlim(-5,5)
        self.viz2.set_ylim(-5,5)
        self.viz2.set_zlim(-5,5)
        self.viz2.axis("off")





