import numpy as np

class Controller:
	def __init__(self, control2idx=None):
		if not control2idx:
			control2idx = {
				'forward':0,
				'turn':1,
				'lift':2,
				'arm_extend':3,
				'wrist_yaw':4,
				'wrist_pitch':5,
				'wrist_roll':6,
				'grip':7,
				'head_pan':8,
				'head_tilt':9
			}
		self.num_controls = len(control2idx)
		self.control2idx = control2idx
		self.controlids = list(control2idx.keys())
		self.idx2control = {v:k for k,v in control2idx.items()}
		self.control_ranges = {
			'forward':[-1,1],
			'turn':[-1,1],
			'lift':[-0.5,0.5],
			'arm_extend':[0,0.52],
			'wrist_yaw':[-1.39,4.42],
			'wrist_pitch':[-0.57,1.57],
			'wrist_roll':[-3.14, 3.14],
			'grip':[-0.005,0.04],
			'head_pan':[-3.9,1.5],
			'head_tilt':[-1.53,0.79]
		}

	def get_control(self, model_data, camera_data:dict, running_time:float=0.0)->list[float]:
		if running_time < 0:
			raise ValueError("Running time cannot be negative")
		if running_time > 5:
			forward_arr = self.move2position('forward', 0.5)
			turn_arr = self.move2position('turn', 0.5)
			lift_arr = self.move2position('lift', 0.5)
			arm_extend_arr = self.move2position('arm_extend', 0.5)
			wrist_yaw_arr = self.move2position('wrist_yaw', 0.5)
			wrist_pitch_arr = self.move2position('wrist_pitch', 0.5)
			wrist_roll_arr = self.move2position('wrist_roll', 0.5)
			grip_arr = self.move2position('grip', 0.03)
			head_pan_arr = self.move2position('head_pan', 0.5)
			head_tilt_arr = self.move2position('head_tilt', 0.5)
		if running_time < 5:
			forward_arr = self.move2position('forward', 0)
			turn_arr = self.move2position('turn', 0)
			lift_arr = self.move2position('lift', 0)
			arm_extend_arr = self.move2position('arm_extend', 0)
			wrist_yaw_arr = self.move2position('wrist_yaw', 0)
			wrist_pitch_arr = self.move2position('wrist_pitch', 0)
			wrist_roll_arr = self.move2position('wrist_roll', 0)
			grip_arr = self.move2position('grip', 0)
			head_pan_arr = self.move2position('head_pan', 0)
			head_tilt_arr = self.move2position('head_tilt', 0)
		
		#adding together all the control arrays
		all_controls = np.array([
			forward_arr,
			turn_arr,
			lift_arr,
			arm_extend_arr,
			wrist_yaw_arr,
			wrist_pitch_arr,
			wrist_roll_arr,
			grip_arr,
			head_pan_arr,
			head_tilt_arr
		])
		#returning the sum of all the control arrays
		return list(np.sum(all_controls, axis=0))
	
	def move2position(self, control:str, position:float):
		control_limit = self.control_ranges[control]
		if control not in self.control2idx:
			raise ValueError(f"Invalid control {control}. Expected one of {self.controlids}")
		if position < control_limit[0] or position > control_limit[1]:
			raise ValueError(f"Position {position} for control {control} is out of range {control_limit}")
		#creating a control array with all zeros and setting the control value at the index of the control
		control_arr = [0]*self.num_controls
		control_arr[self.control2idx[control]] = position
		return control_arr

