# nozzle_wipe.py
#
# Simple nozzle wipe extension for Klipper

import logging

class NozzleWipe:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')

        # Register custom GCODE command
        self.gcode.register_command("NOZZLE_WIPE", self.cmd_NOZZLE_WIPE,
                                    desc="Wipe nozzle on pad/brush")

        # Config options
        self.x_start = config.getfloat("x_start", 265.0)
        self.x_end   = config.getfloat("x_end", 300.0)
        self.y       = config.getfloat("y", 350.0)
        self.z       = config.getfloat("z", 6.0)
        self.passes  = config.getint("passes", 8)
        self.speed   = config.getfloat("speed", 300.0)

    def cmd_NOZZLE_WIPE(self, gcmd):
        # Override defaults with command parameters
        x_start = gcmd.get_float("X_START", self.x_start)
        x_end   = gcmd.get_float("X_END", self.x_end)
        y       = gcmd.get_float("Y", self.y)
        z       = gcmd.get_float("Z", self.z)
        passes  = gcmd.get_int("P", self.passes)
        speed   = gcmd.get_float("F", self.speed)

        # Do the wipe moves
        self.gcode.respond_info("Starting nozzle wipe...")
        self.gcode.run_script_from_command(f"G1 Z{z+10:.3f} F600")
        self.gcode.run_script_from_command(f"G1 X{x_start:.3f} Y{y:.3f} F600")
        self.gcode.run_script_from_command(f"G1 Z{z:.3f} F600")

        for i in range(passes):
            self.gcode.run_script_from_command(
                f"G1 X{x_start:.3f} Y{y:.3f} F{speed*60:.0f}")
            self.gcode.run_script_from_command(
                f"G1 X{x_end:.3f} Y{y:.3f} F{speed*60:.0f}")

        self.gcode.respond_info("Nozzle wipe done.")

def load_config(config):
    return NozzleWipe(config)

