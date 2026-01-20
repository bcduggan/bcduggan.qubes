#!/usr/bin/sh

set -euf

COLLECTION=$(yq '"\(.namespace)-\(.name)-\(.version)"' galaxy.yml 2>/dev/null || echo)

[ -n "${COLLECTION}" ] && export COLLECTION
