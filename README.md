# Vernaculator
A python application to extracts text from images and translate the text to english

## Requirements:
**->Python 3.7 with the following packages installed**<br>
<pre>
      -imutils <br>
      -googletrans <br>
      -pillow <br>
      -OpenCV2(cv2) <br>
      -numpy <br>
      -pytesseract <br>
 </pre>     
**->Tesseract-OCR:** [Tesseract OCR Mannhiem](https://github.com/tesseract-ocr/tesseract/wiki/Downloads)
<pre>     
     Do ensure that you download the list of language package you need. <br>
     Add a path in the system environment variable for access. <br>
</pre>
**->EAST Text Detector Model:** [Download](https://drive.google.com/file/d/1ItInG03matiMjpuX_ozsG9mryOvyHalv/view?usp=sharing) <br>
<pre>
    Download this for text detection. It is a pre-trained model to detect text from image. <br>
</pre>

## How To Run the program:
**Step 1:**
<pre>
      Download all the files specified in the requirement and install in properly.
</pre>
**Step 2:**
<pre>
      Run the .py file in a command prompt or an anaconda command prompt(prefered).
</pre>
**Step 3:**
<pre>
      The GUI would pop up if all the files were installed properly.
</pre>
**Step 4:**
<pre>
      Enter the language to be detected.
</pre>
**Step 5:**
<pre>
      Import the model.pb file.
</pre>
**Step 6:**
<pre>
      Upload the image.
</pre>
**Step 7:**
<pre>
      Keep pressing enter to move the detection box to the words which need to be translated. 
</pre>
