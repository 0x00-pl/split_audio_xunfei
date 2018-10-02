import json


def load_slices(log_json):
    return []


def load_audio(file_name):
    return []


def export_audio(audio, file_name):
    pass


def slice_audio(audio, slices, cb):
    for slice_item in slices:
        cb(audio, slice_item["dst_name"])


def main(json_file, src_audio):
    slices = load_slices(json.load(open(json_file)))
    audio = load_audio(src_audio)
    slice_audio(audio, slices, export_audio)
