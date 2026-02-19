
type ApiRequestParams = {
  url: string,
  method?: "GET" | "POST" | "DELETE" | "PUT" | "PATCH" | "HEAD",
  body?: string | FormData,
  headers?: {[key: string]: string},
};

export type ApiResponse<T = any> = {
  status: number,
  body: T | null
};

export async function apiRequest<T = void>({
  url, 
  method = "GET",
  body,
  headers = {},
} : ApiRequestParams) : Promise<ApiResponse<T>> {

  const response = await fetch(url, {
    method,
    headers: {
      ...headers,
    },
    ...(method !== "GET" && body ? {body} : {})
  });

  let responseBody = await response.json().catch(() => {
    return null
  });

  return {status: response.status, body: responseBody as T};
}
