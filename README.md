VUDS Fast API

Install the requirements.txt file as is. Python version 3.9.13

To run the app:

uvicorn main:app --host 127.0.0.1 --port 8080 --reload

There is only one main view that can run all models:

Logic is put in place if both txt files and images are run. I did NOT invert the array  for the visual meaning that 70 needs to be 30 etc.


## To do

Grey out submit button until:

1)	Txt file AND EBC are uploaded
2)	OR Dicom OR Zip file are uploaded

Error handling:

1)	If they upload a zip file without a DICOM
2)	Ig the txt file and ebc don’t make it to a certain threshold. It’s currently returning “ error”
3)	If DICOM is unreadable for some reason


A message to the user “Problem with file please choose different file”

