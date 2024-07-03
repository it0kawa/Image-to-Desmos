import json
import cv2
import conversion
import potrace
import os

print("Copyright © 2024 [shrimp](https://github.com/it0kawa)")
print("Please provide proper credit to the author (shrimp) in any public use of this software")

frame_num = len(os.listdir('../frames/converted_frames'))

frames = []

"""
assuming every image has same size, if not comment this and uncomment the
ones inside for
"""
img = cv2.imread("../frames/convertedframes/frame0.png") 
height = img.shape[0]

# starting frame is frame1 and not fram0, SORRY
for i in range(frame_num):
    #img = cv2.imread(f"../frames/convertedframes/frame{i}.png")
    #height = img.shape[0]

    frame_latex = []
    path = conversion.img2svg(f"../frames/convertedframes/frame{i}.png")
    print(f"frame {i} of {frame_num}")
    
    """
    you can get this from the pypotrace documentation
    at https://pythonhosted.org/pypotrace/tutorial.html
    """
    
    for curve in path.curves:
        segments = curve.segments
        start_point = curve.start_point
        for segment in segments:
            x0 = start_point.x
            y0 = start_point.y
            if segment.is_corner:
                x1 = segment.c.x
                y1 = segment.c.y
                x2 = segment.end_point.x
                y2 = segment.end_point.y
                # IDK WHY THE IMAGE IS FLIPPED ON THE Y AXIS
                # i just multiplied by -1 and added its height to fix 
                frame_latex.append("((1 - t)%f + t%f, (-1*((1 - t)%f + t%f)) + %d)" % (x0, x1, y0, y1, height))
                frame_latex.append("((1 - t)%f + t%f, (-1*((1 - t)%f + t%f)) + %d)" % (x1, x2, y1, y2, height))
                
            else:
                x1 = segment.c1.x
                y1 = segment.c1.y
                x2 = segment.c2.x
                y2 = segment.c2.y
                x3 = segment.end_point.x
                y3 = segment.end_point.y
                # IDK WHY THE IMAGE IS FLIPPED ON THE Y AXIS
                # i just multiplied by -1 and added its height to fix 
                x_latex = "(1 - t)^3 * %f + 3*(1 - t)^2 * t * %f + 3 * (1 - t) * t^2 * %f + t^3 * %f" % (x0, x1, x2, x3)
                y_latex = "(-1*((1 - t)^3 * %f + 3*(1 - t)^2 * t * %f + 3 * (1 - t) * t^2 * %f + t^3 * %f)) + %d" % (y0, y1, y2, y3, height)
                latex_expression = f"({x_latex}, {y_latex})"
                frame_latex.append(latex_expression)
            
            start_point = segment.end_point
            
    frames.append(frame_latex)

server_frames = json.dumps(frames)

# i saved it into a json for convencience, i guess you could pass it to flask directly
with open('../frames/serverframes.json', 'w') as f:
    f.write(server_frames)
