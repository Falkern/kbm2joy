# Kbm2Joy

This project provides a simple GUI application to convert mouse movements into joystick inputs using a virtual Xbox 360 gamepad. It is built using Python and leverages the `pyautogui` and `vgamepad` libraries for mouse and gamepad interactions, respectively.

## Disclaimer

Use this project at your own risk. The authors are not responsible for any damage or issues that may arise from using this software. It is not guaranteed to be undetectable by all games, so use it at your own risk.

## Features

- **Mouse to Joystick Mapping**: Converts mouse movements to joystick inputs.
- **Sensitivity Adjustment**: Allows users to adjust the sensitivity of the joystick for both X and Y axes.
- **Deadzone Configuration**: Users can set deadzone values to ignore minor mouse movements.
- **Start/Stop Emulation**: Easily start or stop the emulation with a button click.

## Requirements

- Python 3.x
- `pyautogui` library
- `vgamepad` library
- `tkinter` library (usually included with Python)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/kbm2joy.git
   cd kbm2joy
   ```

2. Install the required libraries:
   ```sh
   pip install pyautogui vgamepad
   ```

## Usage

1. Run the `main.py` script:

   ```sh
   python main.py
   ```

2. Use the GUI to adjust sensitivity and deadzone settings as needed.

3. Click the "Start Emulation" button to begin converting mouse movements to joystick inputs. Click the button again to stop the emulation.

## Code Overview

The main script initializes a virtual Xbox 360 gamepad and sets up a Tkinter GUI for user interaction. The core functionality includes:

- **apply_deadzone**: Applies deadzone to joystick values.
- **map_mouse_to_joystick**: Maps mouse movements to joystick inputs.
- **toggle_emulation**: Starts or stops the emulation.
- **update_sensitivity_x/y**: Updates sensitivity settings.
- **update_deadzone_x/y**: Updates deadzone settings.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or suggestions, please open an issue on the GitHub repository.
