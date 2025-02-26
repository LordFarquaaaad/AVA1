// src/pages/PrimarySchoolReportPage.js
import React from "react";
import { Button, Paper, Typography } from "@mui/material";
import StudentRow from "../components/reportGenerator/StudentRow";
import { primaryCategories } from "../constants/categories";
import useReportGenerator from "../hooks/useReportGenerator";

const PrimarySchoolReportPage = () => {
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
  } = useReportGenerator(primaryCategories);

  console.log("📢 Report in PrimarySchoolReportPage.js:", JSON.stringify(report, null, 2)); // Debugging log

  return (
    <Paper elevation={3} sx={{ padding: "16px", margin: "16px" }}>
      <Typography variant="h5" gutterBottom>
        Primary School Report Generator
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

      <Button variant="contained" color="primary" onClick={addStudent} sx={{ marginTop: "16px", marginRight: "16px" }}>
        ➕ Add Student
      </Button>

      <Button
        variant="contained"
        color="secondary"
        onClick={handleGenerateReport}
        disabled={loading}
        sx={{ marginTop: "16px" }}
      >
        {loading ? "Generating..." : "Generate Report"}
      </Button>

      {error && <p style={{ color: "red", marginTop: "16px" }}>{error}</p>}

      {report && Array.isArray(report) && (
        <div style={{ marginTop: "16px" }}>
          <Typography variant="h6">Generated Reports:</Typography>
          {report.map((studentReport, index) => (
            <div key={index} style={{ marginTop: "8px" }}>
              <Typography variant="subtitle1">{studentReport.name || `Student ${index + 1}`}</Typography>
              <p>{studentReport.report || "No report text available"}</p>
            </div>
          ))}
        </div>
      )}
    </Paper>
  );
};

export default PrimarySchoolReportPage;