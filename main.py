import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from matplotlib.widgets import Slider
from fractions import Fraction

# Predefined set of fraction values for the sliders (for both functions)
fraction_values = np.array([-2, -1.5, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.5, 2])

def find_nearest_fraction(value):
    index = np.abs(fraction_values - value).argmin()
    return fraction_values[index]


# Define the function for integration (x^2)
def f(x):
    return - x ** 2

# Define a new function for cubic integration (x^3 - x)
def g(x):
    return x ** 3 - x

# Set up the plot for the first function (f)
fig, ax = plt.subplots(2, 1, figsize=(8, 10))  # Two subplots for two functions
plt.subplots_adjust(bottom=0.35)
x = np.linspace(-2, 2, 1000)
ax[0].plot(x, f(x), 'r', linewidth=2)

# Add sliders below the plot for the first function
axcolor = 'lightgoldenrodyellow'
ax_a = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_b = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

# Update the slider initialization for the first function to use fraction values
slider_a = Slider(ax_a, 'a', -2, 2, valinit=find_nearest_fraction(-1), valstep=fraction_values)
slider_b = Slider(ax_b, 'b', -2, 2, valinit=find_nearest_fraction(1), valstep=fraction_values)


# Updated function to update the first plot with sliders using fraction values
def update_corrected_with_fraction(val):
    global disable_callback

    if disable_callback:
        return

    disable_callback = True

    a = find_nearest_fraction(slider_a.val)
    b = find_nearest_fraction(slider_b.val)

    slider_a.set_val(a)  # Update slider position to the nearest fraction
    slider_b.set_val(b)

    disable_callback = False

    # Remove each collection artist individually from the first plot
    while len(ax[0].collections) > 0:
        ax[0].collections[0].remove()

    # Fill the area under the curve between the sliders
    ax[0].fill_between(x, f(x), where=[(i >= a and i <= b) for i in x], color='gray', alpha=0.5)

    # Calculate and display the new area
    area = quad(f, a, b)[0]
    area_text_f.set_text(f'Area (x^2): {area:.2f} = {Fraction(area).limit_denominator()}')

    plt.draw()


# Connect the updated function to the sliders for the first function
slider_a.on_changed(update_corrected_with_fraction)
slider_b.on_changed(update_corrected_with_fraction)

# Display the initial integration area for the first function
initial_area_f = quad(f, -1, 1)[0]
area_text_f = ax[0].text(0.5, 0.9, f'Area (x^2): {initial_area_f:.2f}', horizontalalignment='center',
                         verticalalignment='center', transform=ax[0].transAxes)

# Set up the plot for the second function (g)
x_cubic = np.linspace(-1.5, 1.5, 1000)
ax[1].plot(x_cubic, g(x_cubic), 'b', linewidth=2)

# Find the roots of the cubic function where it intersects the x-axis
roots = np.roots([1, 0, -1, 0])  # Coefficients of x^3 - x
valid_roots = roots[np.isreal(roots)].real  # Filter out complex roots

# Calculate the area between the roots for the cubic function
area_g = quad(g, min(valid_roots), max(valid_roots))[0]
area_text_g = ax[1].text(0.5, 0.9, f'Area (x^3 - x): {area_g:.2f} = {Fraction(area_g).limit_denominator()}',
                         horizontalalignment='center', verticalalignment='center', transform=ax[1].transAxes)

# Function to update the first plot with corrected method to clear the previous filled area
def update_corrected(val):
    a = slider_a.val
    b = slider_b.val

    # Remove each collection artist individually
    while len(ax[0].collections) > 0:
        ax[0].collections[0].remove()

    # Fill the area under the curve between the sliders
    ax[0].fill_between(x, f(x), where=[(i >= a and i <= b) for i in x], color='gray', alpha=0.5)

    # Calculate and display the new area
    area = quad(f, a, b)[0]
    area_text_f.set_text(f'Area (x^2): {area:.2f} = {Fraction(area).limit_denominator()}')

    plt.draw()

# Connect the update function to the sliders
slider_a.on_changed(update_corrected)
slider_b.on_changed(update_corrected)

# Display the updated plot
#plt.show()




# Function to find the nearest fraction value


# Add sliders below the plot for the second function (g)
ax_c = plt.axes([0.25, 0.08, 0.65, 0.03], facecolor=axcolor)
ax_d = plt.axes([0.25, 0.03, 0.65, 0.03], facecolor=axcolor)

slider_c = Slider(ax_c, 'c', -1.5, 1.5, valinit=min(valid_roots), valstep=fraction_values)
slider_d = Slider(ax_d, 'd', -1.5, 1.5, valinit=max(valid_roots), valstep=fraction_values)

# Temporarily disable slider callback flag for both sliders
disable_callback = False


# Function to update the second plot with sliders for cubic function
def update_cubic(val):
    global disable_callback

    if disable_callback:
        return

    disable_callback = True

    c = find_nearest_fraction(slider_c.val)
    d = find_nearest_fraction(slider_d.val)

    slider_c.set_val(c)  # Update slider position to the nearest fraction
    slider_d.set_val(d)

    disable_callback = False

    # Remove each collection artist individually from the second plot
    while len(ax[1].collections) > 0:
        ax[1].collections[0].remove()
    ax[1].fill_between(x_cubic, g(x_cubic), where=[(i >= c and i <= d) for i in x_cubic], color='gray', alpha=0.5)

    area = quad(g, c, d)[0]
    area_text_g.set_text(f'Area (x^3 - x): {area:.2f} = {Fraction(area).limit_denominator()}')

    plt.draw()


# Connect the update function to the sliders for the second function
slider_c.on_changed(update_cubic)
slider_d.on_changed(update_cubic)

# Display the updated plot
plt.show()