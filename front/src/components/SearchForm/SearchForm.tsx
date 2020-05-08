import * as React from 'react';
import {ComponentElement, useEffect, useState} from "react";
import {Button, Card, Form, OverlayTrigger, Tooltip} from "react-bootstrap";
import Autosuggest from 'react-autosuggest';

import {
  RequestKeywords,
  RequestComponentName,
  RequestAdvancedSearch,
  SearchRequest,
  GetComponentNamesRequest,
  ComponentNames
} from "../../utils/apiTypes";
import InputWithSqlHighlight from "../InputWithSqlHighlight/InputWithSqlHighlight";
import ClearButton from "../ClearButton/ClearButton";

import './SearchForm.css';

interface SearchFormProps {
  sendData?: (searchRequest: SearchRequest) => void;
  getComponentNames?: (getComponentNamesRequest?: GetComponentNamesRequest) => void;
  componentNames?: ComponentNames;
  className?: string;
}

const getSuggestions = (suggestions: string[], value: string) => {
  const inputValue = value.trim().toLowerCase();
  const inputLength = inputValue.length;

  return inputLength === 0 ? [] : suggestions.filter(suggestion =>
    suggestion.toLowerCase().slice(0, inputLength) === inputValue
  );
};

const getSuggestionValue = (suggestion: string): string => suggestion;

const renderSuggestion = (suggestion: string): ComponentElement<any, any> => (
  <div>
    {suggestion}
  </div>
);

const renderSuggestionsContainer = ({containerProps, children}: any) => {
  const {className, ...restProps} = containerProps;
  return <div
    {...restProps}
    className={`${className} dropdown-menu`}
  >
    {children}
  </div>
}

const SearchForm: React.FC<SearchFormProps> = (
  {
    sendData = () => {},
    getComponentNames = () => {},
    componentNames = [],
    className = '',
  }
) => {
  useEffect(
    () => {
      getComponentNames()
    },
    [],
  )

  const [componentName, setComponentName] = useState<RequestComponentName>('');
  const onChangeComponentName = (e: React.ChangeEvent<HTMLInputElement>, {newValue}: any) => setComponentName(newValue);

  const [suggestions, setsuggestions] = useState<string[]>([]);

  const [keywords, setKeywords] = useState<RequestKeywords>('');
  const onChangeSqlKeywords = (keywords: string) => setKeywords(keywords);
  const onChangePlainKeywords = (e: React.ChangeEvent<HTMLInputElement>) => setKeywords(e.currentTarget.value);

  const [advancedSearch, setAdvancedSearch] = useState<RequestAdvancedSearch>(false)
  const onChangeAdvancedSearch = (e: React.ChangeEvent<HTMLInputElement>) => setAdvancedSearch(e.currentTarget.checked)

  const clearComponentName = () => {
    setComponentName('');
  };

  const clearKeywords = () => {
    setKeywords('');
  };

  const onClickSubmit = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    sendData({name: componentName, keywords, advanced: advancedSearch});
  };

  const onSuggestionsClearRequested = () => {
    setsuggestions([])
  };

  const onSuggestionsFetchRequested = ({value}: { value: string }) => {
    setsuggestions(getSuggestions(componentNames, value))
  };

  const inputProps = {
    value: componentName,
    onChange: onChangeComponentName,
    type: "text",
    placeholder: "component name",
    className: 'form-control SearchForm-ComponentName'
  };

  return (
    <Card className={`SearchForm ${className}`}>
      <Card.Body>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>component name</Form.Label>
            <Autosuggest
              suggestions={suggestions}
              getSuggestionValue={getSuggestionValue}
              renderSuggestion={renderSuggestion}
              inputProps={inputProps}
              onSuggestionsFetchRequested={onSuggestionsFetchRequested}
              onSuggestionsClearRequested={onSuggestionsClearRequested}
              renderSuggestionsContainer={renderSuggestionsContainer}
            />
            <ClearButton
              onClick={clearComponentName}
              className={'SearchForm-ClearButton'}
            />
          </Form.Group>

          <Form.Group controlId="formBasicEmail">
            <Form.Label>query</Form.Label>
            {
              advancedSearch
              ? <InputWithSqlHighlight
                  value={keywords}
                  onChange={onChangeSqlKeywords}
                  placeholder="query"
                />
              : <Form.Control
                  value={keywords}
                  onChange={onChangePlainKeywords}
                  placeholder="query"
                  type="text"
                  className="SearchForm-Query"
                />
            }
            <ClearButton
              onClick={clearKeywords}
              className={'SearchForm-ClearButton'}
            />
          </Form.Group>

          <div className='search-and-switch'>
          <Button
            onClick={onClickSubmit}
            variant="primary"
            type="button"
          >
            Search
          </Button>
          <OverlayTrigger
            placement='bottom'
            overlay={<Tooltip id='Switch-tooltip'>Enables specific syntax: brackets, wildcards, AND, OR etc. <br/><strong>Warning: throws error on wrong syntax.</strong></Tooltip>}>
            <Form.Group>
              <Form.Check
                type='switch'
                id="switch"
                label="Advanced Search"
                onChange={onChangeAdvancedSearch}
                checked={advancedSearch}
              >
              </Form.Check>
            </Form.Group>
          </OverlayTrigger>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default SearchForm;
