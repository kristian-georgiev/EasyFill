from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter

def is_white(pixel_val):
    """tuple with (r, g, b) values"""
    return pixel_val > 250 # allow a small noise for white

def inside_image(coords):
    global img
    global width
    global height
    return (coords[0] >= 0 and coords[1] >= 0) and (coords[0] < width and coords[1] < height)

def extend_dir(coords, direction):
    global img
    global width
    global height
    temp_coords = coords
    for magnitude in range(max(width, height)+2):
        if not inside_image(temp_coords):
            return magnitude
        if is_white(img[temp_coords]):
            return magnitude
        temp_coords = (temp_coords[0] + direction[0], temp_coords[1] + direction[1])
    return width

def extend_up(coords):
    high = coords[1]
    low = 0
    ans = coords[1]
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(med, coords[0], coords[1], coords[0]) <= 0:
            high = med-1
            ans = min(ans, med)
        else:
            low = med+1
    return coords[1]-ans
    
def extend_down(coords):
    global height
    low = coords[1]
    high = height-1
    ans = coords[1]
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(coords[1], coords[0], med, coords[0]) <= 0:
            low = med+1
            ans = max(ans, med)
        else:
            high = med-1
    return ans-coords[1]
    
def extend_left(coords):
    high = coords[0]
    low = 0
    ans = coords[0]
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(coords[1], med, coords[1], coords[0]) <= 0:
            high = med-1
            ans = min(ans, med)
        else:
            low = med+1
    return coords[0]-ans
    
def extend_right(coords):
    global width
    low = coords[0]
    high = width-1
    ans = coords[0]
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(coords[1], coords[0], coords[1], med) <= 0:
            low = med+1
            ans = max(ans, med)
        else:
            high = med-1
    return ans-coords[0]
    
def border_distance(coords):
    return min(extend_up(coords), extend_down(coords), extend_left(coords), extend_right(coords))

def max_distance_pixel():
    global width
    global height
    max_border_distance = 0
    candidate_pixel = (1, 1)
    for i in range(0, width, 7):
        for j in range(0, height, 3):
            pixel_distance = border_distance((i, j))
            if pixel_distance > max_border_distance:
                max_border_distance = pixel_distance
                candidate_pixel = (i, j)
    return candidate_pixel

def expand_rectangle_dp(pixel):
    best_area = 0
    best_coords = (0, 0, 0, 0)

    for i in range(height):
        for j in range(height):
            # up will be at pixel[1] - i
            # down will be at pixel[1] + j
            up = pixel[1] - i
            down = pixel[1] + j
            if (not inside_image((pixel[0], up))):
                break
            if (not inside_image((pixel[0], down))):
                continue
            if white_pixels(up, pixel[0], down, pixel[0]) != 0:
                continue
            
            left = get_left(pixel[0], up, down)
            right = get_right(pixel[0], up, down)
            
            new_area = (right-left+1)*(i+j+1)
            if new_area > best_area:
                best_area = new_area
                best_coords = (pixel[0]-left, right-pixel[0], i, j)
                
    return best_coords
            
def get_left(right, up, down):
    high = right
    low = 0
    ans = right
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(up, med, down, right) == 0:
            high = med-1
            ans = min(ans, med)
        else:
            low = med+1
    return ans

def get_right(left, up, down):
    global width
    high = width-1
    low = left
    ans = left
    
    while low <= high:
        med = (low + high)//2
        if white_pixels(up, left, down, med) == 0:
            low = med+1
            ans = max(ans, med)
        else:
            high = med-1
    return ans
    
def expand_strategy(pixel, strategy):
    up = 0
    down = 0
    left = 0
    right = 0
    expanded = True
    while expanded:
        expanded = False
        
        for move in strategy:
            if move == 0: # 0 is left
                if expand_left_right(pixel[1]-up, pixel[1]+down, pixel[0]-left-1):
                    expanded = True
                    left += 1
            
            elif move == 1: # 1 is right
                if expand_left_right(pixel[1]-up, pixel[1]+down, pixel[0]+right+1):
                    expanded = True
                    right += 1
            
            elif move == 2: # 2 is up
                if expand_up_down(pixel[0]-left, pixel[0]+right, pixel[1]-up-1):
                    expanded = True
                    up += 1
                    
            else: # 3 is down
                if expand_up_down(pixel[0]-left, pixel[0]+right, pixel[1]+down+1):
                    expanded = True
                    down += 1
            
    return (left, right, up, down)

def expand_rectangle(pixel):
    best_area = 0
    best_coords = (0, 0, 0, 0)
    
    strategies = [(0, 0, 1, 1, 2, 2, 3, 3), (3, 3, 2, 2, 0, 0, 1, 1), (0, 2, 1, 3),\
                  (2, 0, 3, 1), (0, 0, 1, 1, 2, 3), (3, 3, 2, 2, 0, 1)]
    
    for strategy in strategies:
        new_coords = expand_strategy(pixel, strategy)
        new_area = (new_coords[1]+new_coords[0])*(new_coords[2]+new_coords[3])
        if new_area > best_area:
            best_area = new_area
            best_coords = new_coords
    
    return best_coords
        
def expand_up_down(left, right, line):
    global img
    for i in range(left, right+1):
        if not inside_image((i, line)) or is_white(img[(i, line)]):
            return False # cannot expand
    return True

def expand_left_right(up, down, line):
    global img
    for i in range(up, down+1):
        if not inside_image((line, i)) or is_white(img[(line, i)]):
            return False # cannot expand
    return True

def fill_white(ul, lr): # fill in rectangle from upper-left to lower-right
    global img
    for col in range(ul[0], lr[0]+1):
        for row in range(ul[1], lr[1]+1):
            img[col, row] = 255 # make everything green!
            
def fill_box(ul, lr): # fill in rectangle from upper-left to lower-right
    global img
    for col in range(ul[0], lr[0]+1):
        for row in range(ul[1], lr[1]+1):
            img[col, row] = 255 # make everything white!
    
def white_pixels(up, left, down, right): # get number of white pixels in rectangle from upper-left to lower-right
    global dp
    answer = dp[right][down]
    if up != 0:
        answer -= dp[right][up-1]
    if left != 0:
        answer -= dp[left-1][down]
    if up != 0 and left != 0:
        answer += dp[left-1][up-1]
    return answer
    
def preprocess_dp():
    global dp
    global img
    global width
    global height
    dp = []
    dp.append([])
    for i in range(height):
        dp[0].append(int(is_white(img[0, i])))
    for i in range(1, width):
        for j in range(height):
            if j == 0:
                dp.append([])
                dp[i].append(int(is_white(img[i, j])))
            else:
                dp[i].append(int(dp[i-1][j] + dp[i][j-1] - dp[i-1][j-1] + int(is_white(img[i, j]))))
                
def find_blank(num_points=5):
    boxes = []
    for num in range(num_points):
        preprocess_dp()
        point = max_distance_pixel()
        print(point)
        (left, right, up, down) = expand_rectangle_dp(point)
        fill_white((point[0]-left, point[1]-up), (point[0]+right, point[1]+down))
        boxes.append(((point[0]-left, point[1]-up), (point[0]+right, point[1]+down)))
        #fill_box((point[0]-10, point[1]-10), (point[0]+10, point[1]+10))
    return boxes

def blank_init(filename):
    im = Image.open(filename)
    im1 = im.filter(ImageFilter.FIND_EDGES)
    im2 = im1.filter(ImageFilter.MaxFilter(size=7))
    rgb_im1 = im2.convert('L')
    #rgb_im1.show()
    global img
    global dp
    global width
    global height
    width, height = rgb_im1.size
    #print(width)
    #print(height)
    img = rgb_im1.load()
    poullas = find_blank()
    #rgb_im1.show()
    return poullas
