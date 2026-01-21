#!/usr/bin/bash

set -eufo pipefail

source /dev/stdin <<EOF
$(yq '"BQ_NAMESPACE=\(.namespace)
BQ_NAME=\(.name)
BQ_VERSION=\(.version)"' galaxy.yml)
BQ_BUMPED_VERSION=$(git-cliff --bumped-version)
EOF

export BQ_NAMESPACE
export BQ_NAME
export BQ_VERSION
export BQ_BUMPED_VERSION
