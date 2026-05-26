from PIL import Image, ImageDraw, ImageFont
import calendar

COLORS = {
    "dark_green": (0, 120, 0),
    "light_green": (160, 235, 160),
    "gray": (230, 230, 230),
    "orange": (255, 185, 90),
    "red": (255, 110, 110)
}


WIDTH = CELL_SIZE * 7 + PADDING * 8
HEIGHT = CELL_SIZE * 6 + 160


def draw_rounded_rect(draw, xy, radius, fill):
    draw.rounded_rectangle(xy, radius=radius, fill=fill)


def draw_shadow(draw, xy):
    x1, y1, x2, y2 = xy
    offset = 4

    draw.rounded_rectangle(
        (x1 + offset, y1 + offset, x2 + offset, y2 + offset),
        radius=12,
        fill=(200, 200, 200)
    )


# ✅ Русские названия месяцев
RU_MONTHS = [
    "",  # заглушка (индексация с 1)
    "ЯНВАРЬ", "ФЕВРАЛЬ", "МАРТ", "АПРЕЛЬ",
    "МАЙ", "ИЮНЬ", "ИЮЛЬ", "АВГУСТ",
    "СЕНТЯБРЬ", "ОКТЯБРЬ", "НОЯБРЬ", "ДЕКАБРЬ"
]


def create_calendar_png(calendar_data, year: int, month: int, output_path="calendar.png"):

    img = Image.new("RGB", (WIDTH, HEIGHT), "white")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 30)
        font_day = ImageFont.truetype("arial.ttf", 20)
        font_week = ImageFont.truetype("arial.ttf", 16)
    except:
        font_title = None
        font_day = None
        font_week = None

    # ✅ Заголовок (русский)
    title = f"{RU_MONTHS[month]} {year}"
    draw.text((PADDING, 20), title, fill="black", font=font_title)

    # ✅ Дни недели (русские)
    week_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]

    y_week = 70

    for i, wd in enumerate(week_days):
        x = PADDING + i * (CELL_SIZE + PADDING)

        bbox = draw.textbbox((0, 0), wd, font=font_week)
        w = bbox[2] - bbox[0]

        draw.text(
            (x + (CELL_SIZE - w) / 2, y_week),
            wd,
            fill=(120, 120, 120),
            font=font_week
        )

    # ✅ карта дней
    day_map = {d["day"]: d["color"] for d in calendar_data}

    first_weekday, days_in_month = calendar.monthrange(year, month)

    y_offset = 110
    day = 1

    for row in range(6):
        for col in range(7):

            if row == 0 and col < first_weekday:
                continue

            if day > days_in_month:
                continue

            x = PADDING + col * (CELL_SIZE + PADDING)
            y = y_offset + row * (CELL_SIZE + PADDING)

            color_key = day_map.get(day, "gray")
            color = COLORS.get(color_key, COLORS["gray"])

            # ✅ тень
            draw_shadow(draw, (x, y, x + CELL_SIZE, y + CELL_SIZE))

            # ✅ карточка
            draw_rounded_rect(
                draw,
                (x, y, x + CELL_SIZE, y + CELL_SIZE),
                radius=12,
                fill=color
            )

            # ✅ номер дня
            text = str(day)
            bbox = draw.textbbox((0, 0), text, font=font_day)

            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            draw.text(
                (x + (CELL_SIZE - text_w) / 2,
                 y + (CELL_SIZE - text_h) / 2),
                text,
                fill="black",
                font=font_day
            )

            day += 1

    img.save(output_path)

    return output_path

import calendar


COLORS = {
    "dark_green": (0, 120, 0),
	}