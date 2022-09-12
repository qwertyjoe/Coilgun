import glob
path = '/dev/video*'
video_files = glob.glob(path)
for i,file in enumerate(video_files[::-1]):
    video_files[i] = file[10:]
print(video_files)
# if os.path.isdir(path):
#     # files = [".", ".."] + os.listdir(path)
#     flies = os.walk(path)
#     print(files)
# else:
#     print("No such file or directory")
#     exit()