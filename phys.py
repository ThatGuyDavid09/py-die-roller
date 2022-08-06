import simplepbr
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, load_prc_file, MeshDrawer2D, Plane, MeshDrawer, PointLight, DirectionalLight, Point3
from panda3d.bullet import BulletWorld, BulletConvexHullShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape

load_prc_file("myConfig.prc")

mouse_down = False


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # simplepbr.init()

        self.collision_handled = False
        self.disable_mouse()

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        self.cam.setPos(0, -10, 2)
        self.cam.lookAt(0, 0, 0)

        # World
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -9.81))

        # Plane
        collision_shape = BulletPlaneShape(Vec3(0, 0, 1), 0)
        physics_node = BulletRigidBodyNode('Ground')
        physics_node.addShape(collision_shape)
        physics_node.setFriction(.8)
        node_parent_path = self.render.attachNewNode(physics_node)
        node_parent_path.setPos(0, 0, 0)
        self.world.attachRigidBody(physics_node)
        model = self.loader.loadModel('models/plane/Plane.gltf')
        model.flattenLight()
        model.reparentTo(node_parent_path)

        # Ico
        model_path = 'models/ico/ico.gltf'
        self.ico_start = (0, 0, 2)
        self.ico, self.ico_phys = self.load_model_with_collider("ico", model_path)
        self.ico.setPos(*self.ico_start)
        self.ico_phys.applyTorque((100, 100, 100))
        self.ico.setPythonTag("movable", 1)

        self.taskMgr.add(self.update, 'update')
        # taskMgr.add(self.draw_plane, "meshdrawer task")

    # def draw_plane(self, task):
    #     self.generator.begin(self.cam, self.render)
    #     self.generator.rectangle_raw(-20, -20, 40, 40, 1, 1, 1, 1, (0, 0, 0, 1))
    #     self.generator.end()

    def load_model_with_collider(self, name, path, mass=1):
        model = self.loader.loadModel(path)

        geomNodes = model.findAllMatches('**/+GeomNode')
        geomNode = geomNodes.getPath(0).node()
        geom = geomNode.getGeom(0)
        collision_shape = BulletConvexHullShape()
        collision_shape.addGeom(geom)

        physics_node = BulletRigidBodyNode(name)

        physics_node.setMass(mass)
        physics_node.setFriction(.8)
        # physics_node.setLinearVelocity((0, 0, 4))
        physics_node.addShape(collision_shape)
        node_parent_path = self.render.attachNewNode(physics_node)
        # node_parent_path.setPos(0, 0, 2)
        # physics_node.applyTorque((1, 1, 1))
        self.world.attachRigidBody(physics_node)
        model.flattenLight()
        model.reparentTo(node_parent_path)

        return node_parent_path, physics_node

    # Update
    def update(self, task):
        # print(mouse_down)

        dt = globalClock.getDt()
        self.world.doPhysics(dt)

        self.cam.lookAt(self.ico.getPos())

        if mouse_down and self.mouseWatcherNode.hasMouse():
            # Collision checks with mouse
            pMouse = self.mouseWatcherNode.getMouse()
            pFrom = Point3()
            pTo = Point3()
            self.camLens.extrude(pMouse, pFrom, pTo)

            # Transform to global coordinates
            pFrom = self.render.getRelativePoint(self.cam, pFrom)
            pTo = self.render.getRelativePoint(self.cam, pTo)

            result = self.world.rayTestClosest(pFrom, pTo)

            if not self.collision_handled and result.hasHit() and result.getNode().getPythonTag("movable"):
                f_app_pt = result.getHitPos()
                force_dir_v = (result.getToPos() - result.getFromPos()).normalized()
                result.getNode().applyForce(force_dir_v * 100, f_app_pt)
                print("Collision handled")
                self.collision_handled = True
        else:
            self.collision_handled = False

        return task.cont


class MouseHandler(DirectObject):
    def __init__(self):
        self.accept('mouse1', self.update_down)
        self.accept('mouse1-up', self.update_up)

    def update_down(self):
        global mouse_down
        mouse_down = True

    def update_up(self):
        global mouse_down
        mouse_down = False


# TODO: make it so you can move camera around so forces can be applied properly
class ReadKeys(DirectObject):
    def __init__(self):
        self.accept('r-up', self.reset)

    def reset(self):
        global app
        app.ico.setPos(*app.ico_start)
        app.ico_phys.apply_central_impulse(app.ico_phys.getLinearVelocity() * -1)
        app.ico_phys.applyTorqueImpulse(app.ico_phys.getAngularVelocity() * -1)


m = MouseHandler()
r = ReadKeys()

app = App()
app.run()
