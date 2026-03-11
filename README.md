# Teleoperated Robot with ROS and ESP8266

This project allows you to control a teleoperated robot using ROS Noetic on Ubuntu 20.04 and ESP8266 NodeMCU as the embedded controller and both are connected by rosserial package for communication between them.

---

## 🚧 Hardware Setup

### Motor & Peripheral Connections

* **Motor 1**: D1, D2 (direction), D0 (enable/speed)
* **Motor 2**: D3, D4 (direction), D5 (enable/speed)
* **Headlights**:

  * Front: D6
  * Back: D7

---

## 💻 Software Setup

### 1. ESP8266 Firmware

#### Install Tools:

* [Arduino IDE](https://www.arduino.cc/en/software)
* ESP8266 Board Support via Boards Manager

#### Install ROS Libraries:

```bash
sudo apt-get install ros-noetic-rosserial-arduino
sudo apt-get install ros-noetic-rosserial-python
```

#### Upload Firmware:

* Open your corrected ESP8266 code in Arduino IDE
* Select board: **NodeMCU 1.0 (ESP-12E Module)**
* Baud rate: **115200**
* Upload to correct COM port

### 2. ROS (Ubuntu 20.04)

#### Install ROS Noetic:

```bash
sudo apt install ros-noetic-desktop-full
source /opt/ros/noetic/setup.bash
```

#### Installing Missing ROS Packages

If you encounter an error like missing `rosserial_python`, install the required packages:

```bash
sudo apt-get update
sudo apt-get install ros-noetic-rosserial-arduino
sudo apt-get install ros-noetic-rosserial-python
sudo apt-get install ros-noetic-rosserial
```

After installation, source your ROS environment:

```bash
source /opt/ros/noetic/setup.bash
```

#### Setup Workspace:

```bash
mkdir -p ~/robot_ws/src
cd ~/robot_ws/
catkin_make
source devel/setup.bash
```

#### Create UI Package:

```bash
cd ~/robot_ws/src
catkin_create_pkg teleop_ui rospy std_msgs geometry_msgs
```

#### Add UI Code:

```bash
cd ~/robot_ws/src/teleop_ui
mkdir scripts
cd scripts
nano robot_teleop_ui.py  # Paste and save the Python UI code
chmod +x robot_teleop_ui.py
```

## 🚀 Running the System

### 1. Network Setup

Connect to ESP8266 AP:

* SSID: **GP54**
* Password: **moodle54**
* IP: Usually **192.168.4.2**

Update `~/.bashrc`:

```bash
export ROS_MASTER_URI=http://192.168.4.2:11311
export ROS_IP=192.168.4.2
source ~/.bashrc
```

### 2. Start ROS

```bash
roscore
```

### 3. Start rosserial TCP Server:

```bash
rosrun rosserial_python serial_node.py tcp
```

### 4. Launch UI:

```bash
cd ~/robot_ws
source devel/setup.bash
rosrun teleop_ui robot_teleop_ui.py
```

## 🙌 Contributors

- [@Ujjwal030406](https://github.com/Ujjwal030406)  
- [Vasu-Baliyan]
