from pydantic import BaseModel, Field
from fastapi import UploadFile  # Correct import for UploadFile
from db.models import PatientCharacteristics, Tracing, Images,Dicomseries
from pathlib import Path

class PatientCharacteristicsForm(PatientCharacteristics):
    age: int = Field(default=None)
    sex: str = Field(default=None)
    weight: int = Field(default=None)
    reflux: bool = Field(default=None)
    leak_present: bool = Field(default=None)

class TracingForm(Tracing):
    tracing_file:  Path = Field(default=None, description="Upload a .txt file", pattern=".+\.txt$")
    ebc: int = Field(default=None)

class ImagesForm(Images):
    dcm_file: str = Field(default=None, description="Upload a .dcm file", pattern=".+\.dcm$")
    folder_path: str = Field(default=None, description="Path to a folder")

class DicomSeries(Dicomseries):
    zip_file: str = Field(default=None, description="Upload a .zip file with DICOMs", pattern=".+\.zip$")

class MultiForm(BaseModel):
    patient_form: PatientCharacteristicsForm
    tracing_form: TracingForm
    images_form: ImagesForm