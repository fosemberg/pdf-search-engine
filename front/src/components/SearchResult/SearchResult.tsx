import React from 'react';
import {Document, Page} from 'react-pdf';
import {pdfjs} from 'react-pdf';
import {Alert, Image} from "react-bootstrap";
// @ts-ignore
import { CsvToHtmlTable } from 'react-csv-to-table';

import {SearchResponse} from "../../utils/apiTypes";
import Loader from "../Loader/Loader";

import './SearchResult.css';
import {CardText} from "react-bootstrap/Card";

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
                .map(([page, content]) => (
                  <div key={page} className="container">
                    <h5>Page #{page}<a href={content["url"]} className="float-right">Download full page</a></h5>
                    <div className='SearchResult__page'>
                      {Object.entries(content['images']).map(
                        ([image_num, image_url]) =>
                          <Image src={image_url} fluid/>
                      )}
                      {Object.entries(content['tables']).map(
                        ([table_num, table_url]) =>
                          <CsvToHtmlTable
                            data={table_url}
                            csvDelimiter=","
                          />
                      )}
                    </div>
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
