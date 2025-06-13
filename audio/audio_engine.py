import threading
import weakref

import pyo
from pyo import Server, Sine, Fader, Phasor, SfPlayer, TableRead, SndTable
from pyo.lib import generators, filters

from audio.sound_bank import SoundBank


class AudioEngine:
    _instance = None

    def __init__(self):
        if AudioEngine._instance is not None:
            raise RuntimeError("Use AudioEngine.get_instance() instead of creating directly.")
        
        self.server = Server().boot()
        self.server.start()

        # Strong references to prevent GC
        self._active = []
        
        # Load all sound files into memory
        self.sound_tables = {}
        for sound in SoundBank:
            try:
                self.sound_tables[sound] = SndTable(sound.value)
            except:
                print(f"Failed to load sound: {sound.name} from {sound.value}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = AudioEngine()
        return cls._instance

    def get_sound(self, sound_bank_item: SoundBank) -> SndTable:
        """Get a loaded sound table by its SoundBank enum."""
        return self.sound_tables.get(sound_bank_item)

    def _track(self, obj, dur=None):
        self._active.append(obj)

        if dur:
            def _stop_and_release():
                import time
                time.sleep(dur)
                obj.stop()
                try:
                    self._active.remove(obj)
                except ValueError:
                    pass  # Already removed or not found

            threading.Thread(target=_stop_and_release, daemon=True).start()

    def play_sine(self, freq=440, amp=0.1, dur=None):
        osc = Sine(freq=freq, mul=amp).out()
        self._track(osc, dur)
        return osc

    def play_sound(self, sound: SoundBank, volume=1.0, loop=False, duration=None, pitch_shift=1.0):
        """
        Play a sound file from the SoundBank.
        
        Args:
            sound: SoundBank enum value for the sound to play
            volume: Volume multiplier (0.0 to 1.0)
            loop: Whether to loop the sound
        
        """
        table = self.get_sound(sound)
        if table is None:
            print(f"Sound not found: {sound.name}")
            return

        player = TableRead(table=table, freq=table.getRate() * pitch_shift, loop=loop, mul=volume).out()

        if not duration:
            duration = table.getSize() / table.getRate()
        
        self._track(player, duration)

    def play_chord(self, base_freq=440, amp=0.1, spread=0.1, dur=1.0):
        """
        Play a broken chord (arpeggio) with three notes that fade in and out smoothly,
        plus a continuous bass note two octaves lower and some filtered noise for texture.
        Notes are spread across the stereo field.

        Args:
            base_freq: Base frequency for the chord (default 440Hz/A4)
            amp: Amplitude for each note (default 0.1)
            spread: Time between notes in seconds (default 0.1)
            dur: Total duration for each note (default 1.0)
        """
        from pyo import Noise, ButBP, Pan  # Add Pan for stereo

        # Create frequencies for a major chord (1, 5/4, 3/2)
        freqs = [base_freq, base_freq * 7/4, base_freq * 11/4]

        # Calculate total duration and create master fade envelope
        total_dur = dur + (len(freqs) - 1) * spread
        master_fade = Fader(fadein=0.1, fadeout=0.7, dur=total_dur).play()

        # Add bass note (2 octaves lower) - centered
        bass_fader = Fader(fadein=0.01, fadeout=0.1, dur=total_dur).play()
        bass = Sine(freq=base_freq/4, mul=bass_fader * master_fade * amp * 0.8)
        bass_pan = Pan(bass).out()  # Center the bass

        # Add filtered noise for each note that follows the frequency
        noise = Noise(mul=amp * 0.5)  # Create noise source

        def play_delayed_note(f, pan_pos):
            # Each note gets a sine wave with its own short fade for articulation
            fader = Fader(fadein=0.01, fadeout=0.1, dur=dur).play()

            # Create the main tone
            osc = generators.SuperSaw(freq=f, mul=fader * master_fade * amp)
            osc_pan = Pan(osc, pan=pan_pos).out()

            # Add bandpass filtered noise around the note frequency
            noise_filter = filters.Phaser(noise, freq=100000, q=1, mul=fader * master_fade * 0.1)
            noise_pan = Pan(noise_filter, pan=pan_pos).out()

            self._track(osc, dur)
            self._track(osc_pan, dur)
            self._track(noise_filter, dur)
            self._track(noise_pan, dur)
            self._track(fader, dur)

        # Pan positions for the three notes: left, center, right
        pan_positions = [-0.7, 0, 0.7]

        for i, freq in enumerate(freqs):
            # Start each note after a delay
            if i == 0:
                play_delayed_note(freq, pan_positions[i])
            else:
                def delayed_note(f, pos, delay):
                    time.sleep(delay)
                    play_delayed_note(f, pos)
                threading.Thread(target=delayed_note, args=(freq, pan_positions[i], i * spread), daemon=True).start()

        # Track our continuous elements
        self._track(bass, total_dur)
        self._track(bass_pan, total_dur)
        self._track(bass_fader, total_dur)
        self._track(noise, total_dur)
        self._track(master_fade, total_dur)

        return total_dur  # Return total duration of the chord



if __name__ == "__main__":
    import time
    # Example usage
    audio_engine = AudioEngine.get_instance()
    # audio_engine.play_chord(base_freq=440, amp=0.3, spread=0.1, dur=2.0)
    audio_engine.play_bling(dur=0.5)
    time.sleep(2.5)
