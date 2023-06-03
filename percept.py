# -*- coding: utf-8 -*-

def sense_glitter(self):
    x, y = self.agent['xy']
    return self.state_grid[x][y]['glitter']

def sense_stench(self):
    x, y = self.agent['xy']
    return self.state_grid[x][y]['stench']
    
def sense_breeze(self):
    x, y = self.agent['xy']
    return self.state_grid[x][y]['breeze']
    
def sense_scream(self):
    from action import shoot
    return shoot(self)

def sense_bump(self, x, y):
    return self.state_grid[x][y]['bump']
