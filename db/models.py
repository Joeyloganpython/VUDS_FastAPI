from pydantic import BaseModel, Field
from pathlib import Path


class PatientCharacteristics(BaseModel):
    __tablename__ = "demographics" 
    age: int
    sex: str  # Use str for "M" or "F"
    weight: int
    reflux: bool  # Binary field (True or False)
    leak_present: bool  # Binary field (True or False)


class Tracing(BaseModel):
    tracing_file: Path = Field(..., description="Upload a .txt file", pattern=".+\.txt$")
    ebc: int

class Images(BaseModel):
    dcm_file: str = Field(..., description="Upload a .dcm file", pattern=".+\.dcm$")
    folder_path: str = Field(..., description="Path to a folder")

class Dicomseries(BaseModel):
    zip_file: str = Field(..., description="Upload a .dcm file", pattern=".+\.zip$")
