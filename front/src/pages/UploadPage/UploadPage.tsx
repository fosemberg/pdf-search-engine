import * as React from 'react';
import {cn} from "@bem-react/classname";
import './UploadPage.css';

const cnBuildPage = cn('UploadPage');

class UploadPage extends React.Component {
  render() {
    return (
      <div className={cnBuildPage()}>
        <div>upload page</div>
      </div>
    )
  }
}

export default UploadPage;
