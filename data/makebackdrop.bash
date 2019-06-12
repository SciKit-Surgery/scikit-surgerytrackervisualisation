#! /bin/bash

i=0
while [ $i -lt 30 ]
do
	outname=$(printf %04d.png $i)
	cp logo.png workingdir/$outname
	#convert -size 331x331 xc:"gray(50%)" -seed $i +noise random -channel blue -separate noise_graylinear_random.png
	convert -size 331x331 xc:"gray(50%)" -seed $i +noise random -separate noise_graylinear_random.png
	convert workingdir/$outname noise_graylinear_random.png -compose dissolve -define compose:args="15" -composite workingdir2/$outname
	i=$(($i+1))
done

ffmpeg -i workingdir2/%04d.png -c:v libx264 -r 30 backdrop.avi

