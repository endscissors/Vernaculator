from tkinter import *
from tkinter import filedialog
import sqlite3
from PIL import Image
import time
import io
import pytesseract
import cv2
from googletrans import Translator
import tkinter 
from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
window = Tk()
 
window.title("Vernaculator")
 
window.geometry('400x400')

conn = sqlite3.connect('Language.db') 
c = conn.cursor() 

input_text = tkinter.StringVar()
e1 = Entry(window,textvariable=input_text) 
def action():
    str7=input_text.get()
    lan='mal'
    if str7=='Malayalam':
        lan='mal'
    elif str7=='Tamil':
        lan='tam'
    elif str7=='Gujarati':
        lan='guj'
    elif str7=='Hindi':
        lan='hin'
    elif str7=='Kannada':
        lan='kan'
    elif str7=='Marathi':
        lan='mar'
    elif str7=='Punjabi':
        lan='pan'
    elif str7=='Sanskrit':
        lan='san'
    elif str7=='Telugu':
        lan='tel'
    elif str7=='English':
        lan='eng'
    elif str7=='Bengali':
        lan='ben'    
    #print(str7)
    def action1():
        modelname = filedialog.askopenfilename()
        print(modelname)    
        def clicked():
            #print(str7)
            filename = filedialog.askopenfilename()
            fn=filename.split(':')
            sp=filename.split('/')
            lbl1 = Label(window, text="Filename :"+sp[-1],bd=1,justify=RIGHT)
            lbl1.grid(column=0, row=5)
            img=cv2.imread(filename)
            print(lan)
            tex=pytesseract.image_to_string(Image.open(filename),lang=lan)
            #df = DataFrame(c.fetchall(), columns=['Recongnised_Text'])
            #print (df)
            language=''
            if lan=='mal':
                language='Malayalam'
            elif lan=='tam':
                language='Tamil'
            elif str7=='guj':
                language='Gujarati'
            elif str7=='hin':
                language='Hindi'
            elif str7=='kan':
                language='Kannada'
            elif str7=='mar':
                language='Marathi'
            elif str7=='pan':
                language='Punjabi'
            elif str7=='san':
                language='Sanskrit'
            elif str7=='tel':
                language='Telugu' 
            elif str7=='ben':
                language='Bengali'
            #print(language)
            lbl3=Label(window,text="The Text may open in few seconds.........",anchor=E,justify=CENTER)
            lbl3.grid(column=0,row=7)
            lbl2=Label(window,text="Translation: "+tex,bd=1,anchor=E,justify=RIGHT)
            lbl2.grid(column=0, row=13)
            def decode_predictions(scores, geometry):
                (numRows, numCols) = scores.shape[2:4]
                rects = []
                confidences = []
                for y in range(0, numRows):
                    scoresData = scores[0, 0, y]
                    xData0 = geometry[0, 0, y]
                    xData1 = geometry[0, 1, y]
                    xData2 = geometry[0, 2, y]
                    xData3 = geometry[0, 3, y]
                    anglesData = geometry[0, 4, y]
                    for x in range(0, numCols):
                        if scoresData[x] < args["min_confidence"]:
                            continue
                        (offsetX, offsetY) = (x * 4.0, y * 4.0)
                        angle = anglesData[x]
                        cos = np.cos(angle)
                        sin = np.sin(angle)
                        h = xData0[x] + xData2[x]
                        w = xData1[x] + xData3[x]
                        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                        endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                        startX = int(endX - w)
                        startY = int(endY - h)
                        rects.append((startX, startY, endX, endY))
                        confidences.append(scoresData[x])
                return (rects, confidences)     
            ap = argparse.ArgumentParser()
            ap.add_argument("-c", "--min-confidence", type=float, default=0.5,)
            ap.add_argument("-w", "--width", type=int, default=320,)
            ap.add_argument("-e", "--height", type=int, default=320,)
            ap.add_argument("-p", "--padding", type=float, default=0.0,)
            args = vars(ap.parse_args())
            image = cv2.imread(filename)
            orig = image.copy()
            (origH, origW) = image.shape[:2]
            (newW, newH) = (args["width"], args["height"])
            rW = origW / float(newW)
            rH = origH / float(newH)
            image = cv2.resize(image, (newW, newH))
            (H, W) = image.shape[:2]
            layerNames = [
                "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3"]
            print("Possible detected words:")
            net = cv2.dnn.readNet(modelname)
            blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                (123.68, 116.78, 103.94), swapRB=True, crop=False)
            net.setInput(blob)
            (scores, geometry) = net.forward(layerNames)
            (rects, confidences) = decode_predictions(scores, geometry)
            boxes = non_max_suppression(np.array(rects), probs=confidences)
            results = []
            for (startX, startY, endX, endY) in boxes:
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)
                dX = int((endX - startX) * args["padding"])
                dY = int((endY - startY) * args["padding"])
                startX = max(0, startX - dX)
                startY = max(0, startY - dY)
                endX = min(origW, endX + (dX * 2))
                endY = min(origH, endY + (dY * 2))
                roi = orig[startY:endY, startX:endX]
                config = ("-l eng --oem 1 --psm 7")
                text = pytesseract.image_to_string(roi, config=config)
                results.append(((startX, startY, endX, endY), text))
            results = sorted(results, key=lambda r:r[0][1])
            for ((startX, startY, endX, endY), text) in results:
                print("{}\n".format(text))
                text = ""
                output = orig.copy()
                cv2.rectangle(output, (startX, startY), (endX, endY),
                    (0, 0, 255), 2)
                cv2.putText(output, text, (startX, startY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                cv2.imshow("Text Detection", output)
                cv2.waitKey(0)    
            translator = Translator()
            tr1=translator.translate(tex)
            tr2=translator.translate(tex)
            str1=str(tr1.src)
            str2=str(tr2.text)
            c.execute("INSERT INTO LANGUAGE(Recongnised_text) VALUES(?);",[tex])
            c.execute("INSERT INTO TRANSLATED(Translated_text) VALUES(?);",[str2])
            print("uploaded")
            conn.commit()
            conn.close()
            lbl4=Label(window,text="Language Detected: "+language,bd=1,anchor=E,justify=RIGHT)
            lbl4.grid(column=0,row=9)
            lbl5=Label(window,text="Translated Text: "+str2,bd=1,anchor=E,justify=RIGHT)
            lbl5.grid(column=0,row=115)
        lbl = Label(window, text="Image:",justify=RIGHT)
        lbl.grid(column=0, row=3)      
        btn = Button(window, text="Open", command=clicked)
        btn.grid(column=2, row=3)
    lbl = Label(window, text="Deep Learning Model:",justify=RIGHT)
    lbl.grid(column=0, row=2)     
    btn5 = Button(window, text="Model", command=action1)
    btn5.grid(column=2, row=2)      
lbl = Label(window, text="Language:")
lbl.grid(column=0, row=0)    
btn = Button(window, text="Enter", command=action)
btn.grid(column=3, row=0)  
e1.grid(row=0, column=2)
 
window.mainloop()
