import math

class bezierCurve(object):
    start_pnt = 0
    start_ctrl = 0
    end_pnt = 0
    end_ctrl = 0

    t = 0
    t_increment = 0.0065
    exit_bool = False

    def __init__(self, s_pnt, s_ctrl, e_pnt, e_ctrl):
        self.start_pnt = s_pnt
        self.start_ctrl = s_ctrl
        self.end_pnt = e_pnt
        self.end_ctrl = e_ctrl


    def calculatePoint(self):
        if self.t < 1:
            curr_pointX = math.pow((1-self.t), 3)*self.start_pnt[0] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[0] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[0] + math.pow(self.t,3)*self.end_ctrl[0]
            curr_pointY = math.pow((1-self.t), 3)*self.start_pnt[1] + 3*math.pow((1-self.t),2)*self.t*self.start_ctrl[1] + 3*(1-self.t)*math.pow(self.t,2)*self.end_pnt[1] + math.pow(self.t,3)*self.end_ctrl[1]
            self.t += self.t_increment
            return [curr_pointX, curr_pointY]
        return [0, 0]

    def increaseVelocity(self):
        if not self.exit_bool:
            self.t_increment += 0.003
            self.exit_bool = True
