import * as React from 'react';
import {cn} from "@bem-react/classname";

import FileUploader from "../../components/FileUploader/FileUploader";

import './UploadPage.css';

const cnBuildPage = cn('UploadPage');

class UploadPage extends React.Component {
  render() {
    return (
      <div className={cnBuildPage()}>
        <FileUploader/>
      </div>
    )
  }
}

export default UploadPage;
