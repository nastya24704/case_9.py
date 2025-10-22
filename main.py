import math
import turtle
import time
import webcolors
import local as lcl

available_colors_1 = [
    ('\U0001F48B' f'{lcl.RED}', 'red'),
    ('\U0001F499' f'{lcl.BLUE}', 'blue'),
    ('\U0001F49A' f'{lcl.GREEN}', 'green'),
    ('\U0001F49B' f'{lcl.YELLOW}', 'yellow'),
    ('\U0001F49C' f'{lcl.PURPLE}', 'purple'),
    ('\U0001F4A6' f'{lcl.CYAN}', 'cyan')
]
available_colors_2 = [
    ('\U0001F5A4' f'{lcl.BLACK}', 'black'),
    ('\U0001F47D' f'{lcl.GRAY}', 'gray'),
    ('\U0001F495' f'{lcl.PINK}', 'pink'),
    ('\U0001F9E1' f'{lcl.ORANGE}', 'orange'),
    ('\U0001F90E' f'{lcl.BROWN}', 'brown'),
    ('\U0001F916' f'{lcl.YOUR_COLOUR_HEX_ENGLISH}', None)
]


def get_valid_color_from_user(prompt: str) -> str:
    """
    Prompt user for a color input and validate whether it's a valid HEX code or color name.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: Validated color in HEX or name format.
    """

    while True:
        user_input = input(prompt).strip().lower()
        if user_input.startswith('#'):
            if len(user_input) in (4, 7):
                return user_input
            print(f'{lcl.ERROR_INVALID_HEX}')
        else:
            try:
                webcolors.name_to_hex(user_input)
                return user_input
            except ValueError:
                print(f'{lcl.ERROR_UNKNOWN_COLOR}')


def get_color_choice():
    """
    Allows user to select two colors from predefined options or custom HEX/English names.

    Returns:
        tuple: Two color strings selected by the user.
    """

    print(f'{lcl.AVAILABLE_COLORS}\n')

    max_width = max(len(c[0]) for c in available_colors_1) + 3

    for i, (c1, c2) in enumerate(zip(available_colors_1, available_colors_2), start=1):
        left_num = i
        right_num = i + len(available_colors_1)
        print(f"{left_num:>2}. {c1[0]:<{max_width}} {right_num:>2}. {c2[0]}")

    def choose_color(prompt: str) -> str:
        """
        Helper function to choose a color based on user input number or custom input.

        Args:
            prompt (str): The prompt message.

        Returns:
            str: Selected color.
        """

        while True:
            try:
                num = int(input(prompt))
                if 1 <= num <= 12:
                    if num <= 6:
                        return available_colors_1[num - 1][1]
                    elif num < 12:
                        return available_colors_2[num - 7][1]
                    return get_valid_color_from_user(f'{lcl.ENTER_COLOR_HEX_ENGLISH}')
                print(f'{lcl.NUMBER_MUST_BE_1_TO_12}')
            except ValueError:
                print(f'{lcl.ENTER_NUMBER_1_TO_12}')

    first_color = choose_color(f'{lcl.ENTER_FIRST_COLOR_NUMBER}')
    second_color = choose_color(f'{lcl.ENTER_SECOND_COLOR_NUMBER}')

    return first_color, second_color


def border_thickness() -> int:
    """
    Prompt user to select border thickness.

    Returns:
        int: Border thickness value.
    """

    options = {f'{lcl.THIN}': 1, f'{lcl.MEDIUM}': 3, f'{lcl.THICK}': 5}
    print(f'{lcl.BORDER_TYPES}')

    while True:
        choice = input(f'{lcl.CHOOSE_BORDER_THICKNESS}').strip().lower()
        if choice in options:
            return options[choice]
        print(f'{lcl.INPUT_ERROR}')


def border_color() -> str:
    """
    Prompt the user to select a border color from available options.

    Returns:
        str: The selected border color name in Russian lowercase.
    """

    options = [f'{lcl.RED}'.lower(), f'{lcl.ORANGE}'.lower(), f'{lcl.YELLOW}'.lower(),
               f'{lcl.GREEN}'.lower(), f'{lcl.BLUE}'.lower(), f'{lcl.PURPLE}'.lower(),
               f'{lcl.PINK}'.lower(), f'{lcl.BLACK}'.lower(), f'{lcl.GRAY}'.lower(),
               f'{lcl.WHITE}'.lower()]

    print(f'{lcl.BORDER_COLOR}' + ", ".join(options))

    while True:
        choice = input(f'{lcl.SELECT_BORDER_COLOR}').strip().lower()
        if choice in options: return choice
        print(f'{lcl.INPUT_ERROR}')


def shadow_brightness() -> int:
    """
    Prompt user for shadow brightness.

    Returns:
        int: Shadow intensity value.
    """

    options = {f'{lcl.NO}': 0, f'{lcl.FAINT}': 5, f'{lcl.MEDIUM}': 8, f'{lcl.STRONG}': 12}


    print(f'{lcl.SHADOW_INTENSITY}')

    while True:
        choice = input(f'{lcl.SELECT_SHADOW_INTENSITY}').strip().lower()
        if choice in options:
            return options[choice]
        print(f'{lcl.INPUT_ERROR}')


def get_num_hexagons() -> int:
    """
    Prompt user for the number of hexagons in a row.

    Returns:
        int: Number of hexagons (4–20).
    """

    while True:
        val = input(f'{lcl.HEX_COUNT_IN_ROW}').strip()
        if val.isdigit() and 4 <= int(val) <= 20:
            return int(val)
        print(f'{lcl.ERROR_INVALID_NUMBER}')


def calculate_side_length(number: int, size: float) -> float:
    """
    Calculate the side length of each hexagon based on total size and number of hexagons.

    Args:
        number (int): Number of hexagons.
        size (float): Total size or width constraint.

    Returns:
        float: Computed side length of a hexagon.
    """

    return size / (number + 0.5)


def calculate_hexagon_centers(number: int, size: float) -> tuple:
    """
    Calculate the centers coordinates for a grid of hexagons.

    Args:
        number (int): Number of hexagons per row and column.
        size (float): Approximate total size of the grid.

    Returns:
        tuple: (list of (x, y) centers, side length of hexagons)
    """

    side = calculate_side_length(number, size)
    width_hex = math.sqrt(3) * side

    total_width = width_hex * number
    total_height = side * 1.5 * number

    start_x = -total_width / 2 + width_hex / 2
    start_y = total_height / 2 - side / 2

    centers = []

    for row in range(number):
        y = start_y - row * side * 1.5

        for col in range(number):
            x = start_x + col * width_hex
            if row % 2 == 1:
                x += width_hex / 2
            centers.append((x, y))

    return centers, side


def preview_colors(color1: str, color2: str) -> None:
    """
    Show a preview of the selected colors as filled squares.

    Args:
        color1 (str): First color.
        color2 (str): Second color.
    """

    turtle.clearscreen()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.bgcolor("white")

    def draw_square(x, y, color, label) -> None:
        """
        Draw a filled square with a label.

        Args:
            x (float): X-coordinate.
            y (float): Y-coordinate.
            color (str): Fill color.
            label (str): Label text.
        """

        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()

        turtle.fillcolor(color)
        turtle.begin_fill()

        for _ in range(4):
            turtle.forward(100)
            turtle.right(90)

        turtle.end_fill()

        turtle.penup()
        turtle.goto(x + 50, y - 30)
        turtle.color("black")
        turtle.write(label, align="center", font=("Arial", 14, "normal"))

    draw_square(-150, 50, color1, f'{lcl.COLOR_1}: {color1}')
    draw_square(50, 50, color2, f'{lcl.COLOR_2}: {color2}')

    turtle.penup()
    turtle.goto(0, -100)
    turtle.write(f'{lcl.START_DRAWING_PROMPT}',
                 align="center", font=("Arial", 14, "italic"))
    input(f'\n{lcl.START_DRAWING_WAIT}')


color_map = {
    f'{lcl.RED}'.lower(): 'red',
    f'{lcl.ORANGE}'.lower(): 'orange',
    f'{lcl.YELLOW}'.lower(): 'yellow',
    f'{lcl.GREEN}'.lower(): 'green',
    f'{lcl.BLUE}'.lower(): 'blue',
    f'{lcl.PURPLE}'.lower(): 'purple',
    f'{lcl.PINK}'.lower(): 'pink',
    f'{lcl.BLACK}'.lower(): 'black',
    f'{lcl.GRAY}'.lower(): 'gray',
    f'{lcl.WHITE}'.lower(): 'white',
    f'{lcl.BROWN}'.lower(): 'brown'
}


def draw_shadow(x: float, y: float, side: float, shadow_intensity: int) -> None:
    """
    Draw a shadow hexagon offset from the main hexagon.

    Args:
        x (float): X coordinate of the main hexagon.
        y (float): Y coordinate of the main hexagon.
        side (float): Side length of the hexagon.
        shadow_intensity (int): Offset for shadow.
    """

    if shadow_intensity == 0:
        return

    shadow_x = x + shadow_intensity
    shadow_y = y - shadow_intensity

    turtle.penup()
    turtle.goto(shadow_x, shadow_y)
    turtle.pendown()

    turtle.fillcolor("#686868")
    turtle.begin_fill()
    turtle.setheading(30)

    for _ in range(6):
        turtle.forward(side)
        turtle.right(60)

    turtle.end_fill()
    turtle.setheading(0)


def draw_hexagon(x: float, y: float, side: float, color: str) -> None:
    """
    Draw a filled hexagon at given coordinates.

    Args:
        x (float): X coordinate.
        y (float): Y coordinate.
        side (float): Side length of hexagon.
        color (str): Fill color.
    """

    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.setheading(30)

    for _ in range(6):
        turtle.forward(side)
        turtle.right(60)

    turtle.end_fill()
    turtle.setheading(0)


def draw_hexagon_border(x, y, side, thickness, color) -> None:
    """
    Draws the border of a hexagon at a specified position.

    Args:
        x (float): The x-coordinate of the hexagon's starting position.
        y (float): The y-coordinate of the hexagon's starting position.
        side (float): The length of each side of the hexagon.
        thickness (int): The border's line thickness.
        color (str): The color of the border.
    """

    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

    turtle.pencolor(color_map.get(color, "black"))
    turtle.pensize(thickness)
    turtle.setheading(30)

    for _ in range(6):
        turtle.forward(side)
        turtle.right(60)

    turtle.setheading(0)
    turtle.pensize(1)


def chess_pattern(N: int, color_first: str, color_second: str) -> list:
    """
    Generates a list of colors for a chessboard pattern.

    Args:
        N (int): The size of the grid (number of hexagons in each row and column).
        color_first (str): The first color option.
        color_second (str): The second color option.

    Returns:
        list: A list of length N*N with colors assigned in a chessboard pattern.
    """

    colors = []
    if N % 2 == 0:
        for i in range(N // 2):
            for col in range(N):
                colors.append(color_first)
                colors.append(color_second)
            for col in range(N):
                colors.append(color_second)
                colors.append(color_first)
    else:
        for i in range((N - 1) // 2):
            for col in range(N):
                colors.append(color_first)
                colors.append(color_second)
            for col in range(N):
                colors.append(color_second)
                colors.append(color_first)
        for i in range(N):
            color = color_first if i % 2 == 0 else color_second
            colors.append(color)

    return colors


def alternation(N: int, pattern_type: str, color_first: str, color_second: str) -> list:
    """
    Generates a list of colors for an alternating pattern.

    Args:
        N (int): The grid size.
        pattern_type (str): Either 'по строкам' (by rows) or 'по столбцам' (by columns).
        color_first (str): The first color.
        color_second (str): The second color.

    Returns:
        list: The list of colors following the selected pattern.
    """

    colors = []

    if pattern_type == f'{lcl.ROW_BY_ROW}':
        for row in range(N):
            color = color_first if row % 2 == 0 else color_second
            for _ in range(N):
                colors.append(color)
    else:
        for row in range(N):
            for col in range(N):
                color = color_first if col % 2 == 0 else color_second
                colors.append(color)

    return colors


def chose_pattern_check() -> str:
    """
    Prompts the user to select a fill pattern.

    Returns:
        str: The selected pattern ('chequered' or 'alternation colors').
    """

    patterns = [f'{lcl.CHEQUERED}', f'{lcl.ALTERNATING_COLORS}']

    print(f'{lcl.FILL_OPTIONS}')

    while True:
        pattern = input(f'{lcl.CHOOSE_FILL_OPTION}').strip().lower()
        if pattern in patterns:
            return pattern
        print(f'{lcl.INPUT_ERROR}')


def chose_type_check() -> str:
    """
    Prompts user to select the pattern direction.

    Returns:
        str: The selected type ('по строкам' or 'по столбцам').
    """

    types = [f'{lcl.ROW_BY_ROW}', f'{lcl.COLUMN_WISE}']

    print(f'{lcl.FILL_OPTIONS_COLUMNS}')  # Используем правильную константу

    while True:
        pattern_type = input(f'{lcl.CHOOSE_FILL_OPTION_COLUMNS}').strip().lower()
        if pattern_type in types:
            return pattern_type
        print(f'{lcl.INPUT_ERROR}')


def pattern_colors(N: int, color_first: str, color_second: str, pattern: str, pattern_type: str) -> list:
    """
    Determines the color pattern based on user's choice.

    Args:
        N (int): Grid size.
        color_first (str): First color option.
        color_second (str): Second color option.
        pattern (str): Selected pattern ('шахматный' or 'чередование цветов').
        pattern_type (str): Pattern orientation ('по строкам' or 'по столбцам').

    Returns:
        list: List of colors matching the pattern.
    """

    if pattern == f'{lcl.CHEQUERED}':
        return chess_pattern(N, color_first, color_second)
    elif pattern == f'{lcl.ALTERNATING_COLORS}':
        return alternation(N, pattern_type, color_first, color_second)


def animate_drawing(centers: list, colors: list, side: float, thickness_width: int,
                    border_color: str, shadow_intensity: int) -> None:
    """
    Animate drawing of hexagons with optional shadows and borders.

    Args:
        centers (list): List of (x, y) tuples for hexagon centers.
        colors (list): Corresponding fill colors for each hexagon.
        side (float): Side length of hexagons.
        thickness_width (int): Border line thickness.
        border_color (str): Border color.
        shadow_intensity (int): Shadow darkness intensity; 0 for no shadow.
    """

    turtle.tracer(0, 0)

    for i in range(len(centers)):
        x, y = centers[i]
        color = colors[i]
        if shadow_intensity > 0:
            draw_shadow(x, y, side, shadow_intensity)

        draw_hexagon(x, y, side, color)

        draw_hexagon_border(x, y, side, thickness_width, border_color)

        turtle.update()
        time.sleep(0.05)

    turtle.tracer(1, 10)


def main():
    """
    Main function orchestrating the drawing of hexagonal patterns.
    """

    turtle.setup(800, 800)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.bgcolor("white")

    N = get_num_hexagons()

    color_first, color_second = get_color_choice()
    preview_colors(color_first, color_second)

    thickness_width = border_thickness()
    border_col = border_color()
    shadow_intensity = shadow_brightness()

    size = 500

    centers, side = calculate_hexagon_centers(N, size)
    pattern = chose_pattern_check()

    if pattern == f'{lcl.ALTERNATING_COLORS}':
        pattern_type = chose_type_check()
    else:
        pattern_type = ""

    colors = pattern_colors(N, color_first, color_second, pattern, pattern_type)

    animate_drawing(centers, colors, side, thickness_width, border_col, shadow_intensity)
    turtle.done()


if __name__ == '__main__':
    main()
    
