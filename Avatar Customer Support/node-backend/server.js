const express = require('express');
const fileUpload = require('express-fileupload');
const path = require('path');

const app = express();
const port = 3001;

app.use(express.json());
app.use(fileUpload());

// Set up a static route to serve uploaded files
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

app.post('/process-file', (req, res) => {
    if (!req.files || Object.keys(req.files).length === 0) {
        return res.status(400).send('No files were uploaded.');
    }

    const file = req.files.file; // Assuming your file input in the form is named 'file'
    
    if (!file) {
        return res.status(400).send('File field is missing.');
    }

    const uploadPath = path.join(__dirname, 'uploads', file.name);

    file.mv(uploadPath, (err) => {
        if (err) {
            return res.status(500).send(err);
        }

        // You can add further processing here or send a response
        res.send('File uploaded successfully!');
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
