import cmd
from lil_vi_bot.lil_vi import LilVi
import shlex


class LilViShell(cmd.Cmd):
    intro = "Welcome to the LilVi Admin Console.  Type help or ? to list commands.\n"
    prompt = "V$ "

    def __init__(self, vi_client: LilVi):
        self.vi_client = vi_client
        super().__init__()

    def do_echo(self, arg):
        """Send a message to a given channel id:  echo 1234567 'OwO whats this?'"""
        self.vi_client.send_to_channel_id(*shlex.split(arg))

    def do_ping(self, arg):
        """Return the current latency:  ping"""
        print(f"{self.vi_client.latency * 10 ** -9} ns")

    def do_logout(self, arg):
        """Log out Lil Vi and exit the program:  logout"""
        self.logout()
        return True

    def logout(self):
        self.vi_client.logout()
