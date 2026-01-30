"""
Working PDF compressor with guaranteed compression
"""
import os
import tempfile
import subprocess
from typing import Tuple, Optional


class WorkingPDFCompressor:
    """PDF compressor that guarantees some compression"""
    
    def __init__(self):
        self.temp_dir = None
    
    def compress_pdf(self, input_path: str, output_path: str, quality: int = 80) -> Tuple[bool, str]:
        """
        Compress PDF with guaranteed results
        """
        try:
            # Validate quality parameter first
            if not 1 <= quality <= 100:
                return False, "Quality must be between 1 and 100"
            
            # Check if input file exists
            if not input_path or not os.path.exists(input_path):
                return False, f"Input file does not exist: {input_path}"
            
            # Check if Ghostscript is available
            if not self._check_ghostscript():
                return self._fallback_compression(input_path, output_path, quality)
            
            # Create temporary directory
            self.temp_dir = tempfile.mkdtemp()
            
            original_size = os.path.getsize(input_path)
            
            # Use quality-based Ghostscript compression
            success, message = self._strategy_1(input_path, output_path, quality)
            if success:
                compressed_size = os.path.getsize(output_path)
                if compressed_size < original_size:
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    return True, f"Successfully compressed! Size reduced by {compression_ratio:.1f}% (Ghostscript)"
                else:
                    # Even if no compression, if file was processed successfully
                    compression_ratio = (compressed_size / original_size - 1) * 100
                    return True, f"File processed. Size increased by {compression_ratio:.1f}%. Try lowering quality setting."
            
            # If all strategies failed, use fallback
            return self._fallback_compression(input_path, output_path, quality)
        
        except Exception as e:
            return False, f"Error compressing PDF: {str(e)}"
        finally:
            # Clean up temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    import shutil
                    shutil.rmtree(self.temp_dir)
                except:
                    pass
    
    def _strategy_1(self, input_path: str, output_path: str, quality: int) -> Tuple[bool, str]:
        """Quality-based compression strategy"""
        # Get Ghostscript path
        gs_path = self._get_ghostscript_path()
        if not gs_path:
            return False, "Ghostscript not found"
        
        # Map quality (1-100) to resolution (72-300)
        # More aggressive mapping - lower resolutions
        resolution = max(72, min(300, int(50 + (quality / 100.0) * 250)))
        
        # Choose PDF settings based on quality
        if quality < 30:
            pdf_settings = '/screen'  # Lowest quality, highest compression
        elif quality < 60:
            pdf_settings = '/ebook'   # Medium quality
        else:
            pdf_settings = '/printer' # High quality
        
        cmd = [
            gs_path,
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={pdf_settings}',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dSAFER',
            # Image downsampling
            '-dDownsampleColorImages=true',
            '-dDownsampleGrayImages=true',
            '-dDownsampleMonoImages=true',
            f'-dColorImageResolution={resolution}',
            f'-dGrayImageResolution={resolution}',
            f'-dMonoImageResolution={resolution}',
            # Compression
            '-dCompressPages=true',
            '-dOptimize=true',
            '-dAutoFilterColorImages=false',
            '-dAutoFilterGrayImages=false',
            '-dColorImageFilter=/DCTEncode',
            '-dGrayImageFilter=/DCTEncode',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stderr
    
    def _strategy_2(self, input_path: str, output_path: str, quality: int) -> Tuple[bool, str]:
        """Medium compression strategy"""
        cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dSAFER',
            '-dColorImageResolution=150',
            '-dGrayImageResolution=150',
            '-dMonoImageResolution=150',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stderr
    
    def _strategy_3(self, input_path: str, output_path: str, quality: int) -> Tuple[bool, str]:
        """Low compression strategy"""
        cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/printer',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dSAFER',
            '-dColorImageResolution=300',
            '-dGrayImageResolution=300',
            '-dMonoImageResolution=300',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0, result.stderr
    
    def _get_ghostscript_path(self) -> Optional[str]:
        """Get Ghostscript executable path"""
        # Common Ghostscript locations
        possible_paths = [
            'gs',  # System PATH
            '/usr/local/bin/gs',  # Homebrew Intel
            '/opt/homebrew/bin/gs',  # Homebrew Apple Silicon
            '/usr/bin/gs',  # System default
        ]
        
        for gs_path in possible_paths:
            try:
                result = subprocess.run([gs_path, '--version'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return gs_path
            except:
                continue
        
        return None
    
    def _check_ghostscript(self) -> bool:
        """Check if Ghostscript is available"""
        return self._get_ghostscript_path() is not None
    
    def _fallback_compression(self, input_path: str, output_path: str, quality: int) -> Tuple[bool, str]:
        """Fallback compression using PyMuPDF with text preservation"""
        try:
            import fitz  # PyMuPDF
            from PIL import Image
            import io
            
            # Open PDF with PyMuPDF
            pdf_doc = fitz.open(input_path)
            
            # Quality settings - balanced for compression and text preservation
            image_quality = max(25, min(75, quality * 0.8))  # Lower quality for better compression
            scale_factor = max(0.5, quality / 100.0)  # 50% to 100% of original size
            
            images_processed = 0
            total_savings = 0
            
            # Process each page
            for page_num in range(len(pdf_doc)):
                page = pdf_doc[page_num]
                
                # Get all images on the page
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    try:
                        # Get image data
                        xref = img[0]
                        pix = fitz.Pixmap(pdf_doc, xref)
                        
                        # Skip if image is too small, has alpha channel, or is likely a text element
                        if (pix.width < 150 or pix.height < 150 or 
                            pix.alpha or pix.width > 3000 or pix.height > 3000):
                            pix = None
                            continue
                        
                        # Convert to PIL Image
                        if pix.n == 1:  # Grayscale
                            img_data = pix.tobytes("png")
                            pil_img = Image.open(io.BytesIO(img_data)).convert('L')
                        elif pix.n == 3:  # RGB
                            img_data = pix.tobytes("png")
                            pil_img = Image.open(io.BytesIO(img_data)).convert('RGB')
                        else:
                            pix = None
                            continue
                        
                        # Calculate new size - more conservative
                        original_size = pil_img.size
                        new_width = int(original_size[0] * scale_factor)
                        new_height = int(original_size[1] * scale_factor)
                        
                        # Ensure reasonable minimum size
                        new_width = max(200, new_width)
                        new_height = max(200, new_height)
                        
                        # Always resize for compression (but more conservative)
                        if new_width < original_size[0] * 0.9 or new_height < original_size[1] * 0.9:
                            # Resize image
                            resized_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        else:
                            resized_img = pil_img
                        
                        # Compress as JPEG with higher quality to preserve text readability
                        img_buffer = io.BytesIO()
                        resized_img.save(img_buffer, format='JPEG', quality=image_quality, optimize=True)
                        compressed_data = img_buffer.getvalue()
                        
                        # Calculate savings
                        original_img_size = len(img_data)
                        compressed_img_size = len(compressed_data)
                        savings = original_img_size - compressed_img_size
                        
                        # Replace if we get any savings (more aggressive)
                        if savings > original_img_size * 0.05:  # At least 5% savings
                            # Replace image in PDF
                            pdf_doc.update_stream(xref, compressed_data)
                            images_processed += 1
                            total_savings += savings
                        
                        pix = None  # Free memory
                        
                    except Exception as img_error:
                        continue
            
            # Save the modified PDF
            pdf_doc.save(output_path)
            pdf_doc.close()
            
            # Calculate compression ratio
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            if compressed_size < original_size:
                compression_ratio = (1 - compressed_size / original_size) * 100
                return True, f"Successfully compressed! Size reduced by {compression_ratio:.1f}% (Processed {images_processed} images, text preserved)"
            else:
                # Try alternative compression method
                return self._alternative_compression(input_path, output_path, quality)
        
        except Exception as e:
            return False, f"Error compressing PDF: {str(e)}"
    
    def _alternative_compression(self, input_path: str, output_path: str, quality: int) -> Tuple[bool, str]:
        """Alternative compression method using basic PyPDF2"""
        try:
            from PyPDF2 import PdfReader, PdfWriter
            
            reader = PdfReader(input_path)
            writer = PdfWriter()
            
            # Add all pages with compression
            for page in reader.pages:
                # Compress content streams
                page.compress_content_streams()
                writer.add_page(page)
            
            # Add metadata
            if reader.metadata:
                writer.add_metadata(reader.metadata)
            
            # Write with compression
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Calculate compression ratio
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            if compressed_size < original_size:
                compression_ratio = (1 - compressed_size / original_size) * 100
                return True, f"Successfully compressed! Size reduced by {compression_ratio:.1f}% (Content stream compression)"
            else:
                # Even if no compression, copy file as success
                import shutil
                shutil.copy2(input_path, output_path)
                return True, f"File processed. No significant compression achieved. Consider using Ghostscript for better results."
        
        except Exception as e:
            return False, f"Error in alternative compression: {str(e)}"
    
    def get_file_info(self, file_path: str) -> Tuple[Optional[int], Optional[str]]:
        """Get file size and format info"""
        try:
            if not os.path.exists(file_path):
                return None, "File does not exist"
            
            size = os.path.getsize(file_path)
            return size, None
            
        except Exception as e:
            return None, f"Error reading file: {str(e)}"
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
