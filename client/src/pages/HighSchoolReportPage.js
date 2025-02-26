import React from "react";
import { Button, Paper, Typography } from "@mui/material";
import StudentRow from "../components/reportGenerator/StudentRow";
import { highSchoolCategories } from "../constants/categories";
import useReportGenerator from "../hooks/useReportGenerator";

const HighSchoolReportPage = () => {
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
  } = useReportGenerator(highSchoolCategories);

  return (
    <Paper elevation={3} sx={{ padding: "16px", margin: "16px" }}>
      <Typography variant="h5" gutterBottom>
        High School Report Generator
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

      {report && (
        <div style={{ marginTop: "16px" }}>
          <Typography variant="h6">Generated Reports:</Typography>
          {report.map((studentReport, index) => (
            <div key={index} style={{ marginTop: "8px" }}>
              <Typography variant="subtitle1">Student {index + 1}:</Typography>
              <p>{studentReport}</p>
            </div>
          ))}
        </div>
      )}
    </Paper>
  );
};

export default HighSchoolReportPage;