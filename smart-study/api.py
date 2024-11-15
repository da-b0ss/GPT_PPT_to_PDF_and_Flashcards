from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from typing import List
from main import process_folder, run_ai_script, create_brainrot_lectures, process_all_transcripts

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def check_dependencies(option: str) -> bool:
    """Check if required files/folders exist for each operation"""
    if option in ['terms', 'brainrot']:
        # These operations need PDFs to exist
        return os.path.exists('PDF') and len(os.listdir('PDF')) > 0
    elif option in ['audio', 'video']:
        # These operations need transcripts to exist
        return os.path.exists('Transcripts') and len(os.listdir('Transcripts')) > 0
    return True

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        print(f"Received {len(files)} files for upload")
        if not os.path.exists("PPTX"):
            os.makedirs("PPTX")
            
        for file in files:
            file_path = os.path.join("PPTX", file.filename)
            print(f"Saving {file.filename} to {file_path}")
            
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
                
        return {"status": "success", "message": f"Successfully uploaded {len(files)} files"}
    except Exception as e:
        print(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/{option}")
async def process_files(option: str):
    try:
        print(f"Processing option: {option}")
        
        # Check dependencies
        if not check_dependencies(option):
            if option in ['terms', 'brainrot']:
                raise HTTPException(
                    status_code=400, 
                    detail="No PDF files found. Please convert PowerPoint files to PDF first."
                )
            elif option in ['audio', 'video']:
                raise HTTPException(
                    status_code=400, 
                    detail="No transcripts found. Please generate short-form content first."
                )
        
        # For PDF conversion, check if we have PPTX files
        if option in ['default', 'custom']:
            if not os.path.exists('PPTX') or len(os.listdir('PPTX')) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="No PowerPoint files found. Please upload files first."
                )
            if not os.path.exists("PDF"):
                os.makedirs("PDF")
        
        # Process based on option
        if option == "default":
            process_folder("PPTX", "PDF", use_custom=False)
        elif option == "custom":
            process_folder("PPTX", "PDF", use_custom=True)
        elif option == "terms":
            run_ai_script()
        elif option == "brainrot":
            create_brainrot_lectures()
        elif option in ["audio", "video"]:
            process_all_transcripts()
            
        return {
            "status": "success",
            "message": f"Successfully processed {option}"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)