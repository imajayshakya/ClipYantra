"""
Rendering Tasks for ClipYantra.

Handles video composition, caption rendering, export, and clip creation.

Related Requirements: RND-001, RND-002, RND-003
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict

from celery import shared_task

from app.config import settings
from app.processors.ffmpeg_processor import FFmpegProcessor
from app.processors.base import RenderResult, RenderPreset


@dataclass
class RenderingTaskResult:
    """Result of rendering task."""
    success: bool
    job_id: Optional[str] = None
    output_path: Optional[str] = None
    render_result: Optional[RenderResult] = None
    error: Optional[str] = None


@shared_task(
    bind=True,
    name="app.tasks.rendering.compose_video",
    queue="rendering",
    max_retries=2,
    default_retry_delay=120,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=600,
)
def compose_video(
    self,
    job_id: str,
    timeline_json: str,
    preset_name: Optional[str] = None,
    output_format: str = "mp4",
) -> Dict[str, Any]:
    """
    Compose video from timeline specification.
    
    Timeline includes:
    - Video tracks with clips, transitions, effects
    - Audio tracks with music, voiceover, sound effects
    - Text/caption tracks with styling and animation
    - B-roll overlays
    
    Args:
        job_id: Unique render job identifier
        timeline_json: JSON string of timeline specification
        preset_name: Render preset to use
        output_format: Output format (mp4, mov, webm)
        
    Returns:
        Render result with output path and metadata
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        timeline = json.loads(timeline_json)
        preset_name = preset_name or settings.DEFAULT_RENDER_PRESET
        preset_config = settings.RENDER_PRESETS.get(preset_name, settings.RENDER_PRESETS["vertical"])
        
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "renders" / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"output.{output_format}"
        
        # Build filter complex from timeline
        filter_complex = _build_filter_complex(timeline, preset_config)
        
        # Render
        success = processor.render_composition(
            timeline=timeline,
            output_path=str(output_path),
            filter_complex=filter_complex,
            preset=preset_config,
        )
        
        if not success:
            return {
                "success": False,
                "job_id": job_id,
                "error": "Video composition failed",
            }
        
        # Verify output
        metadata = processor.extract_metadata(str(output_path))
        
        render_result = RenderResult(
            output_path=str(output_path),
            duration=metadata.duration or 0,
            width=metadata.width or 0,
            height=metadata.height or 0,
            file_size=metadata.file_size or 0,
            format=output_format,
            preset=preset_name,
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "output_path": str(output_path),
            "render_result": render_result.to_dict(),
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.rendering.render_captions",
    queue="rendering",
    max_retries=2,
    default_retry_delay=60,
)
def render_captions(
    self,
    job_id: str,
    video_path: str,
    captions_json: str,
    style_json: Optional[str] = None,
    preset_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Burn captions/subtitles into video.
    
    Supports:
    - SRT/ASS subtitle formats
    - Word-level highlighting (karaoke style)
    - Custom styling (font, color, position, animation)
    - Multiple caption tracks
    
    Args:
        job_id: Unique render job identifier
        video_path: Path to source video
        captions_json: JSON string of caption data
        style_json: JSON string of style configuration
        preset_name: Render preset to use
        
    Returns:
        Render result with captioned video
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        captions = json.loads(captions_json)
        style = json.loads(style_json) if style_json else {}
        preset_name = preset_name or settings.DEFAULT_RENDER_PRESET
        preset_config = settings.RENDER_PRESETS.get(preset_name, settings.RENDER_PRESETS["vertical"])
        
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "renders" / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = output_dir / f"captioned_{Path(video_path).name}"
        
        # Generate ASS subtitle file with styling
        ass_path = _generate_ass_subtitles(captions, style, output_dir / "captions.ass")
        
        # Burn subtitles into video
        success = processor.burn_subtitles(
            input_path=video_path,
            subtitle_path=str(ass_path),
            output_path=str(output_path),
            preset=preset_config,
        )
        
        if not success:
            return {
                "success": False,
                "job_id": job_id,
                "error": "Caption rendering failed",
            }
        
        metadata = processor.extract_metadata(str(output_path))
        
        render_result = RenderResult(
            output_path=str(output_path),
            duration=metadata.duration or 0,
            width=metadata.width or 0,
            height=metadata.height or 0,
            file_size=metadata.file_size or 0,
            format=Path(output_path).suffix[1:],
            preset=preset_name,
        )
        
        return {
            "success": True,
            "job_id": job_id,
            "output_path": str(output_path),
            "render_result": render_result.to_dict(),
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.rendering.export_video",
    queue="rendering",
    max_retries=2,
    default_retry_delay=60,
)
def export_video(
    self,
    job_id: str,
    source_path: str,
    export_config: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Export video to different formats/qualities.
    
    Supports:
    - Multiple output formats (MP4, MOV, WebM, GIF)
    - Multiple resolutions/bitrates
    - Platform-specific presets (TikTok, Reels, Shorts, YouTube)
    - Thumbnail/sprite generation
    
    Args:
        job_id: Unique export job identifier
        source_path: Path to source video
        export_config: Export configuration with targets
        
    Returns:
        Dictionary of exported files
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        outputs = export_config.get("outputs", [])
        results = {}
        
        for output_config in outputs:
            target_format = output_config.get("format", "mp4")
            preset_name = output_config.get("preset", settings.DEFAULT_RENDER_PRESET)
            preset_config = settings.RENDER_PRESETS.get(preset_name, settings.RENDER_PRESETS["vertical"])
            
            # Override preset with export-specific settings
            if "width" in output_config:
                preset_config = {**preset_config, "width": output_config["width"]}
            if "height" in output_config:
                preset_config = {**preset_config, "height": output_config["height"]}
            if "bitrate" in output_config:
                preset_config = {**preset_config, "bitrate": output_config["bitrate"]}
            if "fps" in output_config:
                preset_config = {**preset_config, "fps": output_config["fps"]}
            
            output_dir = Path(settings.STORAGE_LOCAL_PATH) / "exports" / job_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_name = output_config.get("name", f"export_{preset_name}")
            output_path = output_dir / f"{output_name}.{target_format}"
            
            success = processor.transcode(
                input_path=source_path,
                output_path=str(output_path),
                video_codec=output_config.get("video_codec", "libx264"),
                audio_codec=output_config.get("audio_codec", "aac"),
                video_filters=f"scale={preset_config['width']}:{preset_config['height']}:force_original_aspect_ratio=decrease,pad={preset_config['width']}:{preset_config['height']}:(ow-iw)/2:(oh-ih)/2",
                video_bitrate=preset_config.get("bitrate", "8M"),
                preset=output_config.get("preset_speed", "medium"),
            )
            
            if success:
                metadata = processor.extract_metadata(str(output_path))
                results[output_name] = {
                    "path": str(output_path),
                    "format": target_format,
                    "width": metadata.width,
                    "height": metadata.height,
                    "duration": metadata.duration,
                    "file_size": metadata.file_size,
                    "bitrate": preset_config.get("bitrate"),
                }
            else:
                results[output_name] = {"error": "Export failed"}
        
        # Generate thumbnails for first output
        if results:
            first_output = next(iter(results.values()))
            if "path" in first_output:
                thumb_result = processor.generate_thumbnails(
                    first_output["path"],
                    str(Path(settings.STORAGE_LOCAL_PATH) / "exports" / job_id / "thumbs"),
                    count=5,
                )
                results["thumbnails"] = thumb_result
        
        return {
            "success": True,
            "job_id": job_id,
            "exports": results,
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


@shared_task(
    bind=True,
    name="app.tasks.rendering.create_clips",
    queue="rendering",
    max_retries=2,
    default_retry_delay=60,
)
def create_clips(
    self,
    job_id: str,
    source_path: str,
    clips_config: List[Dict[str, Any]],
    preset_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create multiple clips from a source video.
    
    Each clip config specifies:
    - Start/end time
    - Output format/preset
    - Optional caption overlay
    - Optional watermark/branding
    
    Args:
        job_id: Unique clip creation job identifier
        source_path: Path to source video
        clips_config: List of clip configurations
        preset_name: Default render preset
        
    Returns:
        Dictionary of created clips
    """
    try:
        processor = FFmpegProcessor(
            ffmpeg_path=settings.FFMPEG_PATH,
            ffprobe_path=settings.FFPROBE_PATH,
        )
        
        preset_name = preset_name or settings.DEFAULT_RENDER_PRESET
        preset_config = settings.RENDER_PRESETS.get(preset_name, settings.RENDER_PRESETS["vertical"])
        
        output_dir = Path(settings.STORAGE_LOCAL_PATH) / "clips" / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = {}
        
        for i, clip_config in enumerate(clips_config):
            start_time = clip_config.get("start", 0)
            end_time = clip_config.get("end")
            duration = clip_config.get("duration")
            
            if end_time is None and duration is not None:
                end_time = start_time + duration
            
            clip_preset = clip_config.get("preset", preset_name)
            clip_preset_config = settings.RENDER_PRESETS.get(clip_preset, preset_config)
            
            output_name = clip_config.get("name", f"clip_{i:03d}")
            output_format = clip_config.get("format", "mp4")
            output_path = output_dir / f"{output_name}.{output_format}"
            
            # Build filters
            filters = []
            if "crop" in clip_config:
                crop = clip_config["crop"]
                filters.append(f"crop={crop['width']}:{crop['height']}:{crop.get('x', 0)}:{crop.get('y', 0)}")
            
            filters.append(f"scale={clip_preset_config['width']}:{clip_preset_config['height']}:force_original_aspect_ratio=decrease")
            filters.append(f"pad={clip_preset_config['width']}:{clip_preset_config['height']}:(ow-iw)/2:(oh-ih)/2")
            
            # Add watermark if specified
            if "watermark" in clip_config:
                wm = clip_config["watermark"]
                filters.append(
                    f"movie={wm['path']}[wm];[in][wm]overlay={wm.get('x', 'W-w-10')}:{wm.get('y', 'H-h-10')}[out]"
                )
            
            filter_chain = ",".join(filters)
            
            success = processor.trim_and_transcode(
                input_path=source_path,
                output_path=str(output_path),
                start_time=start_time,
                end_time=end_time,
                video_codec="libx264",
                audio_codec="aac",
                video_filters=filter_chain,
                video_bitrate=clip_preset_config.get("bitrate", "8M"),
                preset="medium",
            )
            
            if success:
                metadata = processor.extract_metadata(str(output_path))
                results[output_name] = {
                    "path": str(output_path),
                    "start": start_time,
                    "end": end_time,
                    "duration": metadata.duration,
                    "width": metadata.width,
                    "height": metadata.height,
                    "file_size": metadata.file_size,
                    "format": output_format,
                }
            else:
                results[output_name] = {"error": "Clip creation failed"}
        
        return {
            "success": True,
            "job_id": job_id,
            "clips": results,
            "total_clips": len(results),
        }
        
    except Exception as exc:
        self.retry(exc=exc)
        return {"success": False, "job_id": job_id, "error": str(exc)}


def _build_filter_complex(timeline: Dict, preset: Dict) -> str:
    """Build FFmpeg filter complex from timeline specification."""
    # This is a simplified version - full implementation would parse
    # the timeline tracks and generate complex filter graphs
    filters = []
    
    # Video track composition
    video_tracks = timeline.get("video_tracks", [])
    for i, track in enumerate(video_tracks):
        clips = track.get("clips", [])
        for j, clip in enumerate(clips):
            # Each clip gets a labeled input
            filters.append(f"[{i}:v]{clip.get('filters', '')}[v{i}_{j}]")
    
    # Audio track mixing
    audio_tracks = timeline.get("audio_tracks", [])
    for i, track in enumerate(audio_tracks):
        clips = track.get("clips", [])
        for j, clip in enumerate(clips):
            filters.append(f"[{i}:a]{clip.get('filters', '')}[a{i}_{j}]")
    
    # Overlay text/captions
    text_tracks = timeline.get("text_tracks", [])
    for i, track in enumerate(text_tracks):
        for j, item in enumerate(track.get("items", [])):
            style = item.get("style", {})
            filters.append(
                f"drawtext=text='{item['text']}':"
                f"fontsize={style.get('fontsize', 24)}:"
                f"fontcolor={style.get('color', 'white')}:"
                f"x={style.get('x', '(w-text_w)/2')}:"
                f"y={style.get('y', 'h-th-50')}:"
                f"enable='between(t,{item['start']},{item['end']})'"
                f"[v{i}_{j}]"
            )
    
    return ";".join(filters)


def _generate_ass_subtitles(
    captions: List[Dict],
    style: Dict,
    output_path: Path,
) -> Path:
    """Generate ASS subtitle file from caption data."""
    # ASS format header
    header = f"""[Script Info]
Title: ClipYantra Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {style.get('width', 1080)}
PlayResY: {style.get('height', 1920)}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{style.get('font', 'Arial')},{style.get('fontsize', 60)},&H{style.get('color', 'FFFFFF')},&H000000FF,&H{style.get('outline', '000000')},&H{style.get('shadow', '80000000')},{1 if style.get('bold') else 0},{1 if style.get('italic') else 0},0,0,100,100,0,0,1,{style.get('outline_width', 3)},{style.get('shadow_depth', 2)},{style.get('alignment', 2)},20,20,{style.get('margin_v', 100)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    events = []
    for caption in captions:
        start = _seconds_to_ass_time(caption.get("start", 0))
        end = _seconds_to_ass_time(caption.get("end", 0))
        text = caption.get("text", "").replace("\n", "\\N")
        
        # Add karaoke effect if word timestamps available
        if "words" in caption:
            text = _generate_karaoke_text(caption["words"])
        
        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
    
    output_path.write_text(header + "\n".join(events), encoding="utf-8")
    return output_path


def _generate_karaoke_text(words: List[Dict]) -> str:
    """Generate ASS karaoke text from word timestamps."""
    parts = []
    for word in words:
        start = _seconds_to_ass_time(word.get("start", 0))
        end = _seconds_to_ass_time(word.get("end", 0))
        dur = int((word.get("end", 0) - word.get("start", 0)) * 100)
        text = word.get("text", "")
        parts.append(f"{{\\k{dur}}}{text}")
    return "".join(parts)


def _seconds_to_ass_time(seconds: float) -> str:
    """Convert seconds to ASS time format (H:MM:SS.cc)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centiseconds = int((seconds - int(seconds)) * 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"


# RND-001: Video composition from timeline
# RND-002: Caption/subtitle rendering
# RND-003: Multi-format export and clip creation