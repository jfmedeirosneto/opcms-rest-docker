import React from 'react';
import { fetchUtils, Admin, Resource } from 'react-admin';
import { SiteList, SiteEdit } from './sites';
import { UserList, UserEdit, UserCreate } from './users';
import { PortfolioList, PortfolioEdit, PortfolioCreate } from './portfolios';
import { apiUrl } from './settings';
import simpleRestProvider from 'ra-data-simple-rest';
import addUploadFeature from './addUploadFeature';

import Dashboard from './Dashboard';
import authProvider from './authProvider';

import SiteIcon from '@material-ui/icons/Web';
import UserIcon from '@material-ui/icons/Group';

const httpClient = (url, options = {}) => {
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    const logged_token = localStorage.getItem('logged_token');
    options.headers.set('Authorization', `${logged_token}`);
    return fetchUtils.fetchJson(url, options);
}
const dataProvider = simpleRestProvider(apiUrl, httpClient);
const uploadCapableDataProvider = addUploadFeature(dataProvider);

const App = () => (
    <Admin dashboard={Dashboard} authProvider={authProvider} dataProvider={uploadCapableDataProvider}>
        <Resource name="sites" list={SiteList} edit={SiteEdit} icon={SiteIcon} />
        <Resource name="users" list={UserList} edit={UserEdit} create={UserCreate} icon={UserIcon} />
        <Resource name="portfolios" list={PortfolioList} edit={PortfolioEdit} create={PortfolioCreate} />
    </Admin>
);

export default App;