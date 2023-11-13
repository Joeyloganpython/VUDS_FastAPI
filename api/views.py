from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from api.forms import PatientCharacteristicsForm, TracingForm, ImagesForm,DicomSeries
from api.tracing import NN_by_pressure
from api.dicom_pred import Dicom_pred
from api.zipdicom import Zip_Dicom
import logging
from pathlib import Path
from fastapi import Form, UploadFile
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
import pandas as pd
import pydicom
from typing import Optional
import numpy as np

app = FastAPI()



# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get('/', name='index')
def get_index(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})





@app.get("/uploadall")
async def uploadall(request: Request):
    return templates.TemplateResponse("uploadall.html", {"request": request})

@app.post("/uploadall")
async def process_uploadall(
   request: Request,
     tracing_file: UploadFile = None,
       dicom_file: Optional[UploadFile] = None,
       ebc: int = Form(None)):
    dicom_results = None
    txtresults = None

    eventtimes  = np.array([
    0.01, 0.12, 0.25, 0.38, 0.50, 0.63,
    0.75,0.88, 1.00, 1.13, 1.26, 1.38,1.50,1.64,
    1.76, 1.89, 2.00, 2.14, 2.27, 2.39, 2.50, 2.64,
    2.77, 2.90, 3.00, 3.15, 3.27, 3.40, 3.50, 3.65, 3.78,
    3.90, 4.00, 4.16, 4.28, 4.41, 4.50, 4.66, 4.79, 5.00
])
    if dicom_file is not None:
        file_name = dicom_file.filename

        file_extension = file_name.split('.')[-1] if '.' in file_name else ""
        print('zipfile or DICOM',file_extension)

        if file_extension == 'dcm':
            ds = pydicom.dcmread(dicom_file.file, force=True)
            print(ds)
            dcm = Dicom_pred(ds)
            dicom_results = dcm.preprocess()
            print(dicom_results)

            dicom_results = dicom_results[0][:40]
            print(dicom_results)
            print('dicome results type', type(dicom_results))
            print('dicome results type', type(dicom_results))

            print('dicome results type', type(dicom_results))

            print(dicom_results)
        elif file_extension =='zip':    
            zip_content = await dicom_file.read()
            zip_d = Zip_Dicom()
            dicom_results = zip_d.get_dicom(zip_content=zip_content)
            dicom_results = dicom_results[0][:40]

            print(dicom_results)
            print('dicomzipresultstype',type(dicom_results))
            print('dicomresultsshape',dicom_results.shape)
            

    if tracing_file is not None and ebc is not None:
        logging.debug("Reached /upload POST endpoint")
        arr = pd.read_csv(tracing_file.file, sep="\t")
        nn = NN_by_pressure(arr=arr, ebc=ebc)
        txtresults = nn.make_predictions()  
        txtresults = txtresults[0][:40]
 
        print('textfileresults',txtresults)
        print('txtfiledatatype',type(txtresults))
        print('txtfileshape',txtresults.shape)

    if dicom_results is not None and txtresults is not None:
        fresults = (dicom_results + txtresults) /2   ## averaging risk scores
    elif dicom_results is not None:
        fresults = dicom_results
    elif txtresults is not None:
        fresults = txtresults

    print('finalresults',fresults)    
    fiveyearprob = fresults[-1]  ### Probobility of hydro at 5 years


    return templates.TemplateResponse("results.html", {"request": request,"results":fresults,
                                                          "fiveyearprob":fiveyearprob,"eventtimes":eventtimes})
 
   





 