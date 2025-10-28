import os
import shutil
import face_recognition


j = 0
errors = []
dir = "self_photos"
photolen = len(os.listdir(dir))
tag = photolen / 100
print(f"Loaded {photolen} photos. Scanning for matches...")
print("<", end="")
for i in range(100):
    print("-", end="")
i = 0
print(">")
found = 0
print("[", end="")
for photo in os.listdir(dir):
    if not str(photo).__contains__("("):
        known_image = face_recognition.load_image_file("unknown.jpeg")

        unknown_image = face_recognition.load_image_file(f"{dir}/{photo}")

        self_encoding = face_recognition.face_encodings(known_image)[0]
        try:
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
            results = face_recognition.compare_faces([self_encoding], unknown_encoding)
            if str(results).__contains__("True"):
                shutil.move(f"{dir}/{photo}", f"self_photos/{photo}")
                found += 1
        except IndexError as e:
            errors.append(e)
    i += 1
    while j*tag < i:
        j += 1
        print(".", end="")
print("]")
state = ""
if found != 1:
    state = "es"
print(f"Found {found} match{state}.")


if len(errors) > 0:
    print("Errors are: ", end='')
for error in errors:
    print(error)
