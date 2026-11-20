SIGNIFICANT_COLORS = {
    "黑": 0,
    "棕": 1,
    "紅": 2,
    "橙": 3,
    "黃": 4,
    "綠": 5,
    "藍": 6,
    "紫": 7,
    "灰": 8,
    "白": 9,
}

MULTIPLIER_COLORS = {
    "黑": 1,
    "棕": 10,
    "紅": 100,
    "橙": 1_000,
    "黃": 10_000,
    "綠": 100_000,
    "藍": 1_000_000,
    "紫": 10_000_000,
    "灰": 100_000_000,
    "白": 1_000_000_000,
    "金": 0.1,
    "銀": 0.01,
}

TOLERANCE_COLORS = {
    "棕": "±1%",
    "紅": "±2%",
    "綠": "±0.5%",
    "藍": "±0.25%",
    "紫": "±0.1%",
    "灰": "±0.05%",
    "金": "±5%",
    "銀": "±10%",
    "無": "±20%",
}

TEMPERATURE_COLORS = {
    "黑": 250,
    "棕": 100,
    "紅": 50,
    "橙": 15,
    "黃": 25,
    "藍": 10,
    "紫": 5,
}

COLOR_CODES = {
    "0": "黑",
    "1": "棕",
    "2": "紅",
    "3": "橙",
    "4": "黃",
    "5": "綠",
    "6": "藍",
    "7": "紫",
    "8": "灰",
    "9": "白",
    "10": "金",
    "11": "銀",
    "12": "無",
}


def format_resistance(value: float) -> str:
    units = (
        (1_000_000_000, "GΩ"),
        (1_000_000, "MΩ"),
        (1_000, "kΩ"),
        (1, "Ω"),
        (0.001, "mΩ"),
    )
    for divisor, suffix in units:
        if value >= divisor:
            number = value / divisor
            if number.is_integer():
                return f"{int(number)} {suffix}"
            return f"{number:.10g} {suffix}"
    return f"{value:.10g} Ω"


def calculate_resistance(colors: list[str]) -> tuple[float, str, int | None]:
    band_count = len(colors)
    if band_count not in (4, 5, 6):
        raise ValueError("電阻色碼必須是 4、5 或 6 色環")

    if band_count == 4:
        significant = colors[:2]
        multiplier = colors[2]
        tolerance = colors[3]
        if any(color not in SIGNIFICANT_COLORS for color in significant):
            raise ValueError("四色環的前兩個色環必須是有效數字色")
    else:
        significant = colors[:3]
        multiplier = colors[3]
        tolerance = colors[4]
        if any(color not in SIGNIFICANT_COLORS for color in significant):
            raise ValueError("五/六色環的有效數字色環無效")

    if multiplier not in MULTIPLIER_COLORS:
        raise ValueError("倍率色環無效")
    if tolerance not in TOLERANCE_COLORS:
        raise ValueError("誤差色環無效")

    digits = "".join(str(SIGNIFICANT_COLORS[color]) for color in significant)
    resistance = int(digits) * MULTIPLIER_COLORS[multiplier]

    temperature = None
    if band_count == 6:
        temperature_color = colors[5]
        if temperature_color not in TEMPERATURE_COLORS:
            raise ValueError("溫度係數色環無效")
        temperature = TEMPERATURE_COLORS[temperature_color]

    return resistance, TOLERANCE_COLORS[tolerance], temperature


def read_color(prompt: str) -> str:
    while True:
        code = input(prompt).strip()
        if code in COLOR_CODES:
            return COLOR_CODES[code]
        print("請輸入有效色碼數字（0 至 12）。")


def main() -> None:
    print("色碼電阻計算程式")
    print("色碼：0 黑、1 棕、2 紅、3 橙、4 黃、5 綠、6 藍、7 紫、8 灰、9 白")
    print("特殊色碼：10 金、11 銀、12 無")

    while True:
        choice = input("選擇色環數量（4、5、6；輸入 q 結束）：").strip().lower()
        if choice in ("q", "quit", "exit"):
            break

        if choice not in ("4", "5", "6"):
            print("請輸入 4、5 或 6。\n")
            continue

        band_count = int(choice)
        colors = [
            read_color(f"第 {index} 色環：")
            for index in range(1, band_count + 1)
        ]

        try:
            resistance, tolerance, temperature = calculate_resistance(colors)
        except ValueError as error:
            print(f"輸入錯誤：{error}\n")
            continue

        result = f"電阻值：{format_resistance(resistance)}（{resistance:g} Ω）"
        result += f"，誤差：{tolerance}"
        if temperature is not None:
            result += f"，溫度係數：{temperature} ppm/°C"
        print(result + "\n")


if __name__ == "__main__":
    main()