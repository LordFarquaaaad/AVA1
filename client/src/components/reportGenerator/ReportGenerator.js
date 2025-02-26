// src/components/reportGenerator/ReportGenerator.js
import React from "react";
import { Button, Paper, Typography } from "@mui/material";
import StudentRow from "./StudentRow";
import useReportGenerator from "../../hooks/useReportGenerator";
import ReportDisplay from "./ReportDisplay";

const ReportGenerator = () => {
  const {
    students,
    report,
    loading,
    error,
    handleStudentChange,
    handleCategoryChange,
    addCategory,
    addStudent,
    handleGenerateReport,
  } = useReportGenerator();

  console.log("📢 Report in ReportGenerator.js:", JSON.stringify(report, null, 2)); // Detailed debug

  return (
    <Paper elevation={3} sx={{ padding: "16px", margin: "16px" }}>
      <Typography variant="h4" gutterBottom>
        AI School Report Generator
      </Typography>

      {students.map((student, studentIndex) => (
        <StudentRow
          key={studentIndex}
          student={student}
          studentIndex={studentIndex}
          handleCategoryChange={handleCategoryChange}
          handleStudentChange={handleStudentChange}
          addCategory={addCategory}
        />
      ))}

      <Button variant="contained" color="primary" onClick={addStudent} sx={{ marginTop: "16px" }}>
        ➕ Add Student
      </Button>

      <Button variant="contained" color="secondary" onClick={handleGenerateReport} sx={{ marginLeft: "10px" }}>
        📄 Generate Report
      </Button>

      {loading && <p>Loading report...</p>}
      {error && <p className="text-red-500">Error: {error}</p>}
      {report && (
        Array.isArray(report) ? (
          <ReportDisplay report={report} />
        ) : (
          <p className="text-red-500">
            ⚠️ Report is not an array: {typeof report === "object" && report !== null ? Object.keys(report).join(", ") : "Invalid data"}
          </p>
        )
      )}
    </Paper>
  );
};

export default ReportGenerator;









