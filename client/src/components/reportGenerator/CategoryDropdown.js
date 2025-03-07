import React from "react";
import { Select, MenuItem, FormControl, InputLabel, TextField, IconButton, Paper } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useTheme } from "../../context/theme/ThemeContext";

const CategoryDropdown = ({ category, studentIndex, categoryIndex, handleCategoryChange }) => {
  const { theme, themes } = useTheme();

  // Fallback to 'scholar' if theme is undefined or invalid
  const currentTheme = theme && Object.keys(themes).includes(theme) ? theme : "scholar";
  // Ensure category.options is always an array, defaulting to an empty array or a fallback
  const options = category.options || ["Struggling", "Meets Expectations", "Excelling"]; // Fallback options

  return (
    <Paper
      elevation={2}
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 2,
        padding: "16px",
        borderRadius: "8px",
        backgroundColor: themes[currentTheme].lighterCardColor, // Use currentTheme
        marginBottom: "16px",
      }}
    >
      {/* Dropdown */}
      <FormControl fullWidth>
        <InputLabel shrink={!!category.value} sx={{ color: themes[currentTheme].text }}>
          {category.label}
        </InputLabel>
        <Select
          value={category.value || ""}
          onChange={(e) => handleCategoryChange(studentIndex, categoryIndex, "value", e.target.value)}
          label={category.label}
          sx={{
            backgroundColor: themes[currentTheme].lighterCardColor, // Use currentTheme
            color: themes[currentTheme].text,
          }}
        >
          <MenuItem value="" disabled sx={{ color: themes[currentTheme].text }}>
            Select an option
          </MenuItem>
          {options.map((option, index) => ( // Use the safe options array
            <MenuItem key={option} value={option} sx={{ color: themes[currentTheme].text }}>
              {option}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {/* Comments Input */}
      <TextField
        label="Comments"
        fullWidth
        value={category.comments || ""}
        onChange={(e) => handleCategoryChange(studentIndex, categoryIndex, "comments", e.target.value)}
        sx={{
          backgroundColor: themes[currentTheme].lighterCardColor, // Use currentTheme
          "& .MuiInputBase-input": { color: themes[currentTheme].text },
          "& .MuiInputLabel-root": { color: themes[currentTheme].text },
        }}
      />

      {/* Delete Button */}
      <IconButton
        onClick={() => handleCategoryChange(studentIndex, categoryIndex, "remove", null)}
        sx={{
          color: themes[currentTheme].errorColor, // Use currentTheme
        }}
      >
        <DeleteIcon />
      </IconButton>
    </Paper>
  );
};

export default CategoryDropdown;
