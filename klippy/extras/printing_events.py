
class PrintingEvents:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('PRINT_STARTED', self._emit_print_started, desc="Emit print started event")
        self.gcode.register_command('PRINT_COMPLETED', self._emit_print_completed, desc="Emit print completed event")
    

    def _emit_print_started(self, params):
        self.gcode.respond_info("Print started event")
        self.printer.send_event("printing:on")

    def _emit_print_completed(self, params):
        self.gcode.respond_info("Print completed event")
        self.printer.send_event("printing:off")

def load_config(config):
    return PrintingEvents(config)