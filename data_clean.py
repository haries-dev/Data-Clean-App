import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pandastable import Table
import threading

class DataCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Cleaner | Haries Palaniappan")
        self.root.geometry("900x700")

        # Frame for Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Load Data Button
        self.load_button = ttk.Button(self.button_frame, text="Load CSV", command=self.load_csv)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Automatic Cleaning Button
        self.auto_clean_button = ttk.Button(self.button_frame, text="Automatic Clean", command=self.automatic_clean_window)
        self.auto_clean_button.pack(side=tk.LEFT, padx=5)

        # Manual Cleaning Button
        self.manual_clean_button = ttk.Button(self.button_frame, text="Manual Clean", command=self.manual_clean)
        self.manual_clean_button.pack(side=tk.LEFT, padx=5)

        # Split Data Button
        self.split_button = ttk.Button(self.button_frame, text="Split Data", command=self.split_data)
        self.split_button.pack(side=tk.LEFT, padx=5)

        # Find and Replace Button
        self.find_replace_button = ttk.Button(self.button_frame, text="Find and Replace", command=self.find_replace)
        self.find_replace_button.pack(side=tk.LEFT, padx=5)

        # Save Data Button
        self.save_button = ttk.Button(self.button_frame, text="Save CSV", command=self.save_csv)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Frame for Table Preview
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=1)

        # Placeholder for Pandas DataFrame and Table
        self.df = None
        self.pt = None

        # Progress Bar
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(side=tk.BOTTOM, fill=tk.X)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file_path:
            self.progress.start()
            threading.Thread(target=self._load_csv_thread, args=(file_path,)).start()

    def _load_csv_thread(self, file_path):
        self.df = pd.read_csv(file_path)
        self.show_preview()
        self.progress.stop()
        messagebox.showinfo("Info", "CSV Loaded Successfully!")

    def show_preview(self):
        if self.df is not None:
            if self.pt:
                self.pt.destroy()

            # Display DataFrame with watermark in headers (for visualization only)
            df_display = self.df.copy()
            df_display.columns = [f"{col}" for col in df_display.columns]

            self.pt = Table(self.table_frame, dataframe=df_display, showtoolbar=True, showstatusbar=True)
            self.pt.show()

    def automatic_clean_window(self):
        if self.df is not None:
            config_window = tk.Toplevel(self.root)
            config_window.title("Automatic Clean Configuration | Haries Palaniappan")
            config_window.geometry("400x300")

            # Checkboxes for different cleaning options
            self.remove_duplicates_var = tk.BooleanVar(value=True)
            remove_duplicates_cb = ttk.Checkbutton(config_window, text="Remove Duplicates", variable=self.remove_duplicates_var)
            remove_duplicates_cb.pack(anchor='w', padx=10, pady=5)

            self.trim_whitespace_var = tk.BooleanVar(value=True)
            trim_whitespace_cb = ttk.Checkbutton(config_window, text="Trim Whitespace", variable=self.trim_whitespace_var)
            trim_whitespace_cb.pack(anchor='w', padx=10, pady=5)

            self.remove_symbols_var = tk.BooleanVar(value=False)
            remove_symbols_cb = ttk.Checkbutton(config_window, text="Remove Symbols", variable=self.remove_symbols_var)
            remove_symbols_cb.pack(anchor='w', padx=10, pady=5)

            self.fill_missing_values_var = tk.BooleanVar(value=False)
            fill_missing_values_cb = ttk.Checkbutton(config_window, text="Fill Missing Values", variable=self.fill_missing_values_var)
            fill_missing_values_cb.pack(anchor='w', padx=10, pady=5)

            apply_button = ttk.Button(config_window, text="Apply", command=self.automatic_clean)
            apply_button.pack(pady=20)
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first!")

    def automatic_clean(self):
        if self.df is not None:
            # Apply selected cleaning operations
            if self.remove_duplicates_var.get():
                self.df.drop_duplicates(inplace=True)
            if self.trim_whitespace_var.get():
                self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            if self.remove_symbols_var.get():
                self.df = self.df.replace(r'[^A-Za-z0-9\s]', '', regex=True)
            if self.fill_missing_values_var.get():
                self.df.fillna("Unknown", inplace=True)

            self.show_preview()
            messagebox.showinfo("Info", "Automatic Cleaning Done!")
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first!")

    def manual_clean(self):
        if self.df is not None:
            config_window = tk.Toplevel(self.root)
            config_window.title("Manual Configuration | Haries Palaniappan")
            config_window.geometry("400x250")

            tk.Label(config_window, text="Enter Characters to Remove (e.g., \"â‚¹\",\"*\"):").pack(pady=5)
            chars_entry = ttk.Entry(config_window)
            chars_entry.insert(0, "\"â‚¹\"")  # Placeholder
            chars_entry.pack(pady=5)

            clean_all_var = tk.BooleanVar()
            clean_all_checkbox = ttk.Checkbutton(config_window, text="Clean All", variable=clean_all_var)
            clean_all_checkbox.pack(pady=5)

            def apply_manual_clean():
                chars = chars_entry.get()
                chars_to_remove = [char.strip().strip('"') for char in chars.split(',')]
                if clean_all_var.get():
                    for char in chars_to_remove:
                        self.df = self.df.replace({char: ''}, regex=True)
                else:
                    for char in chars_to_remove:
                        self.df = self.df.replace({char: ''}, regex=True)
                        self.show_preview()
                        messagebox.showinfo("Info", f"Manual Cleaning Done for '{char}'!")
                self.show_preview()
                messagebox.showinfo("Info", "Manual Cleaning Done!")
                config_window.destroy()

            apply_button = ttk.Button(config_window, text="Apply", command=apply_manual_clean)
            apply_button.pack(pady=10)
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first!")

    def split_data(self):
        if self.df is not None:
            split_window = tk.Toplevel(self.root)
            split_window.title("Split Data Configuration | Haries Palaniappan")
            split_window.geometry("300x150")

            tk.Label(split_window, text="Enter Range (e.g., 0-10000):").pack(pady=5)
            range_entry = ttk.Entry(split_window)
            range_entry.pack(pady=5)

            def apply_split():
                range_str = range_entry.get()
                try:
                    # Parse the range input
                    start, end = map(int, range_str.split('-'))

                    # Check if start is less than or equal to end
                    if start > end:
                        raise ValueError("Start of range cannot be greater than end.")

                    # Identify numeric columns in the DataFrame
                    numeric_cols = self.df.select_dtypes(include='number').columns.tolist()
                    if not numeric_cols:
                        raise ValueError("No numeric columns found in the DataFrame.")

                    # Assuming splitting based on the first numeric column for simplicity
                    column_name = numeric_cols[0]
                    df_no_watermark = self.df.copy()

                    # Create intervals for splitting
                    intervals = list(range(start, end + 1, (end - start) // 10))
                    intervals.append(end + 1)  # To include the end value in the last interval

                    for i in range(len(intervals) - 1):
                        lower_bound = intervals[i]
                        upper_bound = intervals[i + 1]
                        split_df = df_no_watermark[(df_no_watermark[column_name] >= lower_bound) & (df_no_watermark[column_name] < upper_bound)]
                        split_df.to_csv(f"split_{lower_bound}_{upper_bound}.csv", index=False)

                    self.show_preview()
                    messagebox.showinfo("Info", "Data Split Done!")
                    split_window.destroy()
                except ValueError as ve:
                    messagebox.showerror("Error", f"Invalid input: {ve}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to split data: {e}")

            apply_button = ttk.Button(split_window, text="Apply", command=apply_split)
            apply_button.pack(pady=10)
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first!")

    def find_replace(self):
        if self.df is not None:
            find_replace_window = tk.Toplevel(self.root)
            find_replace_window.title("Find and Replace | Haries Palaniappan")
            find_replace_window.geometry("400x200")

            tk.Label(find_replace_window, text="Find:").pack(pady=5)
            find_entry = ttk.Entry(find_replace_window)
            find_entry.pack(pady=5)

            tk.Label(find_replace_window, text="Replace:").pack(pady=5)
            replace_entry = ttk.Entry(find_replace_window)
            replace_entry.pack(pady=5)

            def apply_find_replace():
                find_text = find_entry.get()
                replace_text = replace_entry.get()
                if find_text:
                    self.df.replace(find_text, replace_text, inplace=True)
                    self.show_preview()
                    messagebox.showinfo("Info", f"Replaced '{find_text}' with '{replace_text}'")
                    find_replace_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Please enter text to find!")

            apply_button = ttk.Button(find_replace_window, text="Apply", command=apply_find_replace)
            apply_button.pack(pady=10)
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first!")

    def save_csv(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                self.df.to_csv(file_path, index=False)
                messagebox.showinfo("Info", "CSV Saved Successfully!")
        else:
            messagebox.showwarning("Warning", "No data to save!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataCleanerApp(root)
    root.mainloop()
