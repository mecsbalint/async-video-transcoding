import { apiRequest, ApiResponse } from "./apiRequest";

export async function uploadVideo(video: File, priorityHigh: boolean): Promise<ApiResponse<null>> {
    const formData = new FormData();
    formData.append("video", video);

    const responseObj = await apiRequest<null>({url: `/api/uploads${priorityHigh ? "?priority=high" : ""}`, method: "POST", body: formData});

    return responseObj;
}
