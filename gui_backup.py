from tkinter import *
from tkinter import filedialog
from tkvideo import tkvideo
from PIL import Image, ImageTk
import cv2 
import numpy as np 
import time
import imutils
import os

class App:
    def __init__(self, window, windowTitle):
        self.backgroundColor = "#404040"
        self.root = window
        self.root.geometry("1000x600")
        self.root.config(background=self.backgroundColor)
        self.root.title(windowTitle)
        self.root.iconbitmap('images/icon.ico')

        self.ImageFrameWidth = 600
        self.ImageFrameHeight = 500
        self.imageFrameBackground = Frame(self.root, width=self.ImageFrameWidth, height=self.ImageFrameHeight)
        self.imageFrameBackground.grid(row=3, column=1, columnspan=3, padx=10, pady=2)

        self.imagePlayer = ImagePlayer(self.root)
        self.videoPlayer = VideoPlayer(self.root)

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
        self.openCam = Button(self.root, text = "Camera Feed", border= 0, command = self.videoPlayer.BrowseFiles) 
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
        self.exitButton = Button(self.root, text="Quit", border= 0, command=self.root.quit)
        self.exit_leave = PhotoImage(file="images/buttons/exit.png") # Location of exit buttons
        self.exit_enter = PhotoImage(file="images/buttons/exit2.png")
        self.exitButton.config(image=self.exit_leave)
        self.exitButton.grid(column = 4,row = 2) # Displaying the button

        # Create the exit button object and bind the events and images
        self.ExitButton = ButtonObj(self.exitButton, self.exit_enter, self.exit_leave)
        self.exitButton.bind("<Enter>", self.ExitButton.on_enter)
        self.exitButton.bind("<Leave>", self.ExitButton.on_leave)

        self.root.mainloop()
    


# Define a button object thats composed of 2 images, the hover and leave image
class ButtonObj:
    def __init__(self, curButton, enter, leave):
        self.curButton = curButton  # Which button were operating on
        self.enter = enter
        self.leave = leave
    
    # When the cursor is hovering over the button, set this image
    def on_enter(self, event):
        self.curButton.config(image=self.enter)
    
    # When the cursor leaves this button, set a different image
    def on_leave(self, event):
        self.curButton.config(image=self.leave)

# # Init exit buttons
# exitButton = Button(root, text="Quit", border= 0, command=root.quit)
# exit_leave = PhotoImage(file="images/buttons/exit.png") # Location of exit buttons
# exit_enter = PhotoImage(file="images/buttons/exit2.png")
# exitButton.config(image=exit_leave)
# exitButton.grid(column = 2,row = 2) # Displaying the button

# # Create the exit button object and bind the events and images
# ExitButton = ButtonObj(exitButton, exit_enter, exit_leave)
# exitButton.bind("<Enter>", ExitButton.on_enter)
# exitButton.bind("<Leave>", ExitButton.on_leave)

# ImageFrameWidth = 600
# ImageFrameHeight = 500
# imageFrameBackground = Frame(root, width=ImageFrameWidth, height=ImageFrameHeight)
# imageFrameBackground.grid(row=3, column=1, columnspan=3, padx=10, pady=2)
# imageFrame = Frame(root, width=ImageFrameWidth, height=ImageFrameHeight)
# imageFrame.grid(row=3, column=1, columnspan=3, padx=10, pady=2)

class ImagePlayer:
    def __init__(self, root):
        # Create image frame
        self.ImageFrameWidth = 600
        self.ImageFrameHeight = 500
        self.imageFrame = Frame(root, width=self.ImageFrameWidth, height=self.ImageFrameHeight)
        self.filename = ''
        # Create a File Explorer label
        self.fileExplorerLabel = Label(root, text = "Select Image/Video or Camera Feed", fg = "white", bg = "#404040")
        self.fileExplorerLabel.grid(column = 1, row = 1, columnspan=3)

        self.displayImage = Label() # Create the label that will hold the image

    # Allow user to select a .png, .jpg, or .jpeg image file using file explorer
    def BrowseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "C:/Users/Mason/Pictures/",
            title = "Select a File",
            filetypes = (("Media Files",
                        "*.png *.jpg *.jpeg"),
                        ("All Files", "*.*")))
        
        # Show media path in console for debugging
        print("Image path: " + self.filename)

        #self.DisplayImage() # Display the image to the UI
        self.showImage(self.filename)
    
    def showImage(self, source):
        fileName = os.path.basename(source)

        img = cv2.imread(source,0)
        img = imutils.resize(img, width = self.ImageFrameWidth)
        cv2.imshow(fileName,img)
        k = cv2.waitKey(0) & 0xFF
        if k == 27 or k == ord('q'):         # wait for ESC key to exit
            cv2.destroyAllWindows()

    # Scale an image to the size of the global frame dimensions imageFrame, returns a tuple of width and height
    def GetScale(self, imgWidth, imgHeight):
        if imgWidth > imgHeight:
            self.scale = self.ImageFrameWidth / imgWidth
        else:
            self.scale = self.ImageFrameHeight / imgHeight
        # Scale the image, subtract 5 pixels to account for image border
        self.width = int(imgWidth * self.scale) - 5
        self.height = int(imgHeight * self.scale) - 5
        self.dsize = (self.width, self.height)
        return self.dsize
    
    def DisplayImage(self):
        self.displayImage.grid_forget()  # Forget the label to clear the frame of any existing images for the upcoming image
        self.imageFrame.grid(row=3, column=1, columnspan=3, padx=10, pady=2) # Add the image frame to the root view
        self.fileExplorerLabel.configure(text="Image File Opened: " + self.filename)  # Display the image path

        # Open unscaled image in cv2 and measure its height and width in pixels
        self.imgUnscaled = cv2.imread(self.filename)    # Read the image using cv2
        if self.imgUnscaled is None:                    # Error handling, ensure the image is opened correctly
            raise ValueError("Unable to open image source", self.filename)
            return
        self.imgWidth = int(self.imgUnscaled.shape[1])  # Get height and width of image before scaling
        self.imgHeight = int(self.imgUnscaled.shape[0])

        # print image height/width and frame height/width to console for debugging
        print("img width: "+str(self.imgWidth))
        print("img height: "+str(self.imgHeight))
        print("frame width: "+str(self.ImageFrameWidth))
        print("frame height: "+str(self.ImageFrameHeight))

        # Scale image to fit the frame
        if self.imgWidth > self.ImageFrameWidth and self.imgHeight > self.ImageFrameHeight:
            self.dsize = self.GetScale(self.imgWidth, self.imgHeight)
            self.img = cv2.resize(self.imgUnscaled, self.dsize)    # Resize the image
            print("Bigger than frame")              # Debugging
            print("img width: "+str(self.img.shape[1]))
            print("img height: "+str(self.img.shape[0]))
        elif self.imgWidth < self.ImageFrameWidth and self.imgHeight < self.ImageFrameHeight:
            print("Smaller than frame")
            self.img = self.imgUnscaled   # If image is smaller than the frame then dont scale it, just pass image along
        elif self.imgWidth > self.ImageFrameWidth:
            self.dsize = self.GetScale(self.imgWidth, self.imgHeight)
            self.img = cv2.resize(self.imgUnscaled, self.dsize)    # Resize the image
            print("Wider than frame")
            print("img width: "+str(self.img.shape[1]))  # Debugging
            print("img height: "+str(self.img.shape[0]))
        elif self.imgHeight > self.ImageFrameHeight:
            self.dsize = self.GetScale(self.imgWidth, self.imgHeight)
            self.img = cv2.resize(self.imgUnscaled, self.dsize)    # Resize the image
            print("Taller than frame")
            print("img width: "+str(self.img.shape[1]))  # Debugging
            print("img height: "+str(self.img.shape[0]))
        else:
            print("Same size as frame")
            self.img = self.imgUnscaled   # If image is the same size as the frame then dont scale it

        # Convert the Image object into a TkPhoto object so we can place it in a frame
        self.cv2image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGBA)
        self.im = Image.fromarray(self.cv2image)
        self.imgtk = ImageTk.PhotoImage(image=self.im) 
        # Put it in the display window
        self.displayImage = Label(self.imageFrame)
        self.displayImage.grid(row=0, column=0)
        self.displayImage.imgtk = self.imgtk
        self.displayImage.configure(image=self.imgtk)

class VideoPlayer:
    def __init__(self, root):
        # Create video frame
        self.VideoFrameWidth = 1000
    
    # Allow user to select a .mov, .mp4, or .avi video file using file explorer
    def BrowseFiles(self):
        self.filename = filedialog.askopenfilename(initialdir = "C:/Users/Mason/Videos/",
            title = "Select a File",
            filetypes = (("Media Files",
                        "*.mov *.mp4 *.avi"),
                        ("All Files", "*.*")))
        
        # Show media path in console for debugging
        print("Video path: " + self.filename)

        self.playVideo(self.filename)

    def playVideo(self, source):
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

            frame = imutils.resize(frame, width = self.VideoFrameWidth)
            if ret == True: 
            
                # Display the resulting frame 
                cv2.imshow(fileName, frame) 
            
                # Press Q on keyboard to  exit 
                k = cv2.waitKey(25) & 0xFF
                if k == 27 or k == ord('q'): 
                    break
            
            # Break the loop 
            else:  
                break
        
        # When everything done, release  
        # the video capture object 
        cap.release() 
        
        # Closes all the frames 
        cv2.destroyAllWindows() 

        # ret, frame = self.vid.get_frame() # Get a frame from the video source
        # self.videoFrame.grid(row=3, column=1, columnspan=3, padx=10, pady=2) # Add frame to root view

        # if ret:
        #     # Resize frame
        #     self.width = int(frame.shape[1])
        #     self.height = int(frame.shape[0])
        #     self.dsize = self.GetScale(self.width, self.height)
        #     self.FrameResized = cv2.resize(frame, self.dsize, interpolation =cv2.INTER_AREA)

        #     self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.FrameResized))
        #     self.lmain.photo = self.photo
        #     self.lmain.configure(image=self.photo)
        #     #self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        # self.lmain.after(15, self.update)
    
    

# displayImage = Label() # Create a global label that will hold the image were displaying
# # Allow user to select a file
# def BrowseFiles():
#     global ImageFrameWidth      # Image frame width
#     global ImageFrameHeight     # Image frame height
#     global displayImage         # Image label
#     displayImage.grid_forget()  # Forget the label to clear the frame for the upcoming image
#     filename = filedialog.askopenfilename(initialdir = "C:/Users/Mason/Pictures/",
#         title = "Select a File",
#         filetypes = (("Media Files",
#                     "*.png *.jpg *.jpeg *.mp4 *.avi"),
#                     ("All Files", "*.*")))
    
#     # Show media path in console for debugging
#     print("Media path: " + filename)

#     # If the file is an image then process it using opencv image processing
#     if (".png" in filename) or (".jpg" in filename) or (".jpeg" in filename):
#         fileExplorerLabel.configure(text="Image File Opened: " + filename)  # Display in frame the image path

#         # Open unscaled image in cv2 and measure its height and width in pixels
#         imgUnscaled = cv2.imread(filename)
#         if imgUnscaled is None:     # Error handling, ensure the image is opened correctly
#             raise ValueError("Unable to open image source", filename)
#             return
#         imgWidth = int(imgUnscaled.shape[1])
#         imgHeight = int(imgUnscaled.shape[0])

#         # print image height/width and frame height/width to console for debugging
#         print("img width: "+str(imgWidth))
#         print("img height: "+str(imgHeight))
#         print("frame width: "+str(ImageFrameWidth))
#         print("frame height: "+str(ImageFrameHeight))

#         # Scale image to fit the frame
#         if imgWidth > ImageFrameWidth and imgHeight > ImageFrameHeight:
#             dsize = GetScale(imgWidth, imgHeight)
#             img = cv2.resize(imgUnscaled, dsize)    # Resize the image
#             print("Bigger than frame")              # Debugging
#             print("img width: "+str(img.shape[1]))
#             print("img height: "+str(img.shape[0]))
#         elif imgWidth < ImageFrameWidth and imgHeight < ImageFrameHeight:
#             print("Smaller than frame")
#             img = imgUnscaled   # If image is smaller than the frame then dont scale it, just pass image along
#         elif imgWidth > ImageFrameWidth:
#             dsize = GetScale(imgWidth, imgHeight)
#             img = cv2.resize(imgUnscaled, dsize)    # Resize the image
#             print("Wider than frame")
#             print("img width: "+str(img.shape[1]))  # Debugging
#             print("img height: "+str(img.shape[0]))
#         elif imgHeight > ImageFrameHeight:
#             dsize = GetScale(imgWidth, imgHeight)
#             img = cv2.resize(imgUnscaled, dsize)    # Resize the image
#             print("Taller than frame")
#             print("img width: "+str(img.shape[1]))  # Debugging
#             print("img height: "+str(img.shape[0]))
#         else:
#             print("Same size as frame")
#             img = imgUnscaled   # If image is the same size as the frame then dont scale it

#         # Convert the Image object into a TkPhoto object so we can place it in a frame
#         cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
#         im = Image.fromarray(cv2image)
#         imgtk = ImageTk.PhotoImage(image=im) 
#         # Put it in the display window
#         displayImage = Label(imageFrame)
#         displayImage.grid(row=0, column=0)
#         displayImage.imgtk = imgtk
#         displayImage.configure(image=imgtk)

#     elif ".mp4" in filename or ".avi" in filename:  # If file is a video then process it as a video
#         fileExplorerLabel.configure(text="Video File Opened: "+filename)
#         cap = cv2.VideoCapture(filename)
#         if not cap.isOpened():     # Error handling, ensure the video is opened correctly
#             raise ValueError("Unable to open video source", filename)
#             return
#         lmain = Label(imageFrame)
#         lmain.grid(row=0, column=0)
#         def show_frame():
#             global cameraFlag

#             # If camera button is untoggled then stop showing camera feed, otherwise continue
#             if cameraFlag == 0:
#                 cap.release()
#                 print("exiting")
#                 lmain.grid_forget()
#                 cap.release()
#                 cameraFlag = 1
#                 return
#             else:
#                 _, frame = cap.read()       # Grab a frame from the video capture
#                 frame = cv2.flip(frame, 1)  # Flip the camera along the vertical axis

#                 # Resize frame
#                 width = int(frame.shape[1])
#                 height = int(frame.shape[0])
#                 dsize = GetScale(width, height)
#                 FrameResized = cv2.resize(frame, dsize, interpolation =cv2.INTER_AREA)

#                 cv2image = cv2.cvtColor(FrameResized, cv2.COLOR_BGR2RGBA)   # Change color format from bgr to rgba
#                 # Convert the Image object into a TkPhoto object so we can place it in a frame
#                 img = Image.fromarray(cv2image)
#                 imgtk = ImageTk.PhotoImage(image=img)
#                 lmain.imgtk = imgtk
#                 lmain.configure(image=imgtk)
#                 lmain.after(10, show_frame)     # Repeat every 10ms while camera button is toggled

#         show_frame()  #Display 2
#     else:
#         fileExplorerLabel.configure(text="Please Open Image of Video File")

# # Create a File Explorer label
# fileExplorerLabel = Label(root, text = "Select Image/Video or Camera Feed", fg = "white", bg = backgroundColor)

# # Init file explorer button
# exploreButton = Button(root, text = "Browse Files", border= 0, command = BrowseFiles) 
# browse_leave = PhotoImage(file="images/buttons/browse.png") # Location of exit buttons
# browse_enter = PhotoImage(file="images/buttons/browse2.png")
# exploreButton.config(image=browse_leave)
# fileExplorerLabel.grid(column = 1, row = 1, columnspan=3)
# exploreButton.grid(column = 1, row = 2)

# # Create the exit button object and bind the events and images
# ExploreButton = ButtonObj(exploreButton, browse_enter, browse_leave)
# exploreButton.bind("<Enter>", ExploreButton.on_enter)
# exploreButton.bind("<Leave>", ExploreButton.on_leave)

# cameraFlag = 1

# def ActivateCamera():
#     global cameraFlag
#     print("cameraFlag: " + str(cameraFlag))
#     cap = cv2.VideoCapture(0)
#     lmain = Label(imageFrame)
#     lmain.grid(row=0, column=0)
#     def show_frame():
#         global cameraFlag

#         # If camera button is untoggled then stop showing camera feed, otherwise continue
#         if cameraFlag == 0:
#             cap.release()
#             print("exiting")
#             lmain.grid_forget()
#             cap.release()
#             cameraFlag = 1
#             return
#         else:
#             _, frame = cap.read()       # Grab a frame from the video capture
#             frame = cv2.flip(frame, 1)  # Flip the camera along the vertical axis

#             # Resize frame
#             width = int(frame.shape[1])
#             height = int(frame.shape[0])
#             dsize = GetScale(width, height)
#             FrameResized = cv2.resize(frame, dsize, interpolation =cv2.INTER_AREA)

#             cv2image = cv2.cvtColor(FrameResized, cv2.COLOR_BGR2RGBA)   # Change color format from bgr to rgba
#             # Convert the Image object into a TkPhoto object so we can place it in a frame
#             img = Image.fromarray(cv2image)
#             imgtk = ImageTk.PhotoImage(image=img)
#             lmain.imgtk = imgtk
#             lmain.configure(image=imgtk)
#             lmain.after(10, show_frame)     # Repeat every 10ms while camera button is toggled

#     show_frame()  #Display 2

# def IsCameraOn():
#     global cameraFlag
#     if cameraButton['text'] == "on":
#         cameraButton.configure(text="off", image=camera_enter)
#         ActivateCamera()
#     else:
#         cameraButton.configure(text="on", image=camera_leave)
#         cameraFlag = 0
#         print("cameraFlag is now 0")


# # Init camera buttons
# cameraButton = Button(root, text="on", border= 0, command=IsCameraOn)
# camera_leave = PhotoImage(file="images/buttons/camera.png") # Location of camera buttons
# camera_enter = PhotoImage(file="images/buttons/camera2.png")
# cameraButton.config(image=camera_leave)
# cameraButton.grid(column = 3,row = 2) # Displaying the button

App(Tk(), "OpenCV Media Editor")
# root.mainloop()