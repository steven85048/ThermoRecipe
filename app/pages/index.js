import React from 'react';
import ReactDOM from 'react-dom';
import Button from '@material-ui/core/Button';


class Index extends React.Component {
    render() {        
        return (
            <div>
                <meta
                name="viewport"
                content="minimum-scale=1, initial-scale=1, width=device-width"
                />

                <Button variant="contained" color="primary">
                Hello World
                </Button>
            </div>
        );
    }
}

export default Index;