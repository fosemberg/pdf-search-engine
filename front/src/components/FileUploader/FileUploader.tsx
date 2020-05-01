import React, {useCallback, useState} from 'react'
import {useDropzone} from 'react-dropzone'
import {Document, Page} from "react-pdf";
import {Card} from "react-bootstrap";
import {cn} from "@bem-react/classname";

import './FileUploader.css'

const cnFileUploader = cn('FileUploader');

const FileUploader = () => {
  const [file, setFile] = useState()
  const [isSuccessLoad, setIsSuccessLoad] = useState();

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file: any) => {
      setFile(file);
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
      {
        !!file &&
        <div className={cnFileUploader('Preview')}>
          <Document
            file={file}
            onLoadSuccess={() => setIsSuccessLoad(true)}
            onLoadError={() => setIsSuccessLoad(false)}
          >
            <Page pageNumber={1}/>
          </Document>
        </div>
      }
    </div>
  )
}

export default FileUploader;
