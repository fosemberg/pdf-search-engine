import {
  SearchResponse,
  SearchRequest, FileUploadResponse, FileUploadRequest
} from "../utils/apiTypes";
import {SERVER_HOST, SERVER_HTTP_PORT} from "../config/env";

const hostUrl = `${SERVER_HOST}:${SERVER_HTTP_PORT}`;

export const sendSearchRequest = async (searchRequest: SearchRequest): Promise<SearchResponse> => {
  const url = 'slow-search';
  const _url = `${hostUrl}/${url}`;
  try {
    const response = await fetch(
      `${_url}`,
      {
        method: 'POST',
        body: JSON.stringify(searchRequest)
      }
    )
    console.log(response)
    const json = await response.json()
    console.log(json)
    return json;
  } catch (error) {
    console.error(error);
    return {
      "NUP4114": {
        "2": "https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-2.pdf",
        "3": "https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-3.pdf"
      }
    }
  }
}

export const sendUploadFileRequest = async ({file, filename}: FileUploadRequest): Promise<FileUploadResponse> => {
  const url = 'upload';
  const _url = `${hostUrl}/${url}`;
  try {
    const formData  = new FormData();
    formData.append('blob', file, filename)

    const response = await fetch(
      `${_url}`,
      {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        body: formData,
      }
    )
    return true;
  } catch (error) {
    console.error(error);
    return false;
  }
}