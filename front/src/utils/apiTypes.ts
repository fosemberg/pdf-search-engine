export type RequestComponentName = string;
export type RequestKeywords = string;
export type RequestAdvancedSearch = boolean;

interface SearchResponseSuccess {
  [key: string]: {
    [key: string]: {
      url: string,
      tables: {
        [key: string]: string
      },
      images: {
        [key: string]: string
      },
    }
  }
}

type SearchResponseError = false

export type SearchResponse = SearchResponseSuccess | SearchResponseError

export interface SearchRequest {
  name: RequestComponentName;
  keywords: RequestKeywords;
  advanced?: RequestAdvancedSearch;
}

export interface FileUploadRequest {
  file: File;
  filename: string;
}

export type FileUploadResponse = boolean;

export type GetComponentNamesRequest = string;

export type ComponentNames = string[];

export interface GetComponentNamesResponse {
  names: ComponentNames;
}
