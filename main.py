from math import pi, sin, cos

import simplepbr
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Material, AmbientLight, load_prc_file

load_prc_file("myConfig.prc")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        simplepbr.init()

        # self.scene = self.loader.loadModel("models/environment")
        # self.scene.reparentTo(self.render)
        # self.scene.setScale(0.25, 0.25, 0.25)
        # self.scene.setPos(-8, 42, 0)
        # self.disableMouse()
        #
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        self.cube = Actor("models/cube/cube.gltf")
        self.cube.reparentTo(self.render)
        self.cube.setScale(1, 1, 1)
        self.cube.setPos(0, 0, 1)

        # for i in self.cube.findAllMaterials():
        #     i.setBaseColor((0, 0, 1, 1))
        #     i.setMetallic(1)

        self.alight = AmbientLight('alight')
        self.alight.setColor((1,1,1,1))
        self.alnp = self.render.attachNewNode(self.alight)
        self.render.setLight(self.alnp)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()
