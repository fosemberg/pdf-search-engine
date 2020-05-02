import React from 'react';
import {Spinner} from "react-bootstrap";

const Loader = () => (
  <Spinner
    animation="border"
    role="status"
  >
    <span className="sr-only">Loading...</span>
  </Spinner>
)

export default Loader;
