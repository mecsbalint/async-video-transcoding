import { JobListElementDto, VideoData } from "../types/types";
import { apiRequest, ApiResponse } from "./apiRequest";

export async function getJobList() : Promise<ApiResponse<JobListElementDto[]>> {
    const responseObj = await apiRequest<JobListElementDto[]>({url: "/api/jobs"});
    return responseObj;
}

export async function getVideoData(id: number) : Promise<ApiResponse<VideoData>> {
    const responseObj = await apiRequest<VideoData>({url: `/api/jobs/${id}`});
    return responseObj;
}
