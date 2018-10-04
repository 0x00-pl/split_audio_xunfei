import json


def load_slices(log_json, dst_path):


    return {
        'beg': slice_beg,
        'end': slice_end,
        'dst_name': dst_name
    }


def load_audio(file_name):
    return []


def export_audio(audio, file_name, format='wav'):
    audio.export(file_name, format=format)


def slice_audio(audio, slices, cb):
    for slice_item in slices:
        audio_slice = audio[slice_item["beg"] : slice_item["end"]]
        cb(audio_slice, slice_item["dst_name"])


def main(json_file, src_audio, dst_path):
    slices = load_slices(json.load(open(json_file)), dst_path)
    audio = load_audio(src_audio)
    slice_audio(audio, slices, export_audio)
