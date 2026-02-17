
type Job = {
    id: number,
    state: "queued" | "running" | "done" | "failed"
}

export type JobListElementDto = Job & {
    thumbnail_url: string | null
}

export type VideoData = Job & {
    original_url: string,
    preview_url: string,
    thumbnail_url: string,
    duration: number,
    video_streams_metadata: VideoStreamMetadata[]
    audio_streams_metadata: AudioStreamMetadata[]
    subtitles_streams_metadata: SubtitlesStreamMetadata[]
}

export type StreamMetadata = {
    fps: number,
    codec: string
}

type VideoStreamMetadata = StreamMetadata & {
    width: number,
    height: number
}

type AudioStreamMetadata = StreamMetadata & {}

type SubtitlesStreamMetadata = StreamMetadata & {}
