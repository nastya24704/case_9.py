import turtle
import math

def draw_hexagon(x, y, side_length): #код маши без заливки
    turtle.right(30)

    turtle.up()
    turtle.goto(x, y)
    turtle.down()

    for _ in range(6):
        turtle.forward(side_length)
        turtle.right(60)
    turtle.left(30)

def get_num_hexagons():
    while True:
        input_str = input("Введите количество шестиугольников, располагаемых в ряд: ").strip()
        if input_str.isdigit():
            num = int(input_str)
            if 4 <= num <= 20:
                return num

def main():
    turtle.speed(0)
    turtle.hideturtle()

    N = get_num_hexagons() #ввод количества шестиугольников в строке

    size = 500
    side_length = size / N #длина стороны зависит от количества
    height = math.sqrt(3) * side_length

    start_x_0 = -size + height #начальное положение
    start_y_0 = size - side_length

    for row in range(N): #смещение по координате y
        y_offset = start_y_0 - row * side_length* 1.5
        if row % 2 == 0: #проверяет четная ли строка по счету
            x_offset = start_x_0 #если да, то она принимает начальное положение
        else:
            x_offset = start_x_0 + (side_length * math.sqrt(3)) / 2 # иначе сдвигается вниз

        for col in range(N):
            x = x_offset + col * side_length * math.sqrt(3)
            y = y_offset
            draw_hexagon(x, y, side_length)

    turtle.done()

if __name__ == "__main__":
    main()
