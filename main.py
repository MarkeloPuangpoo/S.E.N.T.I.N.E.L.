import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import random

# --- ANSI Color Codes for Interface ---
class term:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    AMBER = '\033[93m' # Changed from WARNING to AMBER
    RED = '\033[91m'    # Changed from FAIL to RED
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# --- Interface Helper Functions ---
def print_fast(text, color=term.GREEN):
    """ Prints text rapidly, no delay """
    sys.stdout.write(color + text + term.ENDC)
    sys.stdout.flush()

def print_typed(text, color=term.GREEN, delay=0.005):
    """ Simulates a high-speed data stream """
    for char in text:
        sys.stdout.write(color + char + term.ENDC)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_glitch(text, color=term.RED):
    """ Simulates a screen glitch effect """
    print_fast(f"\r{color}{text}{term.ENDC}", color)
    time.sleep(0.05)
    print_fast(f"\r{' ' * len(text)}\r", term.ENDC)
    time.sleep(0.05)
    print_fast(f"{color}{text}{term.ENDC}\n", color)

def print_status(message, status, color=term.CYAN):
    """ Prints a system status message """
    print(f"{color}[ {status.ljust(10)} ] {term.ENDC}{message}")

def print_progress_bar(iteration, total, prefix='[CALCULATING...]', suffix='STREAM...]', length=50):
    """ Renders a real-time progress bar """
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    
    # Use different characters for a more 'tech' look
    bar_fill = '█' * (filled_length - 1) + '>' if filled_length > 0 else ''
    bar_empty = '.' * (length - filled_length)
    
    bar = bar_fill + bar_empty
    sys.stdout.write(f'\r{term.AMBER}{prefix} |{bar}| {percent}% {suffix}{term.ENDC}')
    sys.stdout.flush()
    if iteration == total:
        print()

# --- Physical Constants ---
G = 6.67430e-11      # Gravitational Constant (m^3 kg^-1 s^-2)
MASS_SUN = 1.989e30  # Sol Mass (kg)
AU = 1.496e11        # 1 Astronomical Unit (m)
KMS_TO_MS = 1000     # km/s to m/s
EARTH_RADIUS_M = 6.371e6 # Earth's radius (m) for impact detection
LD = 3.844e8         # 1 Lunar Distance (m)

class CelestialBody:
    """
    Data structure for celestial objects (HEAVY-CLASS)
    """
    def __init__(self, name, mass, x_pos, y_pos, x_vel, y_vel, color):
        self.name = name
        self.mass = mass
        self.pos = np.array([x_pos, y_pos], dtype=float)
        self.vel = np.array([x_vel, y_vel], dtype=float)
        self.color = color
        self.path = [[], []] # Trajectory data buffer

    def calculate_acceleration_from(self, other_pos, other_mass):
        """
        Calculates gravitational acceleration vector (N-Body Kernel)
        """
        r_vec = other_pos - self.pos
        r_mag = np.linalg.norm(r_vec)
        if r_mag == 0:
            return np.array([0.0, 0.0])
        # a = G*M2/r^2
        a_mag = G * other_mass / r_mag**2
        a_vec = a_mag * (r_vec / r_mag) # Acceleration vector
        return a_vec

    def update_orbit(self, a_vec, dt):
        """
        Updates kinematic state via Euler-Cromer integration
        """
        self.vel += a_vec * dt
        self.pos += self.vel * dt
        self.path[0].append(self.pos[0])
        self.path[1].append(self.pos[1])

# --- Physics & Utility Kernels ---

def get_float_input(prompt):
    """
    Parses user input string to float. Handles exceptions.
    """
    while True:
        try:
            value_str = input(f"{term.CYAN}{prompt}{term.ENDC} ")
            value = float(value_str)
            return value
        except ValueError:
            print(f"{term.RED}--- ! INPUT ERROR: NON-NUMERIC DATA. RETRY... ---{term.ENDC}")

def calculate_perihelion_velocity(q_au, a_au):
    """
    Calculates velocity at Perihelion (q) using Vis-viva equation.
    """
    r = q_au * AU
    a = a_au * AU
    v_sq = (G * MASS_SUN) * ((2 / r) - (1 / a))
    v_ms = np.sqrt(v_sq)
    return v_ms

def calculate_period(a_au):
    """
    Calculates orbital period (years) via Kepler's 3rd Law (P^2 = a^3)
    """
    if a_au <= 0:
        return float('inf') # Unbound (Parabolic/Hyperbolic)
    
    period_years = np.sqrt(a_au**3)
    return period_years

def report_orbital_elements(body, sun_mass):
    """
    Calculates final orbital elements from a state vector (pos, vel).
    Used for simulation integrity check.
    """
    mu = G * sun_mass  # Standard gravitational parameter
    r_vec = body.pos
    v_vec = body.vel
    r_mag = np.linalg.norm(r_vec)
    v_sq = np.linalg.norm(v_vec)**2
    
    try:
        a_m = 1.0 / ((2.0 / r_mag) - (v_sq / mu))
        a_au = a_m / AU
        h = np.abs(r_vec[0] * v_vec[1] - r_vec[1] * v_vec[0])
        e = np.sqrt(1 - (h**2 / (mu * a_m)))
        q_au = a_au * (1 - e)
        Q_au = a_au * (1 + e)
        
        print(f"\n{term.BOLD}--- [STATE VECTOR ANALYSIS]: {body.name} ---{term.ENDC}")
        print(f"  > Semi-major axis (a): {a_au:<.4f} AU")
        print(f"  > Eccentricity (e):    {e:<.4f}")
        print(f"  > Perihelion (q):      {q_au:<.4f} AU")
        print(f"  > Aphelion (Q):        {Q_au:<.4f} AU")
        
    except Exception as e:
        print_glitch(f"--- ! STATE ANALYSIS FAILED: {body.name} (POSSIBLY EJECTED) ---")


# ---===================================---
# ---     MAIN EXECUTION BLOCK        ---
# ---===================================---

# --- 0. System Boot Screen ---
print_typed("...SYSTEM BOOT COMPLETE. ALL SUBSYSTEMS NOMINAL.", term.CYAN)
print_typed("...AWAITING COMMAND.\n", term.CYAN)

# --- 1. Acquire Target Data ---
print_fast(f"{term.AMBER}--- [ACQUIRING TARGET] ---{term.ENDC}\n")
name = input(f"{term.CYAN}INPUT TARGET DESIGNATION:{term.ENDC} ")
mass = get_float_input("  > INPUT TARGET MASS (kg) [DEFAULT 1e10]:")
color = input(f"{term.CYAN}  > INPUT PLOT TAG (e.g., red, cyan):{term.ENDC} ")

print(f"\n{term.AMBER}--- [AWAITING ORBITAL TELEMETRY] ---{term.ENDC}")
q_au = get_float_input("  > q (Perihelion) (AU):")
a_au = get_float_input("  > a (Semi-major) (AU):")

# --- 2. Calculate Initial State Vector ---
try:
    print_status("Calculating Vis-viva solution...", "BUSY", term.AMBER)
    v_at_perihelion_ms = calculate_perihelion_velocity(q_au, a_au)
    v_at_perihelion_kms = v_at_perihelion_ms / KMS_TO_MS
    period_years = calculate_period(a_au)
    
    print(f"\n{term.GREEN}--- [CALCULATION COMPLETE] ---{term.ENDC}")
    print_status(f"Target Velocity (q): {v_at_perihelion_kms:.2f} km/s", "LOCKED", term.GREEN)
    print_status(f"Target Period: {period_years:.2f} years", "LOCKED", term.GREEN)

except Exception as e:
    print_glitch("\n--- ! FATAL ERROR: VELOCITY KERNEL FAILED ---")
    print_glitch(f"--- ! CHECK INPUTS (e.g., a < q?). {e} ---")
    exit()

# --- 3. Instantiate Simulation Objects ---
sun_pos = np.array([0.0, 0.0])
bodies = []

# Add Earth (Reference Object "HOME")
earth_body = CelestialBody(
    name="HOME", mass=5.972e24, color='cyan',
    x_pos=AU, y_pos=0.0,
    x_vel=0.0, y_vel=29780.0
)
bodies.append(earth_body)

# Add User's Object ("TARGET")
user_object_body = CelestialBody(
    name=name.upper(), mass=mass, color=color,
    x_pos=q_au * AU, y_pos=0.0,
    x_vel=0.0, y_vel=v_at_perihelion_ms
)
bodies.append(user_object_body)
print_status("Instantiated system objects: 'HOME' and 'TARGET'", "DONE", term.GREEN)


# --- 4. Configure Simulation Parameters ---
sim_years = int(get_float_input("\nINPUT SIMULATION DURATION (YEARS):"))
dt = 60 * 60 * 12  # Timestep = 12 hours (High-res)
total_time = 60 * 60 * 24 * 365 * sim_years
steps = int(total_time / dt)

# --- 5. Run N-Body Simulation ---
print_typed(f"\n[ EXECUTING ] Engaging N-Body solver for {sim_years} years ({steps} timesteps)...", term.HEADER)
print_typed("...Physics core calibrated. Running...", term.HEADER)

# Proximity analysis buffers
min_distance_found = float('inf')
closest_step_found = 0
collision_detected = False

# Acceleration buffer
accelerations = {body.name: np.array([0.0, 0.0]) for body in bodies}

# Initialize Progress Bar
print_progress_bar(0, steps)

for i in range(steps):
    # --- Step 1: Calculate forces
    for body_i in bodies:
        total_accel = body_i.calculate_acceleration_from(sun_pos, MASS_SUN)
        for body_j in bodies:
            if body_i == body_j: continue
            total_accel += body_i.calculate_acceleration_from(body_j.pos, body_j.mass)
        accelerations[body_i.name] = total_accel

    # --- Step 2: Update positions
    for body in bodies:
        body.update_orbit(accelerations[body.name], dt)
    
    # --- Step 3: Proximity Check (HOME vs TARGET)
    distance_vec = earth_body.pos - user_object_body.pos
    current_distance = np.linalg.norm(distance_vec)
    
    if current_distance < min_distance_found:
        min_distance_found = current_distance
        closest_step_found = i
    
    # Check for direct impact
    if current_distance < EARTH_RADIUS_M:
        collision_detected = True
        print_progress_bar(i + 1, steps, prefix='[CALCULATING...]', suffix='STREAM...]') # Update bar
        print_glitch(f"\n\n--- [CRITICAL ALERT] ---")
        print_glitch(f"--- IMPACT DETECTED AT T+{i*dt/3600:.1f} HOURS ---")
        print_glitch(f"--- SIMULATION HALTED ---")
        break # Halt
    
    # Update progress bar
    print_progress_bar(i + 1, steps, prefix='[CALCULATING...]', suffix='STREAM...]')
            
if not collision_detected:
    print_status("\nSimulation... [TERMINATED_NORMAL]", "DONE", term.GREEN)

# --- 6. Report: Impact Hazard Assessment ---
print("\n" + "="*60)
print_typed(f"--- [IMPACT HAZARD ASSESSMENT]: {name} ---", term.AMBER)

if collision_detected:
    print_typed(f"Simulation Result: {term.RED}{term.BOLD}[DIRECT IMPACT CONFIRMED]{term.ENDC}", term.RED)
else:
    print_typed(f"Simulation Result: {term.GREEN}[NO IMPACT DETECTED] (Within {sim_years}yr window){term.ENDC}", term.GREEN)

# Calculate event time
closest_time_seconds = closest_step_found * dt
closest_time_days = closest_time_seconds / (60*60*24)
closest_time_years = closest_time_days / 365.25

print("\n--- [CLOSEST POINT OF APPROACH (CPA) LOG] ---")
print(f"  > Min. Distance (MOID): {min_distance_found / 1000:,.1f} km")
print(f"  > (Equiv. {min_distance_found / AU:.6f} AU)")
print(f"  > (Equiv. {term.BOLD}{min_distance_found / LD:.2f}{term.ENDC} Lunar Distances [LD])")
print(f"  > Event Epoch:          T+{closest_time_days:.1f} days (or {closest_time_years:.2f} years)")
print("="*60)


# --- 7. Report: Final Orbital Elements (Integrity Check) ---
print(f"\n{term.HEADER}--- [INTEGRITY CHECK // ORBITAL DEVIATION] ---{term.ENDC}")
print(f"(Comparing final q/a values to initial telemetry)")
report_orbital_elements(bodies[0], MASS_SUN) # HOME
report_orbital_elements(bodies[1], MASS_SUN) # TARGET

# --- 8. Render Trajectory Visualization (HUD STYLE) ---
print_typed("\n[ PLOTTING ] Rendering visualization... Transmitting to display.", term.CYAN)

plt.figure(figsize=(12, 12), facecolor='#050505') # Darker background
ax = plt.gca()
ax.set_facecolor('#0a0a0a') # Dark plot area
ax.set_aspect('equal')

# --- Plot Sun (Core) with Glow Effect ---
# Plot the core
plt.plot(sun_pos[0], sun_pos[1], 'o', color='yellow', markersize=20, label='Sol')
# Plot the glow (a larger, semi-transparent marker)
plt.plot(sun_pos[0], sun_pos[1], 'o', color='yellow', markersize=40, alpha=0.2) 

# --- Plot Orbits with Fading Trails ---
trail_split_percent = 0.7 # Show last 30% of the trail as "bright"

for body in bodies:
    path_x_au = np.array(body.path[0]) / AU
    path_y_au = np.array(body.path[1]) / AU
    
    # Prevent error if path is too short
    if len(path_x_au) < 2:
        plt.plot(path_x_au, path_y_au, color=body.color, linewidth=1.2, label=f"{body.name} (Active)")
        continue
        
    # Calculate split point for the trail
    split_index = int(len(path_x_au) * trail_split_percent)
    
    # Plot the "old" faded trail
    plt.plot(path_x_au[:split_index+1], path_y_au[:split_index+1], 
             color=body.color, linewidth=0.5, alpha=0.3)
    
    # Plot the "recent" bright trail
    plt.plot(path_x_au[split_index:], path_y_au[split_index:], 
             color=body.color, label=f"{body.name} (Active)", linewidth=1.2, alpha=1.0)
    
    # Plot the current position (as a brighter marker)
    plt.plot(body.pos[0]/AU, body.pos[1]/AU, 'o', color=body.color, markersize=8,
             markeredgecolor='white', markeredgewidth=1.0)
    
    # Add text label (Annotation)
    plt.text(body.pos[0]/AU + 0.1, body.pos[1]/AU, body.name, 
             color='white', fontsize=10, ha='left', weight='bold')

# --- Plot Closest Point of Approach (CPA) ---
# Get coordinates from the stored path data
try:
    earth_cpa_x = bodies[0].path[0][closest_step_found] / AU
    earth_cpa_y = bodies[0].path[1][closest_step_found] / AU
    target_cpa_x = bodies[1].path[0][closest_step_found] / AU
    target_cpa_y = bodies[1].path[1][closest_step_found] / AU
    
    # Draw a high-visibility line
    plt.plot([earth_cpa_x, target_cpa_x], [earth_cpa_y, target_cpa_y], 
             linestyle='--', color='red', 
             linewidth=1.5, alpha=1.0, label='CPA Event')
    
    # Annotate the CPA line
    mid_x = (earth_cpa_x + target_cpa_x) / 2
    mid_y = (earth_cpa_y + target_cpa_y) / 2
    plt.text(mid_x, mid_y + 0.05, 'CPA', 
             color='red', fontsize=12, weight='bold', ha='center')
             
except IndexError:
    print_glitch("--- ! PLOT ERROR: Could not resolve CPA coordinates ---")
    
# --- Sci-Fi HUD Styling ---
plt.title(f'A.H.E.S. N-Body Trajectory Analysis ({sim_years} Years)', color='green', weight='bold')

# Remove all axis spines and ticks for a clean HUD look
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

# Configure Legend
legend = plt.legend(facecolor='#1a1a1a', edgecolor='cyan', loc='upper right',
                    fontsize=9)
plt.setp(legend.get_texts(), color='white')

# Configure Grid (Main reference)
plt.grid(True, linestyle=':', alpha=0.3, color='green') # Green radar grid

# Set plot limits to be slightly larger than the max orbit
max_range = 0
for body in bodies:
    # Handle cases with no path data
    if len(body.path[0]) > 0:
        # (FIX 1: Added np.array() around body.path lists before dividing)
        max_range = max(max_range, np.max(np.abs(np.array(body.path[0])/AU)), np.max(np.abs(np.array(body.path[1])/AU)))
    else:
        max_range = max(max_range, np.abs(body.pos[0]/AU), np.abs(body.pos[1]/AU))
# Add a fallback in case max_range is still 0 (e.g. only Sun)
if max_range == 0:
    max_range = 5 

plt.xlim(-max_range*1.1, max_range*1.1)
plt.ylim(-max_range*1.1, max_range*1.1)

plt.show()

print_typed(f"\n{term.GREEN}--- A.H.E.S. RUN COMPLETE ---{term.ENDC}")