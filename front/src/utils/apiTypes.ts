export type RequestComponentName = string;
export type RequestKeywords = string;

export interface SearchResponse {
  [key: string]: {
    [key: string]: string
  }
}

export interface SearchRequest {
  name: RequestComponentName;
  keywords: RequestKeywords;
}

export interface FileUploadRequest {
  file: Blob;
  filename: string;
}

export type FileUploadResponse = boolean;
