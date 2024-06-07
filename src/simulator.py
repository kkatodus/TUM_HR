import mujoco
import mujoco.viewer
import mediapy as media
import time
from src.controller import Controller

class Simulator:
    def __init__(self, robot_xml_path='stretch3/stretch.xml', fps=60):
        self._robot_xml_path = robot_xml_path
        self.model = mujoco.MjModel.from_xml_path(self._robot_xml_path)
        self.model_data = mujoco.MjData(self.model)
        self.renderer = mujoco.Renderer(self.model)
        scene_options = mujoco.MjvOption()
        scene_options.flags[mujoco.mjtVisFlag.mjVIS_JOINT] = False
        self.controller = Controller()
        self.fps = fps
        self.accepted_camera_names = [None, 'camera_rgb', 'camera_depth', 'camera_rgb_wrist', 'camera_depth_wrist']

    def run_sim(self, duration:int=10, camera:str='camera_rgb'):
        if camera not in self.accepted_camera_names:
            raise ValueError(f"Invalid camera name: {camera}. Expected one of {self.accepted_camera_names}")
        camera_frames = {
            cam: [] for cam in self.accepted_camera_names
        }
        i = 0
        with mujoco.viewer.launch_passive(self.model, self.model_data) as viewer:
            sim_start_time = time.time()
            mujoco.mj_resetData(self.model, self.model_data)

            #sim should run for the duration specified
            while viewer.is_running() and time.time() - sim_start_time < duration:
                step_start = time.time()
                #step the simulation
                mujoco.mj_step(self.model, self.model_data)
                # Pick up changes to the physics state, apply perturbations, update options from GUI.
                viewer.sync()
                if time.time() - sim_start_time > i / self.fps:
                    i += 1
                    for cam in self.accepted_camera_names:
                        if cam == None:
                            self.renderer.update_scene(self.model_data)
                        else:
                            self.renderer.update_scene(self.model_data, camera=cam)
                        cam_pixels = self.renderer.render()
                        camera_frames[cam].append(cam_pixels)
                #setting the controls for the step from the controller
                self.model_data.ctrl = self.controller.get_control(self.model_data, running_time=time.time()-sim_start_time, camera_data=camera_frames)
        media.show_video(camera_frames[camera], fps=self.fps)
