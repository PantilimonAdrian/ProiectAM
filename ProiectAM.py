from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import cv2
import numpy as np

global processedImage
global initialImage

global negativeImage
global negativeImageCV2
global logarithmicImage
global logarithmicImageCV2
global nthPowerImage
global nthPowerImageCV2

# Value of gamma for the nth power transformation
global gamma
isGammaSet = False

# Variables used to check if an image has been processed using a specific method
hasNegativeBeenProcessed = False
hasLogarithmicBeenProcessed = False
hasNthPowerBeenProcessed = False
# Variable that is used to verify if an image has been uploaded to the app
isImageUploaded = False


# Function definition to open a new image
def openImage():
    global imageOpened
    global initialImage
    global isImageUploaded
    global hasNegativeBeenProcessed
    global hasLogarithmicBeenProcessed
    global hasNthPowerBeenProcessed
    global imageFrame1
    global imageFrame2
    global imageFrame3
    global imageFrame4
    # Image format accepted to be uploaded
    listOfFileTypes = [('jpg', '*.jpg'), ('bmp', '*.bmp'), ('png', '*.png')]
    # Ask for the path of the image that will be processed
    imageFilePath = filedialog.askopenfilename(initialdir="/",
                                               title="Choose an image for edit",
                                               filetypes=listOfFileTypes)
    if imageFilePath != '':
        # Get image that will be displayed
        imageOpened = ImageTk.PhotoImage(Image.open(imageFilePath).resize((280, 300), Image.ANTIALIAS))
        # Read image with cv2 to be processed
        initialImage = cv2.imread(imageFilePath)
        # Activate the checkboxes after image has been uploaded
        checkBoxNegativeGray['state'] = NORMAL
        checkBoxLogarithmicGray['state'] = NORMAL
        checkBoxNthPowerGray['state'] = NORMAL
        # Check if label for original image was created if not then create it otherwise just change the image.
        if not isImageUploaded:
            imageFrame1 = Label(imagesFrame,
                                image=imageOpened,
                                text='Original image',
                                font=("Helvetica", 14, 'bold'),
                                compound='top',
                                bg='#343a40',
                                fg='white')
            imageFrame1.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            isImageUploaded = True
        else:
            # If a new image is uploaded the image will change and all the previous processed images will disappear
            imageFrame1['image'] = imageOpened
            zoomButton.pack_forget()
            if hasNegativeBeenProcessed:
                imageFrame2.pack_forget()
                hasNegativeBeenProcessed = False
            if hasLogarithmicBeenProcessed:
                imageFrame3.pack_forget()
                hasLogarithmicBeenProcessed = False
            if hasNthPowerBeenProcessed:
                imageFrame4.pack_forget()
                hasNthPowerBeenProcessed = False


# Function definition to save an image
def saveImage():
    global initialImage
    # Images stored that will be saved according to the user option
    global negativeImageCV2
    global logarithmicImageCV2
    global nthPowerImageCV2

    def invalidateOthers():
        if saveNegative.get():
            checkSaveLogarithmic['state'] = DISABLED
            checkSavePower['state'] = DISABLED
            saveButton['state'] = NORMAL
        elif saveLogarithmic.get():
            checkSaveNegative['state'] = DISABLED
            checkSavePower['state'] = DISABLED
            saveButton['state'] = NORMAL
        elif savePower.get():
            checkSaveLogarithmic['state'] = DISABLED
            checkSaveNegative['state'] = DISABLED
            saveButton['state'] = NORMAL
        else:
            checkSaveLogarithmic['state'] = NORMAL
            checkSaveNegative['state'] = NORMAL
            checkSavePower['state'] = NORMAL
            saveButton['state'] = DISABLED

    def saveTheFile():
        listOfFileTypes = [('jpg', '*.jpg'), ('bmp', '*.bmp'), ('png', '*.png')]  # Formats for image to be saved
        saveFile = filedialog.asksaveasfile(initialdir="/",
                                            title="Save image as",
                                            mode='w',
                                            filetypes=listOfFileTypes,
                                            defaultextension=listOfFileTypes)
        if saveFile != '' and saveNegative.get():
            cv2.imwrite(saveFile.name, negativeImageCV2)
        elif saveFile != '' and saveLogarithmic.get():
            cv2.imwrite(saveFile.name, logarithmicImageCV2)
        elif saveFile != '' and savePower.get():
            cv2.imwrite(saveFile.name, nthPowerImageCV2)

    # Create a save option window
    saveWindow = Toplevel()
    # Window dimensions
    saveWindow.geometry("320x200")
    # Window title
    saveWindow.title("Select transformation image")
    # Turn image into a PhotoImage, so it can be used by tkinter
    logoSaveImage = PhotoImage(file='logo.png')
    # Add the icon to the window
    saveWindow.iconphoto(False, logoSaveImage)
    # Window background color
    saveWindow.config(background="#343a40")

    infoLabel = Label(saveWindow,
                      bg='#343a40',
                      font=("Helvetica", 10, 'bold'),
                      fg='white')
    infoLabel.pack(ipadx=15, ipady=15, fill='x')

    if not hasNegativeBeenProcessed and not hasLogarithmicBeenProcessed and not hasNthPowerBeenProcessed:
        infoLabel.configure(text=' You can not save an image at this moment ')
    else:
        infoLabel.configure(text=' Select the image you want to save ')
        saveNegative = BooleanVar()
        saveLogarithmic = BooleanVar()
        savePower = BooleanVar()
        checkSaveNegative = Checkbutton(saveWindow,
                                        text='Negative transformation',
                                        font=("Helvetica", 10, 'bold'),
                                        command=invalidateOthers,
                                        variable=saveNegative,
                                        onvalue=True,
                                        offvalue=False,
                                        fg='white',
                                        bg='#343a40',
                                        selectcolor='#219ebc',
                                        activebackground='#343a40',
                                        activeforeground='white')
        checkSaveNegative['state'] = DISABLED

        checkSaveLogarithmic = Checkbutton(saveWindow,
                                           text='Logarithmic transformation',
                                           font=("Helvetica", 10, 'bold'),
                                           command=invalidateOthers,
                                           variable=saveLogarithmic,
                                           onvalue=True,
                                           offvalue=False,
                                           fg='white',
                                           bg='#343a40',
                                           selectcolor='#219ebc',
                                           activebackground='#343a40',
                                           activeforeground='white')
        checkSaveLogarithmic['state'] = DISABLED

        checkSavePower = Checkbutton(saveWindow,
                                     text='Power-Law transformation',
                                     font=("Helvetica", 10, 'bold'),
                                     variable=savePower,
                                     command=invalidateOthers,
                                     onvalue=True,
                                     offvalue=False,
                                     fg='white',
                                     bg='#343a40',
                                     selectcolor='#219ebc',
                                     activebackground='#343a40',
                                     activeforeground='white')
        checkSavePower['state'] = DISABLED

        checkSaveNegative.pack(ipadx=10,
                               ipady=5,
                               expand=True,
                               fill='x')
        checkSaveLogarithmic.pack(ipadx=10,
                                  ipady=5,
                                  expand=True,
                                  fill='x')
        checkSavePower.pack(ipadx=10,
                            ipady=5,
                            expand=True,
                            fill='x')

        saveButton = Button(saveWindow,
                            image=saveIcon,
                            command=saveTheFile,
                            text=' Save',
                            font=("Helvetica", 10, 'bold'),
                            compound='left',
                            bg="#0077b6",
                            fg='white',
                            activebackground='#0096c7',
                            activeforeground='white',
                            relief="ridge")
        saveButton['state'] = DISABLED
        saveButton.pack(ipadx=10,
                        ipady=10,
                        pady=5,
                        fill='y')

        if hasNegativeBeenProcessed:
            checkSaveNegative['state'] = NORMAL
        if hasLogarithmicBeenProcessed:
            checkSaveLogarithmic['state'] = NORMAL
        if hasNthPowerBeenProcessed:
            checkSavePower['state'] = NORMAL


########################################
# Functions used to transform an image #
########################################
# Negative transformation function that returns a openCV2 image
def negativeTransformation(image):
    # Formula: img_negative = 255 - image
    # Creating the negative image
    # Decompose image into three separate color channels
    # and apply the formula for each pixel from that channel
    # b,g,r = cv2.split(image)
    # img_negative = image
    # img_negative[:,:,0] = 255 - b
    # img_negative[:,:,1] = 255 - g
    # img_negative[:,:,2] = 255 - r
    # Another way to implement it in an easier manner
    img_negative = 255 - image
    return img_negative


# Logarithmic transformation function that returns a openCV2 image
def logarithmicTransformation(image):
    # applying log transformation with best c
    c = int(255 / (np.log(1 + np.max(image))))

    logarithmicImage = c * np.log(1 + image)
    # create image
    imageLog = np.array(logarithmicImage, dtype='uint8')
    return imageLog


# Power Law transformation function that returns a openCV2 image
def powerLawTransformation(image, gammaValue):
    # Formula : s = c*r^gamma
    # Here we consider c = 255 and r = colorLayerPixelIntensity/255
    # that is because we have to take into consideration that when
    # we raise to the power of gamma the value will exceed 8 bit = 255,
    # so we need to normalize the value in order to achieve power - law
    # transformation.
    imagePower = np.array((255 * (image / 255) ** gammaValue), dtype='uint8')
    return imagePower


##################################
# Function used in the help menu #
##################################
# Function to show how to use the app in another window
def howToUseApp():
    # Create a how to use window
    useWindow = Toplevel()
    # Window dimensions
    useWindow.geometry("640x595")
    # Window title
    useWindow.title("How to use this app")
    # Turn image into a PhotoImage, so it can be used by tkinter
    logoUseImage = PhotoImage(file='logo.png')
    # Add the icon to the window
    useWindow.iconphoto(False, logoUseImage)
    # Window background color
    useWindow.config(background="#343a40")

    # Use Window title
    titleUseWindow = Label(useWindow,
                           text=' Steps ',
                           bg='#343a40',
                           font=("Helvetica", 14, 'bold'),
                           fg='white')
    titleUseWindow.pack(ipadx=10,
                        ipady=10,
                        fill='x')

    stepOne = Label(useWindow,
                    text='Step 1: Press the \'Open new image\' button and select an image you want to transform. \n '
                         'Now all the transformation buttons will become active.',
                    bg='#343a40',
                    font=("Helvetica", 10, 'bold'),
                    fg='white')
    stepOne.pack(ipadx=15,
                 ipady=5,
                 fill='x')
    stepTwo = Label(useWindow,
                    text='Step 2: Check the box or boxes for which transformation/transformations you want to '
                         'perform.\n After this you will see that the \'Process image\' button will become active.',
                    bg='#343a40',
                    font=("Helvetica", 10, 'bold'),
                    fg='white')
    stepTwo.pack(ipadx=15,
                 ipady=5,
                 fill='x')
    stepThree = Label(useWindow,
                      text='Step 3: Press the \'Process image\' button to start processing the image and wait a few '
                           'moments \n to get the resulting images. Now you can see the image/images of the '
                           'transformations \n you selected displayed on the main window.',
                      bg='#343a40',
                      font=("Helvetica", 10, 'bold'),
                      fg='white')
    stepThree.pack(ipadx=15,
                   ipady=5,
                   fill='x')

    stepFour = Label(useWindow,
                     text='Step 4: Now you can choose to either process a new image following the same steps as \n '
                          'before or save the transformation image or images you managed to obtain. To save the \n '
                          'image/images you need to go to the top of the application and in the file menu you will \n '
                          'find the option to save those images or image.',
                     bg='#343a40',
                     font=("Helvetica", 10, 'bold'),
                     fg='white')
    stepFour.pack(ipadx=15,
                  ipady=5,
                  fill='x')
    stepFive = Label(useWindow,
                     text='Step 5: After the \'Save button\' button is pressed a window will be displayed from which '
                          'you will\n select which transformed image will be saved. The \'Save\' button will be '
                          'available and\n after it is pressed you will need to select the location and the name so '
                          '\n the image can be saved.',
                     bg='#343a40',
                     font=("Helvetica", 10, 'bold'),
                     fg='white')
    stepFive.pack(ipadx=15,
                  ipady=5,
                  fill='x')

    zoomInfoLabel = Label(useWindow,
                          text='Zoom: After an image is processed the \'Zoom image\' button will be available, '
                               'if you press it \na new window will pop up letting you choose which image you want to '
                               'zoom. After you select\n the images you want to zoom you just need to press the zoom '
                               'button and a number of different\n windows will pop up letting you zoom using scroll '
                               'or the specific buttons on the top. If you want\n to close this feature you just need '
                               'to press any key on you keyboard \nand those windows will automatically shut down.',
                          bg='#343a40',
                          font=("Helvetica", 10, 'bold'),
                          fg='white')
    zoomInfoLabel.pack(ipadx=15,
                       ipady=5,
                       fill='x')

    otherInfo = Label(useWindow,
                      text='Other information can be found in the application documentation,\n press the button below '
                           'to check it out.',
                      bg='#343a40',
                      font=("Helvetica", 10, 'bold'),
                      fg='white')
    otherInfo.pack(ipadx=15,
                   ipady=5,
                   fill='x')

    moreInfoButton = Button(useWindow,
                            image=infoIcon,
                            command=openExternalLink,
                            text=' More info',
                            font=("Helvetica", 10, 'bold'),
                            compound='left',
                            bg="#0077b6",
                            fg='white',
                            activebackground='#0096c7',
                            activeforeground='white',
                            relief="ridge")
    moreInfoButton.pack(ipadx=10,
                        ipady=10,
                        pady=5)


# Function used to display app documentation on the web
def openExternalLink():
    webbrowser.open_new(
        "https://docs.google.com/document/d/1kpqbBffdTEgqJLhtjEsc4VGfAIVr3svZ703kmUtfuCo/edit?usp=sharing")


###################################

#########################################################################################################
# Functions of the check buttons used to activate the process button and remove the image if unchecked. #
#########################################################################################################
# Function check button negative image used to activate button and remove negative image
def displayNegative():
    global imageFrame2
    global hasNegativeBeenProcessed
    if negativeGrayCheckVar.get() and isImageUploaded:
        processButton['state'] = NORMAL
    else:
        if not (LogarithmGrayCheckVar.get()) and not (nthPowerCheckVar.get()):
            processButton['state'] = DISABLED
        if hasNegativeBeenProcessed:
            imageFrame2.pack_forget()
            hasNegativeBeenProcessed = False
            if not (LogarithmGrayCheckVar.get()) and not (nthPowerCheckVar.get()):
                zoomButton.pack_forget()


# Function check button logarithmic image used to activate button and remove logarithmic image
def displayLogarithmic():
    global imageFrame3
    global hasLogarithmicBeenProcessed
    if LogarithmGrayCheckVar.get() and isImageUploaded:
        processButton['state'] = NORMAL
    else:
        if not (negativeGrayCheckVar.get()) and not (nthPowerCheckVar.get()):
            processButton['state'] = DISABLED
        if hasLogarithmicBeenProcessed:
            imageFrame3.pack_forget()
            hasLogarithmicBeenProcessed = False
            if not (negativeGrayCheckVar.get()) and not (nthPowerCheckVar.get()):
                zoomButton.pack_forget()


# Function check button power law image used to activate button and remove power law image
def displayNthPower():
    global imageFrame4
    global gamma
    global hasNthPowerBeenProcessed
    if nthPowerCheckVar.get() and isImageUploaded:
        def checkGamma():
            global gamma
            global isGammaSet
            try:
                entryValue = float(entryGammaValue.get())
                try:
                    if 0 < entryValue <= 25:
                        gamma = entryValue
                        isGammaSet = True
                        processButton['state'] = NORMAL
                        gammaWindow.destroy()
                    else:
                        isGammaSet = False
                        # print("Enter valid gamma")
                        raise Exception()
                except Exception:
                    nthPowerCheckVar.set(False)
                    gammaWindow.destroy()
                    messagebox.showerror('Invalid value', 'Something went wrong!\nYour value is out of range!')
            except ValueError:
                nthPowerCheckVar.set(False)
                gammaWindow.destroy()
                messagebox.showerror('Invalid value', 'Something went wrong!\nYou need to introduce a decimal value!')

        # Create a how to use window
        gammaWindow = Toplevel()
        # Window dimensions
        gammaWindow.geometry("320x200")
        # Window title
        gammaWindow.title("Set gamma value ")
        # Turn image into a PhotoImage, so it can be used by tkinter
        logoGammaImage = PhotoImage(file='logo.png')
        # Add the icon to the window
        gammaWindow.iconphoto(False, logoGammaImage)
        # Window background color
        gammaWindow.config(background="#343a40")

        titleWindowGamma = Label(gammaWindow,
                                 text=' Choose gamma value ',
                                 bg='#343a40',
                                 font=("Helvetica", 14, 'bold'),
                                 fg='white')
        titleWindowGamma.pack(ipadx=15, ipady=15, fill='x')

        infoGamma = Label(gammaWindow,
                          text=' Enter a decimal value between 0.0 and 25.0 ',
                          bg='#343a40',
                          font=("Helvetica", 10, 'bold'),
                          fg='white')
        infoGamma.pack(ipadx=10, fill='x')

        entryGammaValue = Entry(gammaWindow)
        entryGammaValue.pack(expand=True)

        submitGammaValue = Button(gammaWindow,
                                  image=numberIcon,
                                  command=checkGamma,
                                  text=' Submit gamma value',
                                  font=("Helvetica", 10, 'bold'),
                                  compound='left',
                                  bg="#0077b6",
                                  fg='white',
                                  activebackground='#0096c7',
                                  activeforeground='white',
                                  relief="ridge")
        submitGammaValue.pack(ipadx=10,
                              ipady=10,
                              pady=5,
                              expand=True)
    else:
        if not (LogarithmGrayCheckVar.get()) and not (negativeGrayCheckVar.get()):
            processButton['state'] = DISABLED
        if hasNthPowerBeenProcessed:
            imageFrame4.pack_forget()
            hasNthPowerBeenProcessed = False
            if not (LogarithmGrayCheckVar.get()) and not (negativeGrayCheckVar.get()):
                zoomButton.pack_forget()


#######################################################################

# Function used to process the original image and display the results
def processImage():
    global initialImage

    global imageFrame2
    global imageFrame3
    global imageFrame4

    global processedImage

    global hasNegativeBeenProcessed
    global hasLogarithmicBeenProcessed
    global hasNthPowerBeenProcessed

    global negativeImage
    global negativeImageCV2
    global logarithmicImage
    global logarithmicImageCV2
    global nthPowerImage
    global nthPowerImageCV2

    global gamma

    if negativeGrayCheckVar.get() and isImageUploaded and processButton['state'] == NORMAL:
        negativeImageCV2 = negativeTransformation(initialImage)
        negativeImage = conversionCV2toImageTk(negativeImageCV2)
        if not hasNegativeBeenProcessed:
            imageFrame2 = Label(imagesFrame,
                                image=negativeImage,
                                text='Negative transformation image',
                                font=("Helvetica", 14, 'bold'),
                                compound='top',
                                bg='#343a40',
                                fg='white')
            imageFrame2.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            hasNegativeBeenProcessed = True
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')
        else:
            negativeImageCV2 = negativeTransformation(initialImage)
            negativeImage = conversionCV2toImageTk(negativeImageCV2)
            imageFrame2.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            imageFrame2['image'] = negativeImage
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')

    if LogarithmGrayCheckVar.get() and isImageUploaded and processButton['state'] == NORMAL:

        logarithmicImageCV2 = logarithmicTransformation(initialImage)
        logarithmicImage = conversionCV2toImageTk(logarithmicImageCV2)
        if not hasLogarithmicBeenProcessed:
            imageFrame3 = Label(imagesFrame,
                                image=logarithmicImage,
                                text='Logarithmic transformation image',
                                font=("Helvetica", 14, 'bold'),
                                compound='top',
                                bg='#343a40',
                                fg='white')
            imageFrame3.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            hasLogarithmicBeenProcessed = True
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')
        else:
            logarithmicImageCV2 = logarithmicTransformation(initialImage)
            logarithmicImage = conversionCV2toImageTk(logarithmicImageCV2)
            imageFrame3.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            imageFrame3['image'] = logarithmicImage
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')

    if nthPowerCheckVar.get() and isImageUploaded and processButton['state'] == NORMAL and isGammaSet:

        nthPowerImageCV2 = powerLawTransformation(initialImage, gamma)
        nthPowerImage = conversionCV2toImageTk(nthPowerImageCV2)
        if not hasNthPowerBeenProcessed:
            imageFrame4 = Label(imagesFrame,
                                image=nthPowerImage,
                                text='Power-Law transformation image',
                                font=("Helvetica", 14, 'bold'),
                                compound='top',
                                bg='#343a40',
                                fg='white')
            imageFrame4.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            hasNthPowerBeenProcessed = True
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')
        else:
            nthPowerImageCV2 = powerLawTransformation(initialImage, gamma)
            nthPowerImage = conversionCV2toImageTk(nthPowerImageCV2)
            imageFrame4.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='both',
                             side='left')
            imageFrame4['image'] = nthPowerImage
            zoomButton.pack(ipadx=10,
                            ipady=10,
                            pady=5,
                            expand=True,
                            fill='y',
                            side='left')


# Function used to convert a cv2 image to PhotoImage tkinter
def conversionCV2toImageTk(imageCV2):
    # cv2 image conversion from BGR to RGB
    imageCV2_RGB = cv2.cvtColor(imageCV2, cv2.COLOR_BGR2RGB)
    return ImageTk.PhotoImage(image=Image.fromarray(imageCV2_RGB).resize((280, 300)))


# Function used to zoom images using openCV2
def zoomImage():
    global initialImage
    global negativeImageCV2
    global logarithmicImageCV2
    global nthPowerImageCV2

    def validateZoom():
        if (zoomOriginal.get() or
                zoomNegative.get() or
                zoomLogarithmic.get() or
                zoomPower.get()):
            zoomSubmitButton['state'] = NORMAL
        if (not (zoomOriginal.get()) and
                not (zoomNegative.get()) and
                not (zoomLogarithmic.get()) and
                not (zoomPower.get())):
            zoomSubmitButton['state'] = DISABLED

    def zoomImages():
        def checkImageProportions(image):
            scale_percent = 15
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            if width > 900 or height > 860:
                image_resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
                return image_resized
            else:
                return image

        zoomWindow.destroy()
        if zoomOriginal.get():
            imageOriginalDisplay = checkImageProportions(initialImage)
            cv2.imshow('Original image', imageOriginalDisplay)
        if zoomNegative.get():
            imageNegativeDisplay = checkImageProportions(negativeImageCV2)
            cv2.imshow('Negative image', imageNegativeDisplay)
        if zoomLogarithmic.get():
            imageNegativeDisplay = checkImageProportions(logarithmicImageCV2)
            cv2.imshow('Logarithmic image', imageNegativeDisplay)
        if zoomPower.get():
            imageNegativeDisplay = checkImageProportions(nthPowerImageCV2)
            cv2.imshow('Power-Law image', imageNegativeDisplay)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Create a zoom option window
    zoomWindow = Toplevel()
    # Window dimensions
    zoomWindow.geometry("320x220")
    # Window title
    zoomWindow.title("Zoom image options")
    # Turn image into a PhotoImage, so it can be used by tkinter
    logoImageZoom = PhotoImage(file='logo.png')
    # Add the icon to the window
    zoomWindow.iconphoto(False, logoImageZoom)
    # Window background color
    zoomWindow.config(background="#343a40")

    infoLabel = Label(zoomWindow,
                      bg='#343a40',
                      font=("Helvetica", 10, 'bold'),
                      fg='white')
    infoLabel.pack(ipadx=15, ipady=5, fill='x')

    infoLabel.configure(text=' Select the images you want to zoom')

    zoomOriginal = BooleanVar()
    zoomNegative = BooleanVar()
    zoomLogarithmic = BooleanVar()
    zoomPower = BooleanVar()

    checkZoomOriginal = Checkbutton(zoomWindow,
                                    text='Original image',
                                    font=("Helvetica", 10, 'bold'),
                                    variable=zoomOriginal,
                                    command=validateZoom,
                                    onvalue=True,
                                    offvalue=False,
                                    fg='white',
                                    bg='#343a40',
                                    selectcolor='#219ebc',
                                    activebackground='#343a40',
                                    activeforeground='white')
    checkZoomOriginal['state'] = DISABLED

    checkZoomNegative = Checkbutton(zoomWindow,
                                    text='Negative transformation image',
                                    font=("Helvetica", 10, 'bold'),
                                    variable=zoomNegative,
                                    command=validateZoom,
                                    onvalue=True,
                                    offvalue=False,
                                    fg='white',
                                    bg='#343a40',
                                    selectcolor='#219ebc',
                                    activebackground='#343a40',
                                    activeforeground='white')
    checkZoomNegative['state'] = DISABLED

    checkZoomLogarithmic = Checkbutton(zoomWindow,
                                       text='Logarithmic transformation image',
                                       font=("Helvetica", 10, 'bold'),
                                       variable=zoomLogarithmic,
                                       command=validateZoom,
                                       onvalue=True,
                                       offvalue=False,
                                       fg='white',
                                       bg='#343a40',
                                       selectcolor='#219ebc',
                                       activebackground='#343a40',
                                       activeforeground='white')
    checkZoomLogarithmic['state'] = DISABLED

    checkZoomPower = Checkbutton(zoomWindow,
                                 text='Power-Law transformation image',
                                 font=("Helvetica", 10, 'bold'),
                                 variable=zoomPower,
                                 command=validateZoom,
                                 onvalue=True,
                                 offvalue=False,
                                 fg='white',
                                 bg='#343a40',
                                 selectcolor='#219ebc',
                                 activebackground='#343a40',
                                 activeforeground='white')
    checkZoomPower['state'] = DISABLED

    checkZoomOriginal.pack(ipadx=10,
                           ipady=5,
                           expand=True,
                           fill='x')

    checkZoomNegative.pack(ipadx=10,
                           ipady=5,
                           expand=True,
                           fill='x')
    checkZoomLogarithmic.pack(ipadx=10,
                              ipady=5,
                              expand=True,
                              fill='x')
    checkZoomPower.pack(ipadx=10,
                        ipady=5,
                        expand=True,
                        fill='x')

    zoomSubmitButton = Button(zoomWindow,
                              image=zoomIcon,
                              command=zoomImages,
                              text=' zoom',
                              font=("Helvetica", 10, 'bold'),
                              compound='left',
                              bg="#0077b6",
                              fg='white',
                              activebackground='#0096c7',
                              activeforeground='white',
                              relief="ridge")
    zoomSubmitButton['state'] = DISABLED
    zoomSubmitButton.pack(ipadx=10,
                          ipady=10,
                          pady=5,
                          fill='y')

    if isImageUploaded:
        checkZoomOriginal['state'] = NORMAL
    if hasNegativeBeenProcessed:
        checkZoomNegative['state'] = NORMAL
    if hasLogarithmicBeenProcessed:
        checkZoomLogarithmic['state'] = NORMAL
    if hasNthPowerBeenProcessed:
        checkZoomPower['state'] = NORMAL


# Instantiate an instance of window
window = Tk()
# Window dimensions
window.geometry("1280x720")
# Window title
window.title("Gray level transformation app")
# Turn image into a PhotoImage, so it can be used by tkinter
logoImage = PhotoImage(file='logo.png')
# Add the icon to the window
window.iconphoto(False, logoImage)
# Window background color
window.config(background="#343a40")

# Menu bar
menuBar = Menu(window)
window.config(menu=menuBar)

# PhotoImages for menu bar icons
openIcon = ImageTk.PhotoImage(Image.open('folder.png').resize((15, 15)))
saveIcon = ImageTk.PhotoImage(Image.open('save-file.png').resize((15, 15)))
exitIcon = ImageTk.PhotoImage(Image.open('log-out.png').resize((15, 15)))
infoIcon = ImageTk.PhotoImage(Image.open('info.png').resize((15, 15)))
howToIcon = ImageTk.PhotoImage(Image.open('user-guide.png').resize((15, 15)))

# Photo images for main window buttons
processIcon = ImageTk.PhotoImage(Image.open('processing.png').resize((20, 20)))
openButtonIcon = ImageTk.PhotoImage(Image.open('folder.png').resize((20, 20)))
numberIcon = ImageTk.PhotoImage(Image.open('numbers.png').resize((15, 15)))
zoomIcon = ImageTk.PhotoImage(Image.open('zoom-in.png').resize((15, 15)))

# File menu
fileMenu = Menu(menuBar, tearoff=0)

# Menu bar link file menu
menuBar.add_cascade(label="File", menu=fileMenu)

# File menu options
fileMenu.add_command(label="Open Image", command=openImage, image=openIcon, compound='left')
fileMenu.add_command(label="Save Image", command=saveImage, image=saveIcon, compound='left')
fileMenu.add_separator()
fileMenu.add_command(label="Exit App", command=window.destroy, image=exitIcon, compound='left')

# Help menu
helpMenu = Menu(menuBar, tearoff=0)

# Link menu bar to help menu
menuBar.add_cascade(label='Help', menu=helpMenu)

# Help menu options
helpMenu.add_command(label='How to use', command=howToUseApp, image=howToIcon, compound='left')
helpMenu.add_separator()
helpMenu.add_command(label='About', command=openExternalLink, image=infoIcon, compound='left')

# Application title label
titleApp = Label(window, text=' Gray Level Transformation ', bg='#343a40', font=("Helvetica", 14, 'bold'), fg='white')
titleApp.pack(ipadx=15, ipady=15, fill='x')

# Variables used to check if a method of processing and visualization was selected
negativeGrayCheckVar = BooleanVar()
LogarithmGrayCheckVar = BooleanVar()
nthPowerCheckVar = BooleanVar()

# Application frame with buttons to select visualization of a specific method or all methods
buttonFrame = Frame(window, bg='#343a40')
buttonFrame.pack(fill='x', side='top')

# All check button are disabled until the first image gets uploaded

# Check button for negative transformation
checkBoxNegativeGray = Checkbutton(buttonFrame,
                                   text='Negative transformation',
                                   font=("Helvetica", 10, 'bold'),
                                   command=displayNegative,
                                   variable=negativeGrayCheckVar,
                                   onvalue=True,
                                   offvalue=False,
                                   fg='white',
                                   bg='#343a40',
                                   selectcolor='#219ebc',
                                   activebackground='#343a40',
                                   activeforeground='white')
checkBoxNegativeGray['state'] = DISABLED
checkBoxNegativeGray.pack(ipadx=10,
                          ipady=10,
                          expand=True,
                          fill='x',
                          side="left")

# Check button for logarithmic transformation
checkBoxLogarithmicGray = Checkbutton(buttonFrame,
                                      text='Logarithmic transformation',
                                      font=("Helvetica", 10, 'bold'),
                                      command=displayLogarithmic,
                                      variable=LogarithmGrayCheckVar,
                                      onvalue=True,
                                      offvalue=False,
                                      fg='white',
                                      bg='#343a40',
                                      selectcolor='#219ebc',
                                      activebackground='#343a40',
                                      activeforeground='white')
checkBoxLogarithmicGray['state'] = DISABLED
checkBoxLogarithmicGray.pack(ipadx=10,
                             ipady=10,
                             expand=True,
                             fill='x',
                             side="left")

# Check button for power - law transformation
checkBoxNthPowerGray = Checkbutton(buttonFrame,
                                   text='Power-Law transformation',
                                   font=("Helvetica", 10, 'bold'),
                                   variable=nthPowerCheckVar,
                                   command=displayNthPower,
                                   onvalue=True,
                                   offvalue=False,
                                   fg='white',
                                   bg='#343a40',
                                   selectcolor='#219ebc',
                                   activebackground='#343a40',
                                   activeforeground='white')
checkBoxNthPowerGray['state'] = DISABLED
checkBoxNthPowerGray.pack(ipadx=10,
                          ipady=10,
                          expand=True,
                          fill='x',
                          side="left")

# Image frame used to display original image and transformation images
imagesFrame = Frame(window, bg='#343a40')
imagesFrame.pack(expand=True, fill='both', side='top')

# Frame for the buttons used to upload image and to start the processing phase
uploadAndProcessFrame = Frame(window, bg='#343a40')
uploadAndProcessFrame.pack(pady=10, fill='x', side='top')

# Button used to upload image calling the openImage function
uploadButton = Button(uploadAndProcessFrame,
                      image=openButtonIcon,
                      command=openImage,
                      text=' Open new image',
                      font=("Helvetica", 10, 'bold'),
                      compound='left',
                      bg="#0077b6",
                      fg='white',
                      activebackground='#0096c7',
                      activeforeground='white',
                      relief="ridge")
uploadButton.pack(ipadx=10,
                  ipady=10,
                  pady=5,
                  expand=True,
                  fill='y',
                  side='left')

# Button used to call the processImage function to display the processed images
# Button is disabled if there is no image uploaded or if none of the transformation is selected
processButton = Button(uploadAndProcessFrame,
                       image=processIcon,
                       command=processImage,
                       text=' Process image',
                       font=("Helvetica", 10, 'bold'),
                       compound='left',
                       bg="#0077b6",
                       fg='white',
                       activebackground='#0096c7',
                       activeforeground='white',
                       relief="ridge")
processButton['state'] = DISABLED
processButton.pack(ipadx=10,
                   ipady=10,
                   pady=5,
                   expand=True,
                   fill='y',
                   side='left')

zoomButton = Button(uploadAndProcessFrame,
                    image=zoomIcon,
                    command=zoomImage,
                    text=' Zoom image',
                    font=("Helvetica", 10, 'bold'),
                    compound='left',
                    bg="#0077b6",
                    fg='white',
                    activebackground='#0096c7',
                    activeforeground='white',
                    relief="ridge")
zoomButton.pack_forget()

# Display window and listen for events
window.mainloop()
