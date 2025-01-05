import os
import threading
import time
import pygame as pg
import cv2
from colorthief import ColorThief
pg.mixer.init()
pg.init()

# Main code
listGuitar = []
listViolin = []
listPiano = []
mynotes1 = []
mynotes2 = []
mynotes3 = []

folder_dir = '' # Insert dir
input_dir = os.path.join(folder_dir, 'frames')
guitar_dir = os.path.join(folder_dir, 'Guitar')
violin_dir = os.path.join(folder_dir, 'Violin')
piano_dir = os.path.join(folder_dir, 'Piano')



# Path of the video
video_path = '' #Insert video path

# Output directory for saving frames
output_directory = '' # Insert folder to save frames created

# Number of frames to skip between saving
frames_to_skip = 30

# Create a directory to save frames if it doesn't exist
frames_directory = os.path.join(output_directory, 'frames')
if not os.path.exists(frames_directory):
    os.makedirs(frames_directory)

# Open the video file
vidcap = cv2.VideoCapture(video_path)


frame_count = 0
saved_frame_count = 0


while True:

    success, frame = vidcap.read()


    if not success:
        break

    # Skip frames if u want
    if frame_count % frames_to_skip != 5:
        frame_count += 1
        continue

    frame_path = os.path.join(frames_directory, f'{saved_frame_count:04d}.png')
    cv2.imwrite(frame_path, frame)

    frame_count += 1
    saved_frame_count += 1


vidcap.release()

print(f"Frames extracted: {saved_frame_count}")


def play_notes(note_path, duration):
    time.sleep(duration)
    pg.mixer.Sound(note_path).play()
    time.sleep(duration)

def play_colorR():
    for note_index in mynotes1:
        note_path = os.path.join(guitar_dir, listGuitar[note_index])
        play_notes(note_path, 0.5)
    time.sleep(5)

def play_colorG():
    time.sleep(0.05)
    for note_index in mynotes2:
        note_path = os.path.join(violin_dir, listViolin[note_index])
        play_notes(note_path, 0.5)
    time.sleep(5)

def play_colorB():
    time.sleep(0.1)
    for note_index in mynotes3:
        note_path = os.path.join(piano_dir, listPiano[note_index])
        play_notes(note_path, 0.5)
    time.sleep(5)

def play_Video():
    cap = cv2.VideoCapture('') # Insert file 

    fps= int(cap.get(cv2.CAP_PROP_FPS))
    print("This is the fps ", fps)

    if cap.isOpened() == False:
        print("Error File Not Found")

    while cap.isOpened():
        ret,frame= cap.read()

        if ret == True:

            time.sleep(1/30)

            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            break

    cap.release()
    cv2.destroyAllWindows()


# Populate file lists
for tune in os.listdir(guitar_dir):
    if tune.endswith(".wav"):
        listGuitar.append(tune)

for tune in os.listdir(violin_dir):
    if tune.endswith(".wav"):
        listViolin.append(tune)

for tune in os.listdir(piano_dir):
    if tune.endswith(".mp3"):
        listPiano.append(tune)

listGuitar.sort(key=len)
listViolin.sort(key=len)
listPiano.sort(key=len)

# Process images in the input directory
for image in os.listdir(input_dir):
    if image.endswith(".png"):
        image_path = os.path.join(input_dir, image)
        ct = ColorThief(image_path)
        dominant_colour = ct.get_color(quality=1)
        
        mynotes1.append(round(dominant_colour[0] / 4.3))
        mynotes2.append(round(dominant_colour[1] / 6.9))
        mynotes3.append(round(dominant_colour[2] / 2.9))

pg.mixer.set_num_channels(len(listGuitar))

t1 = threading.Thread(target=play_colorR)
t2 = threading.Thread(target=play_colorG)
t3 = threading.Thread(target=play_colorB)
t4 = threading.Thread(target=play_Video)

t1.start()
t2.start()
t3.start()
t4.start()