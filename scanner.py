import os
import shutil
import face_recognition as fr
import time

# Variables you can change
dir = "photos"
self_image = "self.jpeg"
# ========================

j = 0
photolen = len(os.listdir(dir))  # Number of photos in target folder
tag = photolen / 100
errors = []
found = 0


def compare_photos(photo):
    if not str(photo).__contains__("("):  # Avoid duplicates (e.g. img(1).jpg)

        known_image = fr.load_image_file("self.jpeg")

        unknown_image = fr.load_image_file(f"{dir}/{photo}")

        self_encoding = fr.face_encodings(known_image)[0]
        try:
            unknown_encoding = fr.face_encodings(unknown_image)[0]
            results = fr.compare_faces([self_encoding], unknown_encoding)
            if str(results).__contains__("True"):
                shutil.move(f"{dir}/{photo}", f"self_photos/{photo}")
                return 1
            else:
                return 0
        except IndexError as e:
            errors.append(e)


start_time = time.process_time()
found += compare_photos(os.listdir(dir)[0])
avg_dur = time.process_time() - start_time

print(f"Loaded {photolen} photos. Estimated {round(photolen*avg_dur/60, 1)} minutes.\
 Scanning for matches...")
print("<", end="")
for i in range(100):
    print("-", end="")
i = 0
print(">")


print("[", end="")
for photo in os.listdir(dir):
    i += 1
    if i == 1:
        continue
    start = time.process_time()
    found += compare_photos(photo)
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
