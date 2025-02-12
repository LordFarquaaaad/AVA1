import { useState } from "react";

const ReportGenerator = () => {
  const [input, setInput] = useState("");
  const [report, setReport] = useState("");
  const [loading, setLoading] = useState(false);

  const generateReport = async () => {
    if (!input) return;
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/reports/generate-from-input", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input }),
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

      const data = await response.json();
      setReport(data.report || "Error generating report. Please try again.");
    } catch (error) {
      console.error("❌ Error fetching report:", error);
      setReport("Server error. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">AI School Report Generator</h1>
      <textarea
        className="w-full p-2 border rounded-md"
        rows="4"
        placeholder="Describe the student's performance..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md disabled:opacity-50"
        onClick={generateReport}
        disabled={loading}
      >
        {loading ? "Generating..." : "Generate Report"}
      </button>
      {report && (
        <div className="mt-6 p-4 bg-gray-100 border rounded-md">
          <h2 className="font-bold">Generated Report:</h2>
          <p>{report}</p>
        </div>
      )}
    </div>
  );
};

export default ReportGenerator;


