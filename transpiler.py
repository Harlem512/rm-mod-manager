from dataclasses import dataclass
import os
import csv
import argparse


# A bit of code assigned to a specific game_object and event
@dataclass(frozen=True)
class Register:
    mod: str
    game_object: str | None
    event: str | None
    code: str


# A specific mod
class Mod:
    mod_name: str
    registered: list[Register]

    def has_submods(self) -> bool:
        mod_names: set[str] = set()
        for register in self.registered:
            mod_names.add(register.mod)
        return len(mod_names) > 1

    # MARK: FROM MD
    @staticmethod
    def from_md(path: str):
        mod = Mod()

        contents = ''
        with open(path) as f:
            contents = f.read()

        basename = os.path.basename(path)
        mod.mod_name = basename.rsplit(".", 1)[0]
        mod.registered = []

        obj = None
        ev = None
        mod_override = mod.mod_name

        in_code = False
        in_comment = False

        code = []

        for line in contents.splitlines():
            if in_code:
                # closing ```
                if line.startswith('```'):
                    # add to map
                    mod.registered.append(
                        Register(
                            mod=mod_override,
                            game_object=obj,
                            event=ev,
                            code='\n'.join(code),
                        )
                    )
                    in_code = False
                    code = []
                else:
                    code.append(line)
                continue

            if in_comment:
                in_comment = not line.endswith('-->')
                continue

            if line.startswith('# '):
                parse = line[2:].split(' ')
                obj = parse[0]
                mod_override = len(parse) > 1 and parse[1] or mod.mod_name
                continue

            if line.startswith('## '):
                ev = line[3:]
                continue

            if line.startswith('```'):
                in_code = True
                continue

            if line.startswith('<!--'):
                in_comment = True
                continue

        return mod

    # MARK: TO MD
    def to_md(self, path: str):
        lines: list[str] = []

        game_start: str | None = None
        # { [(nod,object)]: (event,code) }
        grouped: dict[tuple[str, str | None], list[tuple[str | None, str]]] = {}

        for register in self.registered:
            if register.game_object == None and register.event == None:
                if game_start:
                    raise Exception(
                        f"Multiple game start functions are not supported for .md mods"
                    )
                game_start = register.code
                continue

            key = (register.mod, register.game_object)
            if not key in grouped:
                grouped[key] = []

            grouped[key].append((register.event, register.code))

        has_submods = self.has_submods()

        if game_start:
            lines.append(f'```sp')
            lines.append(game_start)
            lines.append(f'```\n')

        for (mod, obj), events in grouped.items():
            lines.append(
                f'# {obj}\n'
                if mod == None or not has_submods
                else f'# {obj} {mod}\n'
            )

            for event, code in events:
                lines.append(f'## {event}\n')
                lines.append(f'```sp')
                lines.append(code)
                lines.append(f'```\n')

        with open(path, 'w') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

    # MARK: FROM CSV
    @staticmethod
    def from_csv(path: str) -> Mod:
        mod = Mod()
        mod.mod_name = path
        mod.registered = []

        with open(os.path.join(path, "index.csv"), newline="") as f:
            spamreader = csv.reader(f, delimiter=',')
            for row in spamreader:
                if len(row) < 3:
                    raise Exception("CSV bad format")

                obj, event, code_path = row
                submod = row[3] if len(row) >= 4 else path

                code = ''
                with open(os.path.join(path, code_path), 'r') as code_f:
                    code = code_f.read()

                mod.registered.append(
                    Register(
                        game_object=obj or None,
                        event=event or None,
                        code=code,
                        mod=submod,
                    )
                )

        return mod

    # MARK: TO CSV
    def to_csv(self, path: str):
        os.makedirs(path, exist_ok=True)

        index: list[tuple[str, str, str, str | None]] = []
        has_submods = self.has_submods()

        for register in self.registered:
            base_path = (
                f'init.meow'
                if register.game_object == None and register.event == None
                else f'{register.game_object}_{register.event}.meow'
            )
            meow_path = (
                f'{register.mod}_{base_path}' if has_submods else base_path
            )

            index.append(
                (
                    register.game_object or '',
                    register.event or '',
                    meow_path,
                    register.mod if has_submods else None,
                )
            )

            with open(os.path.join(path, meow_path), 'w') as f:
                f.write(register.code)

        with open(os.path.join(path, "index.csv"), 'w') as f:
            for obj, event, path, submod in index:
                f.write(f'{obj},{event},{path}')
                if submod != None:
                    f.write(f',{submod}\n')
                else:
                    f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="rm_transpiler",
        description="Converts .md, index.csv, and .ini mods to each other",
        epilog="begging and pleading for the froy plush",
    )

    parser.add_argument(
        'source',
        help='Input file/directory. Please include its file extension <3',
    )
    parser.add_argument(
        'output',
        help="Output file/directory. Please include its file extension <3",
    )
    parser.add_argument(
        '-f',
        '--format',
        help='Output format override.',
        choices=['md', 'csv', 'ini'],
    )

    args = parser.parse_args()

    source: str = args.source
    output: str = args.output
    output_format: str = args.format
    input_format: str = ''

    if not output_format:
        if output.endswith(".md"):
            output_format = "md"
        elif output.endswith(".ini"):
            output_format = "ini"
        else:
            output_format = "csv"

    if source.endswith(".md"):
        input_format = "md"
    elif source.endswith(".ini"):
        input_format = 'ini'
    else:
        input_format = 'csv'
        source = source.rsplit("index.csv", 1)[0]

    mod: Mod
    if input_format == 'md':
        mod = Mod.from_md(source)
    elif input_format == 'ini':
        raise Exception("Invalid")
    elif input_format == 'csv':
        mod = Mod.from_csv(source)
    else:
        raise Exception("Invalid")

    if output_format == 'md':
        mod.to_md(output)
    elif output_format == 'ini':
        raise Exception("Invalid")
    elif output_format == 'csv':
        mod.to_csv(output)
    else:
        raise Exception("Invalid")
