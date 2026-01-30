"""
PDF DownSizing Tool - Main GUI Application
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from working_pdf_compressor import WorkingPDFCompressor
from drag_drop_handler import DragDropHandler, SimpleDragDropHandler


class PDFDownSizingApp:
    """Main application class for PDF compression tool"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.compressor = WorkingPDFCompressor()
        self.setup_drag_drop()
        
    def setup_window(self):
        """Configure main window"""
        self.root.title("PDF DownSizing Tool_Dino v1.0")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Center window on screen
        self.center_window()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_variables(self):
        """Initialize tkinter variables"""
        self.selected_file = tk.StringVar()
        self.quality_var = tk.IntVar(value=80)
        self.status_var = tk.StringVar(value="Ready to compress PDF files")
        self.progress_var = tk.DoubleVar()
        
    def setup_ui(self):
        """Create and layout UI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF DownSizing Tool", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF File", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # File path display
        self.file_entry = ttk.Entry(file_frame, textvariable=self.selected_file, 
                                   state="readonly", width=50)
        self.file_entry.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Drag and drop info
        drop_label = ttk.Label(file_frame, text="Or drag and drop PDF file here", 
                              font=("Arial", 9), foreground="gray")
        drop_label.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # Quality settings frame
        quality_frame = ttk.LabelFrame(main_frame, text="Compression Settings", padding="10")
        quality_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        quality_frame.columnconfigure(1, weight=1)
        
        # Quality slider
        ttk.Label(quality_frame, text="Quality:").grid(row=0, column=0, sticky=tk.W)
        self.quality_scale = ttk.Scale(quality_frame, from_=1, to=100, 
                                      variable=self.quality_var, orient=tk.HORIZONTAL)
        self.quality_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        # Quality value display
        self.quality_label = ttk.Label(quality_frame, text="80")
        self.quality_label.grid(row=0, column=2)
        
        # Quality description
        quality_desc = ttk.Label(quality_frame, 
                                text="Higher values = better quality, larger file size", 
                                font=("Arial", 8), foreground="gray")
        quality_desc.grid(row=1, column=0, columnspan=3, pady=(5, 0))
        
        # File info frame
        info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10")
        info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        self.info_text = tk.Text(info_frame, height=4, wrap=tk.WORD, state=tk.DISABLED)
        self.info_text.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(1, weight=1)
        
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, sticky=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           mode='determinate')
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        
        # Control buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        # Compress button
        self.compress_btn = ttk.Button(button_frame, text="Start Compression", 
                                      command=self.start_compression)
        self.compress_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_selection)
        clear_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Exit button
        exit_btn = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_btn.grid(row=0, column=2)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Bind events
        self.quality_scale.bind('<Motion>', self.update_quality_label)
        self.quality_var.trace_add('write', self.update_quality_label)
        
        # Initialize quality label
        self.update_quality_label()
    
    def setup_drag_drop(self):
        """Setup drag and drop functionality"""
        try:
            # Try to use advanced drag and drop
            self.drag_drop = DragDropHandler(self.root, self.handle_dropped_file)
        except:
            # Fallback to simple drag and drop
            self.drag_drop = SimpleDragDropHandler(self.root, self.handle_dropped_file)
    
    def handle_dropped_file(self, file_path):
        """Handle dropped PDF file"""
        if file_path and os.path.exists(file_path):
            self.selected_file.set(file_path)
            self.update_file_info()
            self.status_var.set(f"File loaded: {os.path.basename(file_path)}")
        else:
            messagebox.showerror("Error", "Invalid file path")
    
    def update_quality_label(self, *args):
        """Update quality label when slider changes"""
        self.quality_label.config(text=str(int(self.quality_var.get())))
    
    def browse_file(self):
        """Open file dialog to select PDF file"""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file.set(file_path)
            self.update_file_info()
    
    def update_file_info(self):
        """Update file information display"""
        file_path = self.selected_file.get()
        if not file_path:
            return
        
        size, error = self.compressor.get_file_info(file_path)
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if error:
            self.info_text.insert(tk.END, f"Error: {error}")
        else:
            formatted_size = self.compressor.format_file_size(size)
            self.info_text.insert(tk.END, f"File: {os.path.basename(file_path)}\n")
            self.info_text.insert(tk.END, f"Size: {formatted_size}\n")
            self.info_text.insert(tk.END, f"Path: {file_path}\n")
            self.info_text.insert(tk.END, f"Ready for compression")
        
        self.info_text.config(state=tk.DISABLED)
    
    def start_compression(self):
        """Start PDF compression in a separate thread"""
        file_path = self.selected_file.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a PDF file first")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Selected file does not exist")
            return
        
        # Disable compress button
        self.compress_btn.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Compressing PDF...")
        
        # Start compression in separate thread
        thread = threading.Thread(target=self.compress_file, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def compress_file(self, file_path):
        """Compress PDF file (runs in separate thread)"""
        try:
            # Generate output file path
            base_name = os.path.splitext(file_path)[0]
            output_path = f"{base_name}_compressed.pdf"
            
            # Update progress
            self.root.after(0, lambda: self.progress_var.set(25))
            
            # Compress the file
            quality = int(self.quality_var.get())
            success, message = self.compressor.compress_pdf(file_path, output_path, quality)
            
            # Update progress
            self.root.after(0, lambda: self.progress_var.set(100))
            
            # Update UI in main thread
            if success:
                self.root.after(0, lambda: self.status_var.set("Compression completed successfully!"))
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"{message}\n\nCompressed file saved as:\n{output_path}"))
            else:
                self.root.after(0, lambda: self.status_var.set("Compression failed"))
                self.root.after(0, lambda: messagebox.showerror("Error", message))
        
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set("Compression failed"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Unexpected error: {str(e)}"))
        
        finally:
            # Re-enable compress button
            self.root.after(0, lambda: self.compress_btn.config(state=tk.NORMAL))
    
    def clear_selection(self):
        """Clear file selection and reset UI"""
        self.selected_file.set("")
        self.progress_var.set(0)
        self.status_var.set("Ready to compress PDF files")
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = PDFDownSizingApp(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
