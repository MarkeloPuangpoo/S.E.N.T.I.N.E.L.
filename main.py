import numpy as np
# (ลบ matplotlib)
import time
import sys
import random

# อิมพอร์ต Skyfield และ PyVista
from skyfield.api import load, Topos
# KeplerOrbit / OsculatingElements moved between Skyfield versions.
# Try sensible fallbacks so this script works with multiple releases.
try:
    from skyfield.elementslib import OsculatingElements
except Exception:
    # Fallback or error handling if needed, ensure OsculatingElements is defined
    # For simplicity, we might assume it exists if skyfield is installed
    # If this fails later, it indicates a deeper issue with the skyfield install/version
    # A more robust check might be needed depending on supported versions
    try:
        # Check alternative location if applicable to older versions
        pass # Add fallback import if known
    except ImportError:
         OsculatingElements = None # Explicitly set to None if not found


from skyfield.timelib import Time
import pyvista as pv # (ใหม่)

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
# (ฟังก์ชัน print_... ทั้งหมดเหมือนเดิม)
def print_fast(text, color=term.GREEN):
    sys.stdout.write(color + text + term.ENDC)
    sys.stdout.flush()

def print_typed(text, color=term.GREEN, delay=0.005):
    for char in text:
        sys.stdout.write(color + char + term.ENDC)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_glitch(text, color=term.RED):
    print_fast(f"\r{color}{text}{term.ENDC}", color)
    time.sleep(0.05)
    print_fast(f"\r{' ' * len(text)}\r", term.ENDC)
    time.sleep(0.05)
    print_fast(f"{color}{text}{term.ENDC}\n", color)

def print_status(message, status, color=term.CYAN):
    print(f"{color}[ {status.ljust(10)} ] {term.ENDC}{message}")

def print_progress_bar(iteration, total, prefix='[CALCULATING...]', suffix='STREAM...]', length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
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
MU_SUN = G * MASS_SUN

MIN_DISTANCE = EARTH_RADIUS_M * 0.5
MAX_ACCELERATION = 1.0

class CelestialBody:
    """ Data structure for celestial objects (3D) """
    def __init__(self, name, mass, x_pos, y_pos, z_pos, x_vel, y_vel, z_vel, color):
        self.name = name
        self.mass = mass
        self.pos = np.array([x_pos, y_pos, z_pos], dtype=float)
        self.vel = np.array([x_vel, y_vel, z_vel], dtype=float)
        self.color = color
        self.path = [[], [], []]

    def calculate_acceleration_from(self, other_pos, other_mass):
        """ Calculates gravitational acceleration vector (N-Body Kernel) """
        r_vec = other_pos - self.pos
        r_mag = np.linalg.norm(r_vec)
        if r_mag < MIN_DISTANCE: r_mag = MIN_DISTANCE
        a_mag = G * other_mass / r_mag**2
        if a_mag > MAX_ACCELERATION: a_mag = MAX_ACCELERATION
        a_vec = a_mag * (r_vec / r_mag)
        return a_vec

    def update_orbit(self, a_vec, dt):
        """ Updates kinematic state via Euler-Cromer integration """
        self.vel += a_vec * dt
        self.pos += self.vel * dt
        self.path[0].append(self.pos[0])
        self.path[1].append(self.pos[1])
        self.path[2].append(self.pos[2])

# --- Physics & Utility Kernels ---

def get_float_input(prompt):
    """ Parses user input string to float. Handles exceptions. """
    while True:
        try:
            value_str = input(f"{term.CYAN}{prompt}{term.ENDC} ")
            value = float(value_str)
            return value
        except ValueError:
            print(f"{term.RED}--- ! INPUT ERROR: NON-NUMERIC DATA. RETRY... ---{term.ENDC}")

# --- ฟังก์ชันแปลง Elements เป็น State Vector (ใช้ NumPy) ---
def classical_elements_to_state(a_au, e, i_deg, raan_deg, argp_deg, M_deg, mu):
    """ Return (position_m, velocity_m_per_s) in an inertial frame (ecliptic J2000). """
    # Convert units
    a = a_au * AU
    i = np.radians(i_deg)
    raan = np.radians(raan_deg) # Node
    argp = np.radians(argp_deg) # Peri
    M = np.radians(M_deg)       # Mean Anomaly

    # Solve Kepler's equation for eccentric anomaly E (Newton-Raphson)
    if e < 0.8: E = M
    else: E = np.pi
    for _ in range(100):
        f = E - e * np.sin(E) - M
        fp = 1 - e * np.cos(E)
        if fp == 0: break
        dE = -f / fp
        E += dE
        if abs(dE) < 1e-12: break

    cos_E = np.cos(E); sin_E = np.sin(E)
    if e == 0: nu = M
    else: nu = np.arctan2(np.sqrt(1.0 - e**2) * sin_E, cos_E - e)

    r = a * (1.0 - e * cos_E)
    if r <= 0: raise ValueError("Non-positive radius calculated, check elements.")

    x_pf = r * np.cos(nu); y_pf = r * np.sin(nu)
    n = np.sqrt(mu / a**3)
    vx_pf = -(n * a**2 / r) * sin_E
    vy_pf = (n * a**2 * np.sqrt(1.0 - e**2) / r) * cos_E

    cos_raan = np.cos(raan); sin_raan = np.sin(raan)
    cos_i    = np.cos(i);    sin_i    = np.sin(i)
    cos_argp = np.cos(argp); sin_argp = np.sin(argp)

    Xx = cos_raan * cos_argp - sin_raan * sin_argp * cos_i
    Xy = -cos_raan * sin_argp - sin_raan * cos_argp * cos_i
    Yx = sin_raan * cos_argp + cos_raan * sin_argp * cos_i
    Yy = -sin_raan * sin_argp + cos_raan * cos_argp * cos_i
    Zx = sin_argp * sin_i
    Zy = cos_argp * sin_i

    pos_eci = np.array([ Xx * x_pf + Xy * y_pf, Yx * x_pf + Yy * y_pf, Zx * x_pf + Zy * y_pf ])
    vel_eci = np.array([ Xx * vx_pf + Xy * vy_pf, Yx * vx_pf + Yy * vy_pf, Zx * vx_pf + Zy * vy_pf ])

    return pos_eci, vel_eci
# --- (จบฟังก์ชันแปลง) ---

def report_orbital_elements(body, sun_mass):
    """ Reports elements calculated back from state vector """
    mu = G * sun_mass
    r_vec = body.pos
    v_vec = body.vel
    r_mag = np.linalg.norm(r_vec)
    v_sq = np.linalg.norm(v_vec)**2

    if r_mag < 1e-6 or v_sq < 1e-6:
        print_glitch(f"--- ! STATE ANALYSIS SKIPPED: {body.name} (Near Zero State) ---")
        return

    try:
        specific_energy = v_sq / 2.0 - mu / r_mag
        # Handle unbound case where specific_energy might be non-negative
        if specific_energy >= 0:
             a_au = float('inf') # Parabolic or Hyperbolic
        else:
            a_m = -mu / (2.0 * specific_energy)
            a_au = a_m / AU

        h_vec = np.cross(r_vec, v_vec)
        h_mag = np.linalg.norm(h_vec)
        if h_mag < 1e-6:
             print_glitch(f"--- ! STATE ANALYSIS FAILED: {body.name} (Near Zero Angular Momentum) ---")
             return
        e_vec = (np.cross(v_vec, h_vec) / mu) - (r_vec / r_mag)
        e = np.linalg.norm(e_vec)
        arccos_arg = np.clip(h_vec[2] / h_mag, -1.0, 1.0)
        i = np.degrees(np.arccos(arccos_arg))

        # Calculate periapsis distance (q) which is valid for all conics
        q_m = h_mag**2 / (mu * (1.0 + e)) if (1.0 + e) > 1e-9 else 0 # Avoid division by zero if e is exactly -1 (impossible)
        q_au = q_m / AU

        # Calculate apoapsis distance (Q) only for bound orbits
        Q_au = float('inf')
        if e < 1.0 and a_au != float('inf'):
            Q_au = a_au * (1.0 + e)


        print(f"\n{term.BOLD}--- [STATE VECTOR ANALYSIS]: {body.name} ---{term.ENDC}")
        if a_au == float('inf'):
             print(f"  > Semi-major axis (a): Unbound (>= parabolic)")
        else:
             print(f"  > Semi-major axis (a): {a_au:<.4f} AU")
        print(f"  > Eccentricity (e):    {e:<.4f}")
        print(f"  > Inclination (i):     {i:<.4f} deg")
        print(f"  > Perihelion (q):      {q_au:<.4f} AU") # Changed from Periapsis for solar orbit context
        if e < 1.0 and Q_au != float('inf'):
            print(f"  > Aphelion (Q):        {Q_au:<.4f} AU") # Changed from Apoapsis
        else:
            print(f"  > Aphelion (Q):        inf")

    except Exception as e:
        print_glitch(f"--- ! STATE ANALYSIS FAILED: {body.name} ({e}) ---")


# ---===================================---
# ---     MAIN EXECUTION BLOCK        ---
# ---===================================---

# --- 0. System Boot Screen ---
print_fast(r"""
    //                \\
   //                  \\
  //   S.E.N.T.I.N.E.L.  \\
 //   SYSTEM ECLIPTIC      \\
//   NEAR-EARTH TRAJECTORY  //
\\    INTERCEPT LOGIC     //
 \\   v4.6 (PyVista Stable)//
  \\    [3D KERNEL]     //
   \\                  //
    \\                //
""", term.GREEN)
print_typed("...SYSTEM BOOT COMPLETE. 3D KERNEL ENGAGED.", term.CYAN)

# --- 1. โหลด Skyfield Kernel ---
print_typed("...Loading JPL Ephemeris...", term.AMBER)
try:
    planets = load('de421.bsp')
    ts = load.timescale()
    print_status("JPL Kernel 'de421.bsp' loaded.", "OK", term.GREEN)
    print_status("Timescale initialized.", "OK", term.GREEN)
except Exception as e:
    print_glitch(f"\n--- ! FATAL ERROR: COULD NOT LOAD SKYFIELD KERNEL --- {e}")
    exit()

print_typed("...AWAITING COMMAND.\n", term.CYAN)

# --- 2. Acquire Target Data ---
print_fast(f"{term.AMBER}--- [ACQUIRING TARGET] ---{term.ENDC}\n")
name = input(f"{term.CYAN}INPUT TARGET DESIGNATION:{term.ENDC} ")
mass = get_float_input(f"  > INPUT TARGET MASS (kg) [DEFAULT 1e10]:")
color = input(f"{term.CYAN}  > INPUT PLOT TAG (e.g., red, cyan):{term.ENDC} ")

print(f"\n{term.AMBER}--- [AWAITING ORBITAL TELEMETRY (3D)] ---{term.ENDC}")
print(f"{term.AMBER}(All angles in DEGREES, distances in AU){term.ENDC}")
q_au = get_float_input("  > q (Perihelion distance) (AU):")
e = get_float_input("  > e (Eccentricity):")
i_deg = get_float_input("  > i (Inclination) (deg):")
node_deg = get_float_input("  > node (Long. of Asc. Node) (deg):")
peri_deg = get_float_input("  > peri (Argument of Perihelion) (deg):")
M_deg = get_float_input("  > M (Mean Anomaly at Epoch) (deg):")
print(f"{term.AMBER}--- [TELEMETRY RECEIVED] ---{term.ENDC}")


# --- 3. Calculate Initial State Vector ---
try:
    print_status("Calculating state vectors...", "BUSY", term.AMBER)

    t = ts.now() # Get current time for Earth's position
    # Handle potential division by zero if e is exactly 1 (parabolic)
    if abs(1.0 - e) < 1e-9: # If eccentricity is very close to 1
        print_glitch("\n--- ! WARNING: Eccentricity near 1 (parabolic), semi-major axis is infinite. ---")
        a_au = float('inf') # Or handle parabolic case separately if needed
        # Note: classical_elements_to_state might need adjustments for parabolic case
    elif e > 1.0: # Hyperbolic case
        a_au = q_au / (1.0 - e) # a will be negative for hyperbolic
    else: # Elliptical case
        a_au = q_au / (1.0 - e)

    # Use the NumPy-based conversion function
    target_pos, target_vel = classical_elements_to_state(
        a_au=a_au, e=e, i_deg=i_deg,
        raan_deg=node_deg, argp_deg=peri_deg, M_deg=M_deg,
        mu=MU_SUN
    )

    # Get Earth's state vector using Skyfield
    earth = planets['earth']
    sun = planets['sun']
    earth_state = (earth - sun).at(t)
    earth_pos = earth_state.position.m
    earth_vel = earth_state.velocity.m_per_s

    print(f"\n{term.GREEN}--- [STATE VECTORS LOCKED (T=NOW)] ---{term.ENDC}")
    # Only print 'a' if it's not infinite
    if a_au != float('inf'):
        print_status(f"Calculated Semi-major (a): {a_au:.4f} AU", "LOCKED", term.GREEN)
    else:
        print_status(f"Calculated Semi-major (a): Parabolic/Infinite", "LOCKED", term.GREEN)
    print_status(f"HOME Pos [X,Y,Z]: {earth_pos[0]/AU:.2f}, {earth_pos[1]/AU:.2f}, {earth_pos[2]/AU:.2f} AU", "LOCKED")
    print_status(f"TARGET Pos [X,Y,Z]: {target_pos[0]/AU:.2f}, {target_pos[1]/AU:.2f}, {target_pos[2]/AU:.2f} AU", "LOCKED")

except ValueError as ve:
     print_glitch(f"\n--- ! FATAL ERROR: STATE VECTOR CALCULATION FAILED ---")
     print_glitch(f"--- ! {ve} ---")
     exit()
except Exception as e:
    print_glitch(f"\n--- ! FATAL ERROR: COULD NOT GET STATE VECTOR ---")
    print_glitch(f"--- ! CHECK YOUR INPUT VALUES. {e} ---")
    exit()

# --- 4. Instantiate Simulation Objects ---
sun_pos = np.array([0.0, 0.0, 0.0])
bodies = []
earth_body = CelestialBody(
    name="HOME", mass=5.972e24, color='cyan',
    x_pos=earth_pos[0], y_pos=earth_pos[1], z_pos=earth_pos[2],
    x_vel=earth_vel[0], y_vel=earth_vel[1], z_vel=earth_vel[2]
)
bodies.append(earth_body)
user_object_body = CelestialBody(
    name=name.upper(), mass=mass, color=color,
    x_pos=target_pos[0], y_pos=target_pos[1], z_pos=target_pos[2],
    x_vel=target_vel[0], y_vel=target_vel[1], z_vel=target_vel[2]
)
bodies.append(user_object_body)
print_status("Instantiated 3D system objects: 'HOME' and 'TARGET'", "DONE", term.GREEN)

# --- 5. Configure Simulation Parameters ---
sim_years = int(get_float_input("\nINPUT SIMULATION DURATION (YEARS):"))
dt = 60 * 60 * 12  # Timestep = 12 hours
total_time = 60 * 60 * 24 * 365 * sim_years
steps = int(total_time / dt)

# --- 6. Run N-Body Simulation ---
print_typed(f"\n[ EXECUTING ] Engaging 3D N-Body solver for {sim_years} years ({steps} timesteps)...", term.HEADER)
print_typed("...Physics core calibrated. Running...", term.HEADER)
min_distance_found = float('inf')
closest_step_found = 0
collision_detected = False
accelerations = {body.name: np.array([0.0, 0.0, 0.0]) for body in bodies}
print_progress_bar(0, steps)
for i in range(steps):
    for body_i in bodies:
        total_accel = body_i.calculate_acceleration_from(sun_pos, MASS_SUN)
        for body_j in bodies:
            if body_i == body_j: continue
            total_accel += body_i.calculate_acceleration_from(body_j.pos, body_j.mass)
        accelerations[body_i.name] = total_accel
    for body in bodies:
        body.update_orbit(accelerations[body.name], dt) # Corrected loop
    distance_vec = earth_body.pos - user_object_body.pos
    current_distance = np.linalg.norm(distance_vec)
    if current_distance < min_distance_found:
        min_distance_found = current_distance
        closest_step_found = i
    if current_distance < EARTH_RADIUS_M:
        collision_detected = True
        print_progress_bar(i + 1, steps)
        print_glitch(f"\n\n--- [CRITICAL ALERT] --- IMPACT DETECTED AT T+{i*dt/3600:.1f} HOURS --- SIMULATION HALTED ---")
        break
    print_progress_bar(i + 1, steps)
if not collision_detected: print_status("\nSimulation... [TERMINATED_NORMAL]", "DONE", term.GREEN)

# --- 7. Report: Impact Hazard Assessment ---
print("\n" + "="*60)
print_typed(f"--- [IMPACT HAZARD ASSESSMENT]: {name} ---", term.AMBER)
if collision_detected: print_typed(f"Simulation Result: {term.RED}{term.BOLD}[DIRECT IMPACT CONFIRMED]{term.ENDC}", term.RED)
else: print_typed(f"Simulation Result: {term.GREEN}[NO IMPACT DETECTED] (Within {sim_years}yr window){term.ENDC}", term.GREEN)
closest_time_seconds = closest_step_found * dt
closest_time_days = closest_time_seconds / (60*60*24)
closest_time_years = closest_time_days / 365.25
print("\n--- [CLOSEST POINT OF APPROACH (CPA) LOG] ---")
print(f"  > Min. Distance (MOID): {min_distance_found / 1000:,.1f} km")
print(f"  > (Equiv. {min_distance_found / AU:.6f} AU)")
print(f"  > (Equiv. {term.BOLD}{min_distance_found / LD:.2f}{term.ENDC} Lunar Distances [LD])")
print(f"  > Event Epoch:          T+{closest_time_days:.1f} days (or {closest_time_years:.2f} years)")
print("="*60)

# --- 8. Report: Final Orbital Elements ---
print(f"\n{term.HEADER}--- [INTEGRITY CHECK // ORBITAL DEVIATION] ---{term.ENDC}")
print(f"(Comparing final state to known orbital mechanics)")
report_orbital_elements(bodies[0], MASS_SUN)
report_orbital_elements(bodies[1], MASS_SUN)

# --- 9. Render Trajectory Visualization (PyVista 3D HUD) ---
print_typed("\n[ PLOTTING ] Rendering 3D Visualization Core (PyVista)...", term.CYAN)
try:
    plotter = pv.Plotter(window_size=[1200, 1200], lighting='light_kit')
    plotter.set_background('black')
    sun_mesh = pv.Sphere(radius=0.1, center=(0, 0, 0))
    plotter.add_mesh(sun_mesh, color='yellow', emissive=True, label='Sol (Origin)')
    max_range_plot = 0
    for body in bodies:
        # Check if path is not empty before trying to access it
        if body.path and body.path[0]:
             max_range_plot = max(max_range_plot,
                                 np.max(np.abs(np.array(body.path[0])/AU)),
                                 np.max(np.abs(np.array(body.path[1])/AU)))
        # Include current position in range calculation in case path is empty
        max_range_plot = max(max_range_plot, np.abs(body.pos[0]/AU), np.abs(body.pos[1]/AU))

    if max_range_plot == 0: max_range_plot = 5 # Fallback
    plot_lim = max_range_plot * 1.1

    ecliptic_mesh = pv.Plane(center=(0, 0, 0), direction=(0, 0, 1), i_size=plot_lim * 2, j_size=plot_lim * 2, i_resolution=10, j_resolution=10)
    plotter.add_mesh(ecliptic_mesh, color='cyan', style='wireframe', opacity=0.1, label='Ecliptic Plane')

    trail_split_percent = 0.7
    for body in bodies:
        # Check again if path has data
        if not body.path or not body.path[0] or len(body.path[0]) < 2:
            # Optionally plot just the current position if no path
            pos_now_au = body.pos / AU
            plotter.add_mesh(pv.Sphere(radius=plot_lim * 0.01, center=pos_now_au), color=body.color, emissive=True)
            plotter.add_point_labels(pos_now_au + (plot_lim * 0.02), [body.name], font_size=10, text_color='white', always_visible=True, shape=None, show_points=False)
            continue # Skip path plotting for this body


        path_x_au = np.array(body.path[0]) / AU
        path_y_au = np.array(body.path[1]) / AU
        path_z_au = np.array(body.path[2]) / AU

        points = np.column_stack((path_x_au, path_y_au, path_z_au))
        split_index = int(len(path_x_au) * trail_split_percent)

        old_points = points[:split_index+1]
        if len(old_points) > 1: plotter.add_mesh(pv.lines_from_points(old_points), color=body.color, opacity=0.3, line_width=2)
        recent_points = points[split_index:]
        if len(recent_points) > 1: plotter.add_mesh(pv.lines_from_points(recent_points), color=body.color, opacity=1.0, line_width=3, label=f"{body.name} (Active)")

        pos_now_au = body.pos / AU
        plotter.add_mesh(pv.Sphere(radius=plot_lim * 0.01, center=pos_now_au), color=body.color, emissive=True)
        plotter.add_point_labels(pos_now_au + (plot_lim * 0.02), [body.name], font_size=10, text_color='white', always_visible=True, shape=None, show_points=False)

    # Plot CPA line only if simulation ran long enough to have path data
    if closest_step_found > 0 and len(bodies[0].path[0]) > closest_step_found and len(bodies[1].path[0]) > closest_step_found:
        try:
            earth_cpa_pos = np.array([bodies[0].path[0][closest_step_found], bodies[0].path[1][closest_step_found], bodies[0].path[2][closest_step_found]]) / AU
            target_cpa_pos = np.array([bodies[1].path[0][closest_step_found], bodies[1].path[1][closest_step_found], bodies[1].path[2][closest_step_found]]) / AU
            cpa_line = pv.lines_from_points(np.array([earth_cpa_pos, target_cpa_pos]))

            # --- (แก้ไข) ใช้ Property เพื่อตั้งค่าเส้นประ ---
            # Add CPA line as a solid, semi-transparent line. PyVista does not reliably
            # support setting custom stipple patterns on the actor property across versions,
            # so use a solid line with slightly increased width and opacity instead.
            actor = plotter.add_mesh(cpa_line, color='red', line_width=5, opacity=0.85, label='CPA Event')
            # --- (จบส่วนแก้ไข) ---

            mid_pos = (earth_cpa_pos + target_cpa_pos) / 2
            plotter.add_point_labels(mid_pos + (0, 0, plot_lim * 0.02), ['CPA'], font_size=12, text_color='red', always_visible=True, shape=None, show_points=False)
        except IndexError: print_glitch("--- ! PLOT ERROR: Could not resolve CPA coordinates (IndexError) ---")
        except Exception as plot_e: print_glitch(f"--- ! PLOT ERROR: Could not plot CPA line ({plot_e}) ---")
    elif not collision_detected:
         print_status("CPA line skipped (Simulation too short or no close approach found)", "INFO", term.AMBER)


    # Add legend with a subtle semi-transparent background. Avoid unsupported kwargs.
    plotter.add_legend(bcolor=(0.05, 0.05, 0.05, 0.6), size=(0.16, 0.22))
    plotter.enable_anti_aliasing()
    plotter.show_axes()
    plotter.set_focus(sun_mesh.center)
    plotter.camera_position = 'xy'; plotter.camera.elevation = 45; plotter.camera.zoom(0.7)
    print_typed("...Launching 3D Interactive Renderer...", term.HEADER)
    plotter.show(title=f'S.E.N.T.I.N.E.L. 3D N-Body (PyVista) - {sim_years} Years')
except Exception as e:
    # Print detailed traceback for PyVista errors
    import traceback
    print_glitch(f"\n--- ! FATAL ERROR: PYVISTA RENDERER FAILED ---")
    print_glitch(f"--- ! {e} ---")
    print_glitch(f"--- ! Traceback: ---")
    print_glitch(traceback.format_exc()) # Show detailed error
    exit()

print_typed(f"\n{term.GREEN}--- S.E.N.T.I.N.E.L. RUN COMPLETE (v4.6 PyVista Stable) ---{term.ENDC}")