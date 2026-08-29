#!/usr/bin/env bash
# Fetches the two ephemeris datasets used as independent calculation engines.
# Verify the SHA-256 sums against CALCULATION_MANIFEST.json after downloading.
set -euo pipefail
mkdir -p ephe && cd ephe
for f in sepl_18.se1 semo_18.se1 seas_18.se1; do
  echo "fetching $f"
  curl -sSLf -o "$f" "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/$f"
done
echo "fetching de440s.bsp (~32 MB)"
curl -sSLf -o de440s.bsp \
  "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440s.bsp"
sha256sum ./*.se1 de440s.bsp
