import React, { useState, useCallback, useRef } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
  CardDescription,
} from "./ui/card";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";
import {
  AlertCircle,
  CheckCircle,
  File,
  FileText,
  Search,
  Zap,
  UploadCloud,
} from "lucide-react"; // Added UploadCloud
import { cn } from "../lib/utils";
import { motion } from "framer-motion";
import * as pdfjsLib from "pdfjs-dist"; // Import pdfjs
//import pdfWorker from "pdfjs-dist/build/pdf.worker.min.mjs";
import * as mammoth from "mammoth";
//import { extractTextFromFile, preprocessText, analyzeMatch } from './nlp'; // Import the functions  (adjust the path)

// The key change is here:  Set the workerSrc directly to a string.
pdfjsLib.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;





// Mock API (Replace with actual backend calls)
// const mockAPI = {
//   analyzeJobDescription: async (
//     jobDescription: string,
//     resume: string,
//     cv: string
//   ) => {
//     // Simulate processing delay
//     await new Promise((resolve) => setTimeout(resolve, 1500));

//     // Mock analysis logic (replace with real NLP and matching algorithms)
//     const keywords = [
//       "React.js",
//       "JavaScript",
//       "Node.js",
//       "UI",
//       "UX",
//       "Agile",
//       "SQL",
//       "Testing",
//       "Communication",
//       "Problem-solving",
//     ];
//     const jdLower = jobDescription.toLowerCase();
//     const resumeLower = (resume + " " + cv).toLowerCase(); // Combine resume and CV for analysis

//     const matchedKeywords = keywords.filter(
//       (keyword) =>
//         jdLower.includes(keyword.toLowerCase()) &&
//         resumeLower.includes(keyword.toLowerCase())
//     );
//     const matchPercentage = (matchedKeywords.length / keywords.length) * 100;

//     // Simulate different match levels for demonstration
//     let matchLevel: "Perfect" | "Good" | "Fair" | "Poor" = "Fair";
//     if (matchPercentage >= 90) {
//       matchLevel = "Perfect";
//     } else if (matchPercentage >= 70) {
//       matchLevel = "Good";
//     } else if (matchPercentage >= 50) {
//       matchLevel = "Fair";
//     } else {
//       matchLevel = "Poor";
//     }

//     return {
//       matchedKeywords,
//       matchPercentage: Math.round(matchPercentage),
//       matchLevel,
//       missingKeywords: keywords.filter(
//         (keyword) =>
//           !jdLower.includes(keyword.toLowerCase()) ||
//           !resumeLower.includes(keyword.toLowerCase())
//       ),
//     };
//   },
//   extractTextFromFile: async (file: File): Promise<string> => {
//     // Mock text extraction (replace with real logic using a library like pdf-parse, docx-reader, etc.)
//     return new Promise((resolve, reject) => {
//       const reader = new FileReader();
//       reader.onload = () => {
//         // For simplicity, we'll just return the file content as a string.
//         // In a real application, you'd use a library to extract text
//         // from the specific file type (PDF, DOCX, etc.).
//         const text = reader.result as string;
//         // Basic text extraction for demonstration purposes.  This will NOT work for binary files.
//         const plainText = text.substring(0, 500); // Limit to first 500 characters for demo
//         resolve(plainText);
//       };
//       reader.onerror = () => reject(new Error("Failed to read file"));

//       // Check file type and use appropriate reader (simplified for demo)
//       if (file.type === "text/plain") {
//         reader.readAsText(file);
//       } else {
//         //  In a real app, you would use a library to handle other file types.
//         //  This is a placeholder for demonstration.  It will NOT work for binary files.
//         reader.readAsText(file); // Attempt as text for demo.
//       }
//     });
//     // return new Promise((resolve, reject) => {
//     //   const reader = new FileReader();

//     //   reader.onload = async () => {
//     //     try {
//     //       const arrayBuffer = reader.result as ArrayBuffer;
//     //       let text = "";
//     //       console.log("File type:", file.type); // <---- ADD THIS LINE
//     //       if (file.type === "text/plain") {
//     //         text = new TextDecoder().decode(arrayBuffer);
//     //       } else if (file.type === "application/pdf") {
//     //         // Use pdf-parse
//     //         console.log("Processing as PDF"); // <---- ADD THIS LINE
//     //         const pdfData = await pdfjsLib.getDocument(arrayBuffer).promise;
//     //         let pdfText = "";
//     //         for (let i = 1; i <= pdfData.numPages; i++) {
//     //           const page = await pdfData.getPage(i);
//     //           const content = await page.getTextContent();
//     //           const pageText = content.items
//     //             .map((item: any) => (item.str ? item.str : ""))
//     //             .join(" ");
//     //           pdfText += pageText + " ";
//     //         }
//     //         text = pdfText;
//     //       } else if (
//     //         file.type === "application/msword" ||
//     //         file.type ===
//     //           "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
//     //       ) {
//     //         // Use docx-reader
//     //         const buffer = new Uint8Array(arrayBuffer);
//     //         const result = await mammoth.extractRawText({
//     //           arrayBuffer: buffer.buffer,
//     //         });
//     //         text = result.value;
//     //       } else {
//     //         reject(new Error(`Unsupported file type: ${file.type}`));
//     //         return;
//     //       }
//     //       resolve(text);
//     //     } catch (error) {
//     //       reject(error);
//     //     }
//     //   };

//     //   reader.onerror = () => reject(new Error("Failed to read file"));
//     //   reader.readAsArrayBuffer(file); // Use readAsArrayBuffer
//     // });
//   },
// };

const extractTextFromFile = async (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = async () => {
      try {
        const arrayBuffer = reader.result as ArrayBuffer;
        let text = "";
        // console.log("File type:", file.type); // <---- ADD THIS LINE
        if (file.type === "text/plain") {
          text = new TextDecoder().decode(arrayBuffer);
        } else if (file.type === "application/pdf") {
          // console.log("Processing as PDF"); // <---- ADD THIS LINE
          const pdfData = await pdfjsLib.getDocument(arrayBuffer).promise;
          let pdfText = "";
          for (let i = 1; i <= pdfData.numPages; i++) {
            const page = await pdfData.getPage(i);
            const content = await page.getTextContent();
            const pageText = content.items
              .map((item: any) => (item.str ? item.str : ""))
              .join(" ");
            pdfText += pageText + " ";
          }
          text = pdfText;
        } else if (
          file.type === "application/msword" ||
          file.type ===
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ) {
          const result = await mammoth.extractRawText({
            arrayBuffer: arrayBuffer,
          });
          text = result.value;
        } else {
          reject(new Error(`Unsupported file type: ${file.type}`));
          return;
        }
        resolve(text);
      } catch (error) {
        reject(error);
      }
    };

    reader.onerror = () => reject(new Error("Failed to read file"));
    reader.readAsArrayBuffer(file);
  });
};


const JobDescriptionAnalyzer = () => {
  const [jobDescription, setJobDescription] = useState("");
  const [resume, setResume] = useState("");
  const [cv, setCv] = useState(""); // Added CV state
  const [resumeFile, setResumeFile] = useState<File | null>(null); // Added file state
  const [cvFile, setCvFile] = useState<File | null>(null); // Added CV file state.
  const [analysisResult, setAnalysisResult] = useState<{
    matchedKeywords: string[];
    matchPercentage: number;
    matchLevel: string;
    missingKeywords: string[];
  } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const resumeInputRef = useRef<HTMLInputElement>(null); // Ref for resume input
  // const cvInputRef = useRef<HTMLInputElement>(null); // Ref for cv input

  const handleAnalyze = useCallback(async () => {
    if (
      !jobDescription.trim() ||
      (!resume.trim() && !cv.trim() && !resumeFile && !cvFile)
    ) {
      // Modified condition
      setError(
        "Please enter both Job Description and either Resume or CV (text or file)."
      );
      return;
    }
    setError(null);
    setLoading(true);
    setAnalysisResult(null); // Clear previous results

    let resumeText = resume;
    let cvText = cv;

    try {
      // Extract text from files if files are selected
      if (resumeFile) {
        resumeText = await extractTextFromFile(resumeFile); // Await here
        setResume(resumeText); // Update the resume state
      }
      if (cvFile) {
        cvText = await extractTextFromFile(cvFile); // Await here
        setCv(cvText);
      }
      const analysisData = {
        jobDescription: jobDescription,
        resumeText: resumeText,
        cvText: cvText,
      };

      // console.log("-----------------");
      // console.log("FRONTEND: Sending data to backend:");
      // console.log(analysisData);
      // console.log("-----------------");


      const response = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/analyze`, // Use your backend URL
        // "http://localhost:5000/analyze", // Use your backend URL
        {
          // Use your backend URL
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(analysisData),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const result = await response.json();
      // console.log("-----------------");
      // console.log("FRONTEND: Received result from backend:");
      // console.log(result);
      // console.log("-----------------");
      setAnalysisResult(result);
      // Clear the resume and cv text areas after successful analysis
      setResume("");
      // setCv("");
      setResumeFile(null); // Clear the selected file as well
      // setCvFile(null);
      // if (resumeFile) {
      //   resumeText = await mockAPI.extractTextFromFile(resumeFile);
      //   setResume(resumeText); // Update the resume state
      // }
      // if (cvFile) {
      //   cvText = await mockAPI.extractTextFromFile(cvFile);
      //   setCv(cvText);
      // }

      // const result = await mockAPI.analyzeJobDescription(
      //   jobDescription,
      //   resumeText,
      //   cvText
      // );
      // setAnalysisResult(result);
    } catch (err: any) {
      setError(err.message || "An error occurred during analysis.");
    } finally {
      setLoading(false);
    }
  }, [jobDescription, resume, cv, resumeFile, cvFile]); // Added file states to dependencies

  // Animation variants
  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.6, ease: "easeInOut" },
    },
  };

  const resultVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: {
      opacity: 1,
      scale: 1,
      transition: { duration: 0.4, ease: "easeInOut", delay: 0.2 },
    },
  };

  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    setFile: React.Dispatch<React.SetStateAction<File | null>>,
    setText: React.Dispatch<React.SetStateAction<string>>
  ) => {
    // console.log("handleFileChange called");
    // console.log("e.target.files:", e.target.files);
    const file = e.target.files?.[0];
    if (file) {
      // console.log("File selected:", file);

      // Basic file type validation
      if (
        ![
          "text/plain",
          "application/pdf",
          "application/msword",
          "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ].includes(file.type)
      ) {
        setError(
          "Invalid file type. Please upload a .txt, .pdf, or .docx file."
        );
        return; // Stop processing on error
      }

      // File size validation
      if (file.size > 5 * 1024 * 1024) {
        setError("File size too large. Maximum file size is 5MB.");
        return; // Stop processing on error
      }

      setText(""); // Clear previous text *before* setting the file
      setFile(file);
      // console.log("File state updated:", file); // Log *after* setting state
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            Job Description Analyzer
          </h1>
          <p className="text-gray-400 mt-4 text-lg">
            Analyze job descriptions and compare them with your resume or CV to
            find the perfect match.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Input Section */}
          <motion.div
            variants={cardVariants}
            initial="hidden"
            animate="visible"
            className="space-y-6"
          >
            <Card className="bg-gray-800 border-gray-700 shadow-lg">
              <CardHeader>
                <CardTitle className="text-white text-lg flex items-center gap-2">
                  <Search className="w-5 h-5" />
                  Job Description
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Paste the job description here.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Textarea
                  placeholder="Paste job description here..."
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="bg-gray-700 text-white border-gray-600 min-h-[200px] resize-y"
                />
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700 shadow-lg">
              <CardHeader>
                <CardTitle className="text-white text-lg flex items-center gap-2">
                  <FileText className="w-5 h-5" />
                  Resume / CV
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Paste your resume/cv text here or upload a file.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste your resume/cv here..."
                  value={resume}
                  onChange={(e) => setResume(e.target.value)}
                  className="bg-gray-700 text-white border-gray-600 min-h-[100px] resize-y"
                />
                <div className="flex items-center gap-4">
                  <Input
                    type="file"
                    id="resume-upload"
                    accept=".txt,.pdf,.doc,.docx"
                    onChange={(e) => {
                      // console.log("Resume input onChange triggered");
                      handleFileChange(e, setResumeFile, setResume);
                    }}
                    className="hidden"
                    ref={resumeInputRef}
                  />
                  <label
                    htmlFor="resume-upload"
                    onClick={() => {
                      // console.log("Label clicked!");
                      resumeInputRef.current?.click();
                    }}
                  >
                    <Button
                      variant="outline"
                      className="bg-gray-700 text-white border-gray-600 hover:bg-gray-600 flex items-center gap-2"
                    >
                      <UploadCloud className="w-4 h-4" />
                      Upload File
                    </Button>
                  </label>
                  {resumeFile && (
                    <span className="text-gray-400 truncate max-w-[200px]">
                      {resumeFile.name}
                    </span>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* <Card className="bg-gray-800 border-gray-700 shadow-lg">
              <CardHeader>
                <CardTitle className="text-white text-lg flex items-center gap-2">
                  <File className="w-5 h-5" />
                  CV
                </CardTitle>
                <CardDescription className="text-gray-400">
                  Paste your CV text here or upload a file.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder="Paste your CV here..."
                  value={cv}
                  onChange={(e) => setCv(e.target.value)}
                  className="bg-gray-700 text-white border-gray-600 min-h-[100px] resize-y"
                />
                <div className="flex items-center gap-4">
                  <Input
                    type="file"
                    id="cv-upload"
                    accept=".txt,.pdf,.doc,.docx"
                    onChange={(e) => {
                      console.log("CV input onChange triggered");
                      handleFileChange(e, setCvFile, setCv);
                    }}
                    className="hidden"
                    ref={cvInputRef}
                  />
                  <label
                    htmlFor="cv-upload"
                    onClick={() => cvInputRef.current?.click()}
                  >
                    <Button
                      variant="outline"
                      className="bg-gray-700 text-white border-gray-600 hover:bg-gray-600 flex items-center gap-2"
                    >
                      <UploadCloud className="w-4 h-4" />
                      Upload File
                    </Button>
                  </label>
                  {cvFile && (
                    <span className="text-gray-400 truncate max-w-[200px]">
                      {cvFile.name}
                    </span>
                  )}
                </div>
              </CardContent>
            </Card> */}

            <Button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white py-3
                                      hover:from-blue-600 hover:to-purple-600 transition-colors duration-300
                                      disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Zap className="animate-spin w-5 h-5" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Analyze
                </>
              )}
            </Button>
          </motion.div>

          {/* Result Section */}
          <motion.div
            variants={resultVariants}
            initial="hidden"
            animate={analysisResult ? "visible" : "hidden"}
          >
            {analysisResult && (
              <Card className="bg-gray-800 border-gray-700 shadow-lg">
                <CardHeader>
                  <CardTitle className="text-white text-lg">
                    Analysis Result
                  </CardTitle>
                  <CardDescription className="text-gray-400">
                    Here&apos;s how well your resume/CV matches the job
                    description.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-center">
                    <Badge
                      variant="outline"
                      className={cn(
                        "text-lg px-4 py-2 border-2",
                        analysisResult.matchLevel === "Perfect" &&
                          "border-green-500 text-green-400",
                        analysisResult.matchLevel === "Good" &&
                          "border-blue-500 text-blue-400",
                        analysisResult.matchLevel === "Fair" &&
                          "border-yellow-500 text-yellow-400",
                        analysisResult.matchLevel === "Poor" &&
                          "border-red-500 text-red-400"
                      )}
                    >
                      Match Level: {analysisResult.matchLevel}
                    </Badge>
                    <Progress
                      value={analysisResult.matchPercentage}
                      className={cn(
                        "mt-2 h-4",
                        analysisResult.matchLevel === "Perfect" &&
                          "bg-green-500",
                        analysisResult.matchLevel === "Good" && "bg-blue-500",
                        analysisResult.matchLevel === "Fair" && "bg-yellow-500",
                        analysisResult.matchLevel === "Poor" && "bg-red-500"
                      )}
                    />
                    <p className="text-gray-400 mt-1">
                      Match Percentage: {analysisResult.matchPercentage}%
                    </p>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-400" />
                      Matched Keywords
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {
                        //analysisResult.matchedKeywords &&
                        //Array.isArray(analysisResult.matchedKeywords) &&
                        analysisResult.matchedKeywords.map((keyword, index) => (
                          <Badge
                            key={index}
                            className="bg-green-500/20 text-green-400"
                          >
                            {keyword}
                          </Badge>
                        ))}
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-white mb-2 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5 text-red-400" />
                      Missing Keywords
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {
                        // analysisResult.missingKeywords &&
                        //Array.isArray(analysisResult.missingKeywords) &&
                        analysisResult.missingKeywords.map((keyword, index) => (
                          <Badge
                            key={index}
                            className="bg-red-500/20 text-red-400"
                          >
                            {keyword}
                          </Badge>
                        ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </motion.div>
        </div>

        {/* Error Message */}
        {error && (
          <Alert
            variant="destructive"
            className="bg-red-900/90 border-red-700 text-red-300"
          >
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default JobDescriptionAnalyzer;
// function extractTextFromFile(resumeFile: File): string | PromiseLike<string> {
//   throw new Error("Function not implemented.");
// }

