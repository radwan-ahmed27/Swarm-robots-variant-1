
# robot_classifiers.py

def classify_robot_1(row):
    result = "Qualified"
    cause = ""

    length = row["Length"]
    width = row["Width"]
    thickness = row["Thickness"]
    edge = row["Edge Precision"]

    if length < 35:
        result = "Scrap"
        cause = "Length too short"
    elif length > 37:
        result = "Rework"
        cause = "Length too long"

    if result != "Scrap":
        if width < 25:
            result = "Scrap"
            cause = "Width too narrow"
        elif width > 27:
            result = "Rework"
            cause = "Width too wide"

    if result != "Scrap":
        if thickness < 8:
            result = "Scrap"
            cause = "Thickness too thin"
        elif thickness > 9:
            result = "Rework"
            cause = "Thickness too thick"

    if result != "Scrap":
        if edge < 0.85:
            result = "Scrap"
            cause = "Edge precision too low"

    return result, cause or "None"

def classify_robot_2(row):
    result = "Qualified"
    cause = ""

    smooth = row["Surface Smoothness"]
    flat = row["Surface Flatness"]
    burr = row["Burr Presence"]
    coat = row["Coating Thickness"]

    if smooth < 0.88:
        result = "Rework"
        cause = "Surface smoothness too low"

    if flat < 0.90 and result != "Scrap":
        result = "Rework"
        cause = "Surface flatness too low"

    if not (0.015 <= coat <= 0.035) and result != "Scrap":
        result = "Rework"
        cause = "Coating thickness out of range"

    if burr != 0:
        result = "Rework"
        cause = "Burr present"

    return result, cause or "None"

def classify_robot_3(row):
    result = "Qualified"
    cause = ""

    hardness = row["Hardness"]
    weight = row["Weight"]
    density = row["Density"]
    tensile = row["Tensile Strength"]

    if hardness < 59:
        result = "Scrap"
        cause = "Hardness too low"
    elif hardness > 64:
        result = "Rework"
        cause = "Hardness too high"

    if result != "Scrap":
        if weight < 300:
            result = "Scrap"
            cause = "Weight too low"
        elif weight > 325:
            result = "Rework"
            cause = "Weight too high"

    if result != "Scrap":
        if not (7.9 <= density <= 8.1):
            result = "Scrap"
            cause = "Density out of range"

    if result != "Scrap":
        if not (360 <= tensile <= 495):
            result = "Scrap"
            cause = "Tensile strength out of range"

    return result, cause or "None"
