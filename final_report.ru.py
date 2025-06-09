import pandas as pd
import os
from collections import Counter
from datetime import datetime
from io import StringIO

def analyze_robot_logs():
    log_dir = "C:\\Users\\Study\\Desktop\\Dissertation2\\Logs"
    output_dir = os.path.join(log_dir, "Reports")
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    report_path = os.path.join(output_dir, f"Финальный отчёт ({timestamp}).txt")
    buffer = StringIO()

    def log_print(message=""):
        print(message)
        buffer.write(message + "\n")

    suggestions = {
        "Длина слишком короткая": "Проверьте выход инструмента; калибруйте позицию начала ножа.",
        "Длина слишком длинная": "Проверьте точку остановки; отрегулируйте параметры движения серво.",
        "Ширина слишком узкая": "Выравняйте направляющие рейки и проверьте проскальзывание материала.",
        "Ширина слишком широкая": "Проверьте растяжение материала или недостаточное зажимание.",
        "Толщина слишком тонкая": "Убедитесь в равной толщине сырья и отрегулируйте глубину реза.",
        "Толщина слишком толстая": "Проверьте наложение; заточите или почистите нож.",
        "Точность кромки слишком низкая (Брак)": "Замените или заточите нож; уменьшите скорость подачи.",
        "Точность кромки слишком низкая (Переделка)": "Калибруйте датчики края и точно настройте скорость резки.",
        "Гладкость поверхности слишком низкая": "Замените или почистите валики; отрегулируйте размер зерна абразива.",
        "Плоскостность поверхности слишком низкая": "Проверьте распределение давления и сбалансируйте платформу отделки.",
        "Толщина покрытия вне допустимого диапазона": "Калибруйте дюзы покрытия; настройте давление и поток.",
        "Наличие заусенцев": "Настройте щётки или добавьте виброобработку после отделки.",
        "Твёрдость слишком низкая": "Проверьте цикл термообработки и сплав материала.",
        "Твёрдость слишком высокая": "Уменьшите время закалки или отпуска.",
        "Масса слишком мала": "Проверьте точность резки и содержание сырья.",
        "Масса слишком велика": "Удалите лишний материал при резке.",
        "Плотность вне допустимого диапазона": "Проверьте на пористость и источник сырья.",
        "Предел прочности на разрыв вне допустимого диапазона": "Калибруйте термообработку и проверьте на конструктивные дефекты."
    }


    for robot_id in [1, 2, 3]:
        file_path = os.path.join(log_dir, f"robot_{robot_id}_log.csv")
        if not os.path.exists(file_path):
            log_print(f"\n[!] Log file for Robot {robot_id} not found: {file_path}")
            continue

        df = pd.read_csv(file_path)
        status_counts = Counter(df["Final Status"])
        total = len(df)

        summary = {
            "Total Pieces": total,
            "Qualified": status_counts["Qualified"],
            "Rework": status_counts["Rework"],
            "Scrap": status_counts["Scrap"],
            "Qualified %": round(status_counts["Qualified"] / total * 100, 2),
            "Rework %": round(status_counts["Rework"] / total * 100, 2),
            "Scrap %": round(status_counts["Scrap"] / total * 100, 2)
        }

        rework_causes = Counter()
        scrap_causes = Counter()
        rework_ids = {}
        scrap_ids = {}

        for _, row in df.iterrows():
            result = row["Final Status"]
            if result not in ("Rework", "Scrap"):
                continue

            if robot_id == 1:
                length = row["Length"]
                width = row["Width"]
                thickness = row["Thickness"]
                edge = row["Edge Precision"]

                if length < 35:
                    cause = "Length too short"
                elif length > 37:
                    cause = "Length too long"
                elif width < 25:
                    cause = "Width too narrow"
                elif width > 27:
                    cause = "Width too wide"
                elif thickness < 8:
                    cause = "Thickness too thin"
                elif thickness > 9:
                    cause = "Thickness too thick"
                elif edge < 0.85:
                    cause = "Edge precision too low (Scrap)" if result == "Scrap" else "Edge precision too low (Rework)"
                else:
                    cause = "Unknown"

            elif robot_id == 2:
                smooth = row["Surface Smoothness"]
                flat = row["Surface Flatness"]
                burr = row["Burr Presence"]
                coat = row["Coating Thickness"]

                if smooth < 0.88:
                    cause = "Surface smoothness too low"
                elif flat < 0.90:
                    cause = "Surface flatness too low"
                elif not (0.015 <= coat <= 0.035):
                    cause = "Coating thickness out of range"
                elif burr != 0:
                    cause = "Burr present"
                else:
                    cause = "Unknown"

            elif robot_id == 3:
                hardness = row["Hardness"]
                weight = row["Weight"]
                density = row["Density"]
                tensile = row["Tensile Strength"]

                if hardness < 59:
                    cause = "Hardness too low"
                elif hardness > 64:
                    cause = "Hardness too high"
                elif weight < 300:
                    cause = "Weight too low"
                elif weight > 325:
                    cause = "Weight too high"
                elif not (7.9 <= density <= 8.1):
                    cause = "Density out of range"
                elif not (360 <= tensile <= 495):
                    cause = "Tensile strength out of range"
                else:
                    cause = "Unknown"
            else:
                cause = "Invalid robot ID"

            piece_id = row["Piece ID"]
            if result == "Rework":
                rework_causes[cause] += 1
                rework_ids.setdefault(cause, []).append(piece_id)
            elif result == "Scrap":
                scrap_causes[cause] += 1
                scrap_ids.setdefault(cause, []).append(piece_id)

        log_print(f"\n============================")
        log_print(f"\U0001F4CA Robot {robot_id} Performance Summary")
        log_print("============================")
        for k, v in summary.items():
            log_print(f"{k}: {v}")

        log_print("\n\U0001F6A7 Rework Causes and Suggestions:")
        for cause, count in rework_causes.items():
            log_print(f"  - {cause}: {count}")
            log_print(f"    \U0001F527 Suggestion: {suggestions.get(cause, 'No suggestion available.')}")
            log_print(f"    \U0001F9FE Pieces: {', '.join(str(x) for x in rework_ids.get(cause, []) if pd.notna(x))}")

        log_print("\n\U0001F6D1 Scrap Causes and Suggestions:")
        for cause, count in scrap_causes.items():
            log_print(f"  - {cause}: {count}")
            log_print(f"    \U0001F527 Suggestion: {suggestions.get(cause, 'No suggestion available.')}")
            log_print(f"    \U0001F9FE Pieces: {', '.join(str(x) for x in scrap_ids.get(cause, []) if pd.notna(x))}")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(buffer.getvalue())
    log_print(f"\n Report saved to: {report_path}")
