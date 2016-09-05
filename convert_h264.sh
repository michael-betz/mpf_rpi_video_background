for f in *.{mov,mp4}; do 
    OUT_FILE_NAME="./encoded/${f%.*}.h264"
    if [ -e $OUT_FILE_NAME ]; then 
        echo "Skipping: $OUT_FILE_NAME";
    else
        echo "Encoding: $OUT_FILE_NAME";
        # Crop
        ffmpeg -i "$f" -filter:v "crop=1280:800:in_w/2-640:in_h/2-400" -an -bsf:v h264_mp4toannexb $OUT_FILE_NAME;
        # Resize
        #ffmpeg -i "$f" -vf scale=1280:800 -an -bsf:v h264_mp4toannexb $OUT_FILE_NAME;
    fi
done


