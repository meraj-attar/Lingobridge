"""Validated, HTTPS-only video links for lesson content. No URL fetching is performed.

The application embeds YouTube only. An empty string means remove a link;
``None`` and arbitrary external providers are not accepted as video URLs.
"""
import re
from urllib.parse import parse_qs, urlsplit
from pydantic import BaseModel, field_validator

_VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")
_YOUTUBE_HOSTS = frozenset({"youtube.com", "www.youtube.com", "m.youtube.com", "youtube-nocookie.com", "www.youtube-nocookie.com"})
_SHORT_HOSTS = frozenset({"youtu.be", "www.youtu.be"})


def validate_video_url(value):
    """Return unchanged valid URL; raise ValueError on unsupported/unsafe URL.

    Single explicit link (no embedded HTML), no credentials, custom ports,
    alternative schemes or deceptive hostnames. YouTube video ID required.
    """
    if value == "":
        return value  # Intentional clearing from lesson and video editors.
    if not isinstance(value, str) or len(value) > 2048 or value != value.strip():
        raise ValueError("Video URL must be a valid HTTPS YouTube link (or blank to remove it)")
    if any(ord(c) < 33 or ord(c) == 127 for c in value) or "\\" in value:
        raise ValueError("Video URL contains prohibited characters")
    try:
        parts = urlsplit(value)
        hostname = parts.hostname
        invalid_authority = parts.username is not None or parts.password is not None or parts.port is not None
    except ValueError as exc:
        raise ValueError("Video URL has an invalid host or port") from exc
    if (parts.scheme != "https" or invalid_authority or parts.fragment or
            not hostname or hostname not in (_YOUTUBE_HOSTS | _SHORT_HOSTS) or
            not parts.netloc.lower() == hostname or "%" in parts.netloc):
        raise ValueError("Only supported HTTPS YouTube video URLs without credentials or custom ports are allowed")
    path = parts.path
    if hostname in _SHORT_HOSTS:
        video_id = path.removeprefix("/") if path.startswith("/") else ""
    elif path == "/watch":
        query = parse_qs(parts.query, keep_blank_values=True)
        ids = query.get("v", [])
        video_id = ids[0] if len(ids) == 1 else ""
    else:
        match = re.fullmatch(r"/(?:embed|shorts|live|v)/([A-Za-z0-9_-]{11})", path)
        video_id = match.group(1) if match else ""
    if not _VIDEO_ID.fullmatch(video_id):
        raise ValueError("Video URL must contain a valid 11-character YouTube video ID")
    return value


class VideoURLInput(BaseModel):
    """Schema applied to lesson create/update video fields, also for generic editors."""
    video_url: str

    @field_validator('video_url')
    @classmethod
    def safe_url(cls, value):
        return validate_video_url(value)
