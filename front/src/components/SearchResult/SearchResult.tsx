import React from 'react';
import {Document, Page} from 'react-pdf';

import {pdfjs} from 'react-pdf';
import {SearchResponse} from "../../utils/apiTypes";

import './SearchResult.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

interface SearchResultProps {
  searchResponse?: SearchResponse;
}

const SearchResult: React.FC<SearchResultProps> = ({searchResponse = {}}) => {

  const componentNames = Object.keys(searchResponse);

  return <div className='SearchResult'>
    {
      componentNames.map(
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
    }
  </div>
}

export default SearchResult;
