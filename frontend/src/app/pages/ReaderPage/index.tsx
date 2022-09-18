import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import { Stack, Button, Divider} from '@mui/material';
import styled from 'styled-components/macro';
import aruco0 from './assets/4x4_1000-0.svg';
import aruco1 from './assets/4x4_1000-1.svg';
import aruco2 from './assets/4x4_1000-2.svg';
import aruco3 from './assets/4x4_1000-3.svg';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';

export function ReaderPage(props) {

  return (
    <>
      <Helmet>
        <title>{props.score?.name}</title>
      </Helmet>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Stack 
          direction="column"
          justifyContent="space-between"
          alignItems="flex-start"
          style={{height: '100vh', width: '200px'}}
          // divider={<Divider flexItem variant="middle"/>}
        >
          <Img src={aruco0}/>
          <Button style={{minHeight: '50vh', minWidth: '100%'}}><ChevronLeftIcon/></Button>
          <Img src={aruco2}/>
        </Stack>
        <iframe src="Prelude-Renu.pdf#page=2&zoom=page-width" style={{height: '100vh', width: '73vh'}}/>
        <Stack direction="column" justifyContent="space-between" style={{height: '100vh'}}>
          <Img src={aruco1}/>
          <Img src={aruco3}/>
        </Stack>
      </Stack>
    </>
  );
}

const Img = styled.img`
  margin: 10mm
`

