import os
from discord import FFmpegPCMAudio

class LoopingAudioSource(FFmpegPCMAudio):
    def __init__(self, source, *args, **kwargs):
        self.source = source
        super().__init__(source, *args, **kwargs)

    def read(self):
        data = super().read()
        if not data:
            os.lseek(self.process.stdout.fileno(), 0, os.SEEK_SET)
            data = super().read()
        return data