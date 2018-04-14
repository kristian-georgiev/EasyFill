def match(instruction, blanks):
    """
    Procedure that returns the coordinates of the box that is best linked to the specific instruction
    Ideas: Check upper left coordinate, or lower right coordinate
    """
    return closestK(instruction, blanks, k=1)
    
def get_center(coords):
    return ((coords[0][0] + coords[1][0])/2, (coords[0][1] + coords[1][1])/2)

def get_upper_left(coords):
    return coords[0]

def get_lower_right(coords):
    return coords[1]

def get_area(coords):
    """Returns area of blank space"""
    return (coords[1][0] - coords[0][0] + 1)*(coords[1][1] - coords[0][1] + 1)

def euclidean(instruction, blank):
    """is waiting two tuples"""
    """we will add bias such that entries lower or to the right are favored"""
    bias = instruction[0]-blank[0] + instruction[1]-blank[1]
    return (instruction[0] - blank[0])**2 + (instruction[1] - blank[1])**2 + bias

def manhattan(instruction, blank):
    """is waiting two tuples"""
    return abs(instruction[0] - blank[0]) + abs(instruction[1] - blank[1])
    
def closestK(instruction, blanks, k=3):
    blank_dist = []
    for idx in range(len(blanks)):
        blank_dist.append((euclidean(instruction, get_center(blanks[idx])), idx))
    blank_dist.sort()
    
    best_area = 0
    best_idx = 0
    for i in range(k):
        new_area = get_area(blanks[blank_dist[i][1]])
        if new_area > best_area:
            best_area = new_area
            best_idx = blank_dist[i][1]
            
    return best_idx
