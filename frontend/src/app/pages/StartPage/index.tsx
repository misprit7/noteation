import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import logo from './assets/logo.png';
import styled from 'styled-components/macro';

export function StartPage() {
  return (
    <>
      <Helmet>
        <title>Start</title>
      </Helmet>
      <Container>
        <h1>Hello world</h1>
        <img src={logo} className="start-logo"/>
        <Button variant="contained">Test</Button>
      </Container>
    </>
  );
}

const img = styled.a`
  width: 100px;
`;

