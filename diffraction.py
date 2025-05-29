import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def compute_beta(slit_dimension, positions, wavelength, screen_distance):
    return np.pi * slit_dimension * positions / (wavelength * screen_distance)


def normalized_single_slit_intensity(positions, wavelength, slit_width, screen_distance):
    beta = compute_beta(slit_width, positions, wavelength, screen_distance)
    raw = np.sinc(beta / np.pi) ** 2
    return raw / np.max(raw)


def normalized_double_slit_intensity(positions, wavelength, slit_width, slit_separation, screen_distance):
    beta = compute_beta(slit_width, positions, wavelength, screen_distance)
    delta = np.pi * slit_separation * positions / (wavelength * screen_distance)
    raw = np.sinc(beta / np.pi) ** 2 * np.cos(delta) ** 2
    return raw / np.max(raw)


def is_fraunhofer_regime(slit_width, wavelength, screen_distance):
    return screen_distance >= 10 * (slit_width ** 2 / wavelength)


def configure_axes(axis, title):
    axis.set_title(title)
    axis.set_xlabel("Положение на экране (м)")
    axis.set_ylabel("Интенсивность")
    axis.grid(True)


def calculate_and_plot(positions, wavelength, slit_width, slit_separation, screen_distance, axes):
    single_axis, double_axis = axes
    intensity_single = normalized_single_slit_intensity(positions, wavelength, slit_width, screen_distance)
    intensity_double = normalized_double_slit_intensity(positions, wavelength, slit_width, slit_separation, screen_distance)

    single_axis.clear()
    double_axis.clear()

    single_axis.plot(positions, intensity_single, color='blue')
    double_axis.plot(positions, intensity_double, color='red')

    configure_axes(single_axis, "Диффракция одной щели")
    configure_axes(double_axis, "Диффракция двух щелей")


def setup_sliders(fig, initial_values):
    axes_positions = {
        'wavelength': plt.axes([0.1, 0.2, 0.8, 0.03]),
        'slit_width': plt.axes([0.1, 0.15, 0.8, 0.03]),
        'slit_separation': plt.axes([0.1, 0.1, 0.8, 0.03]),
        'screen_distance': plt.axes([0.1, 0.05, 0.8, 0.03])
    }

    sliders = {
        'wavelength': Slider(
            axes_positions['wavelength'], 'λ (нм)', 380, 750,
            valinit=initial_values['wavelength'] * 1e9
        ),
        'slit_width': Slider(
            axes_positions['slit_width'], 'a (мм)', 0.01, 0.3,
            valinit=initial_values['slit_width'] * 1e3
        ),
        'slit_separation': Slider(
            axes_positions['slit_separation'], 'd (мм)', 0.1, 1.0,
            valinit=initial_values['slit_separation'] * 1e3
        ),
        'screen_distance': Slider(
            axes_positions['screen_distance'], 'L (м)', 0.1, 5.0,
            valinit=initial_values['screen_distance']
        )
    }
    return sliders


def main():
    initial_params = {
        'wavelength': 500e-9,
        'slit_width': 0.1e-3,
        'slit_separation': 0.5e-3,
        'screen_distance': 1.0
    }

    positions = np.linspace(-0.02, 0.02, 3000)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    plt.subplots_adjust(bottom=0.3, hspace=0.4)
    status_text = fig.text(0.5, 0.94, '', ha='center', va='center', fontsize=12)

    sliders = setup_sliders(fig, initial_params)

    def on_slider_change(_):
        wl = sliders['wavelength'].val * 1e-9
        width = sliders['slit_width'].val * 1e-3
        separation = sliders['slit_separation'].val * 1e-3
        distance = sliders['screen_distance'].val

        calculate_and_plot(positions, wl, width, separation, distance, axes)

        if is_fraunhofer_regime(width, wl, distance):
            status_text.set_text("✓ Условие Фраунгофера выполнено")
            status_text.set_color("green")
        else:
            status_text.set_text("✗ Условие Фраунгофера не выполнено")
            status_text.set_color("red")

        fig.canvas.draw_idle()

    for slider in sliders.values():
        slider.on_changed(on_slider_change)

    on_slider_change(None)
    plt.show()

if __name__ == "__main__":
    main()