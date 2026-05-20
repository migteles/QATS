from pynput import keyboard, mouse


class EventLogger: # definindo a classe EventLogger

    # mapa dos comandos ctrl+ no teclado
    CTRL_CHARS = {
        '\x01': 'CTRL+A', '\x02': 'CTRL+B', '\x03': 'CTRL+C',
        '\x04': 'CTRL+D', '\x05': 'CTRL+E', '\x06': 'CTRL+F',
        '\x07': 'CTRL+G', '\x08': 'CTRL+H', '\x09': 'CTRL+I',
        '\x0a': 'CTRL+J', '\x0b': 'CTRL+K', '\x0c': 'CTRL+L',
        '\x0d': 'CTRL+M', '\x0e': 'CTRL+N', '\x0f': 'CTRL+O',
        '\x10': 'CTRL+P', '\x11': 'CTRL+Q', '\x12': 'CTRL+R',
        '\x13': 'CTRL+S', '\x14': 'CTRL+T', '\x15': 'CTRL+U',
        '\x16': 'CTRL+V', '\x17': 'CTRL+W', '\x18': 'CTRL+X',
        '\x19': 'CTRL+Y', '\x1a': 'CTRL+Z',
    }

    # lista das teclas usadas para comandos (ou modificadores/modifiers)
    MODIFIERS = {
        keyboard.Key.ctrl,
        keyboard.Key.ctrl_l,
        keyboard.Key.ctrl_r,
        keyboard.Key.shift,
        keyboard.Key.shift_l,
        keyboard.Key.shift_r,
        keyboard.Key.alt,
        keyboard.Key.alt_l,
        keyboard.Key.alt_r,
        keyboard.Key.alt_gr,
        keyboard.Key.cmd,
        keyboard.Key.cmd_l,
        keyboard.Key.cmd_r,
    }

    def __init__(self, clock, logfile): # define o inicio das variaveis

        self.clock = clock
        self.log = open(logfile, "w")

        self.keyboard_listener = None
        self.mouse_listener = None

        # detecta qual tecla de comando está sendo pressionada
        self._held_modifiers = set()

    def log_event(self, event): # definindo a função para gravar um evento

        t = self.clock.formatted()
        self.log.write(f"{t} {event}\n")

    def _modifier_prefix(self): # definindo a função para ler os prefixos
        """Builds a prefix string like 'CTRL+SHIFT+' from held modifiers."""

        prefix = ""

        # normalizando as teclas de comando diferentes para ficar todos como 1 só
        if self._held_modifiers & {keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}:
            prefix += "CTRL+"
        if self._held_modifiers & {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}:
            prefix += "SHIFT+"
        if self._held_modifiers & {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr}:
            prefix += "ALT+"
        if self._held_modifiers & {keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r}:
            prefix += "CMD+"

        return prefix

    def on_press(self, key): # definindo a função de leitura da tecla pressionada

        # detecta se a tecla esta na lista de uso para comandos
        if key in self.MODIFIERS:
            self._held_modifiers.add(key)

        if hasattr(key, 'char') and key.char is not None:

            # verifica se a tecla é a CTRL
            if key.char in self.CTRL_CHARS:
                self.log_event(f"KEY {self.CTRL_CHARS[key.char]}")

            else:
                # verifica se é apenas uma tecla normal ou alguma outra na lista de modificadores
                prefix = self._modifier_prefix()
                label = key.char.upper() if prefix else key.char
                self.log_event(f"KEY {prefix}{label}")

        else:
            # verifica se é uma tecla especial (F5, F9, etc)
            key_name = key.name.upper() if hasattr(key, 'name') else str(key)
            prefix = self._modifier_prefix()

            # caso uma tecla esteja sendo pressionada por muito tempo, não irá gravar como um comando
            if key not in self.MODIFIERS:
                self.log_event(f"KEY {prefix}{key_name}")
            else:
                self.log_event(f"KEY {key_name}")

    def on_release(self, key):

        # limpa o modificador após a tecla ser liberada
        self._held_modifiers.discard(key)

    def on_move(self, x, y): # definindo a gravação do movimento do mouse

        self.log_event(f"MOVE {x},{y}")

    def on_click(self, x, y, button, pressed): # definindo a gravação do clique do mouse

        if pressed:
            self.log_event(f"CLICK {button} {x},{y}")

    def start(self): # define o inicio das funções

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )

        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop(self): # define o fim das funções

        self.keyboard_listener.stop()
        self.mouse_listener.stop()

        self.log.close()
