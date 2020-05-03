import React from 'react';
import {Document, Page} from 'react-pdf';
import {pdfjs} from 'react-pdf';
import {Alert} from "react-bootstrap";

import {SearchResponse} from "../../utils/apiTypes";

import './SearchResult.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

interface SearchResultProps {
  searchResponse?: SearchResponse;
  className?: string;
}

const SearchResult: React.FC<SearchResultProps> = (
  {
    searchResponse = {},
    className= '',
  }
) => (
  <div className={`SearchResult ${className}`}>
    {
      searchResponse !== false
        ? Object.keys(searchResponse).length !== 0
          ? Object.keys(searchResponse).map(
            componentName => (
              Object.entries(searchResponse[componentName])
                .sort(([page1, url1], [page2, url2]) => +page1 - +page2)
                .map(([page, url]) => (
                  <div
                    key={page}
                    className='SearchResult__page'
                  >
                    <Document file={`https://cors-anywhere.herokuapp.com/${url}`}>
                      <Page
                        pageNumber={1}
                      />
                    </Document>
                    <div>{page}</div>
                  </div>
                ))
            )
          )
          : <Alert variant='warning'>Nothing found for this request</Alert>
        : <Alert variant='danger'>We have an error on the server, we are already fixing</Alert>
    }
  </div>
)

export default SearchResult;
