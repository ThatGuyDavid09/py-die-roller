from math import pi, sin, cos

import simplepbr
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.bullet import BulletWorld, BulletPlaneShape, BulletRigidBodyNode, BulletBoxShape
from panda3d.core import Material, AmbientLight, load_prc_file, Vec3, ClockObject

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
        # self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.update, "update")

        # self.cube = self.loader.loadModel("models/cube/cube.gltf")
        # self.cube.reparentTo(self.render)
        # self.cube.setScale(1, 1, 1)
        # self.cube.setPos(0, 0, 1)

        self.camera.lookAt((0, 0, 0))
        self.world = BulletWorld()
        self.world.setGravity((0, 0, -9.81))

        self.shape = BulletPlaneShape(Vec3(0, 0, 1), 1)

        self.node = BulletRigidBodyNode('Ground')
        self.node.addShape(self.shape)

        self.np = self.render.attachNewNode(self.node)
        self.np.setPos(0, 0, -2)

        self.world.attachRigidBody(self.node)

        self.shape = BulletBoxShape(Vec3(0.5, 0.5, 0.5))
        self.node = BulletRigidBodyNode('Box')
        self.node.setMass(1.0)
        self.node.addShape(self.shape)
        self.np = self.render.attachNewNode(self.node)
        self.np.setPos(0, 0, 2)
        self.world.attachRigidBody(self.node)
        self.model = self.loader.loadModel('models/box.egg')
        self.model.flattenLight()
        self.model.reparentTo(self.np)

        # for i in self.cube.findAllMaterials():
        #     i.setBaseColor((0, 0, 1, 1))
        #     i.setMetallic(1)

        # self.alight = AmbientLight('alight')
        # self.alight.setColor((1,1,1,1))
        # self.alnp = self.render.attachNewNode(self.alight)
        # self.render.setLight(self.alnp)

    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont

    def update(self, task):
        dt = ClockObject.getGlobalClock().getDt()
        self.world.doPhysics(dt)
        return task.cont


app = MyApp()
app.run()
