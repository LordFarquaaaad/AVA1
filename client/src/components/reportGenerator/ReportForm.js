import React, { useState, useEffect } from "react";
import { TextField, Button, Paper, Typography } from "@mui/material";
import { getCategoriesBySchoolLevel } from "../constants/categories";
import CategoryDropdown from "./CategoryDropdown";
import { generateReport } from "../services/reportService";
import { useTheme } from "../../context/theme/ThemeContext"; // Import useTheme for styling

const ReportForm = ({ schoolLevel }) => {
  const [categories, setCategories] = useState([]);
  const [studentName, setStudentName] = useState("");
  const [report, setReport] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const { theme, themes } = useTheme(); // Get theme for styling

  // Initialize categories when schoolLevel changes
  useEffect(() => {
    try {
      const initialCategories = getCategoriesBySchoolLevel(schoolLevel) || [];
      setCategories(
        initialCategories.map((category) => ({
          ...category,
          value: "",
          comments: "",
        }))
      );
    } catch (err) {
      console.error("Error initializing categories:", err);
      setError("Failed to load categories for this school level.");
      setCategories([]); // Fallback to empty array
    }
  }, [schoolLevel]);

  const handleNameChange = (event) => {
    setStudentName(event.target.value);
  };

  const handleCategoryChange = (categoryIndex, field, value) => {
    const updatedCategories = [...categories];
    updatedCategories[categoryIndex] = {
      ...updatedCategories[categoryIndex],
      [field]: value,
    };
    setCategories(updatedCategories);
  };

  const handleGenerateReport = async () => {
    if (!studentName.trim() && categories.every((cat) => !cat.value)) {
      setError("Please enter a student name or select at least one category value.");
      return;
    }

    setLoading(true);
    setError(null);

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
        setError("Unexpected response format from server.");
      }
    } catch (error) {
      console.error("Failed to generate report:", error);
      setError("An error occurred while generating the report. Please try again.");
      setReport([{ name: studentName || "Unnamed Student", report: "Error generating report" }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper
      elevation={3}
      sx={{
        padding: "16px",
        marginTop: "16px",
        backgroundColor: themes[theme].cardColor,
        borderRadius: "8px",
      }}
    >
      <Typography variant="h2" gutterBottom sx={{ color: themes[theme].text }}>
        {schoolLevel} Report
      </Typography>

      <TextField
        label="Student Name"
        variant="outlined"
        fullWidth
        margin="normal"
        value={studentName}
        onChange={handleNameChange}
        sx={{
          backgroundColor: themes[theme].lighterCardColor,
          "& .MuiInputBase-input": { color: themes[theme].text },
          "& .MuiInputLabel-root": { color: themes[theme].text },
        }}
      />

      {categories.length > 0 ? (
        categories.map((category, index) => (
          <CategoryDropdown
            key={category.key}
            category={category}
            categoryIndex={index}
            handleCategoryChange={handleCategoryChange}
          />
        ))
      ) : (
        error ? (
          <p style={{ color: themes[theme].errorColor, marginTop: "16px" }}>{error}</p>
        ) : (
          <p style={{ color: "#888", fontStyle: "italic", marginTop: "16px" }}>
            Loading categories...
          </p>
        )
      )}

      {error && !categories.length && (
        <p style={{ color: themes[theme].errorColor, marginTop: "16px" }}>{error}</p>
      )}

      <Button
        variant="contained"
        color="primary"
        onClick={handleGenerateReport}
        disabled={loading}
        sx={{
          marginTop: "16px",
          ...themes[theme].button.split(" ").reduce((acc, cls) => {
            const [prop, value] = cls.split(":");
            if (prop === "hover") return { ...acc, "&:hover": { backgroundColor: value } };
            return { ...acc, backgroundColor: prop, color: value };
          }, {}),
        }}
      >
        {loading ? "Generating..." : "Generate Report"}
      </Button>

      {report && Array.isArray(report) && report.length > 0 && (
        <Paper
          elevation={3}
          sx={{
            marginTop: "20px",
            padding: "16px",
            backgroundColor: themes[theme].lighterCardColor,
          }}
        >
          <Typography variant="h3" sx={{ color: themes[theme].text }}>
            Generated Report:
          </Typography>
          {report.map((item, index) => (
            <div key={index} style={{ marginTop: "8px" }}>
              <Typography variant="h4" sx={{ color: themes[theme].text }}>
                {item.name || `Student ${index + 1}`}
              </Typography>
              <p style={{ color: themes[theme].text }}>{item.report || "No report text available"}</p>
            </div>
          ))}
        </Paper>
      )}

      {error && (
        <p style={{ color: themes[theme].errorColor, marginTop: "16px" }}>{error}</p>
      )}
    </Paper>
  );
};

export default ReportForm;
