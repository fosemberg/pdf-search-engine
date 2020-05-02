import * as React from 'react';
import {cn} from "@bem-react/classname";

import SearchForm from "../../components/SearchForm/SearchForm";
import {SearchResponse, SearchRequest} from "../../utils/apiTypes";
import SearchResult from "../../components/SearchResult/SearchResult";

import './SearchPage.css';

interface SearchPageProps {
  sendData: (searchRequest: SearchRequest) => Promise<SearchResponse>;
}

interface SearchPageState {
  searchResponse: SearchResponse;
}

const cnSearchPage = cn('SearchPage');

class SearchPage extends React.Component<SearchPageProps, SearchPageState> {
  constructor(props: SearchPageProps) {
    super(props);
    this.state = {
      searchResponse: {}
    }
  }

  sendData = async (searchRequest: SearchRequest) => {
    const searchResponse = await this.props.sendData(searchRequest);
    this.setState({searchResponse});
  }

  render() {
    const {
      state: {searchResponse},
      sendData,
    } = this;

    const components = Object.keys(searchResponse);

    return (
      <div className={cnSearchPage()}>
        <h4>Search for information about electronic components</h4>
        <SearchForm sendData={sendData}/>
        {
          components.length !== 0 && <SearchResult
              searchResponse={searchResponse}
          />
        }
      </div>
    )
  }
}

export default SearchPage;
