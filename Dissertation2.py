
# -*- coding: utf-8 -*-
import pygame
import csv
import os
import time
import random
import heapq
import pandas as pd  # needed to load merged_log.csv



# Generate consistent piece IDs
PIECE_IDS = [f"P{str(i+1).zfill(4)}" for i in range(100)]

# Screen settings
WIDTH, HEIGHT = 1750, 1000
TARGETS = []
ROBOTS = [[40, HEIGHT - 60], [80, HEIGHT - 60], [120, HEIGHT - 60]]
SPEED = 10
GRID_SPACING = 10
OBSTACLES = []
OBSTACLE_SIZE = 25
ROBOT_SIZE = 20
SAFETY_MARGIN = 5  # Safety buffer around obstacles

DROP_ZONE_WIDTH = 150
DROP_ZONE_HEIGHT = 150
DROP_ZONE_Y = HEIGHT - DROP_ZONE_HEIGHT - 50  # 50px padding from bottom
DROP_ZONE_X_START = WIDTH - DROP_ZONE_WIDTH - 30  # total padding from right

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_img = pygame.image.load("C:\\Users\\Study\\Desktop\\Dissertation2\\bakground.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

pygame.display.set_caption("Three Robots Moving to Targets with Collision Avoidance")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

log_dir = "C:\\Users\\Study\\Desktop\\Dissertation2\\Logs"
for file in os.listdir(log_dir):
    if file.startswith("robot_") and file.endswith("_log.csv"):
        os.remove(os.path.join(log_dir, file))


goal_images = [
    pygame.image.load("C:\\Users\\Study\\Desktop\\Dissertation2\\goal1.png"),
    pygame.image.load("C:\\Users\\Study\\Desktop\\Dissertation2\\goal2.png"),
    pygame.image.load("C:\\Users\\Study\\Desktop\\Dissertation2\\goal3.png")
]

goal_images = [pygame.transform.scale(img, (100, 100)) for img in goal_images]

robot_img = pygame.image.load("C:\\Users\\Study\\Desktop\\Dissertation2\\robot model.png").convert_alpha()
robot_img = pygame.transform.scale(robot_img, (30, 30))  # Resize to fit ROBOT_SIZE


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (200, 200, 200)

def create_log(robot_id, target_pos):
    log_path = f"C:\\Users\\Study\\Desktop\\Dissertation2\\Logs\\robot_{robot_id}_log.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if robot_id == 1:
        # Cutting Station: Length, Width, Thickness, Edge Precision
        log_data = [["Piece ID", "Timestamp", "Length", "Width", "Thickness", "Edge Precision"]]
        for i in range(100):
            piece_id = PIECE_IDS[i]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            length = round(random.uniform(35, 37), 2)
            width = round(random.uniform(25, 27), 2)
            thickness = round(random.uniform(8.0, 9.0), 2)
            edge_precision = round(random.uniform(0.85, 0.90), 2)
            log_data.append([piece_id, timestamp, length, width, thickness, edge_precision])

    elif robot_id == 2:
        # Finishing Station: Surface Smoothness, Surface Flatness, Burr Presence, Coating Thickness
        log_data = [["Piece ID", "Timestamp", "Surface Smoothness", "Surface Flatness", "Burr Presence", "Coating Thickness"]]
        for i in range(100):
            piece_id = PIECE_IDS[i]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            smoothness = round(random.uniform(0.88, 1.1), 2)
            flatness = round(random.uniform(0.85, 1.2), 2)
            burr = random.choice([0, 1])
            coating_thickness = round(random.uniform(0.02, 0.03), 3)
            log_data.append([piece_id, timestamp, smoothness, flatness, burr, coating_thickness])

    elif robot_id == 3:
        # Mechanical Properties: Hardness, Weight, Density, Tensile Strength
        log_data = [["Piece ID", "Timestamp", "Hardness", "Weight", "Density", "Tensile Strength"]]
        for i in range(100):
            piece_id = PIECE_IDS[i]
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            hardness = round(random.uniform(59, 64), 1)  # Rockwell scale
            weight = round(random.uniform(299, 325), 2)  # grams
            density = round(random.uniform(7.9, 8.1), 2)  # g/cm³
            tensile_strength = round(random.uniform(360, 495), 1)  # MPa
            log_data.append([piece_id, timestamp, hardness, weight, density, tensile_strength])

    else:
        print(f"Unknown robot ID: {robot_id}")
        return

    with open(log_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(log_data)
    print(f"Log file created at: {log_path}")

def is_collision(position, ignore_robot=None):
    for obstacle in OBSTACLES:
        if abs(position[0] - obstacle[0]) < OBSTACLE_SIZE + SAFETY_MARGIN and \
           abs(position[1] - obstacle[1]) < OBSTACLE_SIZE + SAFETY_MARGIN:
            return True
    for i, robot in enumerate(ROBOTS):
        if ignore_robot is not None and i == ignore_robot:
            continue
        if abs(position[0] - robot[0]) < ROBOT_SIZE + SAFETY_MARGIN and \
           abs(position[1] - robot[1]) < ROBOT_SIZE + SAFETY_MARGIN:
            return True
    return False

def a_star(start, goal, robot_index):
    neighbors = [(0, SPEED), (0, -SPEED), (SPEED, 0), (-SPEED, 0)]
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if abs(current[0] - goal[0]) < SPEED and abs(current[1] - goal[1]) < SPEED:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        for dx, dy in neighbors:
            next_pos = (current[0] + dx, current[1] + dy)
            if 0 <= next_pos[0] < WIDTH and 0 <= next_pos[1] < HEIGHT and not is_collision(next_pos, ignore_robot=robot_index):
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(next_pos[0] - goal[0]) + abs(next_pos[1] - goal[1])
                    heapq.heappush(open_set, (priority, next_pos))
                    came_from[next_pos] = current
    return []

def snap_to_grid(pos):
    return (pos[0] - pos[0] % SPEED, pos[1] - pos[1] % SPEED)

robot_paths = [[], [], []]
started = False
goal_click_index = 0
reached = [False, False, False]


# NEW: State for delivery system
robot_carrying = [None, None, None]
robot_task_index = [0, 0, 0]
piece_deliveries = []
delivery_paths = [[], [], []]


running = True
robot_tasks = [[], [], []]
grading_triggered = False

while running:
    screen.blit(background_img, (0, 0))


    # Draw start button
    start_button = pygame.Rect(10, 10, 120, 40)
    pygame.draw.rect(screen, GREEN, start_button)
    text = font.render("Start", True, WHITE)
    screen.blit(text, (30, 15))

    grade_button = pygame.Rect(150, 10, 180, 40)
    pygame.draw.rect(screen, (0, 180, 0), grade_button)
    text = font.render("Grade Pieces", True, WHITE)
    screen.blit(text, (160, 15))

    #Grid
    for x in range(0, WIDTH, GRID_SPACING):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SPACING):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            snapped = snap_to_grid((mx, my))
            if event.button == 1 and grade_button.collidepoint(mx, my):
                grading_triggered = True
            if event.button == 1 and start_button.collidepoint(mx, my):
                if len(TARGETS) == 3:
                    started = True
                    reached = [False, False, False]
                    robot_paths = [a_star(tuple(ROBOTS[i]), TARGETS[i], i) for i in range(3)]
            elif event.button == 2 and not started:
                if not is_collision(snapped):
                    OBSTACLES.append(snapped)
            elif event.button == 3 and not started:
                if len(TARGETS) < 3:
                    TARGETS.append(snapped)
                else:
                    TARGETS[goal_click_index] = snapped
                    goal_click_index = (goal_click_index + 1) % 3

    for obstacle in OBSTACLES:
        pygame.draw.rect(screen, GRAY,
                         (obstacle[0] - SAFETY_MARGIN, obstacle[1] - SAFETY_MARGIN,
                          OBSTACLE_SIZE + SAFETY_MARGIN * 2, OBSTACLE_SIZE + SAFETY_MARGIN * 2), 1)
        pygame.draw.rect(screen, BLACK, (obstacle[0], obstacle[1], OBSTACLE_SIZE, OBSTACLE_SIZE))

    for i, target in enumerate(TARGETS):
        if target:
            screen.blit(goal_images[i], (target[0] - 20, target[1] - 20))

    for robot in ROBOTS:
        screen.blit(robot_img, (robot[0] - 15, robot[1] - 15))  # Center the image

    if started:
        for i in range(3):
            if not reached[i] and i < len(TARGETS):
                if robot_paths[i]:
                    next_step = robot_paths[i].pop(0)
                    if not is_collision(next_step, ignore_robot=i):
                        ROBOTS[i][0], ROBOTS[i][1] = next_step
                    else:
                        robot_paths[i] = a_star(tuple(ROBOTS[i]), TARGETS[i], i)
                if abs(ROBOTS[i][0] - TARGETS[i][0]) < SPEED and abs(ROBOTS[i][1] - TARGETS[i][1]) < SPEED:
                    create_log(i + 1, TARGETS[i])
                    reached[i] = True

        if all(reached):
            started = False
            try:
                print(">>> Calling run_log_analysis()")
                from log_classifier import run_log_analysis
                run_log_analysis()
            except Exception as e:
                print(f"Error running log analysis: {e}")


            from log_classifier import run_log_analysis
            run_log_analysis()
            
            # Load merged log and prepare piece visuals
            merged_df = pd.read_csv("C:\\Users\\Study\\Desktop\\Dissertation2\\Logs\\merged_log.csv")
            piece_visuals = []
            cols = 5  # 5 columns
            rows = 2  # 2 rows
            zone_width = 120
            zone_height = 80
            spacing_x = 20
            spacing_y = 20
            start_x = 600
            start_y = 50
            for i, row in merged_df.iterrows():
                zone_idx = i // 10
                slot_idx = i % 10
                zone_col = zone_idx % cols
                zone_row = (rows - 1) - (zone_idx // cols)
                x_base = start_x + zone_col * zone_width
                y_base = start_y + zone_row * zone_height
                dot_x = x_base + (slot_idx % 5) * spacing_x
                dot_y = y_base + ((1 - (slot_idx // 5)) * spacing_y)

                
                status = row["Final Status"]
                if status == "Qualified":
                    color = (0, 200, 0)  # green
                elif status == "Rework":
                    color = (255, 165, 0)  # orange
                else:
                    color = (255, 0, 0)  # red
                piece_visuals.append((dot_x, dot_y, row["Piece ID"], color))
                
                # NEW: Assign piece to robot in round-robin
                if "robot_tasks" not in locals():
                   robot_tasks = [[], [], []]  # 3 robots
                robot_index = i % 3
                robot_tasks[robot_index].append({
                    "piece_id": row["Piece ID"],
                    "status": status,
                    "start_pos": (dot_x, dot_y)
                })
            

    # NEW: Robot delivery behavior
    if grading_triggered and any(len(tasks) > 0 for tasks in robot_tasks):
        for i in range(3):
            if robot_task_index[i] < len(robot_tasks[i]):
                task = robot_tasks[i][robot_task_index[i]]
                current_pos = tuple(ROBOTS[i])

                # CASE 1: Go to piece if not carrying
                if robot_carrying[i] is None:
                    target = task["start_pos"]

                    if abs(current_pos[0] - target[0]) < SPEED and abs(current_pos[1] - target[1]) < SPEED:
                        robot_carrying[i] = task
                        delivery_paths[i] = []  #  clear path to recalculate next leg
                    else:
                        if not delivery_paths[i]:
                            delivery_paths[i] = a_star(current_pos, target, i)
                        if delivery_paths[i]:
                            ROBOTS[i][0], ROBOTS[i][1] = delivery_paths[i].pop(0)

                # CASE 2: Go to drop zone if carrying
                else:
                    dx = DROP_ZONE_X_START
                    
                    if task["status"] == "Scrap":
                        dy = DROP_ZONE_Y
                    elif task["status"] == "Rework":
                        dy = DROP_ZONE_Y - (DROP_ZONE_HEIGHT + 20)
                    else:  # Qualified
                        dy = DROP_ZONE_Y - 2 * (DROP_ZONE_HEIGHT + 20)
                    dy += 60 
                    target = (dx, dy)

                    if abs(current_pos[0] - dx) < SPEED and abs(current_pos[1] - dy) < SPEED:
                        piece_deliveries.append((dx, dy, task["status"], task["piece_id"]))
                        robot_carrying[i] = None
                        robot_task_index[i] += 1
                        delivery_paths[i] = []  # clear path to start next task
                    else:
                        if not delivery_paths[i]:
                            delivery_paths[i] = a_star(current_pos, target, i)
                        if delivery_paths[i]:
                            ROBOTS[i][0], ROBOTS[i][1] = delivery_paths[i].pop(0)
                        
    if all(reached) and "piece_visuals" in locals():
        for (x, y, piece_id, color) in piece_visuals:
            in_progress = any(task and task["piece_id"] == piece_id for task in robot_carrying)
            delivered = any(pid == piece_id for (dx, dy, status, pid) in piece_deliveries)
            if in_progress or delivered:
                continue
            
            draw_color = color if grading_triggered else BLACK
            pygame.draw.circle(screen, draw_color, (x, y), 6)
            
    
    drop_zone_labels = ["Qualified", "Rework", "Scrap"]
    for i, label_text in enumerate(reversed(drop_zone_labels)):  # Scrap at bottom
        zone_y = DROP_ZONE_Y - i * (DROP_ZONE_HEIGHT + 20)
        pygame.draw.rect(screen, (200, 200, 200), (DROP_ZONE_X_START, zone_y, DROP_ZONE_WIDTH, DROP_ZONE_HEIGHT))
        label = font.render(label_text, True, BLACK)
        screen.blit(label, (DROP_ZONE_X_START + 10, zone_y + 10))
        
    # NEW: Draw delivered pieces
    # Count delivered pieces per category
    zone_counts = {"Qualified": 0, "Rework": 0, "Scrap": 0}
    for (_, _, status, _) in piece_deliveries:
        zone_counts[status] += 1

    # Show a single dot and count per zone
    for i, status in enumerate(reversed(["Qualified", "Rework", "Scrap"])):
        if status == "Qualified":
            color = (0, 200, 0)       # Green
        elif status == "Rework":
            color = (255, 165, 0)     # Orange
        else:
            color = (255, 0, 0)       # Red

        x = DROP_ZONE_X_START +20
        zone_y = DROP_ZONE_Y - i * (DROP_ZONE_HEIGHT + 20)
        y = min(HEIGHT - 30, zone_y + DROP_ZONE_HEIGHT // 2 + 5)  # ensure visible

        pygame.draw.circle(screen, color, (x, y), 10)
        count = zone_counts[status]
        count_surface = font.render(f"x{count}", True, BLACK)
        screen.blit(count_surface, (x + 20, y - count_surface.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

# Run the classifier (can leave this for later)


