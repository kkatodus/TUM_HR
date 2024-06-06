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
		self.control2idx = control2idx
		self.idx2control = {v:k for k,v in control2idx.items()}

	def get_control(self, model_data, running_time:float=0.0)->list[float]:
		return [1]*10
