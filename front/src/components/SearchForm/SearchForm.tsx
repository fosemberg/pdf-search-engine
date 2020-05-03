import * as React from 'react';
import {ComponentElement, useEffect, useState} from "react";
import {Button, Card, Form} from "react-bootstrap";
import Autosuggest from 'react-autosuggest';

import {
  RequestKeywords,
  RequestComponentName,
  SearchRequest,
  GetComponentNamesRequest,
  ComponentNames
} from "../../utils/apiTypes";

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
  const onChangeKeywords = (e: React.ChangeEvent<HTMLInputElement>) => setKeywords(e.currentTarget.value);

  const clearData = () => {
    setComponentName('');
    setKeywords('');
  };

  const onClickSubmit = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    sendData({name: componentName, keywords});
    clearData();
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
    className: 'form-control'
  }

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
          </Form.Group>

          <Form.Group controlId="formBasicEmail">
            <Form.Label>query</Form.Label>
            <Form.Control
              value={keywords}
              onChange={onChangeKeywords}
              type="text"
              placeholder="query"
            />
          </Form.Group>

          <Button
            onClick={onClickSubmit}
            variant="primary"
            type="button"
          >
            Search
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default SearchForm;
