from IPython import start_ipython
from utils import _luck_logo
from embellish import Color
import os
from IPython.terminal.prompts import Prompts, Token


def update_ipython_session(session):
    # type: (Dict[str, Any]) -> None
    """Updates IPython session with a custom one"""
    try:
        from IPython import get_ipython
        get_ipython().user_ns.update(session)
    except Exception:
        pass


class MyPrompt(Prompts):

    def in_prompt_tokens(self, cli=None):
        return [(Token, os.getcwd()), (Token.Prompt, ' >>>')]


if __name__ == '__main__':
    MAIN_COLOR = Color()

    luck_log = _luck_logo()
    for line in luck_log:
        print(line)
    MAIN_COLOR.init()
    # gain ipython's instance
    scope_vars = {'MAIN_COLOR': MAIN_COLOR}
    try:
        import IPython
    except ImportError:
        from code import InteractiveConsole

        InteractiveConsole(locals=scope_vars).interact()
    else:
        start_ipython()
