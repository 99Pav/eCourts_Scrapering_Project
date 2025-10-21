import datetime, random
class EcourtsAPI:
    def __init__(self, simulated=True):
        self.simulated = simulated
        self.base_url = "https://services.ecourts.gov.in/ecourtindia_v6/"
        self._states = [
            {"code": "01", "name": "Andhra Pradesh"},
            {"code": "24", "name": "Telangana"},
            {"code": "14", "name": "Maharashtra"}
        ]
        self._districts = {
            "01": [{"code": "0101", "name": "Visakhapatnam"}],
            "24": [{"code": "2401", "name": "Hyderabad"}],
            "14": [{"code": "1401", "name": "Mumbai"}]
        }
        self._complexes = {
            "0101": [{"code": "C0101", "name": "Visakhapatnam Complex"}],
            "2401": [{"code": "C2401", "name": "Hyderabad Complex"}],
            "1401": [{"code": "C1401", "name": "Mumbai Complex"}]
        }
        self._courts = {
            "C0101": [{"code": "C0101_CRT_1", "name": "Vizag Court 1"}, {"code": "C0101_CRT_2", "name": "Vizag Court 2"}],
            "C2401": [{"code": "C2401_CRT_1", "name": "Hyderabad Court 1"}, {"code": "C2401_CRT_2", "name": "Hyderabad Court 2"}],
            "C1401": [{"code": "C1401_CRT_1", "name": "Mumbai Court 1"}, {"code": "C1401_CRT_2", "name": "Mumbai Court 2"}]
        }

    def get_states(self): return self._states
    def get_districts(self, state): return self._districts.get(state, [])
    def get_complexes(self, dist): return self._complexes.get(dist, [])
    def get_courts(self, comp): return self._courts.get(comp, [])

    def generate_sample_causelist_json(self, code, date, mode='civil'):
        date_fmt = datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        cases = []
        for i in range(1, random.randint(4, 8)):
            cases.append({
                "serial_no": i,
                "case_no": f"CNR{code[-4:]}{i:04d}{date[-4:]}",
                "petitioner": f"Petitioner {i}",
                "respondent": f"Respondent {i}"
            })
        return {
            "court_code": code,
            "court_name": f"{code} Simulated Court",
            "date": date_fmt,
            "mode": mode,
            "cases": cases
        }
