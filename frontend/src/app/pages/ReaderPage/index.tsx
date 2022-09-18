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
import {useHistory} from 'react-router-dom';

export function ReaderPage(props) {

  const history = useHistory()
  const [page, setPage] = React.useState(1);

  var prevTimestamp = [0]

  const makeQuery = (pt) => {
    const API_URL: string = "http://1ec8-2620-101-f000-704-8000-00-eaa.ngrok.io";
    var requestOptions: RequestInit = {
      method: 'GET',
      redirect: 'follow'
    };
    
    let ret = fetch(API_URL + `/events/${prevTimestamp}`, requestOptions)
      .then((response) => {
        return response.json();
      })
      .then((json) => {
        let events: Array<string> = json["events"];
        for(let e of events){
          if(e[0] > pt[0]){
            if(e[1] == "left") onLeft()
            if(e[1] == "right") onRight()
          }
          console.log(e[1])
        }
        pt[0] = events.length == 0 ? pt[0] : events[events.length-1][0]
        console.log(prevTimestamp)
        return events
      })
    // return ret
  }


  React.useEffect(() => {
    let interval
    interval = setInterval(() => {
      makeQuery(prevTimestamp)

    }, 1000)

    return () => clearInterval(interval)
  })

  const onLeft = () => {
    if(page > 1) setPage(page-1)
  }

  const onRight = () => {
    setPage(page+1)
  }

  console.log(props.score)
  if(props.score == null){
    history.push("/reader")
  }


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
          <Button style={{minHeight: '50vh', minWidth: '100%'}} onClick={onLeft}><ChevronLeftIcon fontSize="large"/></Button>
          <Img src={aruco2}/>
        </Stack>
        {/* <iframe src={"Prelude-Renu.pdf#page=" + page + "&zoom=page-width"} style={{height: '100vh', width: '73vh'}}/> */}
        <iframe src={URL.createObjectURL(props.score)} style={{height: '100vh', width: '73vh'}}/>
        <Stack 
          direction="column"
          justifyContent="space-between"
          alignItems="flex-end"
          style={{height: '100vh', width: '200px'}}
          // divider={<Divider flexItem variant="middle"/>}
        >
          <Img src={aruco1}/>
          <Button style={{minHeight: '50vh', minWidth: '100%'}} onClick={onRight}><ChevronRightIcon fontSize="large"/></Button>
          <Img src={aruco2}/>
        </Stack>
      </Stack>
    </>
  );
}

const Img = styled.img`
  margin: 10mm
`

