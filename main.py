from ats import print_cv, read_cv_from_pdf, read_text_file,RequirementParser

#path = r"C:\Users\dell\Desktop\Mohamed-Mostafa-Mohamed.pdf"
#path = r"C:\Users\dell\Desktop\Mohamed Abdelfatah.pdf"
#path = r"C:\Users\dell\Desktop\Ahmed Amr.pdf"

encoder = r"D:\Pretrained Models\nomic-embed-text-v1"

#print_cv(read_cv_from_pdf(path, encoder))

requirement = r"C:\Users\dell\Desktop\AI Engineer1.txt"

parser = RequirementParser(encoder)

print(parser.parse_requirement(read_text_file(requirement)))