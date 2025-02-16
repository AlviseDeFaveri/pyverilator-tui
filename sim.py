from ConsoleWidget.console import BaseConsoleApp, ConsoleWidget
from CustomPanel.panel import Panel

from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import Header, Footer, RichLog

import pyverilator

# Use PyVerilator to build the simulation object.
# This will:
# 1. Run verilator on the circuit
# 2. Automatically create a cpp wrapper
# 3. Compile the verilated simulation into a shared object
# 4. Load the so and build an object to interact with it
sim = pyverilator.PyVerilator.build(
    'circuit/top.sv', preceding_files='circuit/dpi.cpp')


async def next(_):
    return sim.clock.tick()

# Custom commands: the REPL widget will intercept them instead of forwarding to
# the interpreter
COMMANDS = {
    "quit": (lambda self: self.action_quit()),
    "clear": (lambda self: self.query_exactly_one(ConsoleWidget).clear()),
    "next": next,
}


class InPanel(Panel):
    """ Display all the circuit's input signals.
    """

    def update_prev(self):
        self.prev = {}
        for name, width in sim.inputs:
            self.prev[name] = str(sim[name])

    def render(self):
        out = ''
        for name, width in sim.inputs:
            # Highlight signals whose values has changed since the last time.
            if str(self.prev[name]) != str(sim[name]):
                out += f"[magenta][b]{name}[/b]: {str(sim[name])}[/magenta]\n"
            else:
                out += f"[b]{name}[/b]: {str(sim[name])}\n"

        return out


class OutPanel(Panel):
    """ Display all the circuit's input signals.
    """

    def update_prev(self):
        self.prev = {}
        for name, width in sim.outputs:
            self.prev[name] = str(sim[name])

    def render(self):
        out = ''
        for name, width in sim.outputs:
            if str(self.prev[name]) != str(sim[name]):
                # Highlight signals whose values has changed since the last time.
                out += f"[magenta][b]{name}[/b]: {str(sim[name])}[/magenta]\n"
            else:
                out += f"[b]{name}[/b]: {str(sim[name])}\n"

        return out


class SimTui(BaseConsoleApp):
    """ Extend BaseConsoleApp to have interactive REPL capabilities.
    """
    CSS_PATH = "layout.tcss"

    def __init__(self, simulation):
        # Forward the simulation object to the interpreter.
        super().__init__(init_objects={
            "sim": simulation}, custom_commands=COMMANDS)

    def compose(self) -> ComposeResult:
        self.in_panel = InPanel(id="ins", title="Inputs")
        self.out_panel = OutPanel(id="outs", title="Outputs")
        # Save the initial state of IO signals.
        self.in_panel.update_prev()
        self.out_panel.update_prev()

        yield Header()
        with Container(id="main"):
            yield self.in_panel
            yield self.out_panel
        yield self.console_panel
        yield Footer()

        self.set_focus(self.console_panel)

    async def on_console_widget_command(self, message: ConsoleWidget.Command) -> None:
        """ Executed when the user presses "enter" in the REPL.
        """
        # Execute normal REPL functions.
        super().on_console_widget_command(message)
        # Update IO state.
        self.in_panel.update_prev()
        self.out_panel.update_prev()
        # Render panels.
        self.in_panel.refresh()
        self.out_panel.refresh()


if __name__ == "__main__":
    app = SimTui(simulation=sim)
    app.run()
