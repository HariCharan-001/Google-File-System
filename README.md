[![Build Status](https://travis-ci.com/Michael-Tu/cppGFS2.0.svg?branch=master)](https://travis-ci.com/Michael-Tu/cppGFS2.0)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# cppGFS2.0
A distributed Google File System (GFS) with multiple masters, implemented in C++

## Getting Started

In this project, we plan to use [Bazel](http://bazel.build) as our main build tool. You can install Bazel by following their website [instructions](https://docs.bazel.build/versions/master/install.html).

For MacOS, you can use Homebrew:

```
brew tap bazelbuild/tap
brew install bazelbuild/tap/bazel
```

For Linux, you can run the `scripts/install_bazel.sh` with desired Bazel version:

```
export BAZEL_VERSION=3.1.0
chmod +x scripts/install_bazel.sh
scripts/install_bazel.sh
```

Then, from the root directory, you can run Bazel commands as normal. For example:

```
bazel build ...
bazel test ...
```

To learn more about how to use Bazel, or how to write Bazel build rule for C++, see the [official documentation](https://docs.bazel.build/versions/master/bazel-overview.html).

## Running servers using Docker

Make sure you have [Docker](https://docs.docker.com/engine/install/) and [Docker compose](https://docs.docker.com/compose/install/) installed

To start all servers and expose respective server ports outside of Docker for connection, run:

```
docker-compose up --build
```

After all servers have started, try it out by running an example client script:

```
bazel run examples:run_mock_protocol_client_main -- \
  --config_path=data/config.yml \
  --use_docker_dns_server=false \
  --master_name=master_server_01 \
  --chunk_server_name=chunk_server_01
```

After you are done with it, turn everything off by either typing Ctrl + C, or using

```
docker-compose down
```

## Known Issues

1. If the initialization of the first file chunk fails at any of the chunk server during file creation, the metadata will be created but chunks won't be initialized, so future file creation on the same filename fails

2. If advance file version command fails on any of the chunk server replica, that chunk server address is still returned in the response to the client, when it should remove the server from return

3. If anything goes wrong with the primary location, we should update the primary server for the chunk handle in both future returns, and in terms of who to send the lease


## C++ Style Guide

Please, if possible, follow [Google C++ style guide](https://google.github.io/styleguide/cppguide.html). If you use an IDE or any common text editors, they have extensions that help you auto format and lint your code for style errors.


