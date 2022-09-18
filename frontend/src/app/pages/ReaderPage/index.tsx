import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import {Grid, Stack} from '@mui/material';

export function ReaderPage(props) {

  return (
    <>
      <Helmet>
        <title>{props.score?.name}</title>
      </Helmet>
      <Stack justifyContent="center" alignItems="center">
          <iframe src="Prelude-Renu.pdf#page=2&zoom=page-width" style={{height: '100vh', width: '73vh'}}/>
      </Stack>
    </>
  );
}
