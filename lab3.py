import pydicom
import matplotlib.pyplot as plt
import streamlit as st

def load_dicom_file(file):
    if file:
        dicom_data = pydicom.dcmread(file)
        return dicom_data
    else:
        st.error("Please upload a DICOM file")
        return None

def show_patient_position(dicom_data):
    patient_position = dicom_data.get("PatientPosition", "No Patient Position found")
    return f"Patient Position: {patient_position}"

# Відображення зображення DICOM з текстом або без
def show_image(dicom_data, show_text):
    pixel_array = dicom_data.pixel_array
    plt.imshow(pixel_array, cmap=plt.cm.gray)
    if show_text:
        patient_position_text = show_patient_position(dicom_data)
        plt.text(10, 10, patient_position_text, color='red', fontsize=12, backgroundcolor='white')
    plt.title("DICOM Image")
    st.pyplot(plt)


st.title("DICOM Viewer")

uploaded_file = st.file_uploader("Choose a DICOM file", type=["dcm"])

if uploaded_file is not None:
    dicom_data = load_dicom_file(uploaded_file)
    if dicom_data:
        show_text = st.checkbox("Show Patient Position Information", value=False)

        show_image(dicom_data, show_text)