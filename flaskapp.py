from flask import Flask, render_template, Response,request, jsonify, send_file, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import logging
from pathlib import Path
from flask_cors import CORS
import pyttsx3
from flask_mysqldb import MySQL
import cv2
import os
import base64
import glob
import math
from PIL import Image
from os import listdir
import json
import numpy as np
from decimal import Decimal
from datetime import date,datetime, timedelta  

from time import sleep
import logging


# Set up logging configuration
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO

app = Flask(__name__)

CORS(app)

app.secret_key = 'your_secret_key'

#MYSQL DataBase Connection credentials
app.config['MYSQL_HOST'] = '89.116.228.212'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Admin@hydax23'
app.config['MYSQL_DB'] = 'hydax'
mysql = MySQL(app)

#Rendering main page
@app.route('/')
def index():
   return render_template('index.html')

#Rendering RosaI main page
@app.route('/rosai',methods=['GET', 'POST'])
def rosai():

    return render_template('rosai.html')

#Rendering Teach page
@app.route('/teach',methods=['GET', 'POST'])
def teach():
    return render_template('teach.html')

# Code for creating folder
path1 = '/var/www/basic/static/'
global user_folder

global pathh
@app.route('/create',methods=['GET', 'POST'])
def create():
    global user_folder
    global pathh
    data = request.json
    name = data.get('folder_name')
    user_folder = os.path.join(path1, name)
    os.mkdir(user_folder)
    p = Path(user_folder)
    pathh = ('/'.join( p.parts[4:]))
    app.config['USER_FOLDER'] = user_folder

    #return render_template('teach.html') 
    return redirect(url_for('nextpage'))

#Rendering teach page
@app.route('/nextpage')
def nextpage():
    return render_template('teach.html')

global user_folder
global folder_path
global image_path1
    
global pathh1

#Function to save the frist image
@app.route('/page1', methods=['POST'])
def page1():
    global user_folder
    global image_path1
    global pathh1
    global folder_path
    root_folder = app.config.get('USER_FOLDER',)
    app.config['ROOT_FOLDER'] = root_folder


    filename = 'image1.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['ROOT_FOLDER'], securefilename)
        
    # Decode base64 image data
    image_data = request.form.get('image_data').split(',')[1]
    image_data_decoded = base64.b64decode(image_data)
   
    with open(image_path1, 'wb') as f:
         f.write(image_data_decoded)

    return redirect(url_for('next_page'))

@app.route('/next_page')
def next_page():
    return  render_template('page2.html')

#Function to save the second image
@app.route('/page2', methods=['POST'])
def page2():
    global user_folder
    global image_path1
    global pathh1
    global folder_path
    root_folder = app.config.get('USER_FOLDER',)
    app.config['ROOT_FOLDER'] = root_folder


    filename = 'image2.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['ROOT_FOLDER'], securefilename)
        
    # Decode base64 image data
    image_data = request.form.get('image_data').split(',')[1]
    image_data_decoded = base64.b64decode(image_data)
   
    with open(image_path1, 'wb') as f:
         f.write(image_data_decoded)

    return redirect(url_for('next_page1'))

@app.route('/next_page1')
def next_page1():
    return render_template('page3.html')

#Function to save the third image
@app.route('/page3', methods=['POST'])
def page3():
    global user_folder
    global image_path1
    global pathh1
    global folder_path
    root_folder = app.config.get('USER_FOLDER',)
    app.config['ROOT_FOLDER'] = root_folder


    filename = 'image3.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['ROOT_FOLDER'], securefilename)
        
    # Decode base64 image data
    image_data = request.form.get('image_data').split(',')[1]
    image_data_decoded = base64.b64decode(image_data)
   
    with open(image_path1, 'wb') as f:
         f.write(image_data_decoded)

    return redirect(url_for('next_page2'))

@app.route('/next_page2')
def next_page2():
    return render_template('page4.html')

#Function to save the fourth image
@app.route('/page4', methods=['POST'])
def page4():
    global user_folder
    global image_path1
    global pathh1
    global folder_path
    root_folder = app.config.get('USER_FOLDER',)
    app.config['ROOT_FOLDER'] = root_folder


    filename = 'image4.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['ROOT_FOLDER'], securefilename)
        
    # Decode base64 image data
    image_data = request.form.get('image_data').split(',')[1]
    image_data_decoded = base64.b64decode(image_data)
   
    with open(image_path1, 'wb') as f:
         f.write(image_data_decoded)

    return 'Image is saved'

#Function to do mathematical operations and save the data to MySQL DB
@app.route('/submit',methods=['GET','POST'])

def submit():
    global user_folder
    global folder_path
    global image_path1
    global pathh
    global pathh1
    list1 = []
    shapes = []
    firstimgshape = []
    NonBP=[]
    NBP=[]
    calc=[]

    path1 = (user_folder)
    
    
    images=[]

    files = sorted(os.listdir(app.config['ROOT_FOLDER']))

    for f in files:
       images.append(f)
    print('list of image in folder:', images)

    
    firstimage = images[0]
    print("firstimage:", firstimage)
    firstimagepath = app.config['ROOT_FOLDER']
    imagepath1 = os.path.join(firstimagepath, firstimage)
    print("firstimagepath:",imagepath1)
    
    p1 = Path(imagepath1)
    imagepath1 = ('/'.join(p1.parts[4:]))
    
    path1 = (user_folder)
    print('userfolder:', path1)
    
    #Copy the image sto list
    for root, dirs, files in os.walk(path1):
        for file in files:
            if file.lower().endswith(('.png')):
                list1.append(os.path.join(root, file))

    print(list1)
    print(f"Found {len(list1)} image files in the folder:")
    #Read the list and convert that to Canny image
    img1=cv2.imread(list1[0])
    img1_canny=cv2.Canny(img1,550,550)
    cv2.imwrite(f'/var/www/basic/static/cannyimages/cannyimage1.png',img1_canny)

    img2=cv2.imread(list1[1])
    img2_canny=cv2.Canny(img2,550,550)
    cv2.imwrite(f'/var/www/basic/static/cannyimages/cannyimage2.png',img2_canny)
    
    img3=cv2.imread(list1[2])
    img3_canny=cv2.Canny(img3,550,550)
    cv2.imwrite(f'/var/www/basic/static/cannyimages/cannyimage3.png',img3_canny)

    img4=cv2.imread(list1[3])
    img4_canny=cv2.Canny(img4,550,550)
    cv2.imwrite(f'/var/www/basic/static/cannyimages/cannyimage4.png',img4_canny)

    #Compare the shape of images, calculate the non zero values

    if img1_canny.shape == img4_canny.shape:
        
        add1=cv2.subtract(img1_canny,img2_canny)
        num_non_zero_pixels1 = (add1 > 200)
        numnonzeropixels1 = np.sum(num_non_zero_pixels1)
        print("num_non_zero_pixels1:",numnonzeropixels1)

        add2=cv2.subtract(img2_canny,img3_canny)
        num_non_zero_pixels2 = (add2 > 200)
        numnonzeropixels2 = np.sum(num_non_zero_pixels2)
        print("num_non_zero_pixels2:",numnonzeropixels2)

        add3=cv2.subtract(img3_canny,img4_canny)
        num_non_zero_pixels3 = (add3 > 200)
        numnonzeropixels3 = np.sum(num_non_zero_pixels3)
        print("num_non_zero_pixels3:",numnonzeropixels3)

        add4=cv2.subtract(img2_canny,img3_canny)
        num_non_zero_pixels4 = (add4 > 200)
        numnonzeropixels4 = np.sum(num_non_zero_pixels4)
        print("num_non_zero_pixels1:",numnonzeropixels4)

        #Calculate the mean, standard deviation and Upperthreshold
        dat=[numnonzeropixels1,numnonzeropixels2,numnonzeropixels3,numnonzeropixels4]
        Mean=np.mean(dat)
        print("Meann:",Mean)
        Std_dev=np.std(dat)
        print("Dev:",Std_dev)
        Uthreshold=Mean+Std_dev
        print("Uthh:",Uthreshold)
        
        NBP = 200
  

    cursor=mysql.connection.cursor()
    
    # Define the SQL query to insert the data into the table
    insert_query = "INSERT INTO teach (product,image1,Uthreshold,non_black_pixels) VALUES (%s, %s, %s ,%s)"
    data = (pathh,imagepath1,Uthreshold, NBP )

    # Execute the SQL query with the list and string data as parameters
    cursor.execute(insert_query, data)

    # Commit the changes to the database
    mysql.connection.commit()

    # Close the cursor and connection
    cursor.close()
    message = {'message': 'Data Stored!'}
    return jsonify(message)
    
#Rendering open screen
@app.route('/openn',methods=['GET', 'POST'])
def openn():
    cur=mysql.connection.cursor()
   #cur.execute("SELECT image1 FROM teach ")
    cur.execute('SELECT image1 FROM teach ORDER BY SerialNo DESC LIMIT 5')
    image_paths=[row[0] for row in cur.fetchall()]
    mysql.connection.commit()
    cur.close()
    return render_template('openn.html',image_paths=image_paths)

#Function to display the selected image 
global non_black_pixels
global upper_threshold
   
TEST_FOLDER = '/var/www/basic/static/test'
#TEST_FOLDER = 'test'
app.config['TEST_FOLDER'] = TEST_FOLDER

global pathh2
@app.route('/handle_click',methods=['GET','POST'])
def handle_click():
    global pathh2
    href_link = request.form.get('href')
    print('imagepath:', href_link)

    p2 = Path(href_link)
    pathh2 = ('/'.join(p2.parts[2:]))
    print('extractedpath:', pathh2)
   
   #return render_template('display.html', href_value = pathh2)
    return jsonify({'success': True})

@app.route('/display',methods=['GET','POST'])
def display():
    global pathh2
    print("extracted path from handle click:",pathh2)
    return render_template('display.html', href_value = pathh2)

#Function to capture and save the image to folder
@app.route('/test',methods=['GET','POST'])
def test():
    global message
    global user_folder
    global user_folder1
    global image_path1
    global pathh2
    global pathh
   
    filename = 'test.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['TEST_FOLDER'], securefilename)
        
    # Decode base64 image data
    image_data = request.form.get('image_data').split(',')[1]
    image_data_decoded = base64.b64decode(image_data)
   
    with open(image_path1, 'wb') as f:
         f.write(image_data_decoded)

    loadpath = '/var/www/basic/'
    
    user_folder1 = os.path.join(loadpath, pathh2)
   
 
    #return render_template('openn.html')
    return redirect(url_for('openn'))

#Function to test captured image and loaded image
global message

@app.route('/verify',methods=['GET','POST'])
def verify():
    global user_folder
    global user_folder1
    global image_path1
    global pathh2
    global pathh
    global message
   
    message= None
    print("user_folder1:", user_folder1)
 
    frame1 = cv2.imread(image_path1)


    load1 = cv2.imread(user_folder1)
    load1_canny = cv2.Canny(load1,500,500)
    print("shapeframe1:",frame1.shape)
    print("shapeload1:",load1.shape)
    frame1_canny = cv2.Canny(frame1,500,500)
    cv2.imwrite('/var/www/basic/static/test/testcanny.png',frame1_canny)
    partname = os.path.dirname(pathh2)
    
    #Connection to MySQL DataBase
    cur=mysql.connection.cursor()

    cur.execute('SELECT Image1 FROM teach ORDER BY SerialNo DESC LIMIT 5')
    image_paths=[row[0] for row in cur.fetchall()]
    
        
    #Mathematicl operation to compare the test and loaded image
    if load1_canny.shape==frame1_canny.shape:
        add5 = cv2.subtract(load1_canny,frame1_canny)
        #add5 = (add5 > 200)
        #nbp5 = np.sum(add5)
        cv2.imwrite(f'/var/www/basic/static/canny/testt.png',add5)
        frame2=cv2.imread(f'/var/www/basic/static/canny/testt.png')
        
        query="SELECT SerialNo, Uthreshold, non_black_pixels from teach where Product= %s"
        cur.execute(query, (partname,))
        Uth = cur.fetchall()
        NBP = cur.fetchall()

        print("uthershold:",Uth)
        print("NBP:",NBP)
        #print("dtype uth:",type(Uth))
        serialid = Uth[0][0]
        Uthreshold = Uth[0][1]
        Nonblackpixel = Uth[0][2]

        img_array = np.array(frame2)

        # Calculate pixel values above 1
        pixels_above_1 = img_array[img_array > Nonblackpixel]

        # Print the result
        pixelvalue = len(pixels_above_1)
        print("Pixel values above 1:", pixelvalue)

        reject = "Rejected"
        accept = "Accepted"
        if pixelvalue > Uthreshold:
            print("pixel value is greater than uthreshold")
            difference = abs(pixelvalue - Uthreshold)
            quotient = difference/Uthreshold
            percentage = quotient * 100
            formatted_num = format(percentage, ".2f")
            print(str(formatted_num)+ "%" + " " + reject)
            today = datetime.now()
            print("Date and Time:", today)
            #Query to save the calculated values to DataBase
            query1 = "INSERT into open (SerialNo,product,Result,dateandtime) values (%s, %s, %s, %s)"
            data1 = (serialid,partname, reject, today)
            cur.execute(query1, data1)
            message = True
            
            
        else:
            print("pixel value is lesser than uthreshold")
            difference = abs(pixelvalue - Uthreshold)
            quotient = difference/Uthreshold
            percentage = quotient * 100
            formatted_num = format(percentage, ".2f")
            print(str(formatted_num)+ "%" + " " + accept)
            today = datetime.now()
            print("Date and Time:", today)
            #Query to save the calculated values to DataBase
            query1 = "INSERT into open (SerialNo,product,Result,dateandtime) values (%s, %s, %s, %s)"
            data1 = (serialid,partname, accept, today)
            cur.execute(query1, data1)
            message =  False
            
        
        
        mysql.connection.commit()
        cur.close()
 
    return render_template('openn.html', image_paths=image_paths,message = message)



@app.route('/rosac', methods=['GET','POST'])
def rosac():
    
    return render_template('main_rosa_c.html')

@app.route('/setup',methods=['GET'])
def setup():
    #newuser1 = session.get('serialid')

    return render_template('setup.html')



@app.route('/Sync',methods=['GET'])
def Sync():
    return render_template('async.html')


@app.route('/auto',methods=['GET'])
def auto():
    return render_template('auto.html')




# Define the static folder for audio files
STA_FOLDER = '/var/www/basic/static/audio'

# Set the static folder in the app configuration
app.config['STA_FOLDER'] = STA_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    # Check if audio data is present in the request
    if 'audio' not in request.files:
        return 'No audio data found in request'

    # Get the audio data from the request
    audio_data = request.files['audio'].read()

    # Save the audio data to a file in the upload folder
    with open(os.path.join(app.config['STA_FOLDER'], 'recording.ogg'), 'wb') as f:
        f.write(audio_data)

    return 'Audio uploaded successfully!'




STATIC_FOLDER = '/var/www/basic/static/images'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

CASCADE_FILE_PATH = '/var/www/basic/haarcascade_frontalface_default.xml'
app.config['CASCADE_FILE_PATH'] = CASCADE_FILE_PATH

# Load the Haar cascade classifier
face_cascade = cv2.CascadeClassifier(app.config['CASCADE_FILE_PATH'])

# Function to detect faces
def detect_faces(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Check if the image was read successfully
    if img is None:
        return None

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(100, 100))

    # If no face detected, return None
    if len(faces) == 0:
        return None

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Save the image with detected faces
    cv2.imwrite(image_path, img)

    return faces

@app.route('/capture', methods=['POST'])
def capture():
    filename = 'live.png'
    securefilename = secure_filename(filename)
    image_path1 = os.path.join(app.config['STATIC_FOLDER'], securefilename)

    # Get the base64 encoded image data from the request
    image_data = request.form.get('image_data')

    # Check if image data exists
    if not image_data:
        # If no image data, stay on the same page
        return render_template('async.html')

    # Decode and save the image data to a file
    image_data_decoded = base64.b64decode(image_data.split(',')[1])
    with open(image_path1, 'wb') as f:
        f.write(image_data_decoded)

    # Perform face detection
    faces = detect_faces(image_path1)

    if faces is not None and len(faces) > 0:  # Check if faces are detected
        # If face detected, redirect to detected.html
        print("Faces detected:", faces)  # Print detected faces
        return redirect(url_for('face__detected'))  # Redirect using url_for
    else:
        # If no face detected, stay on the same page
        print("No faces detected...")
        return redirect(url_for('async'))

@app.route('/face__detected')
def face__detected():
    # Get current time and add 5 hours and 30 minutes
    current_time = datetime.now() + timedelta(hours=5, minutes=30)
    current_hour = current_time.hour
    
    # Determine the greeting based on the adjusted time
    if current_hour < 12:
        greeting = "Good morning, Welcome to the stall of Hydax. while I speak, please observe the video below. We are engineers who make your products better. Our range of hydraulics accessories will give you one-stop solution for your power pack. Our machines are built with technologies such as Electro Chemical radiusing and Deburring for Deburring applications. Twin station ECM. Vacuum technology which is used for coolant filtration of machine coolant tanks. High pressure Water-based washing machines. Iona, which is a Ionic surface cleaning technology. I am also a product of Hydax and I am called ROSA. I come in different avatars. ROSA I, as you see in this stall, can be used for part inspection. ROSA C is what I am called. I can be your catalog droid to help out humans find information they need. ROSA G is another Avatar which holds our products. We will be manufacturing in Australia soon..."
    elif current_hour < 15:
        greeting = "Good afternoon, Welcome to the stall of Hydax. while I speak, please observe the video below. We are engineers who make your products better. Our range of hydraulics accessories will give you one-stop solution for your power pack. Our machines are built with technologies such as Electro Chemical radiusing and Deburring for Deburring applications. Twin station ECM. Vacuum technology which is used for coolant filtration of machine coolant tanks. High pressure Water-based washing machines. Iona, which is a Ionic surface cleaning technology. I am also a product of Hydax and I am called ROSA. I come in different avatars. ROSA I, as you see in this stall, can be used for part inspection. ROSA C is what I am called. I can be your catalog droid to help out humans find information they need. ROSA G is another Avatar which holds our products. We will be manufacturing in Australia soon..."
    else:
        greeting = "Good evening, Welcome to the stall of Hydax. while I speak, please observe the video below. We are engineers who make your products better. Our range of hydraulics accessories will give you one-stop solution for your power pack. Our machines are built with technologies such as Electro Chemical radiusing and Deburring for Deburring applications. Twin station ECM. Vacuum technology which is used for coolant filtration of machine coolant tanks. High pressure Water-based washing machines. Iona, which is a Ionic surface cleaning technology. I am also a product of Hydax and I am called ROSA. I come in different avatars. ROSA I, as you see in this stall, can be used for part inspection. ROSA C is what I am called. I can be your catalog droid to help out humans find information they need. ROSA G is another Avatar which holds our products. We will be manufacturing in Australia soon..."
    
    # Pass the greeting to the template
    return render_template('detected.html', greeting=greeting)


UPLOAD_FOLDER = 'audio_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/reco')
def record():
    return render_template('record.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_data' not in request.files:
        return 'No file part'
    file = request.files['audio_data']
    if file.filename == '':
        return 'No selected file'
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'recorded_audio.wav'))
        return 'File saved successfully'

