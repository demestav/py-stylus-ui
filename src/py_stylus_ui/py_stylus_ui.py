import configparser
import os
import subprocess
import tkinter as tk
from pathlib import Path


def config_path() -> Path:
    """Provide the configuration path."""
    env_directory = os.environ.get("XDG_CONFIG_HOME") or os.environ.get("APPDATA")

    if env_directory:
        directory = Path(env_directory)
    else:
        directory = Path.home() / ".config"

    return directory / "py-stylus-ui"


def write_settings(config: configparser.ConfigParser) -> None:
    """Write settings to configuration storage."""
    config_directory = config_path()
    file_path = config_directory / "settings.ini"
    with open(file_path, "w") as f:
        config.write(f)


def read_settings() -> configparser.ConfigParser:
    """Read settings from configuration storage."""
    config_directory = config_path()
    if not config_directory.is_dir():
        config_directory.mkdir(parents=True)
    file_path = config_directory / "settings.ini"
    if not file_path.is_file():
        file_path.touch()
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


class MainApplication(tk.Frame):
    """The main window."""

    def __init__(self, parent: tk.Tk) -> None:
        """Tkinter main window."""
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.settings = read_settings()
        resize_btn = tk.Button(
            self, text="Map area to device", command=self.resize_btn_clicked, width=30
        )
        resize_btn.pack()
        aspect_btn = tk.Button(
            self,
            text="Match Device Aspect Ratio (16:10)",
            command=self.set_aspect,
            width=30,
        )
        aspect_btn.pack()
        transparent_btn = tk.Button(
            self, text="Transparent", command=self.make_transparent, width=30
        )
        transparent_btn.pack()
        result = subprocess.run(
            ["xsetwacom", "--list", "devices"], stdout=subprocess.PIPE
        )
        devices = result.stdout.decode("utf-8").split("\n")
        devices = list(map(lambda x: x.split("\t")[0].rstrip(), devices))[:-1]
        self.device_choice = tk.StringVar(self)
        self.device_choice.set(devices[0])  # default value
        devices_select = tk.OptionMenu(self, self.device_choice, *devices)
        devices_select.config(width=30)
        devices_select.pack()
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_settings()

    def load_settings(self) -> None:
        """Set the state of the widgets based on the saved settings."""
        if not self.settings.has_section("pystylusarea"):
            return

        if self.settings.has_option("pystylusarea", "geometry"):
            geometry = self.settings.get("pystylusarea", "geometry")
            if geometry:
                self.parent.geometry(geometry)

        if self.settings.has_option("pystylusarea", "device"):
            device = self.settings.get("pystylusarea", "device")
            if device:
                self.device_choice.set(device)

    def save_settings(self) -> None:
        """Save the state of the widgets to settings."""
        self.settings["pystylusarea"] = {
            "geometry": self.parent.winfo_geometry(),
            "device": self.device_choice.get(),
        }
        write_settings(self.settings)

    def on_closing(self) -> None:
        """Save settings before quitting."""
        self.save_settings()
        self.parent.destroy()

    def resize_btn_clicked(self) -> None:
        """Map device to the defined geometry."""
        geometry = self.parent.geometry()
        os.system(
            f'xsetwacom --set "{self.device_choice.get()}" MapToOutput "{geometry}"'
        )

    def set_aspect(self) -> None:
        """Resize the window to respect the defined ratio."""
        geometry = self.parent.geometry()
        dimensions, offset_x, offset_y = geometry.split("+")

        width, _height = dimensions.split("x")
        new_height = str(round(float(width) / 1.6))
        new_geometry = f"{width}x{new_height}+{offset_x}+{offset_y}"
        self.parent.geometry(new_geometry)

    def make_transparent(self) -> None:
        """Make the window transparent."""
        self.parent.wm_attributes("-alpha", 0.3)


def cli() -> None:
    """Initialize and create application window."""
    root = tk.Tk()
    root.title("pyStylusUI")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    cli()
