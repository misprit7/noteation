/**
 *
 * App
 *
 * This component is the skeleton around the actual pages, and should only
 * contain code that should be seen on all pages. (e.g. navigation bar)
 */

import * as React from 'react';
import { Helmet } from 'react-helmet-async';
import { Switch, Route, BrowserRouter } from 'react-router-dom';

import { GlobalStyle } from '../styles/global-styles';

import { HomePage } from './pages/HomePage/Loadable';
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
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Helmet
          titleTemplate="%s - Noteation"
          defaultTitle="Noteation"
          htmlAttributes={{ lang: i18n.language }}
        >
          <meta name="description" content="Noteation" />
        </Helmet>

        <Switch>
          <Route exact path={process.env.PUBLIC_URL + '/'} component={StartPage} />
        </Switch>
        <GlobalStyle />
      </BrowserRouter>
    </ThemeProvider>
  );
}
