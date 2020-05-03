import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import {Card} from "react-bootstrap";
import {cn} from "@bem-react/classname";

import './FileUploader.css';

interface FileUploaderProps {
  onUploadFile?: (file: File) => void;
  isSuccessLoad?: boolean;
}

const cnFileUploader = cn('FileUploader');

const FileUploader: React.FC<FileUploaderProps> = (
  {
    onUploadFile= () => {},
    isSuccessLoad,
  }
) => {
  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file: File) => {
      onUploadFile(file);
      const reader = new FileReader()

      reader.onabort = () => console.log('file reading was aborted')
      reader.onerror = () => console.log('file reading has failed')
      reader.onload = () => {
        const binaryStr = reader.result
        console.log(binaryStr)
      }
      reader.readAsArrayBuffer(file)
    })

  }, [])
  const {getRootProps, getInputProps} = useDropzone({onDrop})

  return (
    <div className={cnFileUploader()}>
      <Card
        className={cnFileUploader('Drag-n-drop')}
        border={
          isSuccessLoad === undefined ? undefined
            : isSuccessLoad ? "success"
            : "danger"
        }
      >
        <Card.Body {...getRootProps()}>
          <input {...getInputProps()} />
          <p>Drag 'n' drop some files here, or click to select files</p>
        </Card.Body>
      </Card>
    </div>
  )
}

export default FileUploader;
