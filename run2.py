import pygame
import sys
import random
import time

pygame.init()


# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400
CAR_WIDTH, CAR_HEIGHT = 50, 30
ALPHA = 5.0  # Deceleration rate in m/s²
TAU = 1.5  # Reaction time in seconds
RMIN = 25  # Minimum safe distance in meters

# Initialize Pygame
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Car Collision Simulation")

# Fonts
font = pygame.font.Font(None, 30)

def show_instructions():
    window.fill(BLACK)
    instructions = [
        "Press SPACE to Start the Simulation",
        "Controls:",
        "F - Move to the Next Scenario",
        "B - Move to the Previous Scenario",
        "SPACE - Pause/Resume the Simulation",
        "ESC - Quit the Simulation"
    ]

    y_position = 100
    for line in instructions:
        text = font.render(line, True, WHITE)
        window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y_position))
        y_position += 40

    pygame.display.flip()

def wait_for_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return  # Exit the loop and start the simulation

# Car class
class Car:
    def __init__(self, x, y, velocity, color):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.color = color
        self.stopped = False

    def move(self):
        if not self.stopped:
            self.x += self.velocity

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))


# Risk calculation
def calculate_risk(vF, vL, alpha, tau, Rmin):
    return 0.5 * ((vF**2 / alpha) - (vL**2 / alpha)) + (vF * tau) + Rmin


# Initialize scenario
def setup_scenario(scenario):
    if scenario == 1:  # Safe scenario
        return Car(600, 100, 0, WHITE), Car(50, 100, 5, GREEN)
    elif scenario == 2:  # Medium risk
        return Car(600, 200, 0, WHITE), Car(50, 200, 7, YELLOW)
    elif scenario == 3:  # High risk
        return Car(600, 300, 0, WHITE), Car(50, 300, 10, RED)


# Draw simulation

def draw_simulation(lead_car, follow_car, scenario, paused, elapsed_time):
    # Clear screen
    window.fill(BLACK)

    # Display scenario information
    scenario_text = font.render(f"Scenario {scenario}", True, WHITE)
    window.blit(scenario_text, (10, 10))

    # Display pause status
    if paused:
        pause_text = font.render("Paused", True, WHITE)
        window.blit(pause_text, (WINDOW_WIDTH - 100, 10))

    # Draw cars and their states
    lead_car.draw(window)
    follow_car.draw(window)

    # Calculate distance and risk distance
    distance = lead_car.x - (follow_car.x + CAR_WIDTH)
    risk_distance = calculate_risk(follow_car.velocity, lead_car.velocity, ALPHA, TAU, RMIN)

    # Initialize a default status_text
    status_text = "Simulation Running"

    # Determine behavior based on scenario
    if scenario == 1:  # Safe scenario
        stop_distance = 150  # Car stops 150m from the lead car
        if distance > stop_distance:
            follow_car.color = GREEN
            follow_car.velocity = max(0, follow_car.velocity - 0.1)  # Gradual stopping
            status_text = "Safe (No Crash)"
        else:
            follow_car.velocity = 0  # Stop the car
            status_text = "Stopped Safely (150m Away)"

    elif scenario == 2:  # Medium risk
        if distance <= risk_distance and distance > RMIN:
            follow_car.color = YELLOW
            follow_car.velocity = max(2, follow_car.velocity - 0.5)  # Reduce speed
            status_text = "Medium Risk (Slowing Down)"
        elif distance <= RMIN:
            follow_car.color = YELLOW  # Always show yellow in this scenario
            follow_car.velocity = 0
            follow_car.stopped = True
            status_text = "Minor Collision"

    elif scenario == 3:  # High risk
        if distance <= RMIN:
            follow_car.color = RED
            follow_car.velocity = 0
            follow_car.stopped = True
            status_text = "Crash! Simulation Paused"
            paused = True  # Pause simulation upon collision

    # Display parameters
    speed_text = font.render(f"Speed: {follow_car.velocity:.2f} m/s", True, WHITE)
    distance_text = font.render(f"Distance: {distance:.2f} m", True, WHITE)
    status_display = font.render(status_text, True, follow_car.color)

    window.blit(speed_text, (follow_car.x, follow_car.y - 40))
    window.blit(distance_text, (follow_car.x, follow_car.y - 20))
    window.blit(status_display, (10, follow_car.y + 50))

    pygame.display.flip()
    return paused


show_instructions()
wait_for_start()
# Main simulation loop
def main():
    current_scenario = 1
    paused = False
    lead_car, follow_car = setup_scenario(current_scenario)

    clock = pygame.time.Clock()
    running = True
    start_time = time.time()

    while running:
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:  # Pause simulation
                    paused = not paused
                elif event.key == pygame.K_f:  # Next scenario
                    if current_scenario < 3:
                        current_scenario += 1
                        lead_car, follow_car = setup_scenario(current_scenario)
                        start_time = time.time()
                        paused = False
                elif event.key == pygame.K_b:  # Previous scenario
                    if current_scenario > 1:
                        current_scenario -= 1
                        lead_car, follow_car = setup_scenario(current_scenario)
                        start_time = time.time()
                        paused = False

        # Run simulation if not paused
        if not paused:
            follow_car.move()

        # Draw current simulation
        paused = draw_simulation(lead_car, follow_car, current_scenario, paused, elapsed_time)

        clock.tick(60)


# Run the program
if __name__ == "__main__":
    main()
