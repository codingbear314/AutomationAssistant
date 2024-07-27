# import the opencv library 
import cv2 
  
  
# define a video capture object 
vid = cv2.VideoCapture(0) 
print(1)
ret, frame = vid.read() 
cv2.imshow('frame', frame) 

cv2.waitKey(0)