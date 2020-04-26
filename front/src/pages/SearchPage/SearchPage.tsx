import * as React from 'react';

import SearchForm from "../../components/SearchForm/SearchForm";
import {SearchResponse, SearchRequest} from "../../utils/apiTypes";

import './SearchPage.css';

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
        <h4>Search for information about electronic components</h4>
        <SearchForm sendData={sendData}/>
        {
          data.length !== 0 && <div>data</div>
        }
      </div>
    )
  }
}

export default SearchPage;
