import os
from PyPDF2 import PdfMerger
import streamlit as st
from tempfile import NamedTemporaryFile

def merge_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)

    output_file = NamedTemporaryFile(delete=False, suffix=".pdf")
    merger.write(output_file.name)
    merger.close()
    return output_file.name

st.title("PDF Merger App")
st.write("Upload multiple PDF files, arrange them in your preferred order, and merge them into one.")

# File uploader
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    st.write("### Uploaded Files")
    file_names = [file.name for file in uploaded_files]

    # Reorder files using multiselect widget
    reordered_files = st.multiselect("Reorder PDFs", file_names, default=file_names)

    # Merge button
    if st.button("Merge PDFs"):
        if len(reordered_files) == 0:
            st.error("Please select at least one PDF to merge.")
        else:
            # Match reordered file names to uploaded files
            pdf_files = [file for name in reordered_files for file in uploaded_files if file.name == name]
            merged_pdf_path = merge_pdfs(pdf_files)

            # Provide download link for merged PDF
            with open(merged_pdf_path, "rb") as merged_pdf:
                st.download_button(label="Download Merged PDF", data=merged_pdf, file_name="merged_output.pdf", mime="application/pdf")
