import React from "react";
import {ThemeProvider} from "styled-components";
import theme from "./theme";
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import Root from "./routes/Root";
import Training from "./routes/Training";
import Testing from "./routes/Testing";
import AboutUs from "./routes/AboutUs"

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />
  },
  {
    path: "/training",
    element: <Training />,
    loader: async () => {
      return await fetch("http://127.0.0.1:8000/ecg-png")
    }
  },
  {
    path: "/testing",
    element: <Testing />
  },
  {
    path: "/about-us",
    element: <AboutUs />
  }
])

function App() {
  return (
    <ThemeProvider theme={theme}>
      <RouterProvider router={router}/>
    </ThemeProvider>
  );
}

export default App;
