
type Job = {
    id: number,
    state: "queued" | "running" | "done" | "failed"
}

export type JobListElement = Job & {
    thumbnail_url: string
}

export type Video = Job & {
    original_url: string,
    preview_url: string,
    thumbnail_url: string,
    duration: number,
    video_streams_metadata: VideoStreamMetadata[]
    audio_streams_metadata: AudioStreamMetadata[]
    subtitles_streams_metadata: SubtitlesStreamMetadata[]
}

type StreamMetadata = {
    fps: number,
    codec: string
}

type VideoStreamMetadata = StreamMetadata & {
    width: number,
    height: number
}

type AudioStreamMetadata = StreamMetadata & {}

type SubtitlesStreamMetadata = StreamMetadata & {}
