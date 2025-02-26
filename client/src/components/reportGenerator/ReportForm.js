// src/components/reportGenerator/ReportForm.js
import React, { useState } from "react";
import { TextField, Button, Paper } from "@mui/material";
import { getCategoriesBySchoolLevel } from "../constants/categories";
import CategoryDropdown from "./CategoryDropdown";
import { generateReport } from "../services/reportService";

const ReportForm = ({ schoolLevel }) => {
  const [categories, setCategories] = useState(getCategoriesBySchoolLevel(schoolLevel));
  const [studentName, setStudentName] = useState(""); // Store student name
  const [report, setReport] = useState([]); // Change to array to match ReportDisplay

  const handleNameChange = (event) => {
    setStudentName(event.target.value);
  };

  const handleCategoryChange = (categoryIndex, field, value) => {
    const updatedCategories = [...categories];
    updatedCategories[categoryIndex][field] = value;
    setCategories(updatedCategories);
  };

  const handleGenerateReport = async () => {
    try {
      const student = {
        name: studentName || "Unnamed Student",
        categories: {},
      };

      categories.forEach((category) => {
        student.categories[category.key] = {
          value: category.value || "",
          comments: category.comments || "",
        };
      });

      const response = await generateReport({ student });
      console.log("📥 Form response:", JSON.stringify(response, null, 2));

      // Handle the response to match the array structure
      if (response && Array.isArray(response.reports)) {
        setReport(response.reports);
      } else if (response && response.name && response.report) {
        setReport([{ name: response.name, report: response.report }]);
      } else {
        setReport([{ name: studentName || "Unnamed Student", report: "No report generated" }]);
      }
    } catch (error) {
      console.error("Failed to generate report:", error);
      setReport([{ name: studentName || "Unnamed Student", report: "Error generating report" }]);
    }
  };

  return (
    <div>
      <h2>{schoolLevel} Report</h2>
      
      <TextField
        label="Student Name"
        variant="outlined"
        fullWidth
        margin="normal"
        value={studentName}
        onChange={handleNameChange}
      />

      {categories.map((category, index) => (
        <CategoryDropdown
          key={category.key}
          category={category}
          categoryIndex={index}
          handleCategoryChange={handleCategoryChange}
        />
      ))}

      <Button variant="contained" color="primary" onClick={handleGenerateReport}>
        Generate Report
      </Button>

      {report && Array.isArray(report) && (
        <Paper elevation={3} style={{ marginTop: "20px", padding: "16px" }}>
          <h3>Generated Report:</h3>
          {report.map((item, index) => (
            <div key={index}>
              <h4>{item.name}</h4>
              <p>{item.report}</p>
            </div>
          ))}
        </Paper>
      )}
    </div>
  );
};

export default ReportForm;












