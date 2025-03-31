'''
GOAL: balance between clean code, coding style and performance
	- Efficient logic can be developed to determine if two shapes overlap, intersect, 
		or if one is contained within the other, using one or two functions. 
		However, this logic tends to be complex and challenging 
		to read and follow. Additionally, testing the logic can be difficult, 
		particularly when it comes to evaluating the internal structure of the function.
	- Instead, break down the problem into smaller sub-problems, and solve each sub-problem
		one by one, using simple and easy-to-read functions, combining the proper usage of function
		parameters to enhance reusability and maintainability, and finally integrating them
		together to produce the solution to the original problem.
	- To acheive optimal efficiency and performance, analyses the code structure and flow to ensure the correct
		order of execution and avoid unnecessary calculations.

Process: 
	Pick a random polygon shape and a color
	Stretch the chosen polygon
	Repeatedly pick a random x,y position and try to fit the choosen shape so that
		1/ it doesn't touch any other shapes
		2/ it doesn't overlap with any other shapes
		3/ it doesn't hide inside another shape
'''
import turtle
import random
import time

# global constants
YOUR_ID = '124090767'   # TODO: your student id
COLORS = ('green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown')
SHAPE_FILE = 'shapes.txt'
SCREEN_DIM_X = 0.7  # screen width factor
SCREEN_DIM_Y = 0.7  # screen height factor
XY_SPAN = 0.8       # canvas factor 
XY_STEP = 10        # step size of x,y coordinates
MIN_DURATION = 5    
MAX_DURATION = 30
MIN_STRETCH = 1
MAX_STRETCH = 10
MIN_SEED = 1
MAX_SEED = 99

# global variables
g_shapes = []       # list of polygons displayed on canvas
g_screen = None
g_range_x = None
g_range_y = None

def is_shape_overlapped_any(shape: turtle.Turtle, shapes: list[turtle.Turtle]) -> bool:
    """
    检查给定形状是否与列表中的任何形状或画布边界接触、重叠或被包含。

    Args:
        shape (turtle.Turtle): 要检查的形状。
        shapes (list[turtle.Turtle]): 要比较的形状列表。
        canvas_size (tuple): 画布大小 (width, height)。

    Returns:
        bool: 如果形状与任何其他形状或画布边界接触、重叠或被包含，则返回 True;否则返回 False。
    """
    def get_aabb(shape: turtle.Turtle) -> tuple:
        """
        获取形状的 AABB 边界框。

        Args:
            shape (turtle.Turtle): 要计算的形状。

        Returns:
            tuple: AABB 边界框 (min_x, min_y, max_x, max_y)。
        """
        x, y = shape.position()
        width = shape.shapesize()[0] * 20
        height = shape.shapesize()[1] * 20

        min_x = x - width / 2
        max_x = x + width / 2
        min_y = y - height / 2
        max_y = y + height / 2

        return (min_x, min_y, max_x, max_y)

    def is_aabb_overlapping(aabb1: tuple, aabb2: tuple) -> bool:
        """
        检查两个 AABB 是否重叠。

        Args:
            aabb1 (tuple): 第一个 AABB。
            aabb2 (tuple): 第二个 AABB。

        Returns:
            bool: 如果重叠返回 True,否则返回 False。
        """
        return not (aabb1[2] < aabb2[0] or aabb1[0] > aabb2[2] or
                    aabb1[3] < aabb2[1] or aabb1[1] > aabb2[3])
        
    def get_polygon_vertices(shape: turtle.Turtle) -> list:
        """Get shape's vertices with position and scaling applied."""
        x, y = shape.xcor(), shape.ycor()
        shape_size = shape.shapesize()
        vertices = []
        
        # Get the original shape vertices
        original_shape = shape.get_shapepoly()
        if not original_shape:
            return vertices
            
        # Apply scaling and translation
        for vx, vy in original_shape:
            new_x = vx * shape_size[0] + x
            new_y = vy * shape_size[1] + y
            vertices.append((new_x, new_y))
        return vertices
    
    def polygons_collide(vertices1: list[tuple], vertices2: list[tuple]) -> bool:
        """使用分离轴定理(SAT)检测两个凸多边形是否碰撞"""
        def get_edges(vertices):
            """生成所有边的法线轴"""
            edges = []
            for i in range(len(vertices)):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i+1) % len(vertices)]#闭合多边形
                edge = (x2 - x1, y2 - y1)
                # 法线轴为 (-dy, dx) 并归一化
                dx, dy = edge
                length = (dx**2 + dy**2) ** 0.5
                if length == 0:
                    continue
                axis = (-dy/length, dx/length)
                edges.append(axis)
            return edges
    
        def project(vertices, axis):
            """将顶点投影到轴上，返回投影区间"""
            dots = [x*axis[0] + y*axis[1] for (x, y) in vertices]
            return min(dots), max(dots)

         # 检查所有可能的分离轴

        for axis in get_edges(vertices1) + get_edges(vertices2):
            proj1 = project(vertices1, axis)
            proj2 = project(vertices2, axis)
            if proj1[1] < proj2[0] or proj2[1] < proj1[0]:
                return False  # 存在分离轴，不相交
        return True

   

    # 获取当前形状的 AABB 和顶点
    shape_aabb = get_aabb(shape)
    shape_vertices = get_polygon_vertices(shape)

    

    # 检查是否与其他形状重叠
    for other_shape in shapes:
        other_aabb = get_aabb(other_shape)
        other_vertices = get_polygon_vertices(other_shape)

        # AABB 快速排除
        if not is_aabb_overlapping(shape_aabb, other_aabb):
            continue

        # SAT 精确检测
        if polygons_collide(shape_vertices,other_vertices):
            return True

    return False

############################################
################## template ################
############################################

def create_shape(shape:turtle.Turtle, color:str, sz_x:int = 1, sz_y:int = 1) -> turtle.Turtle:
	'''
	Create a turtle shape with specified parameters.
	
	Args:
		shape (turtle.Turtle): The base shape for the turtle.
		color (str): The color to set for the turtle.
		sz_x (int, optional): Horizontal stretch factor for the shape. Defaults to 1.
		sz_y (int, optional): Vertical stretch factor for the shape. Defaults to 1.
	
	Returns:
		turtle.Turtle: A configured turtle object with specified shape, color, and size.
	'''
	t = turtle.Turtle(shape)
	t.up()
	t.color(color)
	t.shapesize(sz_y, sz_x)
	return t

def get_random_home_position(range_x:list[int], range_y:list[int]) -> tuple[int,int]:
	'''
	Generates a random (x, y) coordinate tuple by sampling from 
	the provided x and y coordinate ranges.
	
	Args:
		range_x (list[int]): A list of possible x-coordinate values to sample from.
		range_y (list[int]): A list of possible y-coordinate values to sample from.
	
	Returns:
		tuple[int, int]: A randomly selected (x, y) coordinate pair.
	'''
	x = random.sample(range_x, 1)[0]
	y = random.sample(range_y, 1)[0]   
	return (x,y)

def place_a_random_shape(shape:turtle.Turtle, started:float, duration:int) -> None:
	'''
	Repeatedly tries to place the given shape at random coordinates 
	within the predefined canvas range.
	If the shape does not overlap with existing shapes, 
	it is added to the global shapes list and the screen is updated.
	
	Args:
		shape (turtle.Turtle): The turtle shape to be placed on the canvas.
		started (float): The timestamp when the placement process began.
		duration (int): The maximum time allowed for attempting to place the shape.
	'''
	while time.time() - started <= duration:
		x, y = get_random_home_position(g_range_x, g_range_y)
		shape.goto(x, y)
		if is_shape_overlapped_any(shape, g_shapes) is False:
			g_shapes.append(shape)
			g_screen.title(f'{YOUR_ID} - {len(g_shapes)}')
			g_screen.update()
			break

def fill_canvas_with_random_shapes(shapes:list[turtle.Turtle], colors:list[str], 
						 stretch_factor:int, duration:int) -> float:
	'''
	Fills the canvas with randomly positioned and colored shapes 
	within a specified time duration.
	
	Args:
		shapes (list[turtle.Turtle]): A list of available polygon shapes to choose from.
		colors (list[str]): A list of available colors to apply to the shapes.
		stretch_factor (int): The factor by which to stretch the shapes.
		duration (int): The maximum time allowed for placing shapes.
	
	Returns:
		float: The timestamp when the shape placement process started.
	'''
	started = time.time()
	while time.time() - started <= duration:
		shape = random.sample(shapes,1)[0]
		color = random.sample(colors,1)[0]
		turtle_obj = create_shape(shape, color, stretch_factor, stretch_factor)
		place_a_random_shape(turtle_obj, started, duration)

	return started


def import_custom_shapes(file_name:str) -> list[str]:
	'''
	Import custom turtle shapes from a file with predefined shape names and coordinates,
	where each line contains a shape name and its coordinates separated by a colon.
	
	Add each shape to the turtle screen and returns a list of imported shape names.

	Args:
		file_name (str): Path to the file containing custom shape definitions.

	Returns:
		list[str]: A list of names of the imported custom shapes.
	'''
	shapes = []
	with open(file_name, 'r') as f:
		for line in f.readlines():
			if line.find(':') == -1:
				continue
			name, coordinates = line.split(':')
			coordinates = eval(coordinates) # ok for internal use
			g_screen.addshape(name, coordinates)
			shapes.append(name)

	return shapes
	

def setup_canvas_ranges(w:int, h:int, span:float=0.8, step:int=10) -> tuple[list[int], list[int]]:
	'''
	Calculate valid coordinate ranges for canvas placement.
	
	Args:
		w (int): Canvas width.
		h (int): Canvas height.
		span (float, optional): Proportion of canvas to use. Defaults to 0.8.
		step (int, optional): Increment between coordinate values. Defaults to 10.
	
	Returns:
		tuple[list[int], list[int]]: A tuple containing x and y coordinate ranges, 
		centered at (0,0) within the specified canvas span.
	'''
	sz_w, sz_h = int(w/2*span), int(h/2*span)
	return range(-sz_w, sz_w, step), range(-sz_h, sz_h, step)

def setup_screen() -> turtle.Screen:
	'''
	Initialize and configure a turtle graphics screen with specific settings.

	Sets up a screen with auto-refresh disabled, predefined dimensions, 
	and logo mode orientation to prevent custom shape rotation.

	Returns:
		turtle.Screen: A configured turtle graphics screen ready for drawing.
	'''
	scrn = turtle.Screen()
	scrn.tracer(0)  # disable auto refresh
	scrn.setup(SCREEN_DIM_X, SCREEN_DIM_Y, starty=10)
	scrn.mode("logo") # heading up north to avoid rotation of custom shapes

	return scrn

def get_time_str(time_sec) -> str:
	'''
	Convert a timestamp in seconds to a formatted time string.

	Args:
		time_sec (float): The timestamp in seconds since the epoch.

	Returns:
		str: A formatted time string in "HH:MM:SS" format.
	'''
	struct_time = time.localtime(time_sec)
	return time.strftime("%H:%M:%S", struct_time)

def show_result(started:float, count:int) -> None:
	'''
	Display the final results of the drawing process, 
	including student ID, start and end times, duration, and shape count.
	
	Args:
		started (float): The timestamp when the drawing process began.
		count (int): The total number of shapes drawn during the process.
	
	Side effects:
		- Updates the screen title with ID, timing and count information
		- Changes screen background color to black
		- Prints student ID and shape count to console
	'''
	ended = time.time()	# end time 
	start_time = get_time_str(started)
	end_time = get_time_str(ended)
	diff = round(ended-started,2)

	g_screen.title(f'{YOUR_ID} {start_time} - {end_time} - {diff} - {count}')
	g_screen.bgcolor('black')
	print(f'{YOUR_ID},{count}')	# output your student id and shape count

def prompt(prompt:str, default:any) -> str:
	'''
	Prompts the user for input with a default value.
	
	Args:
		prompt (str): The input prompt message to display.
		default (any): The default value to return if no input is provided.
	
	Returns:
		str: The user's input, or the default value if no input is given.
	'''
	ret = input(f'{prompt} (default is {default}) >')
	return default if ret == "" else ret

def prompt_input() -> tuple[int,int,int,str]:
	'''
	Interactively prompt the user for drawing configuration parameters.
	
	Prompts for and validates user inputs for:
	- Minimum shape stretch value
	- Random seed for reproducibility
	- Drawing duration
	- Termination preference
	
	Returns:
		tuple[int,int,int,str]: A tuple containing (min_stretch, seed, duration, termination)
		with each value validated against predefined constraints.
	
	Raises:
		AssertionError: If any input value is outside its allowed range.
	'''
	min_stretch = int(prompt("Stretch Value", 1))
	assert MIN_STRETCH <= min_stretch <= MAX_STRETCH, \
		f"Stretch Value out of range {MIN_STRETCH} - {MAX_STRETCH}"
	
	seed = int(prompt("Random Seed", 1))
	assert MIN_SEED <= seed <= MAX_SEED, \
		f"Invalid Random Seed out of range {MIN_SEED} - {MAX_SEED}"
	
	duration = int(prompt("Duration (s)", 5))
	assert MIN_DURATION <= duration <= MAX_DURATION, \
		f"Invalid Duration out of range {MIN_DURATION} - {MAX_DURATION}"
	
	termination = prompt("Terminate", 'n')
	assert termination in ('y', 'n'), "Invalid Termination, must be y or n"

	return min_stretch, seed, duration, termination

def main() -> None:
	'''
	Main function to orchestrate the polygon drawing process.
	
	Configures the screen and canvas, imports custom shapes, prompts user for drawing parameters,
	initializes random seed, fills canvas with random shapes, and handles optional termination.
	
	Global variables are used to manage screen and drawing range state.
	
	Args:
		None
	
	Returns:
		None
	'''
	global g_screen, g_range_x, g_range_y
   
	g_screen = setup_screen()

	g_range_x, g_range_y = setup_canvas_ranges(g_screen.window_width(), 
											   g_screen.window_height(),
											   XY_SPAN, XY_STEP)
	
	shapes = import_custom_shapes(SHAPE_FILE)

	min_stretch, seed, duration, termination = prompt_input()

	random.seed(seed)

	started = fill_canvas_with_random_shapes(shapes, COLORS, min_stretch, duration)
	
	show_result(started, len(g_shapes))
	
	if termination == 'y':
		turtle.bye()

if __name__ == '__main__':
	main()
	g_screen.mainloop()
