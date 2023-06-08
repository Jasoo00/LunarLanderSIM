from base   import *


class Communicator(Thread):

    def __init__(self, DB):
        
        self.DB         = DB

        rospy.init_node("lunarlander_sim")    

        rospy.Subscriber("/control_input",Float32MultiArray,self._update_setpoints)

        super().__init__()
        self.daemon     = True

        self.sensor     = rospy.Publisher("/sensor_data",Float32MultiArray,queue_size=1)

        self.io_rate   = rospy.Rate(30)


    def _update_setpoints(self,ctrl_msg):

        ctrl_inputs = ctrl_msg.data

        self.DB.u   = array(ctrl_inputs)


    def run(self):

        while True:

            x = self.DB.x
            
            ### State data ###

            r_wx,r_wy,r_wz = x[0],x[1],x[2]

            v_bx,v_by,v_bz = x[3],x[4],x[5]

            roll,pitch,yaw = x[6],x[7],x[8]

            p,q,r          = x[9],x[10],x[11]

            ### Remaining fuel ###

            sensor_data = Float32MultiArray()

            sensor_data.data = array([r_wx,r_wy,r_wz,\
                                      v_bx,v_by,v_bz,\
                                      roll,pitch,yaw,\
                                      p,q,r])

            self.sensor.publish(sensor_data)

            self.io_rate.sleep()