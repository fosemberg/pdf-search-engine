import * as React from "react";
import {useState} from "react";
import {Alert, Button, Card, Form, Spinner} from "react-bootstrap";
import {cn} from "@bem-react/classname";

import {FileUploadRequest, FileUploadResponse} from "../../utils/apiTypes";
import FileUploader from "../FileUploader/FileUploader";
import FileUploadPreview from "../FileUploadPreview/FileUploadPreview";

import "./UploadForm.css";

interface UploadFormProps {
  sendData?: (fileUploadRequest: FileUploadRequest) => Promise<FileUploadResponse>;
}

enum UploadStatus {
  init,
  uploading,
  success,
  error,
}

enum SendStatus {
  init,
  sending,
  success,
  error,
}

const cnUploadForm = cn('UploadForm');

const UploadForm: React.FC<UploadFormProps> = (
  {
    sendData = () => {
    }
  }
) => {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>(UploadStatus.init)
  const [sendStatus, setSendStatus] = useState<SendStatus>(SendStatus.init)

  const [filename, setFilename] = useState<string>('');
  const onChangeFilename = (e: React.ChangeEvent<HTMLInputElement>) => setFilename(e.currentTarget.value);

  const [file, setFile] = useState<File | undefined>();

  const isSuccessLoad = uploadStatus === UploadStatus.success ? true
    : uploadStatus === UploadStatus.error ? false
    : undefined

  const setIsSuccessLoad = (isSuccessLoad: boolean) => {
    isSuccessLoad
      ? setUploadStatus(UploadStatus.success)
      : setUploadStatus(UploadStatus.error)
  }

  const onClickSubmit = async (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    if (file) {
      setSendStatus(SendStatus.sending)
      setUploadStatus(UploadStatus.init)
      const response = await sendData({filename, file})
      response ? setSendStatus(SendStatus.success) : setSendStatus(SendStatus.error)
      setFilename('');
      setFile(undefined)
    }
  };

  const onUploadFile = (file: File) => {
    setUploadStatus(UploadStatus.uploading)
    setSendStatus(SendStatus.init)
    !filename && file.name && setFilename(file.name.replace('.pdf', ''))
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
              disabled={sendStatus === SendStatus.sending}
              type="text"
              placeholder="file name"
            />
          </Form.Group>
          <FileUploader
            {...{onUploadFile, isSuccessLoad}}
            isDisabled={sendStatus === SendStatus.sending}
          >
            {sendStatus === SendStatus.sending && <p>Disabled while file uploading</p>}
          </FileUploader>
          <Button
            onClick={onClickSubmit}
            className={cnUploadForm('Submit')}
            variant="primary"
            type="submit"
            disabled={!isSuccessLoad || !filename || sendStatus === SendStatus.sending}
          >
            {
              sendStatus === SendStatus.sending
                ? <><Spinner
                  as="span"
                  animation="grow"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                />
                  Upload...
              </>
                : 'Upload'
            }
          </Button>
          <div className={cnUploadForm('Result')}>
            {
              !!file
              ? <>
                  {
                    uploadStatus !== UploadStatus.error &&
                      <h5 className={cnUploadForm('FilePreviewHeader')}>File preview</h5>
                  }
                <FileUploadPreview {...{file, setIsSuccessLoad}} />
              </>
              : sendStatus === SendStatus.success
                ? <Alert variant='success'>File uploaded successfully</Alert>
                : sendStatus === SendStatus.error && <Alert variant='danger'>An error occurred while uploading the file</Alert>
            }
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default UploadForm;
