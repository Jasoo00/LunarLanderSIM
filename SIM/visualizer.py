from base       import *
from lib        import *


class Visualizer:

    def __init__(self, DB):


        self.DB     = DB


        ### init figures ###
        self.fig            = plt.figure(facecolor="black",figsize=(15,15))
        self.viz_world      = self.fig.add_subplot(1,2,1,projection="3d")
        self.viz_world.patch.set_facecolor('black')
        self.viz_world.set_title('Overall View',c="white",style="italic")
        self.viz_body       = self.fig.add_subplot(1,2,2,projection="3d")
        self.viz_body.patch.set_facecolor('black')
        self.viz_body.set_title('Lander Detailed View',c="white",style="italic")


        ### plot size and options ###
        self.viz_world.set_xlim(-3.5e6,3.5e6)
        self.viz_world.set_ylim(-3.5e6,3.5e6)
        self.viz_world.set_zlim(-3.5e6,3.5e6)
        self.viz_world.axis("off")

        self.viz_body.set_xlim(-5,5)
        self.viz_body.set_ylim(-5,5)
        self.viz_body.set_zlim(-5,5)
        self.viz_body.axis("off")


        ### init cublines for lunar lander visualization ###
        self.cubes          = self.generate_cubes()


        ### moon surface visualization ###
        moon_u              = linspace(0, 2 * pi, 20)
        moon_v              = linspace(0,     pi, 10)
        self.moon_x         = outer(R_m*cos(moon_u),        sin(moon_v))
        self.moon_y         = outer(R_m*sin(moon_u),        sin(moon_v))
        self.moon_z         = outer(R_m*ones(size(moon_u)), cos(moon_v))

        self.viz_world.plot_surface(self.moon_x, self.moon_y, self.moon_z, rstride=1, cstride=1, color="white", alpha=0.3)


        ### init trajectory ###
        traj_max_length     = int(30)
        self.traj           = empty((3,traj_max_length))


        ### initialize plots ###
        
        """
        LCI coordinate system
        """
        ### LCI basis vectors ###
        self.x_i            = array([1,0,0])
        self.y_i            = array([0,1,0])
        self.z_i            = array([0,0,1])

        self.LCI_x          = self.viz_world.quiver(0,0,0, self.x_i[0],self.x_i[1],self.x_i[2], color="gray",arrow_length_ratio=0.1,length=2.5e6)
        self.LCI_y          = self.viz_world.quiver(0,0,0, self.y_i[0],self.y_i[1],self.y_i[2], color="gray",arrow_length_ratio=0.1,length=2.5e6)
        self.LCI_z          = self.viz_world.quiver(0,0,0, self.z_i[0],self.z_i[1],self.z_i[2], color="gray",arrow_length_ratio=0.1,length=2.5e6)
        self.LCI_xt         = self.viz_world.text(2.5e6*self.x_i[0]+0.05,2.5e6*self.x_i[1],2.5e6*self.x_i[2],r"$x_I$",color="gray")
        self.LCI_yt         = self.viz_world.text(2.5e6*self.y_i[0],2.5e6*self.y_i[1]+0.05,2.5e6*self.y_i[2],r"$y_I$",color="gray")
        self.LCI_zt         = self.viz_world.text(2.5e6*self.z_i[0],2.5e6*self.z_i[1],2.5e6*self.z_i[2]+0.05,r"$z_I$",color="gray")


        """
        LCMF coordinate system
        """
        self.LCMF_x         = self.viz_world.quiver(0,0,0,0,0,0)
        self.LCMF_y         = self.viz_world.quiver(0,0,0,0,0,0)
        self.LCMF_z         = self.viz_world.quiver(0,0,0,0,0,0)
        self.LCMF_xt        = self.viz_world.text(0,0,0,r"$x_e$")
        self.LCMF_yt        = self.viz_world.text(0,0,0,r"$y_e$")
        self.LCMF_zt        = self.viz_world.text(0,0,0,r"$z_e$")


        """
        ENU coordinate system
        """
        self.ENU_x          = self.viz_world.quiver(0,0,0,0,0,0)
        self.ENU_y          = self.viz_world.quiver(0,0,0,0,0,0)
        self.ENU_z          = self.viz_world.quiver(0,0,0,0,0,0)
        self.ENU_xt         = self.viz_world.text(0,0,0,r"$x_w$")
        self.ENU_yt         = self.viz_world.text(0,0,0,r"$y_w$")
        self.ENU_zt         = self.viz_world.text(0,0,0,r"$z_w$")


        """
        Body coordinate system
        """
        self.Body_x         = self.viz_world.quiver(0,0,0,0,0,0)
        self.Body_y         = self.viz_world.quiver(0,0,0,0,0,0)
        self.Body_z         = self.viz_world.quiver(0,0,0,0,0,0)
        self.Body_xt        = self.viz_world.text(0,0,0,r"$x_b$")
        self.Body_yt        = self.viz_world.text(0,0,0,r"$y_b$")
        self.Body_zt        = self.viz_world.text(0,0,0,r"$z_b$")


        """
        trajectory
        """
        self.trajplot,      = self.viz_world.plot([0],[0],[0])


        """
        Body coordinate system - for subplot 2 
        """
        self.Body2_x        = self.viz_body.quiver(0,0,0,0,0,0)
        self.Body2_y        = self.viz_body.quiver(0,0,0,0,0,0)
        self.Body2_z        = self.viz_body.quiver(0,0,0,0,0,0)
        self.Body2_xt       = self.viz_body.text(0,0,0,r"$x_b$")
        self.Body2_yt       = self.viz_body.text(0,0,0,r"$y_b$")
        self.Body2_zt       = self.viz_body.text(0,0,0,r"$z_b$")
        

        """
        body cubelines
        """
        self.cubelines,     = self.viz_body.plot([0],[0],[0])


        """
        thrust vectors
        """
        self.thrusts        = self.viz_body.quiver(0,0,0,0,0,0)
        
        """
        Fuel percentages
        """
        self.fuel           = self.viz_body.text(0,0,0,r"$0$")


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


    def update(self,frame):


        ### state vector ###
        x                   = self.DB.x        

        ### DCM matrices ###
        C_i2e               = C_I2E(self.DB.t,self.DB.lon)
        C_e2w               = C_E2W(self.DB.lat)
        C_i2b               = C_W2B(x[6],x[7],x[8])
        C_i2w               = C_e2w@C_i2e

        ### LCMF basis vectors ###
        x_e                 = C_i2e.T @ self.x_i
        y_e                 = C_i2e.T @ self.y_i
        z_e                 = C_i2e.T @ self.z_i

        ### ENU basis vectors ###
        x_w                 = C_i2w.T @ self.x_i
        y_w                 = C_i2w.T @ self.y_i
        z_w                 = C_i2w.T @ self.z_i

        ### Body basis vectors ###
        x_b                 = C_i2b.T @ self.x_i
        y_b                 = C_i2b.T @ self.y_i
        z_b                 = C_i2b.T @ self.z_i

        ### update cubes pose ###
        cubes               = C_i2b.T @ self.cubes

        ### ENU center location & Body center location ###
        r_w                 = C_i2w.T @ array([0,0,R_m])
        r_b                 = x[:3]

        ### components ###
        components          = self.DB.components
        
        ### update trajectory ###
        self.traj           = concatenate((self.traj,reshape(r_b,(3,1))),axis=1)


        """
        LCMF coordinate system
        """
        self.LCMF_x.remove()
        self.LCMF_y.remove()
        self.LCMF_z.remove()
        self.LCMF_xt.remove()
        self.LCMF_yt.remove()
        self.LCMF_zt.remove()

        self.LCMF_x         = self.viz_world.quiver( 0,0,0,  x_e[0],x_e[1],x_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.LCMF_y         = self.viz_world.quiver( 0,0,0,  y_e[0],y_e[1],y_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.LCMF_z         = self.viz_world.quiver( 0,0,0,  z_e[0],z_e[1],z_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
        self.LCMF_xt        = self.viz_world.text(2e6*x_e[0]+0.05,2e6*x_e[1],2e6*x_e[2],r"$x_e$",color="red")
        self.LCMF_yt        = self.viz_world.text(2e6*y_e[0],2e6*y_e[1]+0.05,2e6*y_e[2],r"$y_e$",color="red")
        self.LCMF_zt        = self.viz_world.text(2e6*z_e[0],2e6*z_e[1],2e6*z_e[2]+0.05,r"$z_e$",color="red")


        """
        ENU coordinate system
        """
        self.ENU_x.remove()
        self.ENU_y.remove()
        self.ENU_z.remove()
        self.ENU_xt.remove()
        self.ENU_yt.remove()
        self.ENU_zt.remove()

        self.ENU_x          = self.viz_world.quiver( r_w[0],r_w[1],r_w[2],   x_w[0],x_w[1],x_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.ENU_y          = self.viz_world.quiver( r_w[0],r_w[1],r_w[2],   y_w[0],y_w[1],y_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.ENU_z          = self.viz_world.quiver( r_w[0],r_w[1],r_w[2],   z_w[0],z_w[1],z_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
        self.ENU_xt         = self.viz_world.text(r_w[0]+5e5*x_w[0]/2+0.01,r_w[1]+5e5*x_w[1]/2,r_w[2]+5e5*x_w[2]/2,r"$x_w$",color="blue")
        self.ENU_yt         = self.viz_world.text(r_w[0]+5e5*y_w[0]/2,r_w[1]+5e5*y_w[1]/2+0.01,r_w[2]+5e5*y_w[2]/2,r"$y_w$",color="blue")
        self.ENU_zt         = self.viz_world.text(r_w[0]+5e5*z_w[0]/2,r_w[1]+5e5*z_w[1]/2,r_w[2]+5e5*z_w[2]/2+0.01,r"$z_w$",color="blue")


        """
        Body coordinate system
        """
        self.Body_x.remove()
        self.Body_y.remove()
        self.Body_z.remove()
        self.Body_xt.remove()
        self.Body_yt.remove()
        self.Body_zt.remove()

        self.Body_x         = self.viz_world.quiver( r_b[0],r_b[1],r_b[2],   x_b[0],x_b[1],x_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.Body_y         = self.viz_world.quiver( r_b[0],r_b[1],r_b[2],   y_b[0],y_b[1],y_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.Body_z         = self.viz_world.quiver( r_b[0],r_b[1],r_b[2],   z_b[0],z_b[1],z_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
        self.Body_xt        = self.viz_world.text(r_b[0]+5e5*x_b[0]/2+0.01,r_b[1]+5e5*x_b[1]/2,r_b[2]+5e5*x_b[2]/2,r"$x_b$",color="green")
        self.Body_yt        = self.viz_world.text(r_b[0]+5e5*y_b[0]/2,r_b[1]+5e5*y_b[1]/2+0.01,r_b[2]+5e5*y_b[2]/2,r"$y_b$",color="green")
        self.Body_zt        = self.viz_world.text(r_b[0]+5e5*z_b[0]/2,r_b[1]+5e5*z_b[1]/2,r_b[2]+5e5*z_b[2]/2+0.01,r"$z_b$",color="green")


        """
        trajectory
        """
        self.trajplot.remove()

        self.trajplot,      = self.viz_world.plot(self.traj[0,-1-frame:], self.traj[1,-1-frame:], self.traj[2,-1-frame:],"r-",alpha=0.5)



        ### Lunar Module Detailed View ###

        """
        lunar module components
        """

        self.viz_body.lines.clear()

        self.cubelines,     = self.viz_body.plot(cubes[0],cubes[1],cubes[2],"w-",alpha=0.3)   

        thruster_x          = [0]*len(components)
        thruster_y          = [0]*len(components)
        thruster_z          = [0]*len(components)

        uvec_x              = [0]*len(components)
        uvec_y              = [0]*len(components)
        uvec_z              = [0]*len(components)

        for idx, component in enumerate(components):

            uvec            = C_i2b.T @ (-component.uvec)
            p_c             = C_i2b.T @ component.p_c

            thruster_x[idx] = p_c[0]
            thruster_y[idx] = p_c[1]
            thruster_z[idx] = p_c[2]

            uvec_x[idx]     = uvec[0]
            uvec_y[idx]     = uvec[1]
            uvec_z[idx]     = uvec[2]

            # self.cubelines, = self.viz_body.plot(cubes[0,idx*17:idx*17+17],cubes[1,idx*17:idx*17+17],cubes[2,idx*17:idx*17+17],"w-",alpha=0.3)                

        self.thrusts.remove()
            
        self.thrusts        = self.viz_body.quiver(thruster_x,thruster_y,thruster_z,uvec_x,uvec_y,uvec_z,color="red",arrow_length_ratio=0.2,length=0.1,linewidth = 2)

        self.fuel.remove()

        self.fuel           = self.viz_body.text(5,5,0,f"Descent Engine  | {round(self.DB.remaining_fuel[0]*100,1)}%\n\
RCS 1                 | {round(self.DB.remaining_fuel[1]*100,1)}%\n\
RCS 2                 | {round(self.DB.remaining_fuel[2]*100,1)}%",color="white")


        """
        Body coordinate system
        """
        self.Body2_x.remove()
        self.Body2_y.remove()
        self.Body2_z.remove()
        self.Body2_xt.remove()
        self.Body2_yt.remove()
        self.Body2_zt.remove()

        self.Body2_x        = self.viz_body.quiver(0,0,0,x_b[0],x_b[1],x_b[2],color="red",arrow_length_ratio=0.1,length=3)
        self.Body2_y        = self.viz_body.quiver(0,0,0,y_b[0],y_b[1],y_b[2],color="green",arrow_length_ratio=0.1,length=3)
        self.Body2_z        = self.viz_body.quiver(0,0,0,z_b[0],z_b[1],z_b[2],color="blue",arrow_length_ratio=0.1,length=3)
        self.Body2_xt       = self.viz_body.text(3.2*x_b[0],3.2*x_b[1],3.2*x_b[2],r"$x_b$",color="red")
        self.Body2_yt       = self.viz_body.text(3.2*y_b[0],3.2*y_b[1],3.2*y_b[2],r"$y_b$",color="green")
        self.Body2_zt       = self.viz_body.text(3.2*z_b[0],3.2*z_b[1],3.2*z_b[2],r"$z_b$",color="blue")
            

    def run(self):

        sim_viz = FuncAnimation(self.fig, self.update, interval=20, repeat=False)

        plt.show()
