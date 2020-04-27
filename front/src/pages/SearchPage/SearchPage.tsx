import * as React from 'react';

import SearchForm from "../../components/SearchForm/SearchForm";
import {SearchResponse, SearchRequest, PageResponse} from "../../utils/apiTypes";
import SearchResult from "../../components/SearchResult/SearchResult";

import './SearchPage.css';

interface SearchPageProps {
  sendData: (searchRequest: SearchRequest) => Promise<SearchResponse>;
}

interface SearchPageState {
  pages: PageResponse[];
}

class SearchPage extends React.Component<SearchPageProps, SearchPageState> {
  constructor(props: SearchPageProps) {
    super(props);
    this.state = {
      pages: []
    }
  }

  sendData = async (searchRequest: SearchRequest) => {
    const response = await this.props.sendData(searchRequest);
    this.setState(response);
  }

  render() {
    const {
      state: {pages},
      sendData,
    } = this;

    return (
      <div className="SearchPage">
        <h4>Search for information about electronic components</h4>
        <SearchForm sendData={sendData}/>
        {
          pages.length !== 0 && <SearchResult
              pages={pages}
          />
        }
      </div>
    )
  }
}

export default SearchPage;
