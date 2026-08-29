"""Independent validator: JPL DE440s via Skyfield.

Compared against Swiss Ephemeris in the MEAN equinox of date frame
(swe FLG_NONUT vs skyfield ecliptic_latlon(epoch=t)) so the two engines are
expressed in the same reference frame and the residual is a genuine
engine/ephemeris difference rather than a frame mismatch.
"""
import os
from skyfield.api import load_file, load

EPHE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ephe")
_eph = load_file(os.path.join(EPHE, "de440s.bsp"))
_ts = load.timescale(builtin=True)

TARGETS = {
    "Sun": "sun", "Moon": "moon", "Mercury": "mercury barycenter",
    "Venus": "venus barycenter", "Mars": "mars barycenter",
    "Jupiter": "jupiter barycenter", "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter", "Neptune": "neptune barycenter",
    "Pluto": "pluto barycenter",
}


def positions(jd_ut):
    """Apparent geocentric ecliptic longitude, mean ecliptic & equinox of date."""
    t = _ts.ut1_jd(jd_ut)
    earth = _eph["earth"]
    out = {}
    for name, key in TARGETS.items():
        astrometric = earth.at(t).observe(_eph[key]).apparent()
        lat, lon, dist = astrometric.ecliptic_latlon(epoch=t)
        out[name] = {
            "longitude": lon.degrees % 360.0,
            "latitude": lat.degrees,
            "distance_au": dist.au,
        }
    return out


def kernel_info():
    return {
        "kernel": "de440s.bsp",
        "segments": sorted({str(s.target) for s in _eph.segments}),
        "timescale": "builtin (Skyfield bundled leap-second + delta-T tables)",
    }
