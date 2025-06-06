from typing import Any, Generator
from highlight import *
from more_itertools import peekable
import re
import shutil
import zipfile


def post_process(code: str, minify=False, max_width=4090, purgeLogs=False, replaceQuotes=False):
    if purgeLogs:
        code = re.sub(r'\s*global\.rmml\.log\(.+\)', '', code)

    if minify:
        code = untokenize(strip_whitespace(tokenise_meow(code)), max_width)

    if replaceQuotes:
        code = re.sub(
            r"'.'", lambda match: f'ord("{match.group(0)[1]}")', code
        )
        if "'" in code:
            raise SyntaxError("Code contains unclosed single quotes", code)

    return code


def strip_whitespace(
    tokens: Generator[
        tuple[Whitespace, str]
        | tuple[Comment, str]
        | tuple[
            Keyword | Value | TypeName | FunctionName | Variable,
            str,
        ]
        | tuple[Variable, str]
        | tuple[Value, str]
        | tuple[Value | Other, str]
        | tuple[Other, str],
        Any,
        None,
    ],
):
    invalidTerminators = set([Value, Keyword, Variable, FunctionName])
    peek_tokens = peekable(tokens)

    last = None
    while peek_tokens.peek(None) != None:
        [token, label] = next(peek_tokens)
        peeked = peek_tokens.peek(None)
        if peeked != None:
            peeked = type(peeked[0])

        # comments are always ignored
        if type(token) == Comment:
            continue
        # strip whitespace
        if type(token) == Whitespace:
            # `x=3 he=3`
            if last in invalidTerminators and peeked in invalidTerminators:
                yield Whitespace(), ' '
            continue

        last = type(token)

        yield token, label


def untokenize(
    tokens: Generator[
        tuple[Whitespace, str]
        | tuple[Comment, str]
        | tuple[
            Keyword | Value | TypeName | FunctionName | Variable,
            str,
        ]
        | tuple[Variable, str]
        | tuple[Value, str]
        | tuple[Value | Other, str]
        | tuple[Other, str],
        Any,
        None,
    ],
    limit,
):
    concat = ''
    accLen = 0

    for [kind, value] in tokens:
        accLen += len(value)
        if accLen < limit:
            # this segment doesn't put us over, keep going
            concat += value
        else:
            # this segment puts us over the limit, add line break
            if len(value) > limit:
                raise Exception("Limit too small", kind, value)
            concat += "\n" + value
            accLen = len(value)

    return concat


# def buildHeader(mod_name):
#     header = """[object_list]
# controller=enabled
# [controller_events]
# create='if!global.R{B=buffer_load("mods/"""
#     # mod name
#     header += mod_name
#     header += "\")global.__catspeak__.compile(global.__catspeak__.parse(B,"
#     # length, 191 is length of static header elements
#     header += str(len(mod_name) + 191)
#     header += "))()buffer_delete(B)}global.R()'\n"
#     return header


if __name__ == "__main__":
    with open("src/init.meow") as f:
        create = post_process(f.read(), minify=True, purgeLogs=True, replaceQuotes=True)
        pass

    with open("build/rmml.ini", 'w') as f:
        f.writelines(
            [
                "[object_list]\n",
                "controller=enabled\n",
                "basic=enabled\n",
                "[controller_events]\n",
                f"create='{create}'\n",
                "[basic_events]\n",
                "create='if self.mod_name==undefined{self.mod_name=global.rmml_current_mod}'"
            ]
        )

    with open("build/meta_info.ini", 'w') as f:
        f.writelines(
            [
                "[general]\n",
                "mod_enabled=1\n",
                "[meta_info]\n",
                "mod_0=rmml.ini\n",
            ]
        )
    
    with open("src/rmmm.md") as f:
        raw = f.read()
        rmmm_version = raw.splitlines()[4][22:].replace('.', '')

    with open("src/rmml.meow") as f:
        raw = f.read()
        rmml_version = raw.splitlines()[15][11:-1].replace('.', '')
        rmml_src = post_process(raw, purgeLogs=True)

    with open("build/rmml.meow", 'w') as f:
        f.write(rmml_src)

    with open("build/modlist.txt", 'w') as f:
        f.writelines(
            [
                "# put your mods here (or disable them with #)\n",
                "# mods are loaded (and run) in the order written here\n",
                "rmmm.md\n"
            ]
        )
    
    # shutil.copyfile("build/rmml.ini", "D:\\SteamLibrary\\steamapps\\common\\Mose\\mods\\rmml.ini")
    # shutil.copyfile("build/rmml.meow", "D:\\SteamLibrary\\steamapps\\common\\Mose\\mods\\rmml\\rmml.meow")

    # package rmml
    with zipfile.ZipFile(
        f'dist/rmml_{rmml_version}_{rmmm_version}.zip', 'w', zipfile.ZIP_DEFLATED
    ) as package:
        package.write("build/meta_info.ini", "meta_info.ini")
        package.write("build/modlist.txt", "modlist.txt")
        package.write("build/rmml.ini", "rmml.ini")

        package.write("src/rmmm.md", "rmml/rmmm.md")
        package.write("build/rmml.meow", "rmml/rmml.meow")
    
    # package rmml and rmmm
    shutil.copyfile("build/rmml.meow", "dist/rmml.meow")
    shutil.copyfile("src/rmmm.md", "dist/rmmm.md")
