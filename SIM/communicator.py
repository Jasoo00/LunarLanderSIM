from base   import *


class Communicator:

    def __init__(self, DB):
        
        self.DB     = DB

        rospy.init_node("lunarlander_sim")    

        rospy.Subscriber("/control_input",Float32MultiArray,self.update_setpoints)

        self.sub_rate = rospy.Rate(30)



    def update_setpoints(self,ctrl_msg):

        ctrl_inputs = ctrl_msg.data

        self.DB.u   = array(ctrl_inputs)