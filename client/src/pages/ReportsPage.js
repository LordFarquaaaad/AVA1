//pages/ReportsPage.js
import React, { useState } from "react";
import { Button, Paper, Typography, Box, FormControl, InputLabel, Select, MenuItem } from "@mui/material";
import PrimarySchoolReportPage from "./PrimarySchoolReportPage";
import HighSchoolReportPage from "./HighSchoolReportPage";

const ReportsPage = () => {
  const [schoolLevel, setSchoolLevel] = useState("Primary School");

  const handleSchoolLevelChange = (event) => {
    setSchoolLevel(event.target.value);
  };

  return (
    <Paper elevation={3} sx={{ padding: "16px", margin: "16px" }}>
      <Typography variant="h4" gutterBottom>
        Report Generator
      </Typography>

      {/* School Level Dropdown */}
      <FormControl fullWidth sx={{ marginBottom: "16px" }}>
        <InputLabel>School Level</InputLabel>
        <Select
          value={schoolLevel}
          onChange={handleSchoolLevelChange}
          label="School Level"
        >
          <MenuItem value="Primary School">Primary School</MenuItem>
          <MenuItem value="High School">High School</MenuItem>
        </Select>
      </FormControl>

      {/* Render the appropriate report generator based on the selected school level */}
      {schoolLevel === "Primary School" ? (
        <PrimarySchoolReportPage />
      ) : (
        <HighSchoolReportPage />
      )}
    </Paper>
  );
};

export default ReportsPage;

