
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import re


class PharmDataToolGUI:
    """
    Main GUI window for the Centrala University
    Pharmaceutical Data Management Tool.
    Demonstrates recognised HCI design principles
    throughout (Nielsen, 1994).
    """

    def __init__(self, root):
        self.root = root
        self.root.title(
            "Centrala University — Pharmaceutical Data Tool v1.0"
        )
        self.root.geometry("680x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f4f8")

        self._build_header()
        self._build_date_section()
        self._build_action_buttons()
        self._build_status_bar()
        self._build_results_area()
        self._build_footer_buttons()

    def _build_header(self):
        """Application title header."""
        header = tk.Label(
            self.root,
            text="Centrala University — Pharmaceutical Data Tool",
            font=("Arial", 14, "bold"),
            bg="#2e4057",
            fg="white",
            pady=12
        )
        header.pack(fill=tk.X)

    def _build_date_section(self):
        """
        Date input section with default value of today.
        Demonstrates: Error Prevention (Nielsen Heuristic 5)
        Pre-populating with today's date reduces input errors.
        """
        date_frame = tk.Frame(self.root, bg="#f0f4f8", pady=12)
        date_frame.pack(fill=tk.X, padx=20)

        tk.Label(
            date_frame,
            text="Target Date:",
            font=("Arial", 11),
            bg="#f0f4f8"
        ).pack(side=tk.LEFT)

        self.date_entry = tk.Entry(
            date_frame,
            font=("Arial", 11),
            width=16,
            bd=2,
            relief=tk.GROOVE
        )
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.date_entry.pack(side=tk.LEFT, padx=8)

        tk.Button(
            date_frame,
            text="Today",
            font=("Arial", 10),
            bg="#4a90d9",
            fg="white",
            relief=tk.FLAT,
            padx=8,
            command=self._reset_to_today
        ).pack(side=tk.LEFT)

    def _build_action_buttons(self):
        """
        Main action button.
        Demonstrates: Recognition Rather Than Recall
        (Nielsen Heuristic 6) — all actions are visible as buttons.
        """
        btn_frame = tk.Frame(self.root, bg="#f0f4f8", pady=4)
        btn_frame.pack(fill=tk.X, padx=20)

        tk.Button(
            btn_frame,
            text="⬇  Download & Validate Files",
            font=("Arial", 12, "bold"),
            bg="#2e7d32",
            fg="white",
            relief=tk.FLAT,
            padx=16,
            pady=8,
            command=self._run_download
        ).pack(side=tk.LEFT)

    def _build_status_bar(self):
        """
        Status bar showing current system state.
        Demonstrates: Visibility of System Status
        (Nielsen Heuristic 1).
        """
        status_frame = tk.Frame(
            self.root, bg="#dce8f5", pady=6, padx=12
        )
        status_frame.pack(fill=tk.X, padx=20, pady=6)

        tk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 10, "bold"),
            bg="#dce8f5"
        ).pack(side=tk.LEFT)

        self.status_label = tk.Label(
            status_frame,
            text="  Ready — awaiting action.",
            font=("Arial", 10),
            bg="#dce8f5",
            fg="#1a1a2e"
        )
        self.status_label.pack(side=tk.LEFT)

    def _build_results_area(self):
        """Scrollable results display area."""
        tk.Label(
            self.root,
            text="Results:",
            font=("Arial", 11, "bold"),
            bg="#f0f4f8",
            anchor="w"
        ).pack(fill=tk.X, padx=20)

        self.results_box = scrolledtext.ScrolledText(
            self.root,
            height=12,
            font=("Courier", 10),
            bg="white",
            relief=tk.GROOVE,
            bd=2,
            state=tk.DISABLED
        )
        self.results_box.pack(fill=tk.BOTH, padx=20, pady=4)

    def _build_footer_buttons(self):
        """
        Footer buttons for secondary actions.
        Demonstrates: User Control and Freedom
        (Nielsen Heuristic 3).
        """
        footer_frame = tk.Frame(self.root, bg="#f0f4f8", pady=8)
        footer_frame.pack(fill=tk.X, padx=20)

        tk.Button(
            footer_frame,
            text="View Error Log",
            font=("Arial", 10),
            bg="#c62828",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=self._view_error_log
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            footer_frame,
            text="Clear Results",
            font=("Arial", 10),
            bg="#757575",
            fg="white",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=self._clear_results
        ).pack(side=tk.LEFT, padx=4)

    # --- Event Handlers ---

    def _reset_to_today(self):
        """Resets the date field to today's date."""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

    def _validate_date_input(self, date_str):
        """
        Validates the date entry before attempting download.
        Demonstrates: Error Prevention (Nielsen Heuristic 5).
        """
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not pattern.match(date_str):
            return False
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def _write_result(self, text, colour="black"):
        """Appends a line of text to the results box."""
        self.results_box.configure(state=tk.NORMAL)
        self.results_box.insert(tk.END, text + "\n")
        self.results_box.configure(state=tk.DISABLED)
        self.results_box.see(tk.END)

    def _update_status(self, message):
        """Updates the status bar label."""
        self.status_label.configure(text=f"  {message}")
        self.root.update_idletasks()

    def _run_download(self):
        """
        Handles the Download & Validate button click.
        Simulates the full workflow with live status updates.
        Demonstrates: Visibility of System Status
        (Nielsen Heuristic 1).
        """
        date_str = self.date_entry.get().strip()

        if not self._validate_date_input(date_str):
            messagebox.showerror(
                "Invalid Date",
                "Please enter a valid date in YYYY-MM-DD format.\n"
                "Example: 2023-06-03"
            )
            return

        self._clear_results()
        date_nodash = date_str.replace('-', '')

        self._update_status("Connecting to FTP server...")
        self._write_result(f"Connecting to FTP server...  ✓ Connected")

        self._update_status(f"Searching for files dated {date_str}...")
        self._write_result(f"Searching for files dated {date_str}...")

        files = [
            (f"MED_DATA_{date_nodash}140104.csv", True),
            (f"MED_DATA_{date_nodash}140512.csv", False),
            (f"MED_DATA_{date_nodash}141000.csv", True),
        ]

        self._write_result(f"  Found {len(files)} new file(s).\n")

        stored = 0
        rejected = 0

        for filename, is_valid in files:
            self._update_status(f"Processing {filename}...")
            if is_valid:
                self._write_result(
                    f"  {filename}  →  ✓ VALID — Stored"
                )
                stored += 1
            else:
                self._write_result(
                    f"  {filename}  →  ✗ INVALID — Logged"
                )
                rejected += 1

        self._write_result(
            f"\n  Summary: {stored} stored, "
            f"{rejected} rejected."
        )
        self._update_status(
            f"✓ Complete — {stored} stored, {rejected} rejected."
        )

    def _view_error_log(self):
        """Shows a popup with the error log contents."""
        messagebox.showinfo(
            "Error Log",
            "Error log location: /logs/error_log.csv\n\n"
            "No errors logged yet in this session."
        )

    def _clear_results(self):
        """Clears the results display area."""
        self.results_box.configure(state=tk.NORMAL)
        self.results_box.delete(1.0, tk.END)
        self.results_box.configure(state=tk.DISABLED)
        self._update_status("Results cleared — ready.")


def run_gui():
    root = tk.Tk()
    app = PharmDataToolGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()