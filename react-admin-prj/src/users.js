// in src/users.js
import React from 'react';
import { List, Datagrid, TextField, EmailField, Edit, Create, SimpleForm, DisabledInput, TextInput } from 'react-admin';

const NonePagination = ({ page, perPage, total, setPage }) => {
    return ('');
};

export const UserList = props => (
    <List {...props} exporter={false} pagination={<NonePagination/>}>
        <Datagrid rowClick="edit">
            <TextField source="id" sortable={false} />
            <TextField source="username" sortable={false} />
            <TextField source="name" sortable={false} />
            <EmailField source="email" sortable={false} />
        </Datagrid>
    </List>
);

export const UserEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="username" />
            <TextInput source="password" type="password" />
            <TextInput source="name" />
            <TextInput source="email" type="email" />
        </SimpleForm>
    </Edit>
);

export const UserCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="username" />
            <TextInput source="password"  type="password" />
            <TextInput source="name" />
            <TextInput source="email" type="email" />
        </SimpleForm>
    </Create>
);