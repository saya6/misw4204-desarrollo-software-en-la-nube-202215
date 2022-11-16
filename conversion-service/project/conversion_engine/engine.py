from io import BytesIO, StringIO
from mimetypes import init
from types import LambdaType
from os import path
from pydub import AudioSegment
from project.conversion_tasks.model import ConversionTaskFormats as CTF
import gc


class ConversionEngine():
    def __init__(self,source_file_path, source_file_format, taget_file_format, target_file_path):
        self.source_file_path = source_file_path
        self.source_file_format = source_file_format
        self.taget_file_format = taget_file_format
        self.target_file_path = target_file_path
        self.source_file_bytes = None
        self.target_file_bytes = BytesIO()

        self.conver_fn = LambdaType

    def prepare(self):
        self.source_file_format = CTF[self.source_file_format]
        self.taget_file_format = CTF[self.taget_file_format]
        return self

    def set_source_file_bytes(self, byte_array):
        self.source_file_bytes = BytesIO(byte_array)
        return self

    def get_target_file_bytes(self):
        return self.target_file_bytes

    def build(self):
        if self.source_file_format == CTF.MP3:
            if self.taget_file_format == CTF.WAV:
                self.conver_fn = self.mp3_to_wav
                return
            if self.taget_file_format == CTF.OGG:
                self.conver_fn = self.mp3_to_ogg
                return
        if self.source_file_format == CTF.WAV:
            if self.taget_file_format == CTF.MP3:
                self.conver_fn = self.wav_to_mp3
                return
            if self.taget_file_format == CTF.OGG:
                self.conver_fn = self.wav_to_ogg
                return
        if self.source_file_format == CTF.OGG:
            if self.taget_file_format == CTF.MP3:
                self.conver_fn = self.ogg_to_mp3
                return
            if self.taget_file_format == CTF.WAV:
                self.conver_fn = self.ogg_to_wav
                return
        if self.self.source_file_bytes == None:
            raise("source file is required")
        print("UNSOPORTED TYPE: {}\n".format(self.source_file_format))
        raise("source or target file format not supported ")

    def mp3_to_wav(self):
        sound = AudioSegment.from_mp3(self.source_file_bytes)
        sound.export(self.target_file_bytes, format="wav")
        

    def mp3_to_ogg(self):
        sound = AudioSegment.from_mp3(self.source_file_bytes)
        sound.export(self.target_file_bytes, format="ogg")
        del sound
        del self.source_file_bytes
        gc.collect()

    def wav_to_mp3(self):
        sound = AudioSegment.from_wav(self.source_file_bytes)
        sound.export(self.target_file_bytes, format="mp3")
        del sound
        del self.source_file_bytes
        gc.collect()

    def wav_to_ogg(self):
        sound = AudioSegment.from_wav(self.source_file_bytes)
        sound.export(self.target_file_bytes, format="ogg")
        del sound
        del self.source_file_bytes
        gc.collect()

    def ogg_to_mp3(self):
        sound = AudioSegment.from_file(self.source_file_bytes, "ogg")
        sound.export(self.target_file_bytes, format="mp3")
        del sound
        del self.source_file_bytes
        gc.collect()

    def ogg_to_wav(self):
        sound = AudioSegment.from_file(self.source_file_bytes, "ogg")
        sound.export(self.target_file_bytes, format="wav")
        del sound
        del self.source_file_bytes
        gc.collect()

    def convert(self):
        self.conver_fn()
