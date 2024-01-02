import argparse
import yaml

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate a Docker Compose file.')
parser.add_argument('--master_servers', type=int, default = 1, help='Number of master servers.')
parser.add_argument('--chunk_servers', type=int, default = 3, help='Number of chunk servers.')
parser.add_argument('--master_start_port', type=int, default = 50051, help='Starting port for master servers.')
parser.add_argument('--chunk_start_port', type=int, default = 60051, help='Starting port for chunk servers.')
args = parser.parse_args()

# Initialize services dictionary
services = {}

# Add master servers
for i in range(args.master_servers):
    port = args.master_start_port + i
    services[f'master_server_{i+1:02}'] = {
        'container_name': f'master_server_{i+1:02}',
        'build': {
            'context': '.',
            'dockerfile': 'Dockerfile'
        },
        'image': 'gfs-image',
        'command': 'bazel run src/server/master_server:run_master_server_main -- --config_path=data/config.yml --use_docker_dns_server --master_name=master_server_' + f'{i+1:02}',
        'working_dir': '/app',
        'ports': [f'{port}:{port}'],
        'volumes': ['./:/app'],
        'restart': 'unless-stopped'
    }

# Add chunk servers
for i in range(args.chunk_servers):
    port = args.chunk_start_port + i
    services[f'chunk_server_{i+1:02}'] = {
        'container_name': f'chunk_server_{i+1:02}',
        'image': 'gfs-image',
        'command': 'bazel run src/server/chunk_server:run_chunk_server_main -- --config_path=data/config.yml --use_docker_dns_server --chunk_server_name=chunk_server_ ' + f'{i+1:02}',
        'ports': [f'{port}:{port}'],
        'depends_on': [f'master_server_{i%args.master_servers+1:02}'],
        'working_dir': '/app',
        'volumes': ['./:/app'],
        'restart': 'unless-stopped'
    }

# Create config dictionary
config = {
    'version': '3.7',
    'services': services
}

# Write to docker-compose.yml
with open('docker-compose.yml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)