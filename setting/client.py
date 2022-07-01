import os
from typing import Callable, Iterable
import discord
dir_name, name_file = os.path.split(__file__)


def import_file(path_to_module):
    try:
        import os
        import importlib
        module_dir, module_file = os.path.split(path_to_module)
        module_name, module_ext = os.path.splitext(module_file)
        save_cwd = os.getcwd()
        os.chdir(module_dir)
        module_obj = __import__(module_name)
        module_obj.__file__ = path_to_module
        os.chdir(save_cwd)
    except Exception as e:
        raise e
    return module_obj


class Client(discord.Client):

    def __init__(self):
        super().__init__()
        self.PREFIX = '!'
        self.commands = {}

    def setup(self):
        """
        Import all commands and events
        """
        self._setup_event()
        self._setup_commands()

    def _setup_event(self):
        path = os.path.join(dir_name, "../events")
        for file_name in os.listdir(path):
            if file_name.startswith("__"):
                continue
            mod_name = file_name.split(".py")[0]
            mod_path = f"{path}.{file_name}"
            mod = import_file(mod_path)
            mod = mod.__getattribute__(mod_name)
            setattr(self, mod_name, mod.__getattribute__(mod_name))

    def _setup_commands(self):
        path = os.path.join(dir_name, "../commands")
        for file_name in os.listdir(path):
            if file_name.startswith("__"):
                continue
            mod_name = file_name.split(".py")[0]
            mod_path = f"{path}.{mod_name}"
            mod = import_file(mod_path)
            mod = mod.__getattribute__(mod_name)
            aliases = {mod_name}
            try:
                aliases.update(mod.__getattribute__("alias"))
            except AttributeError:
                pass
            self.add_command(aliases, mod.__getattribute__(mod_name))

    def add_command(self, alias: Iterable[str], command: Callable):
        """
        add a function to all aliases.

        This function is call when a message started with the alias is sent on a discord textual channel
        :param alias: List[str], list of command, callable with a discord.Message (Without PREFIX)
        :param command: Callable, function to call when the alias is sent in a message.
        """
        for name in alias:
            if name in self.commands:
                raise ValueError(f"Command {name} already exists")
            self.commands[name] = command

    def dispatch(self, event, *args, **kwargs):
        method = 'on_' + event

        listeners = self._listeners.get(event)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as exc:
                    future.set_exception(exc)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)

            if len(removed) == len(listeners):
                self._listeners.pop(event)
            else:
                for idx in reversed(removed):
                    del listeners[idx]

        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._schedule_event(coro, method, *[self, *args], **kwargs)
