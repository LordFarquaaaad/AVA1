//pages/ReportsPage.js
import React, { useState, useEffect } from "react";
import { Paper, Typography, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import PrimarySchoolReportPage from "./PrimarySchoolReportPage";
import HighSchoolReportPage from "./HighSchoolReportPage";

const ReportsPage = () => {
  const [schoolLevel, setSchoolLevel] = useState("Primary School");

  useEffect(() => {
    console.log("✅ ReportsPage component mounted");
  }, []);

  const handleSchoolLevelChange = (event) => {
    setSchoolLevel(event.target.value);
  };
  return (
    <Paper elevation={3} sx={{ padding: "16px", margin: "16px" }}>
      <Typography variant="h4" gutterBottom>
        Report Generator
      </Typography>

      <FormControl fullWidth sx={{ marginBottom: "16px" }}>
        <InputLabel>School Level</InputLabel>
        <Select value={schoolLevel} onChange={handleSchoolLevelChange} label="School Level">
          <MenuItem value="Primary School">Primary School</MenuItem>
          <MenuItem value="High School">High School</MenuItem>
        </Select>
      </FormControl>

      {schoolLevel === "Primary School" ? (
        <PrimarySchoolReportPage />
      ) : (
        <HighSchoolReportPage />
      )}
    </Paper>
  );
};

export default ReportsPage;

