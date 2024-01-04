### Banner
![Static Badge](https://img.shields.io/badge/Python-3.12-blue)
![Static Badge](https://img.shields.io/badge/License-MIT-green)

### Basic Overview
Enphase (v4) API client to monitor home energy systems. Please review their
[documentation](https://developer-v4.enphase.com/docs.html) for more information.

### Current Support
* Generate access and refresh tokens
* GET /api/v4/systems/{system_id}
* GET /api/v4/systems/{system_id}/summary
* GET /api/v4/systems/{system_id}/devices

### Installation
Using pip
```bash
pip install enphase-home-api-client
```

### Usage
Please review Enphase's [quickstart](https://developer-v4.enphase.com/docs/quickstart.html)
document and set up your account and application accordingly. The client requires specific variables
to be set in order to run. These variables can be set in the environment or a configuration file.

#### Environment Variables
* ENPHASE_CODE (required)
* ENPHASE_CLIENT_ID (required)
* ENPHASE_CLIENT_SECRET (required)
* ENPHASE_API_KEY (required)
* ENPHASE_SYSTEM_ID (required)
* ENPHASE_REFRESH_TOKEN (optional)
* ENPHASE_ACCESS_TOKEN (optional)

#### Configuration
Instead of setting environment variables, you can create a configuration file in the root directory of the project
called enphase-configuration.json.<br />
`
example of the file
`

### Contributing
Please review the contributing guidelines if you would like to add to this project!
