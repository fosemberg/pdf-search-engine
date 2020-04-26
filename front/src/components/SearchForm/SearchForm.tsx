import * as React from 'react';
import {useState} from "react";
import {Button, Card, Form} from "react-bootstrap";

import {RequestKeywords, RequestComponentName, SearchRequest} from "../../utils/apiTypes";

interface IBuildFormProps {
  sendData?: (searchRequest: SearchRequest) => void;
}

const SearchForm: React.FC<IBuildFormProps> = (
  {
    sendData = () => {}
  }
) => {
  const [component_name, setComponent_name] = useState<RequestComponentName>('');
  const onChangeComponentName = (e: React.ChangeEvent<HTMLInputElement>) => setComponent_name(e.currentTarget.value);

  const [keywords, setKeywords] = useState<RequestKeywords>('');
  const onChangeKeywords = (e: React.ChangeEvent<HTMLInputElement>) => setKeywords(e.currentTarget.value);

  const clearData = () => {
    setComponent_name('');
    setKeywords('');
  };

  const onClickSubmit = (e: React.FormEvent<HTMLButtonElement>) => {
    e.preventDefault();
    sendData({component_name, keywords});
    clearData();
  };

  return (
    <Card className="BuildForm">
      <Card.Body>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>component name</Form.Label>
            <Form.Control
              value={component_name}
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
