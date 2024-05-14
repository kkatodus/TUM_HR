# Notes

## Installation Guide

- Install python3.12.2 maybe try something like [this](https://ubuntuhandbook.org/index.php/2023/05/install-python-3-12-ubuntu/)(no guarantees, worked for me with option2 by installing the source)
- install required packages with `pip install -r requirements.txt`
- to get mediapy working you also need to run `sudo apt install ffmpeg`

## Commands for Mujoco

- `python -m mujoco.viewer` launches an empty visualization session, where a model can be loaded by drag-and-drop.

- `python -m mujoco.viewer --mjcf=/path/to/some/mjcf.xml` launches a visualization session for the specified model file.

## Coding with mujoco notes

- don't have two renderers, it will not work

## Model file things

- Converting URDF to MJCF: [https://mujoco.readthedocs.io/en/stable/modeling.html#CURDF]

## Other issues with linux and GPU

- go to root user on boot by starting a system in recovery mode
- check if the nvidia drivers are installed with `nvidia-smi`
- if not, check the recommended driver with `sudo apt list --installed | grep nvidia-driver`
- install the recommended driver with `sudo apt install nvidia-driver-XXX`
- continue with the booting sequence
