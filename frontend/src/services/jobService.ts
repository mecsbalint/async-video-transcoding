import { JobListElementDto } from "../types/types";
import { apiRequest, ApiResponse } from "./apiRequest";

export async function getJobList() : Promise<ApiResponse<JobListElementDto[]>>{
    const responseObj = await apiRequest<JobListElementDto[]>({url: "api/jobs"});
    return responseObj;
}
