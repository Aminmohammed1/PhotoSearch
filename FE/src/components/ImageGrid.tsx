import { Image as ImageIcon } from "lucide-react";

interface ImageData {
  id: string;
  url: string;
  description?: string;
  ocrText?: string;
}

interface ImageGridProps {
  images: ImageData[];
  isLoading?: boolean;
}

const ImageGrid = ({ images, isLoading }: ImageGridProps) => {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="aspect-square rounded-xl bg-muted animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (images.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-24 animate-fade-in">
        <div className="p-8 rounded-full bg-muted/50 mb-6">
          <ImageIcon className="h-16 w-16 text-muted-foreground" />
        </div>
        <h3 className="text-2xl font-semibold mb-2">No images found</h3>
        <p className="text-muted-foreground text-center max-w-md">
          Try a different search term or upload an image to find similar results
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {images.map((image, index) => (
        <div
          key={image.id}
          className="group relative aspect-square rounded-xl overflow-hidden bg-muted shadow-soft hover:shadow-large transition-all duration-300 animate-fade-in cursor-pointer"
          style={{ animationDelay: `${index * 50}ms` }}
        >
          <img
            src={image.url}
            alt={image.description || "Image"}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/0 to-black/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="absolute bottom-0 left-0 right-0 p-4 text-white">
              {image.description && (
                <p className="text-sm font-medium line-clamp-2 mb-1">
                  {image.description}
                </p>
              )}
              {image.ocrText && (
                <p className="text-xs opacity-75 line-clamp-1">{image.ocrText}</p>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default ImageGrid;
