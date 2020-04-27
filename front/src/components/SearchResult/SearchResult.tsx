import React from 'react';
import { Document, Page } from 'react-pdf';

import { pdfjs } from 'react-pdf';
import { PageResponse } from "../../utils/apiTypes";

import './SearchResult.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

interface SearchResultProps {
  pages?: PageResponse[];
}

const SearchResult: React.FC<SearchResultProps> = ({pages= []}) => {
  return <div className='SearchResult'>
    {
      pages
        ?.sort(({number: number1},{number: number2}) => number1 - number2)
        .map(
        page =>
          <div className='SearchResult__page'>
            <Document file={page.content}>
              <Page
                pageNumber={1}
              />
            </Document>
            <div>{page.number}</div>
          </div>
      )
    }
  </div>;
}

export default SearchResult;
