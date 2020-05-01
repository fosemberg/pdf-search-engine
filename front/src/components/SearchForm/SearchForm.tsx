import * as React from 'react';
import {useState} from "react";
import {Button, Card, Form} from "react-bootstrap";

import {RequestKeywords, RequestComponentName, SearchRequest} from "../../utils/apiTypes";

interface SearchFormProps {
  sendData?: (searchRequest: SearchRequest) => void;
}

const SearchForm: React.FC<SearchFormProps> = (
  {
    sendData = () => {}
  }
) => {
  const [componentName, setComponentName] = useState<RequestComponentName>('');
  const onChangeComponentName = (e: React.ChangeEvent<HTMLInputElement>) => setComponentName(e.currentTarget.value);

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

  return (
    <Card className="SearchForm">
      <Card.Body>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>component name</Form.Label>
            <Form.Control
              value={componentName}
              onChange={onChangeComponentName}
              type="text"
              placeholder="component name"
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
            type="submit"
          >
            Search
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default SearchForm;
