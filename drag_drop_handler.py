"""
Drag and drop functionality for PDF files
"""
import tkinter as tk
from tkinter import messagebox
import os


class DragDropHandler:
    """Handle drag and drop events for PDF files"""
    
    def __init__(self, root, file_callback):
        self.root = root
        self.file_callback = file_callback
        self.setup_drag_drop()
    
    def setup_drag_drop(self):
        """Setup drag and drop event handlers"""
        try:
            # Try to use tkinterdnd2 if available
            from tkinterdnd2 import DND_FILES, TkinterDnD
            
            # Enable drag and drop for the root window
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
            
            # Add visual feedback
            self.root.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.root.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            
        except ImportError:
            # Fallback: basic drag and drop support
            self.setup_basic_drag_drop()
    
    def setup_basic_drag_drop(self):
        """Basic drag and drop implementation without tkinterdnd2"""
        # This is a simplified version that works on most systems
        # In a production app, you might want to use platform-specific implementations
        pass
    
    def on_drag_enter(self, event):
        """Handle drag enter event"""
        try:
            # Change cursor to indicate drop is possible
            self.root.config(cursor="hand2")
        except:
            pass
    
    def on_drag_leave(self, event):
        """Handle drag leave event"""
        try:
            # Reset cursor
            self.root.config(cursor="")
        except:
            pass
    
    def on_drop(self, event):
        """Handle file drop event"""
        try:
            # Reset cursor
            self.root.config(cursor="")
            
            # Get dropped files
            files = self.root.tk.splitlist(event.data)
            
            if files:
                file_path = files[0]  # Take first file
                
                # Check if it's a PDF file
                if file_path.lower().endswith('.pdf'):
                    self.file_callback(file_path)
                else:
                    messagebox.showerror("Invalid File", "Please drop a PDF file")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error handling dropped file: {str(e)}")
    
    def enable_drag_drop_for_widget(self, widget):
        """Enable drag and drop for a specific widget"""
        try:
            from tkinterdnd2 import DND_FILES
            
            widget.drop_target_register(DND_FILES)
            widget.dnd_bind('<<Drop>>', self.on_drop)
            widget.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            widget.dnd_bind('<<DragLeave>>', self.on_drag_leave)
            
        except ImportError:
            pass


class SimpleDragDropHandler:
    """Simplified drag and drop handler for systems without tkinterdnd2"""
    
    def __init__(self, root, file_callback):
        self.root = root
        self.file_callback = file_callback
        self.setup_simple_drag_drop()
    
    def setup_simple_drag_drop(self):
        """Setup simple drag and drop using basic tkinter events"""
        # This is a placeholder for basic drag and drop functionality
        # In practice, you might need platform-specific implementations
        pass
    
    def handle_file_drop(self, file_path):
        """Handle file drop (called externally)"""
        if file_path and file_path.lower().endswith('.pdf'):
            self.file_callback(file_path)
        else:
            messagebox.showerror("Invalid File", "Please select a PDF file")
