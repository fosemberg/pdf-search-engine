import {
  SearchResponse,
  SearchRequest
} from "../utils/apiTypes";
import {SERVER_HOST, SERVER_HTTP_PORT} from "../config/env";

const hostUrl = `${SERVER_HOST}:${SERVER_HTTP_PORT}`;

export const sendSearchRequest = (searchRequest: SearchRequest): Promise<SearchResponse> => {
  const url = 'search';
  const _url = `${hostUrl}/${url}`;
  return fetch(
    `${_url}`,
    {
      method: 'POST',
      body: JSON.stringify(searchRequest)
    }
  )
    .then((res) => res.json());
};