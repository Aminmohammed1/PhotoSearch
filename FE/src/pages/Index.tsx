import { useState } from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Search, Upload, Grid3x3 } from "lucide-react";
import SearchBar from "@/components/SearchBar";
import ImageUpload from "@/components/ImageUpload";
import ImageGrid from "@/components/ImageGrid";

const Index = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("search");
  
  // Mock data - replace with actual API calls
  const mockImages = [
    {
      id: "1",
      url: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
      description: "Mountain landscape at sunset",
      ocrText: "Nature Photography",
    },
    {
      id: "2",
      url: "https://images.unsplash.com/photo-1511300636408-a63a89df3482",
      description: "Abstract colorful pattern",
    },
    {
      id: "3",
      url: "https://images.unsplash.com/photo-1518709268805-4e9042af9f23",
      description: "City skyline at night",
      ocrText: "Urban Architecture",
    },
  ];

  const handleSearch = () => {
    console.log("Searching for:", searchQuery);
    // Implement search functionality here
  };

  const handleImageUpload = (file: File) => {
    console.log("Uploaded file:", file.name);
    // Implement image upload and search here
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-hero opacity-10" />
        <div className="relative container mx-auto px-4 py-16">
          <div className="text-center mb-12 animate-fade-in">
            <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Visual Search Engine
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Search images by description, OCR text, or upload an image to find similar results
            </p>
          </div>

          <Tabs
            value={activeTab}
            onValueChange={setActiveTab}
            className="w-full"
          >
            <TabsList className="grid w-full max-w-md mx-auto grid-cols-3 mb-8 glass-effect h-14">
              <TabsTrigger value="search" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                <Search className="h-4 w-4 mr-2" />
                Search
              </TabsTrigger>
              <TabsTrigger value="upload" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                <Upload className="h-4 w-4 mr-2" />
                Upload
              </TabsTrigger>
              <TabsTrigger value="all" className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground">
                <Grid3x3 className="h-4 w-4 mr-2" />
                All
              </TabsTrigger>
            </TabsList>

            <TabsContent value="search" className="space-y-12">
              <div className="flex justify-center">
                <SearchBar
                  value={searchQuery}
                  onChange={setSearchQuery}
                  onSearch={handleSearch}
                />
              </div>
              <ImageGrid images={mockImages} />
            </TabsContent>

            <TabsContent value="upload" className="space-y-12">
              <div className="flex justify-center">
                <ImageUpload onUpload={handleImageUpload} />
              </div>
              <ImageGrid images={[]} />
            </TabsContent>

            <TabsContent value="all" className="space-y-12">
              <ImageGrid images={mockImages} />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Index;
