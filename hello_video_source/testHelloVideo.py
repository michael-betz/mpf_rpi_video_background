import hello_video

p = hello_video.HelloVideoPlayer()
print("Enter `0` to play ./loop0.h264")
while True:
    lId = int(input("?"))
    p.play("./loop{0:d}.h264".format(lId), True, -100)
