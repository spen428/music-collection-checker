from . import BaseChecker


class MissingMetadataChecker(BaseChecker):
    def __init__(self, work_dir: str):
        super().__init__('Missing metadata', work_dir)

    required_tags = [
        "MusicBrainz Release Id",
        "MusicBrainz Recording Id",
        "MusicBrainz Track Id",
        "contentgroup",
        "Grouping",
        "Date",
        "ReplayGain Album Gain",
        "ReplayGain Album Peak",
        "ReplayGain Track Gain",
        "ReplayGain Track Peak",
    ]

    def _check(self, current_path: str, dirs: list, files: list, depth: int):
        raise NotImplementedError
