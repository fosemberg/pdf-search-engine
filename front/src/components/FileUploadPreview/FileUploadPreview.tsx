import React from 'react'
import {Document, Page} from "react-pdf";
import {cn} from "@bem-react/classname";

import Loader from "../Loader/Loader";

import './FileUploadPreview.css'

interface FileUploadPreviewProps {
  file: File;
  setIsSuccessLoad: (isSuccessLoad: boolean) => void;
}

const cnFileUploadPreview = cn('FileUploadPreview');

const FileUploadPreview: React.FC<FileUploadPreviewProps> = (
  {
    file,
    setIsSuccessLoad,
  }
) => {
  return (
    <div className={cnFileUploadPreview()}>
      <Document
        file={file}
        onLoadSuccess={() => setIsSuccessLoad(true)}
        onLoadError={() => setIsSuccessLoad(false)}
        loading={<Loader/>}
      >
        <Page pageNumber={1}/>
      </Document>
    </div>
  )
}

export default FileUploadPreview;
