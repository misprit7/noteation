import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Stack from '@mui/material/Stack';
import logo from './assets/logo.png';
import background from './assets/background.png';
import styled from 'styled-components/macro';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import { useHistory } from "react-router-dom";
import { useState } from 'react';


export function StartPage(props) {

  const history = useHistory()
  const [prevTimestamp, setPrevTimestamp] = useState(0);

  const onFileUpload = (e: React.FormEvent<HTMLInputElement>) => {
    history.push("/reader")
    if(e?.currentTarget?.files != null)
      props.onScoreChange(e.currentTarget.files[0])
  }

  const makeQuery = () => {
    const API_URL: string = "https://283d-2620-101-f000-704-00-f5.ngrok.io";
    var requestOptions: RequestInit = {
      method: 'GET',
      redirect: 'follow'
    };
    
    return fetch(API_URL + `/events/${prevTimestamp}`, requestOptions)
      .then(response => {
        return response.json();
      })
      .then(json => {
        let events: Array<string> = json["events"];
        return events
      })
      .catch(error => console.log('error', error));
  }

  console.log(makeQuery());

  return (
    <Bg>
      <Helmet>
        <title>Start</title>
      </Helmet>
      <Stack justifyContent="center" alignItems="center" spacing={10}>
        <Img src={logo}/>
        <Button variant="contained" component="label" style={{minWidth: 100}}>
          <AudioFileIcon/>
          <input
            type="file"
            accept="application/pdf"
            hidden
            onChange={onFileUpload}
          />
        </Button>
      </Stack>
    </Bg>
  );
}

const Img = styled.img`
  width: 40%;
`;

const Bg = styled.div`
  background-image: url(${background});
  width: 100vw;
  height: 100vh;
`

