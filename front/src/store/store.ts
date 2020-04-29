import {
    SearchResponse,
    SearchRequest
} from "../utils/apiTypes";
import {SERVER_HOST, SERVER_HTTP_PORT} from "../config/env";

const hostUrl = `${SERVER_HOST}:${SERVER_HTTP_PORT}`;

export const sendSearchRequest = async (searchRequest: SearchRequest): Promise<SearchResponse> => {
    const url = 'slow-search';
    const _url = `${hostUrl}/${url}`;
    return fetch(
        `${_url}`,
        {
            method: 'POST',
            mode: 'no-cors',
            body: JSON.stringify(searchRequest)
        }
    )
        .then((res) => res.json())
        // TODO: delete when will be backend
        .catch(() => ({
            "NUP4114": {
                "2": "https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-2.pdf",
                "3": "https://github.com/antosha417/test_temp/raw/master/NUP4114/NUP4114-3.pdf"
            }
        }))
};