//Categorydropdowns
import React from "react";
import { Select, MenuItem, FormControl, InputLabel, TextField, IconButton, Paper } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useTheme } from "../../context/theme/ThemeContext";

const CategoryDropdown = ({ category, studentIndex, categoryIndex, handleCategoryChange }) => {
  const { theme, themes } = useTheme();

  return (
    <Paper
      elevation={2}
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 2,
        padding: "16px",
        borderRadius: "8px",
        backgroundColor: themes[theme].lighterCardColor,
        marginBottom: "16px",
      }}
    >
      {/* Dropdown */}
      <FormControl fullWidth>
        <InputLabel shrink={!!category.value}>{category.label}</InputLabel>
        <Select
          value={category.value || ""}
          onChange={(e) => {
            handleCategoryChange(studentIndex, categoryIndex, "value", e.target.value);
          }}
          label={category.label}
          sx={{
            backgroundColor: themes[theme].lighterCardColor,
          }}
        >
          <MenuItem value="" disabled>
            Select an option
          </MenuItem>
          {category.options.map((option, index) => (
            <MenuItem key={option} value={option}>
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
        onChange={(e) => {
          handleCategoryChange(studentIndex, categoryIndex, "comments", e.target.value);
        }}
        sx={{
          backgroundColor: themes[theme].lighterCardColor,
        }}
      />

      {/* Delete Button */}
      <IconButton
        onClick={() => handleCategoryChange(studentIndex, categoryIndex, "remove", null)}
        sx={{
          color: themes[theme].errorColor,
        }}
      >
        <DeleteIcon />
      </IconButton>
    </Paper>
  );
};

export default CategoryDropdown;













