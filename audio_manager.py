from pathlib import Path

from PySide6.QtCore import QUrl, QSettings
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect


class AudioManager:
    """Theme-aware audio playback. Does not interact with chess rules or Stockfish."""

    def __init__(self, root: Path, parent=None):
        self.root = Path(root)
        self.settings = QSettings("ChessStudio", "ChessStudio")

        self.music_output = QAudioOutput(parent)
        self.player = QMediaPlayer(parent)
        self.player.setAudioOutput(self.music_output)
        self.player.mediaStatusChanged.connect(self._on_media_status)

        self.effects = {}
        self.theme_dir = None
        self.audio_config = {}

        self.music_volume = float(self.settings.value("audio/music_volume", 0.30))
        self.effects_volume = float(self.settings.value("audio/effects_volume", 0.65))
        self.muted = self.settings.value("audio/muted", False, type=bool)

        self.music_output.setVolume(0.0 if self.muted else self.music_volume)

    def set_theme(self, theme_name: str, theme: dict):
        """Load a theme's optional audio section and switch its soundtrack."""
        self.theme_dir = self.root / "themes" / theme_name
        self.audio_config = theme.get("audio", {})

        self.player.stop()
        self.effects.clear()

        if not self.audio_config.get("enabled", True):
            return

        music_rel = self.audio_config.get("music")
        if music_rel:
            music_path = self.theme_dir / music_rel
            if music_path.is_file():
                self.player.setSource(QUrl.fromLocalFile(str(music_path.resolve())))
                self.player.play()

        sounds = self.audio_config.get("effects", {})
        for event_name, relative_path in sounds.items():
            sound_path = self.theme_dir / relative_path
            if not sound_path.is_file():
                continue
            effect = QSoundEffect(self.player)
            effect.setSource(QUrl.fromLocalFile(str(sound_path.resolve())))
            effect.setLoopCount(1)
            effect.setVolume(0.0 if self.muted else self.effects_volume)
            self.effects[event_name] = effect

    def _on_media_status(self, status):
        # Loop only once Qt reports that the current file has finished.
        from PySide6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()

    def play(self, event_name: str):
        effect = self.effects.get(event_name)
        if effect is not None and not self.muted:
            effect.stop()
            effect.play()

    def set_music_volume(self, value: int):
        self.music_volume = max(0, min(100, int(value))) / 100.0
        self.music_output.setVolume(0.0 if self.muted else self.music_volume)
        self.settings.setValue("audio/music_volume", self.music_volume)

    def set_effects_volume(self, value: int):
        self.effects_volume = max(0, min(100, int(value))) / 100.0
        for effect in self.effects.values():
            effect.setVolume(0.0 if self.muted else self.effects_volume)
        self.settings.setValue("audio/effects_volume", self.effects_volume)

    def set_muted(self, muted: bool):
        self.muted = bool(muted)
        self.music_output.setVolume(0.0 if self.muted else self.music_volume)
        for effect in self.effects.values():
            effect.setVolume(0.0 if self.muted else self.effects_volume)
        self.settings.setValue("audio/muted", self.muted)

    def close(self):
        self.player.stop()
        for effect in self.effects.values():
            effect.stop()
