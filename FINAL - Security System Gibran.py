from math import e
import cv2
import numpy as np
import face_recognition
import os
import time
import email_test
import pyautogui
import pyttsx3
import cvzone
import sys
import smtplib
from datetime import datetime
import speech_recognition as sr
from plyer import notification
from playsound import playsound
 

#___________Extra Modules ki coding_____________
def Speak(audio):
    # code pyttsx3 module initialize krne ke liye
    engine = pyttsx3.init()
    engine.say(audio)
    engine.runAndWait()


# Email bhejne ke liye code
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jarvis.6283@gmail.com', 'Welcome@628')
    server.sendmail('jarvis.6283@gmail.com', to, content)
    server.close()


# command lene ka code for input from the user via voice
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 500
        audio = r.listen(source, timeout=5, phrase_time_limit=8)

    try:
        print("Recognizing...")
        # Using google for voice recognition.
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        Speak("Say that again please!")
        print("say that again please...")
        return "None"
    query = query.lower()
    return query

# command jo lia usko execute karne ke liye
def command_ki_execution():
    while True:
        bolkar_query = takecommand().lower()
        
#__________Extra Modules Khatam_______________

#_________________________________________________________________________________________

# Opening of main code is from here
path = 'Dataset Ki Images'
images = []
count = 0
classKeNames = []
meri_list = os.listdir(path)
#print(meri_list)

#Path jo dia hai images ka unko sabko read karne ke liye
for x in meri_list:
    curImg = cv2.imread(f'{path}/{x}')
    images.append(curImg)
    classKeNames.append(os.path.splitext(x)[0])
#print(classKeNames)


#Dataset ki images ko yahan Encode karke bnaya
def images_ki_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
 

#Entry jiski hui hai usko note krne ka function
def entry_note_karo(name):
    with open('entry_timings.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'n{name},{dtString}')
 
encodeListKnown = images_ki_encodings(images)
print("Facial Biometrics now synced from the Server")
Speak("Facial Biometrics now synced from the Server") 
#Just to confirm images have been taken as dataset from the folder


#PW entries ka variable hai ENTRIES
entries = 0

#Intruder (unknown banda) ke liye entries
intruder_ki_entries = 0 

#Webcam use krne ka variable CAP (CAPture)
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
 
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
 
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        # #Agar face ka match hogya
        if matches[matchIndex]: #Check karo ki webcam ka face encoding me hai ki nhi
            name = classKeNames[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            entry_note_karo(name)
            time.sleep(0.8)
            if classKeNames[matchIndex] == 'gibran': #Check karo ki webcam face stored 'Gibran' ka hai
                cv2.imshow('Webcam',img)
                print("Face of Gibran Sir Verified. To Fully Verify its Gibran sir, Enter the Password to Continue")
                Speak("Face of Gibran Sir Verified. To Fully Verify its Gibran sir, Enter the Password to Continue")
                #User se uska Input lo
                user_ka_input = pyautogui.password(text='Additional Security Layer. Enter the Password to Enter the House', title='Password Protected', default='', mask='*')
                
                #Agar pehla PW attempt hi galat
                if user_ka_input != "hello123":
                    print("Wrong Password, You only have 2 more Attempts. Try again in 5 seconds")
                    Speak("Wrong Password, You only have 2 more Attempts. Try again in 5 seconds")
                    entries=entries+1
                    #print(entries,"Wrong attempts")->To show no.of wrong attempts
                    time.sleep(3)
                    retry_attempt = pyautogui.password(text='Try again with the Password', title='Password Protected', default='', mask='*')
                    
                    if retry_attempt != "hello123": #doosraretry attempt bhi galat
                        entries=entries+1
                        #print(entries,"Wrong attempts") -> To show no.of wrong attempts
                        print("Wrong Password, this is the Last warning. Try again in 5 seconds")
                        Speak("Wrong Password, this is the Last warning. Try again in 5 seconds")
                        time.sleep(3)

                        last_attempt = pyautogui.password(text='Last Try of yours with the Password', title='Password Protected', default='', mask='*')
                        
                        if last_attempt != "hello123": #last retry attempt bhi agar galat
                            entries=entries+1
                            print(entries,"Wrong attempts limit exceeded")
                            cv2.imwrite("pakka_intruder%d.jpg" % count, imgS)
                            print("Wrong attempts limit is exceeded. Access Has been denied, you are an Intruder. An Image of yours has been sent to Local police and Owner")
                            Speak("Wrong attempts limit is exceeded. Access Has been denied, you are an Intruder. An Image of yours has been sent to Local police and Owner")
                            try:
                                notification.notify(
                                    title="***INRUDER***",
                                    message="Police Is Alarmed",
                                    app_icon="images/danger.ico",
                                    timeout=7
                                )
                                playsound('Alarm.wav')
                                #email_test() #[Details of the Email ID and PW have to be changed as per ur own use]
                            except Exception as e:
                                pass                            
                            time.sleep(5)
                            sys.exit()
                        
                        else: #lsat retry attempt pe agar sahi
                            print("Identity Verified! Access Granted. Welcome Gibran Sir to the home")
                            Speak("Identity Verified! Access Granted. Welcome Gibran Sir to the home")
                            try:
                                playsound('door.wma')
                                notification.notify(
                                    title="***DOOR UNLOCKED***",
                                    message="Door is now unlocked",
                                    app_icon="images/1.ico",
                                    timeout=7
                                )
                            except Exception as e:
                                pass
                            time.sleep(5)
                            sys.exit()

                    else: #doosre retry attempt pe agar sahi
                        print("Identity Verified! Access Granted. Welcome Gibran Sir to the home")
                        Speak("Identity Verified! Access Granted. Welcome Gibran Sir to the home")
                        try:
                            playsound('door.wma')
                            notification.notify(
                                title="***DOOR UNLOCKED***",
                                message="Door is now unlocked",
                                app_icon="images/1.ico",
                                timeout=7
                            )
                        except Exception as e:
                            pass
                        time.sleep(5)
                        sys.exit()
                
                else: #Agar Pehle PW attempt pr sahi
                    print("Identity Verified! Welcome Gibran Sir to the home")
                    Speak("Identity Verified! Welcome Gibran Sir to the home")
                    try:
                        playsound('door.wma')
                        notification.notify(
                            title="***DOOR UNLOCKED***",
                            message="Door is now unlocked",
                            app_icon="images/1.ico",
                            timeout=7
                        )
                    except Exception as e:
                        pass
                    #playsound('door.wma')
                    time.sleep(5)
                    sys.exit()

                        
        #Agar face thode distance pe hai aur match hota hai toh fir note karo vrna 
        # if not in the dataset (unknown hua toh) to display unknown and save image
        elif (faceDis[matchIndex]) < 0.50:
            name = classKeNames[matchIndex].upper()
            entry_note_karo(name)

        # Neeche ka code to Handle Intruders (unknown people)
        else: 
            name = 'Unknown'
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(255,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(255,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            cv2.imshow('Webcam',img)
            print("Unknown Person Detected. You have 2 minutes to explain the reason why you are in Gibran Sir's Property?")
            Speak("Unknown Person Detected. You have 2 minutes to explain the reason why you are in Gibran Sir's Property?")
            cv2.imshow('Webcam',img)
            bolkar_query = takecommand().lower()

            # Given predefined recovery phrase given is "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda"
            #Pehla attempt for Recovery Code
            if 'tiger is alive' not in bolkar_query: # Agar 1st try me hi galat bola
                print("Wrong Input, Giving you the last chance")
                Speak("Wrong Input, Giving you the last chance")
                last_bolkar_query = takecommand().lower()
                if 'tiger is alive' not in last_bolkar_query:
                    print("You have successfully wasted your last chance")
                    Speak("You have successfully wasted your last chance")
                    print(" Access Has been denied, you are an Intruder. An Image of yours has been sent to Local police and Owner")
                    Speak(" Access Has been denied, you are an Intruder. An Image of yours has been sent to Local police and Owner")
                    cv2.imwrite("recovery_failure%d.jpg" % count, imgS)
                    try:
                        notification.notify(
                            title="***INTRUDER***",
                            message="Police is Alarmed",
                            app_icon="images/danger.ico",
                            timeout=7
                        )
                        playsound('Alarm.wav')
                        #email_test() [Details of the Email ID and PW have to be changed as per ur own use]
                    except Exception as e:
                        pass
                    #send to local police now and to owner
                    time.sleep(2)
                    sys.exit()

                #Agar 2nd retry of Recovery phrase me sahi hojaye
                else:
                    #__________________________
                    Speak("Recovery Phrase detected")
                    print("Recovery Phrase detected")
                    print("Enter the complete Phrase given to You by Gibran Sir")
                    Speak("Enter the complete Phrase given to You by Gibran Sir")
                    #Pehla chance of enter input
                    recoveryphrase_input = pyautogui.prompt(text='Enter the Exact Phrase given to You by Gibran Sir', title='Case of the Phrase also Matters')
                    # Neeche wala checks First attempt user has written exactly "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda"
                    if recoveryphrase_input != "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda":
                        Speak("Last Chance, Try Again with Recovery Phrase")
                        print("Last Chance, Try Again with Recovery Phrase")
                        retry_recovery = pyautogui.prompt(text='Enter the Exact Phrase given to You by Gibran Sir', title='Case of the Phrase also Matters')
                        if retry_recovery == "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda":
                            Speak("Processing your Input")
                            #Agar recovery phrase retry sahi hojaye
                            cv2.imshow('Webcam',img)
                            Speak("I will now read the Recovery Code you Entered")
                            Speak("Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda")
                            print("Verifying....")
                            time.sleep(0.8)
                            # after verified niche ka
                            name = "Guest"
                            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                            print("Guest Code Verified. Hello our Guest. Welcome To The House")
                            Speak("Guest Code Verified. Hello our Guest. Welcome To The House")
                            cv2.imshow('Webcam',img)
                            try:
                                playsound('door.wma')
                                notification.notify(
                                    title="***DOOR UNLOCKED***",
                                    message="Door is now unlocked",
                                    app_icon="images/1.ico",
                                    timeout=7
                                )
                            except Exception as e:
                                pass
                            cv2.imwrite("verified_guest%d.jpg" % count, imgS)
                            #ab send alert to gibran email for login
                            time.sleep(5)
                            sys.exit()
                            
                        else:
                            print("Sorry get out")
                            sys.exit()


                    else: #Agar pehla Attempt hi sahi dediya toh niche ka code
                        cv2.imshow('Webcam',img)
                        Speak("I will now read the Recovery Code you Entered")
                        Speak("Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda")
                        print("Verifying....")
                        time.sleep(0.8)
                        # after verified niche ka
                        name = "Guest"
                        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                        print("Guest Code Verified. Hello our Guest. Welcome To The House")
                        Speak("Guest Code Verified. Hello our Guest. Welcome To The House")
                        cv2.imshow('Webcam',img)
                        cv2.imwrite("verified_guest%d.jpg" % count, imgS)
                        #ab send alert to gibran email for login
                        time.sleep(5)
                        sys.exit()



                    #__________________________
                
            
            else: # Agar recovery phrase Successfully 1st try me hi detect hua
                Speak("Recovery Phrase detected")
                print("Recovery Phrase detected")
                print("Enter the complete Phrase given to You by Gibran Sir")
                Speak("Enter the complete Phrase given to You by Gibran Sir")
                #Pehla chance of enter input
                recoveryphrase_input = pyautogui.prompt(text='Enter the Exact Phrase given to You by Gibran Sir', title='Case of the Phrase also Matters')
                # Neeche wala checks First attempt user has written exactly "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda"
                if recoveryphrase_input != "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda":
                    Speak("Last Chance, Try Again with Recovery Phrase")
                    print("Last Chance, Try Again with Recovery Phrase")
                    retry_recovery = pyautogui.prompt(text='Enter the Exact Phrase given to You by Gibran Sir', title='Case of the Phrase also Matters')
                    if retry_recovery == "Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda":
                        Speak("Processing your Input")
                        #Agar recovery phrase retry sahi hojaye
                        cv2.imshow('Webcam',img)
                        Speak("I will now read the Recovery Code you Entered")
                        Speak("Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda")
                        print("Verifying....")
                        time.sleep(0.8)
                        # after verified niche ka
                        name = "Guest"
                        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                        print("Guest Code Verified. Hello our Guest. Welcome To The House")
                        Speak("Guest Code Verified. Hello our Guest. Welcome To The House")
                        cv2.imshow('Webcam',img)
                        try:
                            playsound('door.wma')
                            notification.notify(
                                title="***DOOR UNLOCKED***",
                                message="Door is now unlocked",
                                app_icon="images/1.ico",
                                timeout=7
                            )
                        except Exception as e:
                            pass
                        cv2.imwrite("verified_guest%d.jpg" % count, imgS)
                        #ab send alert to gibran email for login
                        time.sleep(5)
                        sys.exit()
                        
                    else:
                        print("Sorry get out")
                        sys.exit()


                else: #Agar pehla Attempt hi sahi dediya toh niche ka code
                    cv2.imshow('Webcam',img)
                    Speak("I will now read the Recovery Code you Entered")
                    Speak("Tiger Hai Abhi Zinda. Kholdo Darwaza Mat Karo Sharminda")
                    print("Verifying....")
                    time.sleep(0.8)
                    # after verified niche ka
                    name = "Guest"
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    print("Guest Code Verified. Hello our Guest. Welcome To The House")
                    Speak("Guest Code Verified. Hello our Guest. Welcome To The House")
                    cv2.imshow('Webcam',img)
                    try:
                        playsound('door.wma')
                        notification.notify(
                            title="***DOOR UNLOCKED***",
                            message="Door is now unlocked",
                            app_icon="images/1.ico",
                            timeout=7
                        )
                    except Exception as e:
                        pass
                    cv2.imwrite("verified_guest%d.jpg" % count, imgS)
                    #ab send alert to gibran email for login
                    time.sleep(5)
                    sys.exit()
 
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)