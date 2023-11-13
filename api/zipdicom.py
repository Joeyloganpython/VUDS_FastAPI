import numpy as np
import cv2
import zipfile
import pydicom
import io
from api.dicom_pred import Dicom_pred

class Zip_Dicom:


    @staticmethod
    def _contours(image):
        image= np.uint8(image)
        binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 13)
        binary_image = np.uint8(binary_image)  # Convert to uint8 data type
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        if len(contours) > 0:
            contour_area = cv2.contourArea(max(contours, key=cv2.contourArea))
        else:
            contour_area = 0
        return(contour_area)

    def get_dicom(self, zip_content):
        highest_contour_value = -1
        selected_dsa_image = None
    
        with io.BytesIO(zip_content) as zip_buffer:
            with zipfile.ZipFile(zip_buffer, "r") as zip_archive:
                for file_name in zip_archive.namelist():
                    if file_name.endswith(".dcm"):
                        with zip_archive.open(file_name) as dcm_file:
                            # Read and process the DICOM file
                            try:
                                dcm_data = dcm_file.read()
                                dicom = pydicom.dcmread(io.BytesIO(dcm_data),force=True)
                                arr = dicom.pixel_array/255
                                dst = cv2.resize(arr, (224, 224))
                                contours = self._contours(dst)
                                avg_pix_value = dst.mean()


                                if contours > highest_contour_value:
                                    highest_contour_value =contours
                                    selected_dsa_image = dicom
                                    print(selected_dsa_image)
                            except:
                                pass            

        if selected_dsa_image is not None:
            dicom_results = self.selected_dsa_image(selected_dsa_image) 
            return dicom_results     
                                     

    def selected_dsa_image(self,selected_dsa_image):
        dcm = Dicom_pred(selected_dsa_image)
        results = dcm.preprocess()
        return results


