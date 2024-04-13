import mclang.syntax.PrcParser as prc
import mclang.parser as pr
from mclang.namespace import Namespace
import mido


class MidiParser:
    def __init__(self, file_name):
        self.midi = None
        self.actions_raw = None
        self.file_name = file_name

    def parse(self):
        self.actions_raw = []
        self.midi = mido.MidiFile(self.file_name)
        tempo = 400000

        for message in self.midi.merged_track:
            time_multiplier = tempo / 400000
            time = round(message.time * time_multiplier)

            if message.type == "set_tempo":
                tempo = message.tempo
            elif message.type == "note_on":
                note = message.note
                velocity = message.velocity
                self.actions_raw.append((note, velocity, time))
            elif message.type == "note_off":
                note = message.note
                velocity = 0
                self.actions_raw.append((note, velocity, time))

        return self.actions_raw

    def parse_time_abs(self):
        data_raw = self.parse()
        cur_time = 0
        data = []
        for i in data_raw:
            cur_time += i[2]
            data.append((i[0], i[1], cur_time))
        return data

    def parse_only_start(self):
        data_raw = self.parse_time_abs()
        data = []
        for i in data_raw:
            if i[1] == 0:
                continue
            data.append(i)
        return data

    def parse_chords(self):
        data_raw = self.parse_only_start()
        data = [[]]
        timing = [0]
        current_time = data_raw[0][2]

        for i in data_raw:
            note, velocity, time = i
            timing[-1] = time
            if current_time == time:
                data[-1].append(note)
            else:
                timing.append(time)
                data.append([note])
                current_time = time

        timing.insert(0, data_raw[0][2])
        return data, timing


def figs(s):
    return "{" + s + "}"


def is_black(note):
    form = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    form = ["#" in x for x in form]
    return form[note % 12]


class Parser(prc.PrcParser):
    def __init__(self):
        self.varname = None
        self.midi = None
        self.midi_path = None

    def getName(self):
        return "midi"

    def parse(self, block, meta, base=None, data=None):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        varname, path = [x.strip() for x in block.split("=")]
        self.midi_path = eval(path)
        self.varname = varname

        ns.setValue(varname, "midi")
        ns.getValue(varname)["pointer"] = self

        self.midi = MidiParser(self.midi_path)

        val_iP = f"{varname}_iP"
        val_Pos = f"{varname}_Pos"
        val_iP_raw = ns.setValue(val_iP, "scoreboard", meta="dummy")['value']
        val_Pos_raw = ns.setValue(val_Pos, "scoreboard", meta="dummy")['value']

        code = [
            f"{val_iP} = 0",
            f"{val_Pos} = 0",
            f"func {varname}_play() -> @a",
        ]
        midi = self.midi.parse_only_start()[:50]
        time = midi[-1][2] // 60
        code.extend([
            f"    {val_Pos} = {val_Pos} + 1",
            f"    if {val_Pos} > {time}",
            f"        {val_iP} = 0",
            f"        {val_Pos} = 0",
            f"        return",
        ]
        )
        for action in midi:
            note = action[0]
            velocity = round(1 + action[1] / 127, 3)
            time = action[2] // 60
            code.append(
                f"    mod at @s if score @s {val_Pos_raw} matches {time}"
            )
            code.append(
                f"        execute execute run playsound custom:audnote_{note} ambient @s ~ ~ ~ {velocity}"
            )

            y = 0.75
            x = (10 * (1 - (note / 127)) - 5)
            z = 1.5
            color = (18000000, 18000000, 18000000)
            if is_black(note):
                color = (0, 0, 0)
            code.append(
                f"        execute execute run particle minecraft:dust {color[0]} {color[1]} {color[2]} 0.7 ~{x} ~{y} ~{z} 0 0 0.1 0 20 force @s"
            )

        code.extend([
            f"observe {varname}_play -> @a",
            f"    if score @s {val_iP_raw} matches 1",
        ]
        )

        code = "\n".join(code)
        res = parser.parse_prcs(code)
        return res

    def start(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = f"{self.varname}_iP = 1"
        return parser.parse_prcs(cmd)

    def pause(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = f"{self.varname}_iP = -1"
        return parser.parse_prcs(cmd)

    def stop(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = (f"{self.varname}_iP = 0\n"
               f"{self.varname}_Pos = -1\n")

        return parser.parse_prcs(cmd)

    def set_time(self, args, meta):
        nmeta = meta["NMETA"]
        ns: Namespace = meta["NMETA"].getNamespace()
        parser: pr.CodeParser = meta["PARSER"]

        cmd = f"{self.varname}_Pos = {args[0]}"
        return parser.parse_prcs(cmd)
