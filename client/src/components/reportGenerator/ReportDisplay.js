// src/components/reportGenerator/ReportDisplay.js
import React from "react";

const ReportDisplay = ({ report }) => {
  if (!report || !Array.isArray(report) || report.length === 0) {
    return <p>No report data available.</p>;
  }

  return (
    <div>
      {report.map((item, index) => (
        <div key={index}>
          <h2>{item.name || "Unnamed Student"}</h2>
          <p>{item.report || "No report text available"}</p>
        </div>
      ))}
    </div>
  );
};

export default ReportDisplay;
