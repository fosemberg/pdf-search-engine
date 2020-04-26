import React from 'react';
import {Nav, Navbar} from "react-bootstrap";
import {Link} from "react-router-dom";

const AppNavbar = () => {
  return (
    <Navbar collapseOnSelect={true} expand="lg" bg="light" variant="light">
      <Link className="navbar-brand" to="/">PDF search engine</Link>
      <Navbar.Toggle aria-controls="responsive-navbar-nav"/>
      <Navbar.Collapse>
        <Nav>
          <Link className="nav-link" to="/">Search</Link>
        </Nav>
        <Nav className="mr-auto">
          <Link className="nav-link" to="/upload">Upload</Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default AppNavbar;