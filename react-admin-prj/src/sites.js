// in src/users.js
import React from 'react';
import { List, Datagrid, TextField, Edit, Create, SimpleForm, DisabledInput, TextInput } from 'react-admin';

const NonePagination = ({ page, perPage, total, setPage }) => {
    return ('');
};

export const SiteList = props => (
    <List {...props} exporter={false} pagination={<NonePagination/>}>
        <Datagrid rowClick="edit">
            <TextField source="id" sortable={false} />
            <TextField source="name" sortable={false} />
            <TextField source="title" sortable={false} />
            <TextField source="info" sortable={false} />
            <TextField source="template_dir" sortable={false} />
            <TextField source="template_file" sortable={false} />
            <TextField source="template_assets" sortable={false} />
        </Datagrid>
    </List>
);

export const SiteEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="name" />
            <TextInput source="title" />
            <TextInput source="info" />
            <TextInput source="template_dir" />
            <TextInput source="template_file" />
            <TextInput source="template_assets" />
        </SimpleForm>
    </Edit>
);

export const SiteCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="name" />
            <TextInput source="title" />
            <TextInput source="info" />
            <TextInput source="template_dir" />
            <TextInput source="template_file" />
            <TextInput source="template_assets" />
        </SimpleForm>
    </Create>
);