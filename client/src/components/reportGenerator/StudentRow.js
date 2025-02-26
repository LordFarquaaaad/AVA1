//StudentRow
import React from "react";
import { TextField, Paper, Button } from "@mui/material";
import CategoryDropdown from "./CategoryDropdown";

const StudentRow = ({ student, studentIndex, handleCategoryChange, handleStudentChange, addCategory }) => {
  return (
    <Paper elevation={2} sx={{ padding: "16px", borderRadius: "8px", marginBottom: "16px" }}>
      {/* ✅ Student Name Input */}
      <TextField
        label="Student Name"
        value={student.name || ""}
        onChange={(e) => handleStudentChange(studentIndex, "name", e.target.value)}
        fullWidth
        margin="normal"
      />

      {/* ✅ Category Dropdowns */}
      {student.categories.length > 0 ? (
        student.categories.map((category, categoryIndex) => (
          <CategoryDropdown
            key={category.key || categoryIndex}
            category={category}
            studentIndex={studentIndex}
            categoryIndex={categoryIndex}
            handleCategoryChange={handleCategoryChange}
          />
        ))
      ) : (
        <p style={{ color: "#888", fontStyle: "italic" }}>No categories added yet.</p>
      )}

      {/* ✅ Add Category Button */}
      <Button variant="contained" color="secondary" onClick={() => addCategory(studentIndex)} sx={{ marginTop: "16px" }}>
        ➕ Add Category
      </Button>
    </Paper>
  );
};

export default StudentRow;




