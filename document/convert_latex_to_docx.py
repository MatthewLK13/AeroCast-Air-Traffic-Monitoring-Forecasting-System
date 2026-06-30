import pypandoc

try:
    print("Checking pandoc...")
    pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc not found, downloading...")
    pypandoc.download_pandoc()

print("Converting main_VN.tex to docx...")
output_file = r'D:\Project\AeroCast-VAA-System-V2\AeroCast-VAA-System-V2\document\Literature_Review_Final.docx'
input_file = r'D:\Project\AeroCast-VAA-System-V2\AeroCast-VAA-System-V2\document\main_VN.tex'

pypandoc.convert_file(
    input_file, 
    'docx', 
    outputfile=output_file,
    extra_args=['--mathml'] # Pandoc naturally converts LaTeX math to DOCX native math.
)
print("Done!")
