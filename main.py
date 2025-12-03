from ats import print_cv, read_cv_from_pdf, read_requirements_from_text, ATSEvaluator, save_data, load_saved_data, \
    ATSConfig

path = r"C:\Users\dell\Desktop\Mohamed-Mostafa-Mohamed.pdf"
#path = r"C:\Users\dell\Desktop\Mohamed Abdelfatah.pdf"
#path = r"C:\Users\dell\Desktop\Ahmed Amr.pdf"

encoder = r"D:\Pretrained Models\nomic-embed-text-v1"
#encoder = r"all-MiniLM-L6-v2"

# cv = read_cv_from_pdf(path, encoder)
#
# save_data("CV", cv)
#
requirement = r"C:\Users\dell\Desktop\AI Engineer1.txt"

req = read_requirements_from_text(requirement, encoder)

save_data("Req", req)

cv = load_saved_data("CV.ats")
req = load_saved_data("Req.ats")

evaluator = ATSEvaluator(encoder)

print(evaluator.evaluate(cv, req))
