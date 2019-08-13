import { AUTH_LOGIN, AUTH_LOGOUT, AUTH_ERROR, AUTH_CHECK } from 'react-admin';
import { loginUrl } from './settings';

export default (type, params) => {
    // called when the user attempts to log in
    if (type === AUTH_LOGIN) {
        const { username, password } = params;
        const request = new Request(loginUrl, {
            method: 'POST',
            body: JSON.stringify({ 'username': username, 'password': password }),
            headers: new Headers({ 'Content-Type': 'application/json' })
        });
        localStorage.removeItem('logged_token');
        return fetch(request)
            .then(response => {
                if (response.status !== 200) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then((json_data) => {
                if( json_data.is_logged_in ) {
                    localStorage.setItem('logged_token', json_data.logged_token);
                }
            });
    }
    // called when the user clicks on the logout button
    if (type === AUTH_LOGOUT) {
        localStorage.removeItem('logged_token');
        return Promise.resolve();
    }
    // called when the API returns an error
    if (type === AUTH_ERROR) {
        const { status } = params;
        if (status === 401 || status === 403) {
            localStorage.removeItem('logged_token');
            return Promise.reject();
        }
        return Promise.resolve();
    }
    // called when the user navigates to a new location
    if (type === AUTH_CHECK) {
        return ('logged_token' in localStorage)
            ? Promise.resolve()
            : Promise.reject();
    }
    return Promise.reject('Unknown method');
};