# The Rowan Tree Event Server

The server will generate game world events (content) for all active players.

## Usage

To install the server:
```
pip install rowantree.server
```

To execute the server:
```
python -m rowantree.server.server
```

## Configuration
`rowantree.config` Sample File
```
[DIRECTORY]
logs_dir = ./logs

[DATABASE]
server=127.0.0.1
database=trtdb
username=trt_api_service
password=trt_api_service!123
```
