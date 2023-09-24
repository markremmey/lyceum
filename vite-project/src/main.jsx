import React from 'react'
import ReactDOM from 'react-dom/client'

import { MsalProvider } from "@azure/msal-react";
import { PublicClientApplication } from "@azure/msal-browser";
import App from './App.jsx'
import './index.css'

export const msalInstance = new PublicClientApplication({
  auth: {
      clientId: "ca02e15c-f52d-4dab-8dec-41c1611c5095",
      authority: "https://lyceummembers.b2clogin.com/lyceummembers.onmicrosoft.com/B2C_1_signup-signin",
      redirectUri: "http://localhost:5173/",
      knownAuthorities: ["lyceummembers.b2clogin.com"]
  },
});


// Log tokens (Take out in production)
// const { accounts, instance } = useMsal();
// console.log("Authenticated accounts:", accounts);
// // Or
// console.log("Current instance:", instance);

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    <MsalProvider instance={msalInstance}>
      <App />
    </MsalProvider>
  </React.StrictMode>
);