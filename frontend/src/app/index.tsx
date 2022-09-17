/**
 *
 * App
 *
 * This component is the skeleton around the actual pages, and should only
 * contain code that should be seen on all pages. (e.g. navigation bar)
 */

import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import { Switch, Route, BrowserRouter, withRouter } from 'react-router-dom';

import { GlobalStyle } from '../styles/global-styles';

import { ReaderPage } from './pages/ReaderPage/Loadable';
import { StartPage } from './pages/StartPage/Loadable';
import { useTranslation } from 'react-i18next';

import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      light: '#8e8e8e',
      main: '#616161',
      dark: '#373737',
      contrastText: '#fff',
    }
  }
});

export function App() {
  const { i18n } = useTranslation();
  
  const [score, setScore] = React.useState(null)

  // const onScoreChange = (score: File) => {
  //   setScore(score)
  // }

  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <React.StrictMode>
          <Helmet
            titleTemplate="%s - Noteation"
            defaultTitle="Noteation"
            htmlAttributes={{ lang: i18n.language }}
          >
            <meta name="description" content="Noteation" />
          </Helmet>

          <Switch>
            <Route exact path={process.env.PUBLIC_URL + '/'} component={withRouter(StartPage)} />
            <Route path={process.env.PUBLIC_URL + '/reader'} component={withRouter(ReaderPage)} />
          </Switch>
          <GlobalStyle />
        </React.StrictMode>
      </BrowserRouter>
    </ThemeProvider>
  );
}
