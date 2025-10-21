#!/usr/bin/env python3
"""eCourts Cause List — Offline JSON Demo (Final Fixed Version)"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime, os, json
from ecourts_api import EcourtsAPI

BASE_DIR = os.path.dirname(__file__)
SAVE_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(SAVE_DIR, exist_ok=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("eCourts Cause List — Offline JSON Demo (Final Fixed)")
        self.geometry("900x600")
        self.api = EcourtsAPI(simulated=True)
        self.state_map, self.dist_map, self.complex_map, self.court_map = {}, {}, {}, {}
        self._build_ui()

    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frm, text="OFFLINE SIMULATION MODE — JSON OUTPUT", foreground="darkred").grid(row=0, column=0, sticky=tk.W, pady=(0,8))
        ttk.Button(frm, text="Load States", command=self.load_states).grid(row=1, column=0, sticky=tk.W)
        self.state_cb = ttk.Combobox(frm, state="readonly", width=46)
        self.state_cb.grid(row=1, column=1, sticky=tk.W)
        ttk.Button(frm, text="Load Districts", command=self.load_districts).grid(row=1, column=2, sticky=tk.W)
        self.dist_cb = ttk.Combobox(frm, state="readonly", width=34)
        self.dist_cb.grid(row=1, column=3, sticky=tk.W)
        ttk.Button(frm, text="Load Complexes", command=self.load_complexes).grid(row=2, column=0, sticky=tk.W)
        self.complex_cb = ttk.Combobox(frm, state="readonly", width=46)
        self.complex_cb.grid(row=2, column=1, sticky=tk.W)
        ttk.Button(frm, text="Load Courts", command=self.load_courts).grid(row=2, column=2, sticky=tk.W)
        self.court_cb = ttk.Combobox(frm, state="readonly", width=34)
        self.court_cb.grid(row=2, column=3, sticky=tk.W)
        ttk.Label(frm, text="Cause List Date (dd-mm-yyyy):").grid(row=3, column=0, sticky=tk.W, pady=(10,0))
        self.date_var = tk.StringVar(value=datetime.date.today().strftime("%d-%m-%Y"))
        ttk.Entry(frm, textvariable=self.date_var, width=20).grid(row=3, column=1, sticky=tk.W)
        ttk.Button(frm, text="Fetch Civil Cause List", command=lambda: self.fetch_causelist('civil')).grid(row=4, column=0, pady=10)
        ttk.Button(frm, text="Fetch Criminal Cause List", command=lambda: self.fetch_causelist('criminal')).grid(row=4, column=1, pady=10)
        ttk.Button(frm, text="Download Entire Cause List", command=self.download_all).grid(row=4, column=2, columnspan=2, sticky=tk.W, pady=10)
        ttk.Separator(frm, orient='horizontal').grid(row=5, column=0, columnspan=4, sticky='ew', pady=8)
        ttk.Label(frm, text="Check Case:").grid(row=6, column=0, sticky=tk.W)
        self.case_entry = ttk.Entry(frm, width=60)
        self.case_entry.grid(row=6, column=1, columnspan=2, sticky=tk.W)
        ttk.Button(frm, text="Check Today/Tomorrow", command=self.check_case).grid(row=6, column=3, sticky=tk.W)
        self.console = tk.Text(frm, height=15, wrap=tk.WORD)
        self.console.grid(row=7, column=0, columnspan=4, sticky="nsew")
        frm.rowconfigure(7, weight=1); frm.columnconfigure(3, weight=1)
        self.log("Ready. Click 'Load States' to start.")

    def log(self, *args):
        self.console.insert(tk.END, " ".join(map(str, args)) + "\n")
        self.console.see(tk.END)

    def load_states(self):
        states = self.api.get_states()
        self.state_map = {f"{s['name']} ({s['code']})": s['code'] for s in states}
        self.state_cb['values'] = list(self.state_map.keys())
        self.log("Loaded states:", len(states))

    def load_districts(self):
        sel = self.state_cb.get()
        if not sel:
            return messagebox.showwarning("Select", "Please select a State")
        state = self.state_map[sel]
        districts = self.api.get_districts(state)
        self.dist_map = {f"{d['name']} ({d['code']})": d['code'] for d in districts}
        self.dist_cb['values'] = list(self.dist_map.keys())
        self.log("Loaded districts:", len(districts))

    def load_complexes(self):
        sel = self.dist_cb.get()
        if not sel:
            return messagebox.showwarning("Select", "Please select a District")
        dist = self.dist_map[sel]
        complexes = self.api.get_complexes(dist)
        self.complex_map = {f"{c['name']} ({c['code']})": c['code'] for c in complexes}
        self.complex_cb['values'] = list(self.complex_map.keys())
        self.log("Loaded complexes:", len(complexes))

    def load_courts(self):
        sel = self.complex_cb.get()
        if not sel:
            return messagebox.showwarning("Select", "Please select a Complex")
        comp = self.complex_map[sel]
        courts = self.api.get_courts(comp)
        self.court_map = {f"{c['name']} ({c['code']})": c['code'] for c in courts}
        self.court_cb['values'] = list(self.court_map.keys())
        self.log("Loaded courts:", len(courts))

    def fetch_causelist(self, mode):
        sel = self.court_cb.get()
        if not sel:
            return messagebox.showwarning("Select", "Please select a Court")
        code = self.court_map[sel]
        date = self.date_var.get().strip()
        data = self.api.generate_sample_causelist_json(code, date, mode)
        filename = os.path.join(SAVE_DIR, f"{code}_{mode}_{date}.json")
        json.dump(data, open(filename, "w", encoding="utf-8"), indent=2)
        self.log("Saved:", filename)
        messagebox.showinfo("Saved", f"JSON file saved: {filename}")

    def download_all(self):
        sel = self.complex_cb.get()
        if not sel:
            return messagebox.showwarning("Select", "Please select a Complex")
        comp = self.complex_map[sel]
        date = self.date_var.get().strip()
        courts = self.api.get_courts(comp)
        for court in courts:
            data = self.api.generate_sample_causelist_json(court['code'], date, 'civil')
            filename = os.path.join(SAVE_DIR, f"{court['code']}_{date}.json")
            json.dump(data, open(filename, "w", encoding="utf-8"), indent=2)
        messagebox.showinfo("Completed", f"Saved {len(courts)} cause list files.")
        self.log("Saved", len(courts), "JSON cause lists.")

    def check_case(self):
        query = self.case_entry.get().strip().lower()
        if not query:
            return messagebox.showwarning("Input", "Enter a case number or query")
        found = []
        for fn in os.listdir(SAVE_DIR):
            if fn.endswith(".json"):
                text = open(os.path.join(SAVE_DIR, fn), encoding="utf-8").read().lower()
                if query in text:
                    found.append(fn)
        if found:
            out_file = os.path.join(SAVE_DIR, f"found_{query}.json")
            json.dump({"query": query, "matches": found}, open(out_file, "w", encoding="utf-8"), indent=2)
            messagebox.showinfo("Found", f"{len(found)} matches found. Saved in {out_file}")
            self.log("Found", len(found), "matches.")
        else:
            messagebox.showinfo("Not Found", "No matches found.")
            self.log("No matches for", query)

if __name__ == "__main__":
    App().mainloop()
