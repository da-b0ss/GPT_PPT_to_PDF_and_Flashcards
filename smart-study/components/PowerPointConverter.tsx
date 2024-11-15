'use client';

import React, { useState } from 'react';
import { Loader2, Upload, FileText, Video, Brain, PlayCircle } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

export default function PowerPointConverter() {
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [files, setFiles] = useState<File[]>([]);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);

  const features = [
    {
      title: 'PowerPoint Conversion',
      description: 'Convert PPTX files to PDF format',
      icon: <FileText className="w-6 h-6" />,
      options: [
        { label: 'Default PDF', value: 'default', requiresFiles: true },
        { label: 'Custom PDF with Notes', value: 'custom', requiresFiles: true }
      ]
    },
    {
      title: 'Content Generation',
      description: 'Generate study materials and content',
      icon: <Brain className="w-6 h-6" />,
      options: [
        { label: 'Generate Term Definitions', value: 'terms', requiresPDF: true },
        { label: 'Create Short-Form Content', value: 'brainrot', requiresPDF: true }
      ]
    },
    {
      title: 'Media Creation',
      description: 'Generate audio and video content',
      icon: <Video className="w-6 h-6" />,
      options: [
        { label: 'Generate Audio', value: 'audio', requiresTranscripts: true },
        { label: 'Create Videos', value: 'video', requiresTranscripts: true }
      ]
    }
  ];

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) return;
    const uploadedFiles = Array.from(event.target.files);
    setFiles(prev => [...prev, ...uploadedFiles]);
  };

  const handleOptionSelect = (value: string) => {
    setSelectedOption(value);
    setError(null);
  };

  const handleExecute = async () => {
    if (!selectedOption) {
      setError('Please select an operation to perform');
      return;
    }

    setProcessing(true);
    setError(null);
    
    try {
      // If we need to upload files first
      if (files.length > 0) {
        const formData = new FormData();
        files.forEach(file => {
          console.log('Appending file:', file.name);
          formData.append('files', file);
        });
        
        console.log('Uploading files...');
        const uploadResponse = await fetch('http://localhost:8000/upload', {
          method: 'POST',
          body: formData
        });
        
        if (!uploadResponse.ok) {
          const errorData = await uploadResponse.json();
          throw new Error(errorData.message || 'File upload failed');
        }
        
        console.log('Files uploaded successfully');
      }
      
      console.log('Processing with option:', selectedOption);
      const response = await fetch(`http://localhost:8000/process/${selectedOption}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Processing failed');
      }
      
      const result = await response.json();
      console.log('Processing result:', result);
      
      if (result.status === 'error') {
        throw new Error(result.message);
      }
      
      // Clear files only after PDF conversion
      if (selectedOption === 'default' || selectedOption === 'custom') {
        setFiles([]);
      }
      setSelectedOption(null);
    } catch (err) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setProcessing(false);
      setProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">PowerPoint Converter</h1>
        
        {/* File Upload */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload PowerPoint Files
            </CardTitle>
            <CardDescription>
              Upload your PowerPoint files for processing
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="border-2 border-dashed rounded-lg p-8 text-center">
              <input
                type="file"
                accept=".pptx,.ppt"
                multiple
                onChange={handleFileUpload}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <div className="flex flex-col items-center">
                  <Upload className="w-12 h-12 text-gray-400 mb-4" />
                  <p className="text-sm text-gray-600">
                    Click to browse or drag and drop
                  </p>
                </div>
              </label>
            </div>
            
            {files.length > 0 && (
              <div className="mt-4">
                <h3 className="font-medium mb-2">Files to Process:</h3>
                <ul className="space-y-2">
                  {files.map((file, index) => (
                    <li key={index} className="flex items-center gap-2 text-sm">
                      <FileText className="w-4 h-4" />
                      {file.name}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Features */}
        <div className="space-y-4">
          {features.map((feature, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {feature.icon}
                  {feature.title}
                </CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  {feature.options.map((option) => (
                    <Button
                      key={option.value}
                      variant={selectedOption === option.value ? "default" : "outline"}
                      onClick={() => handleOptionSelect(option.value)}
                      className="w-full"
                    >
                      {option.label}
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Execute Button */}
        <Card className="mt-4">
          <CardContent className="pt-6">
            <Button 
              className="w-full"
              onClick={handleExecute}
              disabled={processing || !selectedOption}
            >
              {processing ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <PlayCircle className="w-4 h-4 mr-2" />
                  Execute Selected Operation
                </>
              )}
            </Button>
            
            {processing && (
              <div className="mt-4">
                <Progress value={progress} className="mb-2" />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive" className="mt-4">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
}