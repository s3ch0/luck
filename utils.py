from __future__ import absolute_import
from typing import Union,Tuple,Optional,List
import os
from .embellish import Color
import six
import struct
from .consts import *
from random import choice
MY_COLOR = Color()


def _prepare_quote(quote, author, max_len=78):
    # type: (str, str, int) -> List[str]
    """
    This function processes a quote and returns a string that is ready
    to be used in the fancy prompt.

    """
    _quote = quote.split(' ')
    max_len -= 6
    lines = []
    cur_line = []  # type: List[str]

    def _len(line):
        # type: (List[str]) -> int
        return sum(len(elt) for elt in line) + len(line) - 1
    while _quote:
        if not cur_line or (_len(cur_line) + len(_quote[0]) - 1 <= max_len):
            cur_line.append(_quote.pop(0))
            continue
        lines.append('    | %s' % ' '.join(cur_line))
        cur_line = []
    if cur_line:
        lines.append('    | %s' % ' '.join(cur_line))
        cur_line = []
    lines.append('    | %s--  %s' % (" " * (max_len - len(author) - 5), author))
    return lines

def get_terminal_width():
    # type: () -> Optional[int]
    """Get terminal width (number of characters) if in a window.

    Notice: this will try several methods in order to
    support as many terminals and OS as possible.
    """
    # Let's first ty using the official API
    # (Python 3.3+)
    sizex = None  # type: Optional[int]
    if not six.PY2:
        import shutil
        sizex = shutil.get_terminal_size(fallback=(0, 0))[0]
        if sizex != 0:
            return sizex
    # Backups / Python 2.7
    if WINDOWS:
        from ctypes import windll, create_string_buffer  # type: ignore
        # http://code.activestate.com/recipes/440694-determine-size-of-console-window-on-windows/
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)  # noqa: E501
            sizex = right - left + 1
            # sizey = bottom - top + 1
            return sizex
        return sizex
    else:
        # We have various methods
        # COLUMNS is set on some terminals
        try:
            sizex = int(os.environ['COLUMNS'])
        except Exception:
            pass
        if sizex:
            return sizex
        # We can query TIOCGWINSZ
        try:
            import fcntl
            import termios
            s = struct.pack('HHHH', 0, 0, 0, 0)
            x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
            sizex = struct.unpack('HHHH', x)[1]
        except IOError:
            pass
        return sizex

def split_dict(your_dict: dict) -> Tuple[list,list]:
    """
    Split a dict to two list
    :param d: dict
    :param key: key to split
    :return: list
    """
    key_list = []
    value_list = []
    for key,value in your_dict.items():
        key_list.append(key)
        value_list.append(value)
    return key_list,value_list


def _luck_logo():
    QUOTES = [
    ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela"),
    ("The way to get started is to quit talking and begin doing.", "Walt Disney"),
    ("When you reach the end of your rope, tie a knot in it and hang on.", "Franklin D. Roosevelt"),
    ("Craft me if you can.", "IPv6 layer"),
    ("To craft a packet, you have to be a packet, and learn how to swim in "
     "the wires and in the waves.", "Jean-Claude Van Damme"),
    ("We are in France, we say Skappee. OK? Merci.", "Sebastien Chabal"),
    ("You are a lucky dog", "Zhou Hao Busy"),
    ("What is dead may never die!", "Python 2"),
    ("Get busy living or get busy dying.", "Stephen King"),
    ("If you want to live a happy life, tie it to a goal, not to people or things.", "Albert Einstein"),
    ("Never let the fear of striking out keep you from playing the game.", "Babe Ruth"),

]

    mini_banner = (get_terminal_width() or 84) <= 75
    the_logo = [
           "                                        ",
           "            ccLllLLlL/Yccu              ",
           "        CUyyyyCY//LL//////YCuu          ",
           "     CLuY//////YCCKC l/CkCY//clc        ",
           "   CLC///C//YkL/Yc     LULycluCul       ",
           "  LLYYYYY///Yu L/Ccc  ccC/cCl////C      ",
           " CyLkCCCCY//kLUC/CLLcULcCC///           ",
           "CKL/CYYYY////////CccLkKk/               ",
           "Cl//////////ULKKC CKu                   ",
           "LL/CcK LUk///UY/l/C          MISFORTUNE.",
           "CC CC CUCY////Ycc CCCL                  ",
           " CuLLLUUkluckccuC UUCCCLcc              ",
           " CY////////uc///uLLLCkUuKlC/            ",
           "  cuyCyuy////////////////lucCCCL        ",
           "    Y/YuY//////UC/LUUllulluCcCC//       ",
           "      CCuccuCY//YCykuukyCY//YCcC        ",
           "         LLUUukCYY//////YYCclL          ",
           "             cUCUcCcCLculLC             ",
           "                                      ",
        ]

        # Used on mini screens
    the_logo_mini = [
            "      .LLCCUUKKKKCC  ",
            "C /KLLLLLLL///LUl//LC",
            "       /ucL   lCLLl/L",
            "     ////cL   ul//CcC",
            "        KUL   cKKC(LU",
            "       CKK/   kCCCLCC",
            "   C/CKCCLL        LU",
            "    UK*KKCcCLUKKCKCAA",
            "         UUCU//KCKC  ",
        ]

    the_banner = [
            "",
            "",
            "    |",
            "    | Welcome to Luck",
            "    | Version %s" % 1.0,
            "    |",
            "    | http://zhouhaobusy.com",
            "    |",
            "    | Have fun!",
            "    |",
        ]

    if mini_banner:
        the_logo = the_logo_mini
        the_banner = [x[2:] for x in the_banner[3:-1]]
        the_banner = [""] + the_banner + [""]
        banner_text = [logo + banner for logo, banner in six.moves.zip_longest(
                (str(MY_COLOR.get(choice(['cyan'])))+line for line in the_logo),
                (str(MY_COLOR.get(choice(['green'])))+line for line in the_banner),
                fillvalue=""
            )]

    else:
        quote, author = choice(QUOTES)
        the_banner.extend(_prepare_quote(quote, author, max_len=40))
        the_banner.append("    |")
        
        banner_text = [logo + banner for logo, banner in six.moves.zip_longest(
                (str(MY_COLOR.get(choice(['green','cyan','blue','purple','yellow'])))+line for line in the_logo),
                (str(MY_COLOR.get(choice(['green'])))+line for line in the_banner),
                fillvalue=""
            )]


    return banner_text
    
    
if __name__ == '__main__':
    logo_str = _luck_logo()
    for line in logo_str:
        print(line)
    
