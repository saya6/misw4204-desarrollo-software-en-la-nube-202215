from mimetypes import init
from types import LambdaType
from os import path
from pydub import AudioSegment
from project.conversion_tasks.model import ConversionTaskFormats as CTF


class ConversionEngine():
    def __init__(self):
        self.source_file_path = ""
        self.source_file_format = ""
        self.taget_file_format = ""
        self.target_file_path = ""
        self.conver_fn = LambdaType
        
    def build_source_file_path(self, source_file_path):
        self.source_file_path = source_file_path
        return self

    def build_source_file_format(self, source_file_format):
        self.source_file_format = source_file_format
        return self
    
    def build_taget_file_format(self, taget_file_format):
        self.taget_file_format = taget_file_format
        return self

    def build_target_file_path(self, target_file_path):
        self.target_file_path = target_file_path
        return self

    def build(self):
        if self.source_file_format == CTF.MP3:
            if self.taget_file_format == CTF.WAV:
                self.conver_fn = self.mp3_to_wav
                return
            if self.taget_file_format == CTF.OGG:
                self.conver_fn = self.mp3_to_wma
                return
        if self.source_file_format == CTF.WAV:
            if self.taget_file_format == CTF.MP3:
                self.conver_fn = self.mp3_to_wav
                return
            if self.taget_file_format == CTF.OGG:
                self.conver_fn = self.mp3_to_wma
                return
        if self.source_file_format == CTF.OGG:
            if self.taget_file_format == CTF.MP3:
                self.conver_fn = self.mp3_to_wav
                return
            if self.taget_file_format == CTF.WAV:
                self.conver_fn = self.mp3_to_wma
                return
        print("UNSOPORTED TYPE: {}\n".format(self.source_file_format))
        raise("source or target file format not supported ")

    def mp3_to_wav(self):
        sound = AudioSegment.from_mp3(self.source_file_path)
        sound.export(self.target_file_path, format="wav")

    def mp3_to_wma(self):
        sound = AudioSegment.from_mp3(self.source_file_path)
        sound.export(self.target_file_path, format="ogg")

    def wav_to_mp3(self):
        sound = AudioSegment.from_wav(self.source_file_path)
        sound.export(self.target_file_path, format="mp3")

    def wav_to_wma(self):
        sound = AudioSegment.from_wav(self.source_file_path)
        sound.export(self.target_file_path, format="wma")

    def wma_to_mp3(self):
        sound = AudioSegment.from_file(self.source_file_path, "wma")
        sound.export(self.target_file_path, format="mp3")

    def wma_to_wav(self):
        sound = AudioSegment.from_file(self.source_file_path, "wma")
        sound.export(self.target_file_path, format="wav")

    def convert(self):
        try:
            self.conver_fn()
            return True
        except:
            # TODO: log the error here
            return False