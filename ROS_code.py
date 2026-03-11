# my laptop code which helps me connect it to esp(basically ROS code)-
import tkinter as tk
from tkinter import *
import rospy
from geometry_msgs.msg import Twist
import time

# Initialize ROS
rospy.init_node('Teleop_UI')
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10)

# Tkinter root setup
root = tk.Tk()
root.geometry('+550+150')
root.title("Teleoperated Robot with Reverse")

# Variables
var = IntVar()
var.set(3)
check_light = IntVar()
pressed_keys = set()
last_combo = None
last_time = time.time()
movement_stack = []

# Reverse key logic
def reverse_command(combo):
    reverse = []
    if 'w' in combo: reverse.append('s')
    if 's' in combo: reverse.append('w')
    if 'a' in combo: reverse.append('d')
    if 'd' in combo: reverse.append('a')
    return reverse

# Publish twist message
def publish_combo(combo):
    # twist = Twist()
    twist.linear.x = 0
    twist.angular.z = 0
    twist.angular.y = int(var.get())
    twist.angular.x = check_light.get()

    if 'w' in combo: twist.linear.x += 2
    if 's' in combo: twist.linear.x -= 2
    if 'a' in combo: twist.angular.z += 2
    if 'd' in combo: twist.angular.z -= 2
    pub.publish(twist)

# Update motion and track input
def update_motion():
    global last_combo, last_time
    current_combo = tuple(sorted(pressed_keys))

    now = time.time()
    if current_combo != last_combo:
        if last_combo:
            duration = now - last_time
            movement_stack.append((reverse_command(last_combo), duration))
            print(f"Pushed to stack: {reverse_command(last_combo)} for {duration:.2f}s")
        last_time = now
        last_combo = current_combo

    if current_combo:
        publish_combo(current_combo)
    else:
        twist = Twist()
        twist.angular.x = check_light.get()
        pub.publish(twist)

    root.after(100, update_motion)

# Key press/release handlers
def on_key_press(event):
    pressed_keys.add(event.keysym.lower())

def on_key_release(event):
    pressed_keys.discard(event.keysym.lower())

# Reverse playback
def start_reverse_sequence():
    print("Starting reverse sequence...")
    while movement_stack:
        combo, duration = movement_stack.pop()
        print(f"Reversing: {combo} for {duration:.2f}s")
        start_time = time.time()
        while time.time() - start_time < duration:
            publish_combo(combo)
            rate.sleep()
    print("Reverse sequence complete.")

# Auto-trigger reverse after 10s of inactivity
def check_inactive():
    if not pressed_keys and time.time() - last_time > 10 and movement_stack:
        start_reverse_sequence()
    root.after(1000, check_inactive)

# "End" button clears the stack
def on_end_button_click():
    movement_stack.clear()
    print("End button clicked. Movement stack cleared.")

# UI Layout
label1 = tk.Label(root, text="ROS Teleop with Auto-Reverse", font=('Helvetica', 14, 'bold'))
label1.grid(row=0, column=0, columnspan=3, pady=10)

# Movement buttons
buttonf = tk.Button(root, text="↑", font=('Arial', 16), padx=20, pady=10)
buttonb = tk.Button(root, text="↓", font=('Arial', 16), padx=20, pady=10)
buttonl = tk.Button(root, text="←", font=('Arial', 16), padx=20, pady=10)
buttonr = tk.Button(root, text="→", font=('Arial', 16), padx=20, pady=10)
buttonstop = tk.Button(root, text="Stop", font=('Arial', 12), bg="red", fg="white", padx=10, pady=10)

buttonf.grid(row=1, column=1, pady=5)
buttonl.grid(row=2, column=0, padx=5)
buttonstop.grid(row=2, column=1, pady=5)
buttonr.grid(row=2, column=2, padx=5)
buttonb.grid(row=3, column=1, pady=5)

# Headlights toggle
check_box_light = tk.Checkbutton(root, text='Headlights', variable=check_light, onvalue=1, offvalue=0)
check_box_light.grid(row=4, column=2, pady=10, sticky=E)

# Speed scale
speed_scale = tk.Scale(root, from_=0, to=7, variable=var, length=250, label="Speed", orient=HORIZONTAL)
speed_scale.grid(row=4, column=0, columnspan=2, pady=10)

# "End" button to clear the movement stack
end_button = tk.Button(root, text="End", command=on_end_button_click, bg="gray", fg="white", padx=10, pady=5)
end_button.grid(row=5, column=1, pady=10)

# ROS status
status_label = tk.Label(root, text="ROS Status: Connected", bd=1, relief=SUNKEN, anchor=W)
status_label.grid(row=6, column=0, columnspan=3, sticky=W+E)

def update_status():
    if rospy.is_shutdown():
        status_label.config(text="ROS Status: Disconnected", fg="red")
    else:
        status_label.config(text="ROS Status: Connected", fg="green")
    root.after(1000, update_status)

# Bind key events
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

# Start recurring updates
update_motion()
check_inactive()
update_status()

root.resizable(False, False)
root.mainloop()
