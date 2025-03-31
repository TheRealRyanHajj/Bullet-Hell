from util.grefs import grefs

class BombManager:
    def __init__(self):
        self.cooldownLength = 2000  #ms
        self.cooldown       = 0     #ms
    
    def canSpawnNewBomb(self) -> bool:
        if self.cooldown <= 0:
            self.cooldown = self.cooldownLength
            return True
        
    def updateCooldown(self):
        self.cooldown -= grefs["TimeMachine"].dt *1000