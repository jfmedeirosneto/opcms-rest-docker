import React from 'react';
import { List, Datagrid, TextField, Edit, Create, SimpleForm, DisabledInput, TextInput, LongTextInput } from 'react-admin';

const NonePagination = ({ page, perPage, total, setPage }) => {
    return ('');
};

export const SiteList = props => (
    <List {...props} exporter={false} pagination={<NonePagination />}>
        <Datagrid rowClick="edit">
            <TextField source="id" sortable={false} />
            <TextField source="name" sortable={false} />
            <TextField source="site_title" sortable={false} />
        </Datagrid>
    </List>
);

export const SiteEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="name" fullWidth />
            <TextInput source="site_title" fullWidth />
            <LongTextInput source="site_description" fullWidth />
            <TextInput source="site_copyright" fullWidth />
            <TextInput source="page_title" fullWidth />
            <LongTextInput source="page_content" fullWidth />
            <TextInput source="owner_name" fullWidth />
            <TextInput source="owner_email" type="email" fullWidth />
            <LongTextInput source="owner_address" fullWidth />
            <TextInput source="owner_map_url" fullWidth />
            <TextInput source="owner_phones" label="Owner phones (comma separated)" parse={v => v.split(',')} fullWidth />
            <TextInput source="owner_whatsapp_phones" label="Owner whatsapp phones (comma separated)" parse={v => v.split(',')} fullWidth />
            <TextInput source="owner_facebook_url" fullWidth />
            <TextInput source="owner_twitter_url" fullWidth />
            <TextInput source="owner_instagram_url" fullWidth />
            <TextInput source="template_dir" fullWidth />
            <TextInput source="template_file" fullWidth />
            <TextInput source="template_assets" label="Template assets (comma separated)" parse={v => v.split(',')} fullWidth />
        </SimpleForm>
    </Edit>
);

export const SiteCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="name" fullWidth />
            <TextInput source="site_title" fullWidth />
            <LongTextInput source="site_description" fullWidth />
            <TextInput source="site_copyright" fullWidth />
            <TextInput source="page_title" fullWidth />
            <LongTextInput source="page_content" fullWidth />
            <TextInput source="owner_name" fullWidth />
            <TextInput source="owner_email" type="email" fullWidth />
            <LongTextInput source="owner_address" fullWidth />
            <TextInput source="owner_map_url" fullWidth />
            <TextInput source="owner_phones" label="Owner phones (comma separated)" parse={v => v.split(',')} fullWidth />
            <TextInput source="owner_whatsapp_phones" label="Owner whatsapp phones (comma separated)" parse={v => v.split(',')} fullWidth />
            <TextInput source="owner_facebook_url" fullWidth />
            <TextInput source="owner_twitter_url" fullWidth />
            <TextInput source="owner_instagram_url" fullWidth />
            <TextInput source="template_dir" fullWidth />
            <TextInput source="template_file" fullWidth />
            <TextInput source="template_assets" label="Template assets (comma separated)" parse={v => v.split(',')} fullWidth />
        </SimpleForm>
    </Create>
);