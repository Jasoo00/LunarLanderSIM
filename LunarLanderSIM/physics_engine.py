from base       import *
from lib        import *



class PhysicsEngine(Thread):


    def __init__(self, DB):

        self.DB     = DB

        super().__init__()
        self.daemon = True


    
    def run(self):

        while True:

            self.DB.update_quantities()
            
            update_state(self.DB)

            time.sleep(self.DB.rate)

            self.DB.t += self.DB.del_t