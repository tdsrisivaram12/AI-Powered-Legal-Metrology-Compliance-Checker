"use client";

import { useEffect, useRef, useState } from "react";
import { analyzeProduct } from "@/lib/api";

type Violation = {
  rule: string;
  reason: string;
  severity: "Low" | "Medium" | "High";
};

type Result = {
  product: string;
  mrp: string;
  quantity: string;
  manufacturer: string;
  packedDate: string;
  bestBefore: string;
  status: "Compliant" | "Violation";
  complianceScore: number;
  confidence: number;
  violations: Violation[];
};

export default function ScanPage() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const [image, setImage] = useState<string | null>(null);
  const [fileName, setFileName] = useState("");
  const [cameraOpen, setCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<Result | null>(null);

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  async function openCamera() {
    setCameraError("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: "environment" },
        },
        audio: false,
      });

      streamRef.current = stream;
      setCameraOpen(true);

      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      }, 100);
    } catch (error) {
      console.error(error);

      setCameraError(
        "Camera access was blocked or is not available. Please allow camera permission and try again."
      );
    }
  }

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }

    setCameraOpen(false);
  }

  function capturePhoto() {
    const video = videoRef.current;

    if (!video) return;

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    if (!context) return;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const capturedImage = canvas.toDataURL("image/jpeg", 0.9);

    setImage(capturedImage);
    setFileName("Camera capture.jpg");

    stopCamera();
  }

  function handleUpload(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) return;

    setFileName(file.name);
    setImage(URL.createObjectURL(file));
    setResult(null);
  }

  function removeImage() {
    setImage(null);
    setFileName("");
    setResult(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  async function handleAnalyze() {
    if (!image) return;

    setIsAnalyzing(true);
    setResult(null);

    try {
      const analysisResult = await analyzeProduct(image);
      setResult(analysisResult);
    } catch (error) {
      console.error("Analysis failed:", error);
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <div className="mx-auto max-w-6xl space-y-8">

      {/* Page heading */}
      <div>
        <p className="text-sm font-medium text-[#0F2742]">
          Inspection Workspace
        </p>

        <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
          Scan Product
        </h1>

        <p className="mt-2 max-w-2xl text-sm text-slate-500">
          Capture or upload a product package to extract its declarations
          and check legal metrology compliance.
        </p>
      </div>

      {/* Camera */}
      {cameraOpen && (
        <div className="border border-slate-200 bg-white">

          {/* Camera header */}
          <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
            <div>
              <h2 className="text-sm font-semibold text-slate-900">
                Camera Inspection
              </h2>

              <p className="mt-1 text-xs text-slate-500">
                Position the product clearly inside the frame.
              </p>
            </div>

            <span className="text-xs font-medium text-[#0F766E]">
              Camera active
            </span>
          </div>

          {/* Camera preview */}
          <div className="relative flex min-h-[420px] items-center justify-center bg-slate-950">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="max-h-[600px] w-full object-contain"
            />

            {/* Inspection frame */}
            <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
              <div className="relative h-72 w-72 border border-white/80 sm:h-80 sm:w-80">

                {/* Corner markers */}
                <span className="absolute -left-px -top-px h-7 w-7 border-l-2 border-t-2 border-white" />
                <span className="absolute -right-px -top-px h-7 w-7 border-r-2 border-t-2 border-white" />
                <span className="absolute -bottom-px -left-px h-7 w-7 border-b-2 border-l-2 border-white" />
                <span className="absolute -bottom-px -right-px h-7 w-7 border-b-2 border-r-2 border-white" />

              </div>
            </div>
          </div>

          {/* Camera controls */}
          <div className="flex justify-center gap-3 border-t border-slate-200 p-5">
            <button
              onClick={capturePhoto}
              className="inline-flex items-center gap-2 rounded-md bg-[#0F2742] px-6 py-2.5 text-sm font-medium text-white transition hover:bg-[#173B61]"
            >
              <span>●</span>
              Capture
            </button>

            <button
              onClick={stopCamera}
              className="rounded-md border border-slate-200 bg-white px-5 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Camera error */}
      {cameraError && (
        <div className="border-l-2 border-red-600 bg-red-50 px-4 py-3 text-sm text-red-700">
          {cameraError}
        </div>
      )}

      {/* Choose image */}
      {!image && !cameraOpen && (
        <div>

          <div className="mb-4">
            <h2 className="text-sm font-semibold text-slate-900">
              Start Inspection
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Choose how you want to provide the product image.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2">

            {/* Camera option */}
            <button
              onClick={openCamera}
              className="group border border-slate-200 bg-white p-6 text-left transition hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-[#0F2742] text-sm text-white">
                📷
              </div>

              <h2 className="mt-5 text-base font-semibold text-slate-900">
                Scan with Camera
              </h2>

              <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">
                Use your device camera to capture the product packaging
                during an inspection.
              </p>

              <div className="mt-5 text-xs font-semibold text-[#0F2742] group-hover:underline">
                Open Camera →
              </div>
            </button>

            {/* Upload option */}
            <button
              onClick={() => fileInputRef.current?.click()}
              className="group border border-slate-200 bg-white p-6 text-left transition hover:border-slate-300 hover:bg-slate-50"
            >
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-slate-100 text-sm text-slate-700">
                ↑
              </div>

              <h2 className="mt-5 text-base font-semibold text-slate-900">
                Upload Image
              </h2>

              <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">
                Select an existing product image from your device for
                inspection.
              </p>

              <div className="mt-5 text-xs font-semibold text-[#0F2742] group-hover:underline">
                Choose Image →
              </div>
            </button>

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleUpload}
            />

          </div>

          {/* Inspection guidance */}
          <div className="mt-6 border border-slate-200 bg-white p-5">
            <div className="flex gap-3">

              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-[#CCFBF1] text-sm font-semibold text-[#0F766E]">
                i
              </div>

              <div>
                <p className="text-sm font-medium text-slate-800">
                  For better inspection results
                </p>

                <p className="mt-1 text-xs leading-5 text-slate-500">
                  Capture the package clearly and ensure declarations such
                  as MRP, net quantity, manufacturer details and dates are
                  visible.
                </p>
              </div>

            </div>
          </div>

        </div>
      )}

      {/* Image + result */}
      {image && (
        <div className="grid gap-6 lg:grid-cols-2">

          {/* Product image */}
          <div className="border border-slate-200 bg-white">

            <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <div>
                <h2 className="text-sm font-semibold text-slate-900">
                  Product Image
                </h2>

                <p className="mt-1 max-w-[250px] truncate text-xs text-slate-500">
                  {fileName}
                </p>
              </div>

              <span className="text-xs font-medium text-slate-400">
                Image
              </span>
            </div>

            <div className="flex min-h-[420px] items-center justify-center bg-slate-50 p-6">
              <img
                src={image}
                alt="Selected product"
                className="max-h-[500px] object-contain"
              />
            </div>

          </div>

          {/* Result */}
          <div className="space-y-4">

            {!result ? (
              <div className="flex min-h-[420px] flex-col items-center justify-center border border-slate-200 bg-white p-8 text-center">

                <div className="flex h-12 w-12 items-center justify-center rounded-md bg-[#0F2742] text-lg text-white">
                  AI
                </div>

                <h2 className="mt-5 text-base font-semibold text-slate-900">
                  Ready for Analysis
                </h2>

                <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">
                  Analyze the image to extract product declarations and
                  identify potential compliance issues.
                </p>

                <button
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  className="mt-6 inline-flex items-center gap-2 rounded-md bg-[#0F2742] px-6 py-2.5 text-sm font-medium text-white transition hover:bg-[#173B61] disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isAnalyzing ? (
                    <>
                      <span className="animate-pulse">●</span>
                      Analyzing Product...
                    </>
                  ) : (
                    <>
                      Analyze Product
                      <span>→</span>
                    </>
                  )}
                </button>

                <p className="mt-4 text-[11px] text-slate-400">
                  Analysis currently uses demo inspection data.
                </p>

              </div>
            ) : (
              <ResultCard result={result} />
            )}

            {/* Choose another image */}
            <button
              onClick={removeImage}
              className="w-full rounded-md border border-slate-200 bg-white px-5 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Choose Another Image
            </button>

          </div>
        </div>
      )}
    </div>
  );
}

function ResultCard({ result }: { result: Result }) {
  const compliant = result.status === "Compliant";

  return (
    <div className="border border-slate-200 bg-white">

      {/* Result header */}
      <div className="border-b border-slate-200 px-5 py-4">

        <div className="flex items-start justify-between gap-4">

          <div>
            <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
              Inspection Result
            </p>

            <h2 className="mt-1 text-lg font-semibold text-slate-900">
              {result.product}
            </h2>
          </div>

          <span
            className={`text-xs font-semibold ${
              compliant
                ? "text-[#15803D]"
                : "text-[#B91C1C]"
            }`}
          >
            {compliant ? "✓ Compliant" : "✕ Violation"}
          </span>

        </div>
      </div>

      {/* Compliance summary */}
      <div className="grid grid-cols-2 divide-x divide-slate-200 border-b border-slate-200">

        <div className="p-5">
          <p className="text-xs text-slate-500">
            Compliance Score
          </p>

          <p
            className={`mt-1 text-2xl font-semibold ${
              result.complianceScore >= 80
                ? "text-[#15803D]"
                : result.complianceScore >= 60
                  ? "text-[#B45309]"
                  : "text-[#B91C1C]"
            }`}
          >
            {result.complianceScore}%
          </p>
        </div>

        <div className="p-5">
          <p className="text-xs text-slate-500">
            AI Confidence
          </p>

          <p className="mt-1 text-2xl font-semibold text-slate-900">
            {result.confidence}%
          </p>
        </div>

      </div>

      {/* Extracted information */}
      <div className="p-5">

        <h3 className="text-xs font-semibold uppercase tracking-wide text-slate-500">
          Extracted Information
        </h3>

        <div className="mt-3 divide-y divide-slate-100">
          <InfoRow
            label="Maximum Retail Price"
            value={result.mrp}
          />

          <InfoRow
            label="Net Quantity"
            value={result.quantity}
          />

          <InfoRow
            label="Manufacturer"
            value={result.manufacturer}
          />

          <InfoRow
            label="Packed Date"
            value={result.packedDate}
          />

          <InfoRow
            label="Best Before"
            value={result.bestBefore}
          />
        </div>

      </div>

      {/* Violations */}
      {result.violations.length > 0 && (
        <div className="border-t border-slate-200">

          <div className="border-l-2 border-red-600 bg-red-50/60 p-5">

            <div>
              <h3 className="text-sm font-semibold text-red-900">
                Compliance Issues Detected
              </h3>

              <p className="mt-1 text-xs text-red-700">
                The following items require further verification.
              </p>
            </div>

            <div className="mt-4 space-y-3">

              {result.violations.map((violation, index) => (
                <div
                  key={index}
                  className="border border-slate-200 bg-white p-4"
                >

                  <div className="flex items-start justify-between gap-4">

                    <div>
                      <p className="text-sm font-semibold text-slate-900">
                        {violation.rule}
                      </p>

                      <p className="mt-2 text-sm leading-6 text-slate-600">
                        {violation.reason}
                      </p>
                    </div>

                    <span
                      className={`shrink-0 text-[10px] font-bold uppercase tracking-wide ${
                        violation.severity === "High"
                          ? "text-[#B91C1C]"
                          : violation.severity === "Medium"
                            ? "text-[#B45309]"
                            : "text-slate-500"
                      }`}
                    >
                      {violation.severity}
                    </span>

                  </div>

                  <button className="mt-4 rounded-md bg-[#0F2742] px-4 py-2 text-xs font-medium text-white transition hover:bg-[#173B61]">
                    View Evidence
                  </button>

                </div>
              ))}

            </div>

          </div>
        </div>
      )}

      {/* Compliant state */}
      {result.violations.length === 0 && (
        <div className="border-t border-slate-200 bg-emerald-50/50 p-5">
          <div className="flex items-start gap-3">

            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-emerald-50 text-sm font-semibold text-[#15803D]">
              ✓
            </div>

            <div>
              <p className="text-sm font-semibold text-[#15803D]">
                No compliance issues detected
              </p>

              <p className="mt-1 text-xs text-slate-500">
                The extracted declarations passed the current inspection
                checks.
              </p>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}

function InfoRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4 py-3">

      <span className="text-xs text-slate-500">
        {label}
      </span>

      <span className="text-right text-sm font-medium text-slate-900">
        {value}
      </span>

    </div>
  );
}