from tkinter import *
from tkinter import filedialog
from tkvideo import tkvideo
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
import cv2 
import numpy as np 
import time
import imutils
import os

class App:
    def __init__(self, window, windowTitle):
        # Root window settings
        self.backgroundColor = "#404040"
        self.root = window
        self.root.geometry("800x600")
        self.root.config(background=self.backgroundColor)
        self.root.title(windowTitle)
        self.root.iconbitmap('images/icon.ico')

        # Frame that holds all our frame settings
        self.ImageFrameWidth = 700
        self.ImageFrameHeight = 500
        self.imageFrameBackground = Frame(self.root, width=self.ImageFrameWidth, height=self.ImageFrameHeight)
        self.imageFrameBackground.grid(row=3, column=1, columnspan=5)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(6, weight=1)

        # File explorer instance for image and video locating
        self.fileExplorerLabel = Label(self.root, text = "Select Image/Video or Camera Feed", fg = "white", bg = "#404040")
        self.fileExplorerLabel.grid(column = 1, row = 1, columnspan=5)

        # Image, video, and camera instances
        self.faceColor = ColorEditor()
        self.ballColor = ColorEditor()
        self.imagePlayer = ImagePlayer(self.root, self.faceColor, self.ballColor)
        self.videoPlayer = VideoPlayer(self.root, self.faceColor, self.ballColor)
        self.camera = Camera(self.root, self.faceColor, self.ballColor)

        # Flags for frame toggle buttons
        self.face_is_on = False
        self.ball_is_on = False
        self.record_is_on = False
        self.pro_is_on = False

        # toggle button on and off images
        self.on = PhotoImage(file = "images/buttons/on.png") 
        self.off = PhotoImage(file = "images/buttons/off.png") 

        ############################################# Image Button #############################################
        # Init file image browse button
        self.openImage = Button(self.root, text = "Browse Images", border= 0, command = self.imagePlayer.BrowseFiles) 
        self.imageBtn_leave = PhotoImage(file="images/buttons/imageBtn.png") # Location of exit buttons
        self.imageBtn_enter = PhotoImage(file="images/buttons/imageBtn2.png")
        self.openImage.config(image=self.imageBtn_leave)
        self.openImage.grid(column = 1, row = 2)

        # Create the image browse button object and bind the events and images
        self.ImageButton = ButtonObj(self.openImage, self.imageBtn_enter, self.imageBtn_leave)
        self.openImage.bind("<Enter>", self.ImageButton.on_enter)
        self.openImage.bind("<Leave>", self.ImageButton.on_leave)

        ############################################# Video Button #############################################
        # Init file video browse button
        self.openVideo = Button(self.root, text = "Browse Videos", border= 0, command = self.videoPlayer.BrowseFiles) 
        self.videoBtn_leave = PhotoImage(file="images/buttons/videoBtn.png") # Location of exit buttons
        self.videoBtn_enter = PhotoImage(file="images/buttons/videoBtn2.png")
        self.openVideo.config(image=self.videoBtn_leave)
        self.openVideo.grid(column = 2, row = 2)

        # Create the image browse button object and bind the events and images
        self.VideoButton = ButtonObj(self.openVideo, self.videoBtn_enter, self.videoBtn_leave)
        self.openVideo.bind("<Enter>", self.VideoButton.on_enter)
        self.openVideo.bind("<Leave>", self.VideoButton.on_leave)

        ############################################# Camera Feed Button #############################################
        # Init file camera feed button
        self.openCam = Button(self.root, text = "Camera Feed", border= 0, command = self.camera.DisplayCamera)
        self.camBtn_leave = PhotoImage(file="images/buttons/camera.png") # Location of exit buttons
        self.camBtn_enter = PhotoImage(file="images/buttons/camera2.png")
        self.openCam.config(image=self.camBtn_leave)
        self.openCam.grid(column = 3, row = 2)

        # Create the image browse button object and bind the events and images
        self.camButton = ButtonObj(self.openCam, self.camBtn_enter, self.camBtn_leave)
        self.openCam.bind("<Enter>", self.camButton.on_enter)
        self.openCam.bind("<Leave>", self.camButton.on_leave)

        ############################################# Exit Button #############################################
        # Init exit buttons
        self.exitButton = Button(self.root, text="Quit", border= 0, command=self.QuitGUI)
        self.exit_leave = PhotoImage(file="images/buttons/exit.png") # Location of exit buttons
        self.exit_enter = PhotoImage(file="images/buttons/exit2.png")
        self.exitButton.config(image=self.exit_leave)
        self.exitButton.grid(column = 4,row = 2) # Displaying the button

        # Create the exit button object and bind the events and images
        self.ExitButton = ButtonObj(self.exitButton, self.exit_enter, self.exit_leave)
        self.exitButton.bind("<Enter>", self.ExitButton.on_enter)
        self.exitButton.bind("<Leave>", self.ExitButton.on_leave)

        ############################################# Frame Label #############################################
        # Label for the frame settings, record, color face, color ball
        self.settingsLabel = Label(self.imageFrameBackground, text = "Frame Settings", font=(44))
        self.settingsLabel.grid(column = 0, row = 0, columnspan = 2, padx=269, pady=5)

        ############################################# Record Camera Button #############################################
        # Init file record feed button
        self.recordLabel = Label(self.imageFrameBackground, text = "Record Camera Output", fg = "grey")
        self.recordLabel.grid(column = 0, row = 1, columnspan = 2, pady=5)
        self.recordButton = Button(self.imageFrameBackground, image = self.off, bd = 0, command = self.RecordToggle) 
        self.recordButton.grid(column = 0, row = 2, columnspan = 2)

        ############################################# Pro Cascade Button #############################################
        # Init pro haar cascade button
        self.proLabel = Label(self.imageFrameBackground, text = "Use Pro Cascades", fg = "grey")
        self.proLabel.grid(column = 0, row = 3, columnspan = 2, pady=5)
        self.proButton = Button(self.imageFrameBackground, image = self.off, bd = 0, command = self.ProToggle) 
        self.proButton.grid(column = 0, row = 4, columnspan = 2)

        ############################################# Color Face Button #############################################
        # Label and toggle switch for editing the coloring on a detected face
        self.faceLabel = Label(self.imageFrameBackground, text = "Color Face", fg = "grey")
        self.faceLabel.grid(column = 0, row = 5)
        self.faceButton = Button(self.imageFrameBackground, image = self.off, bd = 0, command = self.FaceSwitch) 
        self.faceButton.grid(column = 0, row = 6)

        ############################################# Color Face Settings #############################################
        # Frame that holds all our color face settings, frames nested inside imageFrameBackground
        self.FaceScaleWidth = 700
        self.FaceScaleHeight = 500
        self.faceScaleBackground = Frame(self.imageFrameBackground, width=self.FaceScaleWidth, height=self.FaceScaleHeight)
        self.faceScaleBackground.grid(row=7, column=0)

        # tKinter scale that colors red inside detected face, from 0 to 255
        self.faceLabelR = Label(self.faceScaleBackground, text = "Red", fg = "grey")
        self.faceLabelR.grid(column = 0, row = 0)
        self.faceR = Scale(self.faceScaleBackground, from_=0, to=255, command=self.setFaceRed)
        self.faceR.grid(column = 0, row = 1)

        # tKinter scale that colors green inside detected face, from 0 to 255
        self.faceLabelG = Label(self.faceScaleBackground, text = "Green", fg = "grey")
        self.faceLabelG.grid(column = 1, row = 0)
        self.faceG = Scale(self.faceScaleBackground, from_=0, to=255, command=self.setFaceGreen)
        self.faceG.grid(column = 1, row = 1)

        # tKinter scale that colors blue inside detected face, from 0 to 255
        self.faceLabelB = Label(self.faceScaleBackground, text = "Blue", fg = "grey")
        self.faceLabelB.grid(column = 2, row = 0)
        self.faceB = Scale(self.faceScaleBackground, from_=0, to=255, command=self.setFaceBlue)
        self.faceB.grid(column = 2, row = 1)

        ############################################# Color Ball Button #############################################
        # Label and toggle switch for editing the coloring on a detected ball
        self.ballLabel = Label(self.imageFrameBackground, text = "Color Ball", fg = "grey")
        self.ballLabel.grid(column = 1, row = 5)
        self.ballButton = Button(self.imageFrameBackground, image = self.off, bd = 0, command = self.BallSwitch) 
        self.ballButton.grid(column = 1, row = 6)

        ############################################# Color Ball Settings #############################################
        # Frame that holds all our color ball settings, frames nested inside imageFrameBackground
        self.BallScaleWidth = 700
        self.BallScaleHeight = 500
        self.ballScaleBackground = Frame(self.imageFrameBackground, width=self.BallScaleWidth, height=self.BallScaleHeight)
        self.ballScaleBackground.grid(row=7, column=1)

        # tKinter scale that colors red inside detected ball, from 0 to 255
        self.ballLabelR = Label(self.ballScaleBackground, text = "Red", fg = "grey")
        self.ballLabelR.grid(column = 0, row = 0)
        self.ballR = Scale(self.ballScaleBackground, from_=0, to=255, command=self.setBallRed)
        self.ballR.grid(column = 0, row = 1)

        # tKinter scale that colors green inside detected ball, from 0 to 255
        self.ballLabelG = Label(self.ballScaleBackground, text = "Green", fg = "grey")
        self.ballLabelG.grid(column = 1, row = 0)
        self.ballG = Scale(self.ballScaleBackground, from_=0, to=255, command=self.setBallGreen)
        self.ballG.grid(column = 1, row = 1)

        # tKinter scale that colors blue inside detected ball, from 0 to 255
        self.ballLabelB = Label(self.ballScaleBackground, text = "Blue", fg = "grey")
        self.ballLabelB.grid(column = 2, row = 0)
        self.ballB = Scale(self.ballScaleBackground, from_=0, to=255, command=self.setBallBlue)
        self.ballB.grid(column = 2, row = 1)

        # Begin the main event loop in our root window now that the UI components are initialized
        self.root.mainloop()

    # Toggles record inside the camera object and color button based on record_is_on flag
    def RecordToggle(self):
        if self.record_is_on == False:
            self.recordButton.config(image = self.on) 
            self.recordLabel.config(fg = "green") 
            self.record_is_on = True
            self.camera.RecordTrue()
        else: 
            self.recordButton.config(image = self.off) 
            self.recordLabel.config(fg = "grey") 
            self.record_is_on = False
            self.camera.RecordFalse()
    
    # Toggles pro haar cascade in image and video objects, also colors buttons
    def ProToggle(self):
        if self.pro_is_on == False:
            self.proButton.config(image = self.on) 
            self.proLabel.config(fg = "green") 
            self.pro_is_on = True
            self.camera.UseProTrue()
            self.imagePlayer.UseProTrue()
            self.videoPlayer.UseProTrue()
        else: 
            self.proButton.config(image = self.off) 
            self.proLabel.config(fg = "grey") 
            self.pro_is_on = False
            self.camera.UseProFalse()
            self.imagePlayer.UseProFalse()
            self.videoPlayer.UseProFalse()
    
    # Toggles whether or not we want to color a detected face, changes button color
    def FaceSwitch(self):
        if self.face_is_on:
            self.faceButton.config(image = self.off) 
            self.faceLabel.config(fg = "grey")
            self.faceLabelR.config(fg = "grey")
            self.faceLabelG.config(fg = "grey") 
            self.faceLabelB.config(fg = "grey") 
            self.face_is_on = False
            self.faceColor.ColorFalse()
        else: 
            self.faceButton.config(image = self.on) 
            self.faceLabel.config(fg = "green") 
            self.faceLabelR.config(fg = "black")
            self.faceLabelG.config(fg = "black") 
            self.faceLabelB.config(fg = "black") 
            self.face_is_on = True
            self.faceColor.ColorTrue()
    
    # Toggles whether or not we want to color a detected ball, changes button color
    def BallSwitch(self):
        if self.ball_is_on:
            self.ballButton.config(image = self.off) 
            self.ballLabel.config(fg = "grey")
            self.ballLabelR.config(fg = "grey")
            self.ballLabelG.config(fg = "grey") 
            self.ballLabelB.config(fg = "grey") 
            self.ball_is_on = False
            self.ballColor.ColorFalse()
        else: 
            self.ballButton.config(image = self.on) 
            self.ballLabel.config(fg = "green") 
            self.ballLabelR.config(fg = "black")
            self.ballLabelG.config(fg = "black") 
            self.ballLabelB.config(fg = "black") 
            self.ball_is_on = True
            self.ballColor.ColorTrue()

    # Passes red, green, and blue values to face color object
    def setFaceRed(self, red):
        self.faceColor.SetRed(red)
    def setFaceGreen(self, green):
        self.faceColor.SetGreen(green)
    def setFaceBlue(self, blue):
        self.faceColor.SetBlue(blue)
    
    # Passes red, green, and blue values to ball color object
    def setBallRed(self, red):
        self.ballColor.SetRed(red)
    def setBallGreen(self, green):
        self.ballColor.SetGreen(green)
    def setBallBlue(self, blue):
        self.ballColor.SetBlue(blue)
    
    # Toggles destruction of root tkinter object
    def QuitGUI(self):
        self.root.destroy()
        self.root.quit()
    

############################################# ButtonObj Class #############################################
# Define a button object thats composed of 2 images, the hover and leave image
class ButtonObj:
    def __init__(self, curButton, enter, leave):
        self.curButton = curButton  # Which button were operating on
        self.enter = enter          # Image for when hovering over an image
        self.leave = leave          # Image for when were not hovering over and image
    
    # When the cursor is hovering over the button, set this image
    def on_enter(self, event):
        self.curButton.config(image=self.enter)
    
    # When the cursor leaves this button, set a different image
    def on_leave(self, event):
        self.curButton.config(image=self.leave)

############################################# ImagePlayer Class #############################################
# Defines the properties and behavior of playing an image in a tkinter window
class ImagePlayer:
    # initialize the image player variables
    def __init__(self, root, faceColor, ballColor):
        self.ImageFrameWidth = 600
        self.filename = ''
        self.use_pro = False
        self.haar = Haar(faceColor, ballColor)
    
    # Toggle the use of a pro cascade classifier
    def UseProTrue(self):
        self.use_pro = True
    
    # Toggle off the use of a pro cascade classifier
    def UseProFalse(self):
        self.use_pro = False

    # Allow user to select a .png, .jpg, or .jpeg image file using file explorer
    def BrowseFiles(self):
        # get the path of the image we want to show
        self.filename = filedialog.askopenfilename(initialdir = "C:/Users/Mason/Pictures/",
            title = "Select a File",
            filetypes = (("Media Files",
                        "*.png *.jpg *.jpeg"),
                        ("All Files", "*.*")))
        
        # Show media path in console for debugging
        # print("Image path: " + self.filename)

        # Display the image to the UI
        self.ShowImage(self.filename)
    
    # Displays the image to the UI
    def ShowImage(self, source):
        # Get only the images name from the system for labeling the image frame
        fileName = os.path.basename(source)

        # read the image into a image object
        img = cv2.imread(source)
        # resize the image while keeping the aspect ratio
        img = imutils.resize(img, width = self.ImageFrameWidth)
        
        # draw on the image with the detected object
        frameHaar = self.haar.Detect(img, self.use_pro)

        # show the image to the user using cv2
        cv2.imshow(fileName,frameHaar)

        # get the user key, if its ESC or 'q' then destroy the frame
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):
            cv2.destroyAllWindows()

############################################# VideoPlayer Class #############################################
# Defines the properties and behavior of playing a video in a tkinter window
class VideoPlayer:
    # initialize the video player variables
    def __init__(self, root, faceColor, ballColor):
        self.VideoFrameWidth = 1000
        self.VideoFrameHeight = 600
        self.use_pro = False
        self.haar = Haar(faceColor, ballColor)
    
    # Toggle the use of a pro cascade classifier
    def UseProTrue(self):
        self.use_pro = True
    
    # Toggle off the use of a pro cascade classifier
    def UseProFalse(self):
        self.use_pro = False

    # Allow user to select a .mov, .mp4, or .avi video file using file explorer
    def BrowseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "C:/Users/Mason/Videos/",
            title = "Select a File",
            filetypes = (("Media Files",
                        "*.mov *.mp4 *.avi"),
                        ("All Files", "*.*")))
        
        # Show media path in console for debugging
        # print("Video path: " + self.filename)

        # now that we have the file name then play the video
        self.PlayVideo(self.filename)

    # gets every frame of the video and display it
    def PlayVideo(self, source):
        # get the name of the video to label the window its displayed in
        fileName = os.path.basename(source)

        # Create a VideoCapture object and read from input file 
        cap = cv2.VideoCapture(source) 
        
        # Check if camera opened successfully 
        if (cap.isOpened()== False):  
            print("Error opening video file") 
        
        # Read until video is completed 
        while(cap.isOpened()): 
            
            # Capture frame-by-frame 
            ret, frame = cap.read() 

            # if we have a value frame then continue, added to avoid error at end of video
            if ret == True: 
                # resizes the video frame to be a reasonable size
                frame = imutils.resize(frame, width = self.VideoFrameWidth)
                frame = imutils.resize(frame, height = self.VideoFrameHeight)

                # see if we have detected any objects in this frame of the video
                frameHaar = self.haar.Detect(frame, self.use_pro)

                # Display the resulting frame 
                cv2.imshow(fileName, frameHaar) 
            
                # Press 'q' or ESC on keyboard to exit 
                k = cv2.waitKey(10) & 0xFF
                if k == 27 or k == ord('q'): 
                    break
            
            # Break the loop if no valid frame exists
            else:  
                break
        
        # When everything done, release  
        # the video capture object 
        cap.release() 
        
        # Closes all the frames 
        cv2.destroyAllWindows() 

############################################# Camera Class #############################################
# Defines the properties and behavior of playing a camera in a tkinter window
class Camera:
    # initialize the camera variables
    def __init__(self, root, faceColor, ballColor):
        self.record = False                     # flag for recording
        self.use_pro = False                    # flag for using a pro cascade
        self.haar = Haar(faceColor, ballColor)  # define the haar cascade object

    # triggers record flag to true
    def RecordTrue(self):
        self.record = True
    
    # triggers record flag to false
    def RecordFalse(self):
        self.record = False
    
    # triggers pro cascade flag to true
    def UseProTrue(self):
        self.use_pro = True
    
    # triggers pro cascade flag to false
    def UseProFalse(self):
        self.use_pro = False

    # loop for displaying every frame captured from the camera
    def DisplayCamera(self):

        # get the camera display object
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Define the codec and create VideoWriter object for writing the camera content to a file
        if(self.record):
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

        # while we have a camera input
        while(cap.isOpened()):
            # read a frame from the camera
            ret, frame = cap.read()

            # try to detect an object in this frame
            frameHaar = self.haar.Detect(frame, self.use_pro)

            # if we want to record then write the the frame to the output video
            if(self.record):
                out.write(frameHaar)

            # display the camera frame to a cv2 window
            cv2.imshow('Camera Output',frameHaar)

            # Press 'q' or ESC on keyboard to exit 
            k = cv2.waitKey(25) & 0xFF
            if k == 27 or k == ord('q'): 
                break

        # Release everything if job is finished
        cap.release()
        # if were recording then release the video output
        if(self.record):
            out.release()
        cv2.destroyAllWindows()

############################################# Haar Class #############################################
# Defines the properties and behavior of a haar cascade classifier
class Haar:
    # initialize the haar cascade variables
    def __init__(self, faceColor, ballColor):
        self.pro_face_cascade = cv2.CascadeClassifier('ProFaceHaarCascade.xml')     # professional cascade
        self.face_cascade = cv2.CascadeClassifier('FaceHaarCascade.xml')            # my face cascade
        self.tennis_cascade = cv2.CascadeClassifier('TennisBallHaarCascade.xml')    # my ball cascade
        self.faceColor = faceColor  # color editor object for coloring a face
        self.ballColor = ballColor  # color editor object for coloring a ball
    
    # try and detect an object within this frame
    def Detect(self, frame, use_pro):

        # Ensure the image has 3 color channels or else cvtColor will crash app
        if len(frame.shape) > 2:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame

        # if were using a pro cascade then do that, otherwise use our cascade
        if (use_pro == True):
            faces = self.pro_face_cascade.detectMultiScale(gray, 1.3, 5)
        else:
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        tennis = self.tennis_cascade.detectMultiScale(gray, 1.3, 5)
        
        # the cascade returns x and y coord of where the haar detected the face
        # and the width and height of that face
        for (x,y,w,h) in faces:

            # change the color of the detected object based on our selected RGB values
            frame = self.faceColor.ChannelEdit(frame, (x,y,w,h))

            # draw a rectangle around our detected face objects
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
        
        # the cascade returns x and y coord of where the haar detected the ball
        # and the width and height of that ball
        for (x,y,w,h) in tennis:

            # change the color of the detected object based on our selected RGB values
            frame = self.ballColor.ChannelEdit(frame, (x,y,w,h))

            # draw a rectangle around our detected ball objects
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
            cv2.putText(frame, 'Ball', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2, cv2.LINE_AA)
        
        # return the detected object so the players can display it
        return frame

############################################# ColorEditor Class #############################################
# Defines the properties and behavior coloring a detected object
class ColorEditor:
    # initialize the color editor variables
    def __init__(self):
        self.color = False  # flag for if we want to color the object or not
        self.red = 0        # the RGB values for what color we will make the detected object
        self.green = 0
        self.blue = 0
    
    # triggers color flag to true
    def ColorTrue(self):
        self.color = True
    
    # triggers color flag to false
    def ColorFalse(self):
        self.color = False
    
    # for setting the red value of RGB
    def SetRed(self, red):
        self.red = red

    # for setting the blue value of RGB
    def SetBlue(self, blue):
        self.blue = blue

    # for setting the green value of RGB
    def SetGreen(self, green):
        self.green = green

    # changes the frames color depending on selected RBG value
    def ChannelEdit(self, img, rect):
        # change colors of frame if weve chosen the color button
        if self.color:
            # get the coords of the detected object so we can color only that region
            x, y, w, h = rect

            # crop the image to the region weve detected an object
            detectedImg = img[y:y+h, x:x+w]

            # color the different RGB channels of the image based on our RBG selection
            detectedImg[:,:,2] = self.red
            detectedImg[:,:,1] = self.green
            detectedImg[:,:,0] = self.blue

            # place the colored image back onto the frame
            img[y:y+h, x:x+w] = detectedImg

            return img
        else:
            return img

# create the tkinter root window
App(Tk(), "OpenCV Media Editor")