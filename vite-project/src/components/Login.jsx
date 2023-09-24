// Login.jsx
import { useMsal } from "@azure/msal-react";

function Login() {
    const { instance } = useMsal();


    // const handleLoginPopup()
    return (
        <div className="login-container">
            <button onClick={() => instance.loginPopup()}>Login with Azure AD B2C (popup)</button>
            <button onClick={() => instance.loginRedirect()}>Login with Azure AD B2C (Redirect)</button>
        </div>
    );
}

export default Login;