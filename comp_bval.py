import nibabel as nib
import numpy as np
import sys
import tkinter as tk
from tkinter import filedialog


def generate_maps(path_b0_file, path_b1000_file,s,path_o):
    
    b0_img = nib.load(path_b0_file)
    b0_data = b0_img.get_fdata()
    affine = b0_img.affine
    
    b1000_img = nib.load(path_b1000_file)
    b1000_data = b1000_img.get_fdata()
    
    adc_data = np.log(b0_data / b1000_data)/1000
    # Sc = Sa exp (− [bc − ba] ADC)
    sintetic = (np.exp((1000-int(s))*adc_data)) * b1000_data
    exp_adc = np.exp(-1000*adc_data)

    guarda_niftis(adc_data, sintetic, exp_adc, affine,path_o)
    
def guarda_niftis(adc_data,sintetic,exp_adc,affine,o):

    adc_nifti= nib.Nifti1Image(adc_data, affine)
    nib.save(adc_nifti, o + "/ADC.nii.gz")

    sintetic_DWI_nifti= nib.Nifti1Image(sintetic, affine)
    nib.save(sintetic_DWI_nifti, o + "/sDWI.nii.gz")

    eadc_nifti= nib.Nifti1Image(exp_adc, affine)
    nib.save(eadc_nifti,o + "/eADC.nii.gz")

def devuelve_path_b0():
    path=filedialog.askopenfilename()
    entry_b0.delete(0,tk.END)
    entry_b0.insert(0, path)

def devuelve_path_b1000():
    path=filedialog.askopenfilename()
    entry_b1000.delete(0,tk.END)
    entry_b1000.insert(0, path)

def devuelve_path_output():
    path=filedialog.askdirectory()
    entry_destino.delete(0,tk.END)
    entry_destino.insert(0, path)

def go():
    path_b0_file=entry_b0.get()
    path_b1000_file=entry_b1000.get()
    s=entry_s.get()
    path_o=entry_destino.get()
    print(path_b0_file,path_b1000_file,path_o,s)
    generate_maps(path_b0_file, path_b1000_file,s,path_o)

root=tk.Tk()

screen_width = int(root.winfo_screenwidth() - root.winfo_screenwidth()*0.5)
screen_height = int(root.winfo_screenheight() - root.winfo_screenheight()*0.5)

root.geometry(str(screen_width) +"x" + str(screen_height)) 

lbl_description=tk.Label(text="DWI computed B value",font=("arial",20))
lbl_description.pack()

lbl_intro_path_b0=tk.Label(text="Ingrese el volumen B0:")
lbl_intro_path_b0.pack()

entry_b0=tk.Entry()
entry_b0.pack()

btn_b0=tk.Button(text="Abrir...",command=devuelve_path_b0)
btn_b0.pack()

lbl_intro_path_b1000=tk.Label(text="Ingrese el volumen B1000:")
lbl_intro_path_b1000.pack()

entry_b1000=tk.Entry()
entry_b1000.pack()

btn_b1000=tk.Button(text="Abrir...",command=devuelve_path_b1000)
btn_b1000.pack()

lbl_s_value=tk.Label(text="Ingrese el valor B sintetico:")
lbl_s_value.pack()

entry_s=tk.Entry()
entry_s.pack()

lbl_intro_path_destino=tk.Label(text="Ingrese el directorio de destino:")
lbl_intro_path_destino.pack()

entry_destino=tk.Entry()
entry_destino.pack()

btn_destino=tk.Button(text="Abrir...",command=devuelve_path_output)
btn_destino.pack()

btn_go=tk.Button(text="CREAR VOLUMENES",font=("arial",20),command=go)
btn_go.pack()

root.mainloop()