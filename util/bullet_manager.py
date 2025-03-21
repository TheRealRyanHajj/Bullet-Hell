from util.grefs import grefs

class BulletManager:
    def __init__(self):
        self.cooldownLength = 0   #ms
        self.cooldown       = 0     #ms
    
    def canSpawnNewBullet(self) -> bool:
        if self.cooldown <= 0:
            self.cooldown = self.cooldownLength
            return True
        
    def updateCooldown(self):
        self.cooldown -= grefs["TimeMachine"].dt *1000