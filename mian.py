import json
import os

import pydub


def load_slices(log_json, dst_path):
    if log_json['ok'] == -1:
        return []

    data_list = json.loads(log_json['data'])
    for item, idx in zip(data_list, range(len(data_list))):
        slice_beg = int(item['bg'])
        slice_end = int(item['ed'])
        dst_name = os.path.join(dst_path, str(idx) + '.wav')
        yield {
            'beg': slice_beg,
            'end': slice_end,
            'dst_name': dst_name,
            'info': item
        }


def load_audio(file_name):
    return pydub.AudioSegment.from_file(file_name)


def export_audio(audio, file_name, info, format='wav'):
    file_dir = os.path.dirname(file_name)
    os.makedirs(file_dir, exist_ok=True)
    audio.export(file_name, format=format)
    json.dump(info, open(file_name + '.json', 'w'), ensure_ascii=True)


def slice_audio(audio, slices, cb):
    for slice_item in slices:
        audio_slice = audio[slice_item["beg"]: slice_item["end"]]
        cb(audio_slice, slice_item["dst_name"], slice_item['info'])


def process_file(json_file, src_audio, dst_path):
    slices = load_slices(json.load(open(json_file)), dst_path)
    audio = load_audio(src_audio)
    slice_audio(audio, slices, export_audio)


def process_path(json_path, src_path, dst_path):
    for path_prefix, dirs, files in os.walk(json_path):
        for file_name in files:
            print('[info]', file_name)
            rel_file_name = os.path.relpath(os.path.join(path_prefix, file_name), json_path)
            json_file_name = os.path.join(json_path, rel_file_name)
            src_file_name = os.path.join(src_path, rel_file_name)[:-len('.log')]
            dst_file_name = os.path.join(dst_path, rel_file_name)[:-len('.log')]
            if os.path.exists(src_file_name):
                process_file(json_file_name, src_file_name, dst_file_name)


def main(json_path, src_path, dst_path):
    process_path(json_path, src_path, dst_path)


if __name__ == '__main__':
    main('test/json', 'test/mp3/', 'test/dst/')
