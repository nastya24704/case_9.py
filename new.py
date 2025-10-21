import turtle
import math

def calculate_side_length(number, size):
    """Вычисление длины стороны шестиугольника для равномерного заполнения."""
    # Расчет с учетом ширины между центрами
    side = size / (number + 0.5)
    return side

def calculate_hexagon_centers(number, size):
    """Рассчет координат центров шестиугольников для центрирования и заполнения."""
    side = calculate_side_length(number, size)
    width_hexagon = math.sqrt(3) * side  # ширина по горизонтали
    # Расчеты позволяют центрировать сетку на холсте
    total_width = width_hexagon * number
    total_height = side * 1.5 * number  # приблизительная высота сетки

    # Начальная позиция (центральная точка экрана)
    start_x = - total_width/2 + width_hexagon/2
    start_y = total_height/2 - side/2

    centers = []

    for row in range(number):
        y = start_y - row * side * 1.5
        for col in range(number):
            x = start_x + col * width_hexagon
            if row % 2 == 1:
                x += width_hexagon / 2  # смещение для нечетных строк
            centers.append((x, y))
    return centers

def draw_hexagon(x, y, side_length):
    """Рисование шестиугольника с центром в (x, y)."""
    turtle.right(30)

    turtle.up()
    turtle.goto(x, y)
    turtle.down()

    for index in range(6):
        turtle.forward(side_length)
        turtle.right(60)
    turtle.left(30)

def main():
    turtle.speed(0)
    turtle.hideturtle()

    user_number = int(input("Введите количество шестиугольников в ряд: "))
    size = 500  # размер области

    centers = calculate_hexagon_centers(user_number, size)# Расчет координат центров шестиугольников
    side = calculate_side_length(user_number, size) # Длина стороны шестиугольника


    for (x, y) in centers: # Рисуем каждый шестиугольник на своей позиции
        draw_hexagon(x, y, side)

    turtle.done()

if __name__ == "__main__":
    main()
