import React, { useState } from 'react';
import { Document, Outline, Page } from 'react-pdf';

import { pdfjs } from 'react-pdf';
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

const highlightPattern = (text: any, pattern: any) => {
  const splitText = text.split(pattern);

  if (splitText.length <= 1) {
    return text;
  }

  const matches = text.match(pattern);

  return splitText.reduce((arr: any, element: any, index: any) => (matches[index] ? [
    ...arr,
    element,
    <mark>
      {matches[index]}
    </mark>,
  ] : [...arr, element]), []);
};

function SearchResult() {

  const [pageNumber, setPageNumber] = useState(1);
  const makeTextRenderer = (searchText: any) => (textItem: any) => highlightPattern(textItem.str, searchText);
  const matches = [{page: 1, text: 'Low Clamping Voltage'}, {page: 2, text: 'some other match text'}, {page: 5,  text: 'another match text'}];

  return <div style={{display: 'flex', flexDirection: 'row'}}>
    <ul style={{cursor: 'pointer'}}>
      {matches.map(m => <li onClick={() => setPageNumber(m.page)}>
        {m.page} {m.text}
      </li>)}
    </ul>
    <Document file={'/test.pdf'}>
      <Outline onItemClick={(n) => setPageNumber(Number.parseInt(n.pageNumber))} />
      <Page
        pageNumber={pageNumber || 1}
        customTextRenderer={makeTextRenderer('Voltage')}
      />
    </Document>
  </div>;
}

export default SearchResult;
