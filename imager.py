import Image
import ImageChops
from selenium import webdriver
from cStringIO import StringIO

verbose = 1


browser = webdriver.Firefox()
browser.get('http://127.0.0.1:8000/')
browser.maximize_window()
js = 'return Math.max( document.body.scrollHeight, document.body.offsetHeight,  document.documentElement.clientHeight,  document.documentElement.scrollHeight,  document.documentElement.offsetHeight);'

scrollheight = browser.execute_script(js)

if verbose > 0:
    print scrollheight

slices = []
offset = 0
while offset < scrollheight:
    if verbose > 0:
        print offset

    browser.execute_script("window.scrollTo(0, %s);" % offset)
    img = Image.open(StringIO(browser.get_screenshot_as_png()))
    offset += img.size[1]
    slices.append(img)

    if verbose > 0:
        browser.get_screenshot_as_file('%s/screen_%s.png' % ('/tmp', offset))
        print scrollheight


screenshot = Image.new('RGB', (slices[0].size[0], scrollheight))
offset = 0
for img in slices:
    screenshot.paste(img, (0, offset))
    offset += img.size[1]

screenshot.save('screen2.png')
browser.quit()

im1 = Image.open("screen1.png")
im1 = im1.convert('RGB')
im2 = Image.open("screen2.png")
im2 = im2.convert('RGB')

diff = ImageChops.difference(im2, im1)

diff.save("diff.png")