import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib as mpl

# Set up a professional-looking style
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.3
mpl.rcParams['font.family'] = 'Arial'
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['figure.dpi'] = 100
mpl.rcParams['figure.figsize'] = [12, 8]

# Constants
g = 9.81  # Acceleration due to gravity (m/s^2)

# Function to calculate critical speed
def critical_speed(ball_diam_cm, cylinder_diam_cm):
    """
    Calculate critical speed of a ball mill
    
    Parameters:
    ball_diam_cm (float): Ball diameter in cm
    cylinder_diam_cm (float): Cylinder diameter in cm
    
    Returns:
    float: Critical speed in RPM
    """
    # Convert to meters and calculate radii
    ball_radius_m = (ball_diam_cm / 100) / 2
    cylinder_radius_m = (cylinder_diam_cm / 100) / 2
    
    # Check for valid dimensions
    if cylinder_radius_m <= ball_radius_m:
        return 0
    
    # Calculate critical speed (revolutions per second)
    critical_speed_rps = (1 / (2 * np.pi)) * np.sqrt(g / (cylinder_radius_m - ball_radius_m))
    
    # Convert to RPM
    return critical_speed_rps * 60

# Create the figure
fig, (ax, ax_info) = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [3, 1]})
plt.subplots_adjust(bottom=0.25, top=0.92, left=0.08, right=0.95, wspace=0.2)

# Set main plot title
fig.suptitle("Ball Mill Critical Speed Analyzer", fontsize=18, fontweight='bold')

# Initial values
initial_ball_diam = 1.5  # cm
cylinder_diams = np.linspace(5, 50, 100)  # Cylinder diameters from 5 to 50 cm

# Calculate initial critical speeds
critical_speeds = [critical_speed(initial_ball_diam, d) for d in cylinder_diams]

# Plot the initial curve
line, = ax.plot(critical_speeds, cylinder_diams, 'b-', linewidth=2.5, 
                label=f'Ball Diameter: {initial_ball_diam} cm')
ax.set_xlabel('Critical Speed (RPM)', fontsize=14, fontweight='bold')
ax.set_ylabel('Cylinder Diameter (cm)', fontsize=14, fontweight='bold')
ax.set_title('Critical Speed vs Cylinder Diameter', fontsize=16)
ax.grid(True, alpha=0.4)
ax.set_ylim(5, 50)
ax.set_xlim(0, max(critical_speeds) * 1.1)

# Add a reference line for 70% of critical speed
seventy_percent_line = ax.axvline(x=0, color='g', linestyle='--', alpha=0.7, 
                                  label='70% of Critical Speed (Recommended)')

# Add legend
ax.legend(loc='upper right', frameon=True)

# Add a slider for ball diameter
ax_ball = plt.axes([0.25, 0.1, 0.5, 0.03])
ball_slider = Slider(
    ax=ax_ball,
    label='Ball Diameter (cm):',
    valmin=0.1,
    valmax=5.0,
    valinit=initial_ball_diam,
    valstep=0.1
)

# Text boxes for click results
click_result_text = ax.text(0.05, 0.95, "Click on a cylinder diameter to see critical speed", 
                           transform=ax.transAxes, fontsize=11, verticalalignment='top',
                           bbox=dict(facecolor='white', alpha=0.8))

# Add physics explanation to the info panel
ax_info.set_title("Physics of Ball Mill Critical Speed", fontsize=14)
ax_info.set_axis_off()

physics_text = """
The critical speed is the rotational speed at which grinding balls are pinned to the inner wall of the mill due to centrifugal force, preventing them from cascading down to perform grinding operations.

Formula:
    N_c = (1 / (2π)) × √(g / (R - r)) × 60

Where:
    N_c = Critical speed (RPM)
    g = Gravitational acceleration (9.81 m/s²)
    R = Mill radius (meters)
    r = Ball radius (meters)

Key Relationships:
- As cylinder size increases, critical speed decreases
- Larger balls require lower critical speeds
- Optimal operation is typically at 65-80% of critical speed
"""
ax_info.text(0.02, 0.98, physics_text, fontsize=11, 
             ha='left', va='top', wrap=True)

# Add key relationships
ax_info.text(0.02, 0.25, "Practical Guidelines:", 
             fontsize=12, fontweight='bold', ha='left', va='top')
guidelines = """
• Critical speed: Full centrifuging speed
• Recommended speed: 70% of critical speed
• For nano grinding: 70-100 RPM
• Ball size: 0.5-2mm for nano particles
• Cylinder size: 10-20cm for lab mills
"""
ax_info.text(0.05, 0.20, guidelines, fontsize=11, 
             ha='left', va='top', wrap=True)

# Add a diagram of a ball mill
def add_mill_diagram(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Draw cylinder
    cyl_height = 0.7
    cyl_width = 0.4
    cylinder = plt.Rectangle((0.3, 0.15), cyl_width, cyl_height, 
                            fill=True, color='lightblue', alpha=0.7, ec='navy', lw=2)
    ax.add_patch(cylinder)
    
    # Draw balls
    ball_size = 0.03
    ball_positions = [(0.4, 0.3), (0.5, 0.5), (0.4, 0.7), (0.5, 0.3), (0.45, 0.6)]
    for pos in ball_positions:
        ball = plt.Circle(pos, ball_size, color='red', alpha=0.8, ec='darkred', lw=1)
        ax.add_patch(ball)
    
    # Add rotation arrow
    ax.arrow(0.75, 0.5, 0.15, 0, head_width=0.05, head_length=0.03, 
            fc='darkblue', ec='darkblue')
    ax.text(0.8, 0.45, "Rotation", fontsize=9, color='darkblue', ha='center')
    
    ax.set_axis_off()

# Add diagram to the info panel
ax_diagram = fig.add_axes([0.75, 0.55, 0.15, 0.3])
add_mill_diagram(ax_diagram)

# Variables to store click markers
click_marker = None
click_text = None

# Click event handler
def on_click(event):
    global click_marker, click_text
    
    if event.inaxes != ax:
        return
    
    # Get cylinder diameter from y-coordinate
    cylinder_diam = event.ydata
    
    # Get current ball diameter from slider
    ball_diam = ball_slider.val
    
    # Calculate critical speed
    cs = critical_speed(ball_diam, cylinder_diam)
    
    # Calculate 70% of critical speed
    seventy_percent = cs * 0.7
    
    # Remove previous markers and text
    if click_marker:
        click_marker.remove()
    if click_text:
        click_text.remove()
    
    # Add new marker and text
    click_marker = ax.scatter(cs, cylinder_diam, s=80, c='red', marker='o', edgecolor='black', zorder=5)
    
    # Create text box with results
    result_text = f"Cylinder Diameter: {cylinder_diam:.1f} cm\n" \
                 f"Ball Diameter: {ball_diam:.1f} cm\n" \
                 f"Critical Speed: {cs:.1f} RPM\n" \
                 f"70% Recommended: {seventy_percent:.1f} RPM"
    
    click_text = ax.text(0.05, 0.85, result_text, transform=ax.transAxes, fontsize=11,
                         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.9))
    
    # Update the 70% line
    seventy_percent_line.set_xdata(seventy_percent)
    
    # Update the plot
    fig.canvas.draw_idle()

# Connect the click event
fig.canvas.mpl_connect('button_press_event', on_click)

# Update function for slider
def update(val):
    ball_diam = ball_slider.val
    # Update critical speeds for the new ball diameter
    new_critical_speeds = [critical_speed(ball_diam, d) for d in cylinder_diams]
    line.set_xdata(new_critical_speeds)
    line.set_label(f'Ball Diameter: {ball_diam:.1f} cm')
    
    # Update the 70% line position
    if click_marker:
        # If there's a marker, recalculate for that cylinder diameter
        cylinder_diam = click_marker.get_offsets()[0][1]
        cs = critical_speed(ball_diam, cylinder_diam)
        seventy_percent = cs * 0.7
        seventy_percent_line.set_xdata(seventy_percent)
        
        # Update the marker position
        click_marker.set_offsets([[cs, cylinder_diam]])
        
        # Update the text
        if click_text:
            result_text = f"Cylinder Diameter: {cylinder_diam:.1f} cm\n" \
                          f"Ball Diameter: {ball_diam:.1f} cm\n" \
                          f"Critical Speed: {cs:.1f} RPM\n" \
                          f"70% Recommended: {seventy_percent:.1f} RPM"
            click_text.set_text(result_text)
    
    # Update legend
    ax.legend(loc='upper right', frameon=True)
    
    # Update x-axis limits
    ax.set_xlim(0, max(new_critical_speeds) * 1.1)
    
    # Redraw
    fig.canvas.draw_idle()

# Register update function with slider
ball_slider.on_changed(update)

# Add reset button
resetax = plt.axes([0.8, 0.05, 0.1, 0.04])
reset_button = Button(resetax, 'Reset All', color='lightgoldenrodyellow', hovercolor='0.975')

def reset(event):
    global click_marker, click_text
    
    # Reset slider
    ball_slider.reset()
    
    # Remove click markers
    if click_marker:
        click_marker.remove()
        click_marker = None
    
    if click_text:
        click_text.remove()
        click_text = None
    
    # Reset the 70% line
    seventy_percent_line.set_xdata(0)
    
    # Reset the instruction text
    click_result_text.set_text("Click on a cylinder diameter to see critical speed")
    
    # Redraw
    fig.canvas.draw_idle()

reset_button.on_clicked(reset)

plt.tight_layout()
plt.show()
