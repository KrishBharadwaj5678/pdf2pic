import streamlit as st
import fitz
import zipfile
import os

st.set_page_config(
    page_title="Extract PDF images - quick, online, free",
    page_icon="icon.png",
    menu_items={
        "About":"Our streamlined tool extracts high-quality images from your PDFs and compiles them into a convenient ZIP file. Perfect for designers, researchers, and anyone who needs to access and utilize images embedded in PDFs. Get started today and bring your documents to life with ease!"
    }
)

st.write("<h2 style='color:#EA6E55;'>Transform Your PDFs into Images.</h2>",unsafe_allow_html=True)

pdf_file=st.file_uploader("Upload Your PDF",type="pdf")

btn=st.button("Extract Images")

if btn:

    # Removing the zip file
    zip_file_path = os.path.join(os.getcwd(), "extract.zip")
    if os.path.exists(zip_file_path):
         os.remove(zip_file_path)

    # Deleting All Images 
    for filename in os.listdir(os.path.join(os.getcwd(),"images")):
         os.remove(os.path.join(os.getcwd(),"images",filename))

    count=1
    if pdf_file:
        pdf_doc = fitz.open(stream=pdf_file.read())

        for page_num in range(len(pdf_doc)):
            page=pdf_doc.load_page(page_num)
            images=page.get_images(full=True)

            for index,image in enumerate(images):
                xref = image[0]
                base_image = pdf_doc.extract_image(xref)
                image_bytes = base_image["image"]
                filepath=os.path.join("images")

                # Writing image in images folder
                with open(f"{os.path.join(os.getcwd(),"images",f'extract{count}.png')}","wb") as image:
                        image.write(image_bytes)
                
                # Writing image in extract.zip 
                with zipfile.ZipFile("extract.zip","a") as zip:
                        path=os.path.join(os.getcwd(),"images",f'extract{count}.png')
                        zip.write(os.path.relpath(path,os.getcwd()))
                count+=1

        with open(os.path.join(os.getcwd(),"extract.zip"),"rb") as f:
             st.download_button("⬇️ Download",f,"Image.zip")

    else:
        st.warning("Upload A PDF File!")