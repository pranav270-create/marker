import os
import pypandoc


def convert_docx_to_pdf(input_file, output_file):
    try:
        pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)
        return True
    except Exception:
        return False


# List all files in the resume directory
resume_dir = "./resume"
output_dir = "./output"
files = os.listdir(resume_dir)

# Filter out .docx files
docx_files = [f for f in files if f.endswith(".docx")]

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Convert each .docx file to PDF
successful_conversions = 0
unsuccessful_files = []
for file in docx_files:
    input_path = os.path.join(resume_dir, file)
    output_path = os.path.join(output_dir, file.replace(".docx", ".pdf"))

    print(f"Converting: {file}")
    success = convert_docx_to_pdf(input_path, output_path)

    if success:
        successful_conversions += 1
        print(f"Converted: {file}")
    else:
        print(f"Failed to convert: {file}")
        unsuccessful_files.append(file)

# List files in the output directory
output_files = os.listdir(output_dir)
print(f"\nFiles in output directory: {output_files}")
print(f"Total files converted: {successful_conversions} out of {len(docx_files)}")
print(f"Unsuccessful files: {unsuccessful_files}")
# write them to text file
with open("unsuccessful_files.txt", "w") as f:
    for file in unsuccessful_files:
        f.write(file + "\n")
