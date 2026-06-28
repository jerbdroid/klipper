
class ExhaustControl:
    def __init__(self, config):
        self.fan_name = config.get('fan', None)
        self.heater_name = config.get('heater', None)
        self.active_while_priting = config.getboolean('active_while_printing', False)
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.fan = None

        self.printer.register_event_handler("heaters:hot", self._handle_heaters_warm_state)
        self.printer.register_event_handler("heaters:cool", self._handle_heater_cool_state)
        self.printer.register_event_handler("printing:on", self._handle_printing_on)
        self.printer.register_event_handler("printing:off", self._handle_printing_off)

        self.warm = False
        self.printing = False
        

    def _update_fan_state(self):
        # Ensure we have a valid fan object
        if self.fan is None:
            for _, obj in self.printer.lookup_objects("fan_generic"):
                if obj.fan_name == self.fan_name:
                    self.fan = obj
                    break

        if self.fan is None:
            self.gcode.respond_info(f"Fan '{self.fan_name}' not found")
            return

        # Determine whether fan should be ON
        should_turn_on = (
            self.warm and (
                (self.active_while_priting and self.printing) or
                (not self.active_while_priting and not self.printing)
            )
        )

        # Apply state
        if should_turn_on:
            self.gcode.respond_info("Turning fan ON")
            self.fan.fan.set_speed(1.0)
        else:
            self.gcode.respond_info("Turning fan OFF")
            self.fan.fan.set_speed(0.0)
        
    def _handle_heaters_warm_state(self, heater_name):
        self.gcode.respond_info("Received warm event")
        if self.heater_name and heater_name == self.heater_name:
            self.warm = True
            self._update_fan_state()

    def _handle_heater_cool_state(self, heater_name):
        self.gcode.respond_info("Received cool event")
        if self.heater_name and heater_name == self.heater_name:
            self.warm = False
            self._update_fan_state()
    
    def _handle_printing_on(self):
        self.gcode.respond_info("Received printing on event")
        self.printing = True
        self._update_fan_state()
    
    def _handle_printing_off(self):
        self.gcode.respond_info("Received printing off event")
        self.printing = False
        self._update_fan_state()
    
def load_config_prefix(config):
    return ExhaustControl(config)