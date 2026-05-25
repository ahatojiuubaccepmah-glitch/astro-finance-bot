from PIL import Image, ImageDraw, ImageFont
import calendar


# ✅ Цвета по ТЗ
COLORS = {
    "dark_green": (0, 100, 0),
    "light_green": (144, 238, 144),
    "gray": (200, 200, 200),
    "orange": (255, 165, 0),
    "red": (255, 0, 0)
}


# ✅ размеры
CELL_SIZE = 100
WIDTH = CELL_SIZE * 7
HEIGHT = CELL_SIZE * 6 + 50  # + заголовок


def create_calendar_png(calendar_data, year: int, month: int, output_path="calendar.png"):
    """
    вход:
    - календарь (из calendar_builder)
    - год
    - месяц

    выход:
    - PNG файл
    """

    # создаём изображение
    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    # ✅ заголовок
    title = f"{calendar.month_name[month]} {year}"
    draw.text((10, 10), title, fill="black")

    # ✅ карта дней → цвет
    day_map = {d["day"]: d["color"] for d in calendar_data}

    # ✅ первый день месяца
    first_weekday, days_in_month = calendar.monthrange(year, month)

    x_offset = 0
    y_offset = 50

    day = 1

    # ✅ сетка 6x7
    for row in range(6):
        for col in range(7):

            if row == 0 and col < first_weekday:
                continue

            if day > days_in_month:
                continue

            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE + y_offset
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            color_key = day_map.get(day, "gray")
            color = COLORS.get(color_key, (200, 200, 200))

            # ✅ заливка
            draw.rectangle([x1, y1, x2, y2], fill=color, outline="black")

            # ✅ номер дня (разрешено ТЗ)
            draw.text((x1 + 5, y1 + 5), str(day), fill="black")

            day += 1

    img.save(output_path)

    return output_path
