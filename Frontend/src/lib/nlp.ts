import pdfParse from "pdf-parse";
//import docxReader from 'docx-reader'; // REMOVE THIS LINE
import fs from "fs";
import natural from "natural";
import { Buffer } from "buffer";

// Declare docxReader as any to bypass TypeScript checking (for now)
const docxReader: any = require("docx-reader");

const tokenizer = new natural.WordTokenizer();
const tfidf = new natural.TfIdf();

async function extractTextFromFile(file: File | string): Promise<string> {
  try {
    let fileContent: Buffer;
    let fileExtension: string;

    if (typeof file === "string") {
      const filePath = file;
      fileContent = fs.readFileSync(filePath);
      fileExtension = filePath.split(".").pop()?.toLowerCase() || "";
    } else {
      fileExtension = file.name.split(".").pop()?.toLowerCase() || "";
      const arrayBuffer = await file.arrayBuffer();
      fileContent = Buffer.from(arrayBuffer);
    }

    if (fileExtension === "pdf") {
      try {
        const data = await pdfParse(fileContent);
        return data.text;
      } catch (e: any) {
        console.error("Error parsing pdf", e);
        return "";
      }
    } else if (fileExtension === "docx") {
      try {
        const result = await docxReader(Buffer.from(fileContent)); // Use it directly
        return result.value;
      } catch (e: any) {
        console.error("Error parsing docx", e);
        return "";
      }
    } else if (fileExtension === "txt") {
      return fileContent.toString();
    } else {
      throw new Error("Unsupported file type.");
    }
  } catch (error: any) {
    console.error("Error extracting text:", error);
    throw new Error(`Error extracting text from file: ${error.message}`);
  }
}

function preprocessText(text: string): string[] {
  if (!text) return [];
  const lowerCaseText = text.toLowerCase();
  const cleanText = lowerCaseText.replace(/[^\w\s]/g, "");
  const words = tokenizer.tokenize(cleanText);
  const stopWords = [
    "the",
    "and",
    "is",
    "are",
    "a",
    "an",
    "in",
    "on",
    "at",
    "to",
    "for",
    "with",
    "by",
    "of",
  ];
  const filteredWords = words.filter((word) => !stopWords.includes(word));
  return filteredWords;
}

function analyzeMatch(
  jobDescription: string,
  resumeText: string,
  cvText: string
): any {
  try {
    const processedJD = preprocessText(jobDescription);
    const processedResume = preprocessText(resumeText);
    const processedCV = preprocessText(cvText);
    const documents = [processedJD, processedResume, processedCV];

    tfidf.addDocument(processedJD);
    tfidf.addDocument(processedResume);
    tfidf.addDocument(processedCV);

    const allTerms: string[] = Array.from(
      new Set([...processedJD, ...processedResume, ...processedCV])
    );

    const getVector = (doc: string[]): number[] => {
      const vector: number[] = [];
      for (const term of allTerms) {
        vector.push(tfidf.tfidf(term, documents.indexOf(doc)));
      }
      return vector;
    };

    const jdVector = getVector(processedJD);
    const resumeVector = getVector(processedResume);
    const cvVector = getVector(processedCV);

    const similarity = cosineSimilarity(jdVector, resumeVector);
    const cvSimilarity = cosineSimilarity(jdVector, cvVector);
    const overallSimilarity = Math.max(similarity, cvSimilarity);

    let matchLevel: "Perfect" | "Good" | "Fair" | "Poor";
    if (overallSimilarity > 0.8) {
      matchLevel = "Perfect";
    } else if (overallSimilarity > 0.6) {
      matchLevel = "Good";
    } else if (overallSimilarity > 0.4) {
      matchLevel = "Fair";
    } else {
      matchLevel = "Poor";
    }
    const matchedKeywords = processedJD.filter(
      (word) => processedResume.includes(word) || processedCV.includes(word)
    );

    return {
      matchPercentage: Math.round(overallSimilarity * 100),
      matchLevel,
      matchedKeywords,
    };
  } catch (error) {
    console.error("Analysis error:", error);
    throw error;
  }
}

function cosineSimilarity(vectorA: number[], vectorB: number[]): number {
  if (vectorA.length === 0 || vectorB.length === 0) {
    return 0;
  }
  if (vectorA.length !== vectorB.length) {
    throw new Error("Vectors must have the same length");
  }

  let dotProduct = 0;
  let magnitudeA = 0;
  let magnitudeB = 0;

  for (let i = 0; i < vectorA.length; i++) {
    dotProduct += vectorA[i] * vectorB[i];
    magnitudeA += vectorA[i] * vectorA[i];
    magnitudeB += vectorB[i] * vectorB[i];
  }

  magnitudeA = Math.sqrt(magnitudeA);
  magnitudeB = Math.sqrt(magnitudeB);

  if (magnitudeA === 0 || magnitudeB === 0) {
    return 0;
  }

  return dotProduct / (magnitudeA * magnitudeB);
}

export { extractTextFromFile, preprocessText, analyzeMatch };
