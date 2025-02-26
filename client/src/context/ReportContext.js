// src/context/ReportContext.js
import React, { createContext, useContext, useState } from "react";
import { generateReport } from "../services/reportService";

const ReportContext = createContext();

export const ReportProvider = ({ children }) => {
  const [report, setReport] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generateReportHandler = async (student) => {
    setLoading(true);
    setError(null);

    try {
      const response = await generateReport(student);
      console.log("📥 Context response:", JSON.stringify(response, null, 2));

      if (response && Array.isArray(response.reports)) {
        setReport(response.reports);
      } else if (response && response.name && response.report) {
        setReport([{ name: response.name, report: response.report }]);
      } else {
        setReport([{ name: student.name || "Unnamed Student", report: "No report generated" }]);
      }
    } catch (err) {
      console.error("❌ Error generating report:", err);
      setError("Failed to generate report. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ReportContext.Provider value={{ report, loading, error, generateReportHandler }}>
      {children}
    </ReportContext.Provider>
  );
};

export const useReport = () => useContext(ReportContext);