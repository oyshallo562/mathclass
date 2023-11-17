import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from matplotlib.widgets import Slider
from fractions import Fraction


# Define the modified function for integration
def f(x):
    return x ** 2


# Predefined set of fraction values for the sliders
fraction_values = np.array([-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])


# Function to find the nearest fraction value
def find_nearest_fraction(value):
    index = np.abs(fraction_values - value).argmin()
    return fraction_values[index]


# Initial integration range and constants
a, b = -1, 1

# Set up the plot
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
x = np.linspace(-2, 2, 1000)
ax.plot(x, f(x), 'r', linewidth=2)

# Add sliders below the plot
axcolor = 'lightgoldenrodyellow'
ax_a = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_b = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

slider_a = Slider(ax_a, 'a', -2, 2, valinit=a, valstep=fraction_values)
slider_b = Slider(ax_b, 'b', -2, 2, valinit=b, valstep=fraction_values)

# Display the initial integration area
initial_area = quad(f, a, b)[0]
area_text = ax.text(0.5, 0.9, f'Area: {initial_area:.2f}', horizontalalignment='center',
                    verticalalignment='center', transform=ax.transAxes)

# Temporarily disable slider callback flag
disable_callback = False


# Slider update function
def update(val):
    global a, b, disable_callback

    if disable_callback:
        return

    disable_callback = True

    a = find_nearest_fraction(slider_a.val)
    b = find_nearest_fraction(slider_b.val)

    slider_a.set_val(a)  # Update slider position to the nearest fraction
    slider_b.set_val(b)

    disable_callback = False

    # Remove each collection artist individually
    while len(ax.collections) > 0:
        ax.collections[0].remove()
    ax.fill_between(x, f(x), where=[(i >= a and i <= b) for i in x], color='gray', alpha=0.5)
    area = quad(f, a, b)[0]
    area_text.set_text(f'Area: {area:.2f} = {Fraction(area).limit_denominator()}')

    plt.draw()


slider_a.on_changed(update)
slider_b.on_changed(update)

plt.show()