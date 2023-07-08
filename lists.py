class_list = [(0, "Flagship"), (1, "Probe"),
              (2, "Medium-class Explorer (MIDEX)"), (3, "Small Explorer (SMEX)")]
class_list_cost = [10000, 5000, 2000, 1000]
location_list = [(0, "Near Earth Orbit [Hubble]"), (1, "L2 [JWST]"), (2, "Other Solar System Orbit [Spitzer]"),
                 (3, "The Moon [Artemis]"), (4, "Outside of the Solar System [Voyager]")]
location_list_cost = [1000, 100, 100, 100, 100]
wavelength_list = [(0, "Gamma Ray"), (1, "X-Ray"), (2, "UV"), (3, "Visible"),
                   (4, "Infrared"), (5, "Microwave/Sub-millimeter"), (6, "Radio")]
wavelength_list_cost = [100, 100, 100, 100, 100, 100, 100]
temperature_list = [
    (0, "No Cooling"), (1, "Actively Cooled [Spitzer]"), (2, "Passively Cooled")]
temperature_list_cost = [100, 100, 100]
design_list = [(0, "Standard tube [Hubble]"),
               (1, "Open mirror plus sun shield [JWST]")]
design_list_cost = [100, 100]
optics_list = [(0, "Standard mirror [Hubble]"), (1, "Segmented mirror [JWST]"),
               (2, "Parabolic grazing incidence mirror [Chandra]"), (3, "No Mirror [Fermi]")]
optics_list_cost = [100, 100, 100, 100]
fov_list = [(0, "Narrow [Hubble]"), (1, "Wide [Roman]")]
fov_list_cost = [100, 100]
instrument_list = [(0, "Imager (camera)"), (1, "Photometers"),
                   (2, "Spectrographs"), (3, "Polarimeters")]
instrument_list_cost = [100, 100, 100, 100]
extras_list = [(0, "Coronograph"), (1, "Starshade")]
extras_list_cost = [200, 200]
