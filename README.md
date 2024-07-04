# Image to Desmos
This repo let's you convert an image (or frames of videos) to Bezier functions and sends them to a Desmos calculator.

## Why / Thanks
<p>I am in college and this is my first more or less serious project that i did MOSTLY by myself (i had to search for help for some js parts and some flask things).</p>
<p>It probably sucks (especially the js parts) but yeah im kinda proud of myself for using the documentations and planning almost everything by myself for the first time.</p>

I learned a lot :D and did a funny video, check it out [here!](https://youtu.be/L6Y5WIH5WVQ)<br>

Huge thanks to [Junferno](https://www.youtube.com/@Junferno) for insipiring me and giving me an overall idea on how to do this with the explanations in this [video](https://www.youtube.com/watch?v=BQvBq3K50u8).
</p>

## Installation
Use [pip](https://pip.pypa.io/en/stable/) to install the requirements.

```bash
pip install requirements.txt
```

## Setup
**1. Get your images**
<p>Get your image (or images). If you want to render a video, you could use ffmpeg to separate the video into frames with.</p>

```bash
ffmpeg -i video.mp4 -vf fps=24 -start_number 0 frame%d.png
```

I recommend saving your original frames in [originalframes](.\frames\originalframes) to follow a general structure. However, **it's not required**. 

**<br>2. Converting Your images**
- Convert your images from BGR to GRAY (if they weren't) to apply canny.<br><br>
- Canny makes the background black and the lines white, you should use reverse in [`conversion`](./backend/conversion.py) to change that before converting to .svg format.<br><br>
- There are many ways to do this but i provided very simple functions in [`conversion.py`](./backend/conversion.py).
</p>

**Your code could look like this (example).**

```python
import conversion #make sure conversion is in the same directory
import cv2
import os

# assuming this code is executed in the backend directory
num_frames = len(os.listdir('../frames/originalframes'))
for i in range(num_frames):
    img = cv2.imread(f"../frames/originalframes/frame{i}.png")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny_img = conversion.canny(gray_img)
    reversed_img = conversion.reverse(canny_img)
    cv2.imwrite(f"../frames/convertedframes/frame{i}.png", reversed_img) 
print("finished!")
```

**<br>3. Note that:**
- you **must only** store your converted frames, in [convertedframes](.\frames\convertedframes).
- your desmos calculator screenshots will be stored in [desmosframes](.\frames\desmosframes).


**<br>4.You might want to change some variables:**

in [`index.html`](./frontend/index.html):<br>
```JavaScript
// lagtrain is 1280x720, adjust for others
const xmin = -100;
const xmax = 1380;
const ymin = -100;
const ymax = 820;

...

// restrictions (for black frames i just used 2 inequations)
calculator.setExpression({ id: 'bottom', latex: 'y=0 \\{0 <= x <= 1280\\}', color: '#000000' });
calculator.setExpression({ id: 'top', latex: 'y=720 \\{0 <= x <= 1280\\}', color: '#000000' });
calculator.setExpression({ id: 'left', latex: 'x=0 \\{0 <= y <= 720\\}', color: '#000000' });
calculator.setExpression({ id: 'right', latex: 'x=1280 \\{0 <= y <= 720\\}', color: '#000000' });
```

the waiting time to take a screenshot in [`index.html`](./frontend/index.html):<br>
```JavaScript
async function screenshot(index, is_empty) {
    console.log("taking a screenshot..."); 
    // wait to ensure the frame is rendered most of the times
    await sleep(5000);  
    
    ...
}
```

</p>

## Usage
- Execute [`calculate_frames.py`](./backend/calculate_frames.py). **(the expressions will be stored in [`serverframes.json`](.\frames\serverframes.json))**. 
- [`serverframes.json`](.\frames\serverframes.json) **must** be kept in [frames](.\frames) directory.
- Upload [`serverframes.json`](.\frames\serverframes.json) to your local server with [`app.py`](./backend/app.py).
- Open [`index.html`](./frontend/index.html) with your browser.
- Type start() in the browser's console and you are ready to go!

## Copyright

Copyright © 2024 [shrimp](https://github.com/it0kawa). Please provide proper credit to the author (shrimp) in any public use of this software.

This project is licensed under the GNU General Public License v3.0. See the [`LICENSE`](./LICENSE) file for details.

## Terms of Service
Anyone who uses this software should comply with the [Desmos Terms of Service](https://www.desmos.com/terms). **This swoftware and it's author arent responsible for any User use or modification that constitutes a breach in those terms.**