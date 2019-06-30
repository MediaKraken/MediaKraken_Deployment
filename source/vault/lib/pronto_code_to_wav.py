#!/usr/bin/python

# http://www.remotecentral.com/features/irdisp2.htm

import sys
import wave


class IrSoundFile:
    def __init__(self, make, model, signal):
        self.shift = 0
        dir = make + '/' + model
        # `mkdir -p $dir`
        self.file = wave.open(dir + '/' + signal + '.wav', 'wb')
        self.data = []

    def write_data(self):
        data_str = ''.join(self.data)
        self.file.setparams((2, 2, self.base_frequency, len(data_str), 'NONE', 'noncompressed'))
        self.file.writeframes(data_str)

    def close(self):
        self.file.close()

    def add_vals(self, count, val):
        counter = 0
        half_base = self.base_frequency / 2
        while counter < count:
            if val == 1:
                ir_val = 0xFF7F
                if self.shift > (half_base):
                    ir_val = 0xFFFF - ir_val
            else:
                ir_val = 0x7FFF
            self.data.append(wave.struct.pack('>H', ir_val))  # left channel
            self.data.append(wave.struct.pack('>H', ir_val))  # right channel
            old_shift = self.shift
            self.shift += self.frequency
            if self.shift > self.base_frequency:  # I guess this is faster than %
                self.shift = self.shift - self.base_frequency
            if not ((old_shift < half_base) and (self.shift < half_base) or (
                    old_shift > half_base) and (self.shift > half_base)):
                counter += 1

    def add_pairs(self, ones, zeros):
        self.add_vals(int(ones, 16), 1)
        self.add_vals(int(zeros, 16), 0)
        sys.stdout.write("%s %s | " % (ones, zeros))

    def write_ir_code(self, str):
        self.base_frequency = 44100  # the freq of the wav file
        frequencies = {'006d': 38200 / 2}  # IR freq / 2 (b/c we're using 2 of those)
        codes = str.split(' ')
        (self.frequency, sequence_1_len, sequence_2_len) = (
        frequencies[codes[1]], int(codes[2], 16), int(codes[3], 16))
        print
        "S1L:%d S2L:%d FRQ:%d BFRQ:%d" % (
        sequence_1_len, sequence_2_len, self.frequency, self.base_frequency)
        print
        "Writing sequence 1 240 times"
        for j in range(1, 4):
            for i in range(1, sequence_1_len + 1):
                self.add_pairs(codes[i * 2 + 2], codes[i * 2 + 1 + 2])
        print
        "\nWriting sequence 2 one time"
        for j in range(1, 1):
            for i in range(1, sequence_2_len + 1):
                self.add_pairs(codes[i * 2 + 2 + sequence_1_len],
                               codes[i * 2 + 1 + 2 + sequence_1_len])
        self.write_data()
