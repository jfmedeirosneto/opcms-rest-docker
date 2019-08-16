import React from 'react';
import { List, Datagrid, TextField, Edit, Create, SimpleForm, DisabledInput, TextInput, ImageInput, ImageField } from 'react-admin';

const NonePagination = ({ page, perPage, total, setPage }) => {
    return ('');
};

export const PortfolioList = props => (
    <List {...props} exporter={false} pagination={<NonePagination />}>
        <Datagrid rowClick="edit">
            <TextField source="id" sortable={false} />
            <TextField source="category" sortable={false} />
            <TextField source="project_name" sortable={false} />
        </Datagrid>
    </List>
);

export const PortfolioEdit = props => (
    <Edit {...props}>
        <SimpleForm>
            <DisabledInput source="id" />
            <TextInput source="category" fullWidth />
            <TextInput source="project_name" fullWidth />
            <ImageInput source="pictures" label="Portfolio picture" accept="image/*" maxSize={5242880} multiple={true} placeholder={<p>Drop some pictures to upload, or click to select one.<br/>JPEG and PNG are accepted.<br/>5Mb maximun file size.<br/>(650 x 350) minimun file width and height.</p>}>
                <ImageField source="thumbnail_url" title="title" />
            </ImageInput>
        </SimpleForm>
    </Edit>
);

export const PortfolioCreate = props => (
    <Create {...props}>
        <SimpleForm>
            <TextInput source="category" fullWidth />
            <TextInput source="project_name" fullWidth />
        </SimpleForm>
    </Create>
);