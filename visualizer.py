from base       import *
from lib        import *


class Visualizer(Thread):

    def __init__(self, DB):

        self.DB     = DB

        super().__init__()
        self.daemon = True

        warnings.filterwarnings("ignore")

        self.cubes  = self.generate_cubes()


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

        fig = plt.figure(figsize=(15,15))
        viz = fig.add_subplot(1,2,1,projection="3d")
        viz2 = fig.add_subplot(1,2,2,projection="3d")

        traj = zeros(3)

        moon_u = linspace(0, 2 * pi, 20)
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

            viz.quiver( 0,0,0,  x_i[0],x_i[1],x_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
            viz.quiver( 0,0,0,  y_i[0],y_i[1],y_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
            viz.quiver( 0,0,0,  z_i[0],z_i[1],z_i[2],   color="black",arrow_length_ratio=0.1,length=2e6)
            viz.text(2e6*x_i[0]+0.05,2e6*x_i[1],2e6*x_i[2],r"$x_I$",color="black")
            viz.text(2e6*y_i[0],2e6*y_i[1]+0.05,2e6*y_i[2],r"$y_I$",color="black")
            viz.text(2e6*z_i[0],2e6*z_i[1],2e6*z_i[2]+0.05,r"$z_I$",color="black")

            viz.quiver( 0,0,0,  x_e[0],x_e[1],x_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
            viz.quiver( 0,0,0,  y_e[0],y_e[1],y_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
            viz.quiver( 0,0,0,  z_e[0],z_e[1],z_e[2],   color="red",arrow_length_ratio=0.1,length=2e6)
            viz.text(2e6*x_e[0]+0.05,2e6*x_e[1],2e6*x_e[2],r"$x_e$",color="red")
            viz.text(2e6*y_e[0],2e6*y_e[1]+0.05,2e6*y_e[2],r"$y_e$",color="red")
            viz.text(2e6*z_e[0],2e6*z_e[1],2e6*z_e[2]+0.05,r"$z_e$",color="red")

            viz.quiver( r_w[0],r_w[1],r_w[2],   x_w[0],x_w[1],x_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
            viz.quiver( r_w[0],r_w[1],r_w[2],   y_w[0],y_w[1],y_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
            viz.quiver( r_w[0],r_w[1],r_w[2],   z_w[0],z_w[1],z_w[2],   color="blue",arrow_length_ratio=0.1,length=5e5)
            viz.text(r_w[0]+5e5*x_w[0]/2+0.01,r_w[1]+5e5*x_w[1]/2,r_w[2]+5e5*x_w[2]/2,r"$x_w$",color="blue")
            viz.text(r_w[0]+5e5*y_w[0]/2,r_w[1]+5e5*y_w[1]/2+0.01,r_w[2]+5e5*y_w[2]/2,r"$y_w$",color="blue")
            viz.text(r_w[0]+5e5*z_w[0]/2,r_w[1]+5e5*z_w[1]/2,r_w[2]+5e5*z_w[2]/2+0.01,r"$z_w$",color="blue")

            viz.quiver( r_b[0],r_b[1],r_b[2],   x_b[0],x_b[1],x_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
            viz.quiver( r_b[0],r_b[1],r_b[2],   y_b[0],y_b[1],y_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
            viz.quiver( r_b[0],r_b[1],r_b[2],   z_b[0],z_b[1],z_b[2],   color="green",arrow_length_ratio=0.1,length=5e5)
            viz.text(r_b[0]+5e5*x_b[0]/2+0.01,r_b[1]+5e5*x_b[1]/2,r_b[2]+5e5*x_b[2]/2,r"$x_b$",color="green")
            viz.text(r_b[0]+5e5*y_b[0]/2,r_b[1]+5e5*y_b[1]/2+0.01,r_b[2]+5e5*y_b[2]/2,r"$y_b$",color="green")
            viz.text(r_b[0]+5e5*z_b[0]/2,r_b[1]+5e5*z_b[1]/2,r_b[2]+5e5*z_b[2]/2+0.01,r"$z_b$",color="green")

            viz.plot(traj[1:,0],traj[1:,1],traj[1:,2],'k-')

            viz.set_xlim(-3.5e6,3.5e6)
            viz.set_ylim(-3.5e6,3.5e6)
            viz.set_zlim(-3.5e6,3.5e6)
            viz.axis("off")

            x       = self.DB.x

            r_i     = x[:3]
            v_b     = x[3:6]
            O_i     = x[6:9]
            
            x_dot   = self.DB.x_dot

            r_i_dot = x_dot[:3]
            v_b_dot = x_dot[3:6]

            C_i2b   = C_W2B(O_i[0],O_i[1],O_i[2])

            v_i     = C_i2b.T @ v_b

            v_i_dot = C_i2b.T @ v_b_dot

            viz2.cla()

            cubes   = C_i2b.T @ self.cubes

            for idx, component in enumerate(self.DB.components):

                uvec = C_i2b.T @ (-component.uvec)
                p_cg = C_i2b.T @ component.p_cg
                p_c = C_i2b.T @ component.p_c

                viz2.plot(cubes[0,idx*17:idx*17+17],cubes[1,idx*17:idx*17+17],cubes[2,idx*17:idx*17+17],"k-",alpha=0.1)                
                # viz2.scatter(p_cg[0],p_cg[1],p_cg[2],color='black')
                # viz2.scatter(p_c[0],p_c[1],p_c[2],color='red')
                viz2.quiver(p_cg[0],p_cg[1],p_cg[2],uvec[0],uvec[1],uvec[2],color="red",arrow_length_ratio=0.2,length=10000,linewidth = 2)
            

            viz2.quiver(0,0,0,x_b[0],x_b[1],x_b[2],color="red",arrow_length_ratio=0.1,length=3)
            viz2.quiver(0,0,0,y_b[0],y_b[1],y_b[2],color="green",arrow_length_ratio=0.1,length=3)
            viz2.quiver(0,0,0,z_b[0],z_b[1],z_b[2],color="blue",arrow_length_ratio=0.1,length=3)
            viz2.text(3.2*x_b[0],3.2*x_b[1],3.2*x_b[2],r"$x_b$",color="red")
            viz2.text(3.2*y_b[0],3.2*y_b[1],3.2*y_b[2],r"$y_b$",color="green")
            viz2.text(3.2*z_b[0],3.2*z_b[1],3.2*z_b[2],r"$z_b$",color="blue")

            viz2.set_xlim(-5,5)
            viz2.set_ylim(-5,5)
            viz2.set_zlim(-5,5)
            viz2.axis("off")

            # viz2.view_init(30,5*i)

            # viz2.quiver(0,0,0,v_b[0],v_b[1],v_b[2],color="blue",arrow_length_ratio=0.1,length=1e-7*norm(v_b))
            # viz2.quiver(0,0,0,v_b_dot[0],v_b_dot[1],v_b_dot[2],color="red",arrow_length_ratio=0.1,length=0.1*norm(v_b_dot))

            # viz.quiver(r_b[0],r_b[1],r_b[2],v_i_dot[0],v_i_dot[1],v_i_dot[2],color="red",arrow_length_ratio=0.1,length=5e5*norm(v_i_dot))
            # viz.quiver(r_b[0],r_b[1],r_b[2],v_i[0],v_i[1],v_i[2],color="blue",arrow_length_ratio=0.1,length=5e-1*norm(r_i_dot))

            # viz.view_init(20,45)

            plt.pause(0.01)






