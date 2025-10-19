import { Upload, Image as ImageIcon, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface ImageUploadProps {
  onUpload: (file: File) => void;  // called when user clicks Send
}

const ImageUpload = ({ onUpload }: ImageUploadProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      handleFileSelect(file);
    }
  };

  const handleFileSelect = (file: File) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
      setSelectedFile(file);
    };
    reader.readAsDataURL(file);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleSend = () => {
    if (selectedFile) {
      onUpload(selectedFile);
    }
  };

  return (
    <div className="w-full max-w-3xl animate-fade-in">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          relative border-2 border-dashed rounded-2xl p-12 transition-all duration-300
          ${isDragging 
            ? "border-primary bg-primary/5 scale-105" 
            : "border-border/50 hover:border-primary/50 hover:bg-muted/50"}
        `}
      >
        {preview ? (
          <div className="space-y-6 flex flex-col items-center">
            <img
              src={preview}
              alt="Preview"
              className="w-full h-64 object-contain rounded-xl shadow-medium"
            />

            <div className="flex gap-4 w-full">
              <Button
                variant="outline"
                onClick={() => {
                  setPreview(null);
                  setSelectedFile(null);
                }}
                className="w-1/2"
              >
                Upload Different Image
              </Button>

              <Button
                variant="default"
                onClick={handleSend}
                className="w-1/2 gradient-primary"
              >
                <Send className="h-5 w-5 mr-2" />
                Send
              </Button>
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-6 text-center">
            <div className="p-6 rounded-full bg-primary/10">
              <Upload className="h-12 w-12 text-primary" />
            </div>
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">Upload an image to search</h3>
              <p className="text-muted-foreground">
                Drag and drop or click to browse
              </p>
            </div>
            <label htmlFor="file-upload">
              <Button variant="default" className="gradient-primary" asChild>
                <span className="cursor-pointer">
                  <ImageIcon className="mr-2 h-5 w-5" />
                  Choose Image
                </span>
              </Button>
              <input
                id="file-upload"
                type="file"
                accept="image/*"
                onChange={handleFileInput}
                className="hidden"
              />
            </label>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;
