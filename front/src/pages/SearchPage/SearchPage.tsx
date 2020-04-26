import * as React from 'react';

import SearchForm from "../../components/SearchForm/SearchForm";
import {SearchResponse, SearchRequest} from "../../utils/apiTypes";

import './SearchPage.css';
import SearchResult from "../../components/SearchResult/SearchResult";

interface SearchPageProps {
  sendData: (searchRequest: SearchRequest) => Promise<SearchResponse>;
}

interface SearchPageState {
  data: SearchResponse[];
}

class SearchPage extends React.Component<SearchPageProps, SearchPageState> {
  constructor(props: SearchPageProps) {
    super(props);
    this.state = {
      data: [],
    }
  }

  render() {
    const {
      state: {data},
      props: {sendData},
    } = this;

    return (
      <div className="SearchPage">
        <SearchForm sendData={sendData}/>
        {
          data.length !== 0 && <div>data</div>
        }
        <SearchResult/>
      </div>
    )
  }
}

export default SearchPage;
