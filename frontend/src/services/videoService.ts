import { apiRequest, ApiResponse } from "./apiRequest";

export async function uploadVideo(video: File): Promise<ApiResponse<null>> {
    const formData = new FormData();
    formData.append("video", video);

    const responseObj = await apiRequest<null>({url: "/api/uploads", method: "POST", body: formData, headers: {"content-type": "multipart/form-data"}});

    return responseObj;
}
