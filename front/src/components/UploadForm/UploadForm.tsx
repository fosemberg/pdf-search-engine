import * as React from 'react';
import {useState} from "react";
import {Button, Card, Form} from "react-bootstrap";
import {cn} from "@bem-react/classname";

import {RequestComponentName, FileUploadRequest} from "../../utils/apiTypes";
import FileUploader from "../FileUploader/FileUploader";
import FileUploadPreview from "../FileUploadPreview/FileUploadPreview";

import './UploadForm.css';

interface UploadFormProps {
  sendData?: (fileUploadRequest: FileUploadRequest) => void;
}

const cnUploadForm = cn('UploadForm');

const UploadForm: React.FC<UploadFormProps> = (
  {
    sendData = () => {
    }
  }
) => {
  const [filename, setFilename] = useState<string>('');
  const onChangeFilename = (e: React.ChangeEvent<HTMLInputElement>) => setFilename(e.currentTarget.value);

  const [file, setFile] = useState<File | undefined>();

  const [isSuccessLoad, setIsSuccessLoad] = useState<boolean | undefined>();

  const clearData = () => {
    setFilename('');
    setFile(undefined);
    setIsSuccessLoad(undefined)
  };

  const onClickSubmit = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    file && sendData({filename, file});
    clearData();
  };

  const onUploadFile = (file: File) => {
    !filename && file.name && setFilename(file.name)
    setFile(file)
  }

  return (
    <Card className="UploadForm">
      <Card.Body>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>file name</Form.Label>
            <Form.Control
              value={filename}
              onChange={onChangeFilename}
              type="text"
              placeholder="file name"
            />
          </Form.Group>
          <FileUploader {...{onUploadFile, isSuccessLoad}} />
          <Button
            onClick={onClickSubmit}
            className={cnUploadForm('Submit')}
            variant="primary"
            type="submit"
            disabled={!isSuccessLoad}
          >
            Upload
          </Button>
          {
            !!file &&
            <div className={cnUploadForm('FilePreview')}>
              <h5 className={cnUploadForm('FilePreviewHeader')}>
                File preview
              </h5>
              <FileUploadPreview {...{file, setIsSuccessLoad}} />
            </div>
          }
        </Form>
      </Card.Body>
    </Card>
  );
};

export default UploadForm;
