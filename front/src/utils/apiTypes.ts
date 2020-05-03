export type RequestComponentName = string;
export type RequestKeywords = string;

interface SearchResponseSuccess {
  [key: string]: {
    [key: string]: string
  }
}

type SearchResponseError = false

export type SearchResponse = SearchResponseSuccess | SearchResponseError

export interface SearchRequest {
  name: RequestComponentName;
  keywords: RequestKeywords;
}

export interface FileUploadRequest {
  file: Blob;
  filename: string;
}

export type FileUploadResponse = boolean;

export type GetComponentNamesRequest = string;

export type ComponentNames = string[];

export interface GetComponentNamesResponse {
  names: ComponentNames;
}
