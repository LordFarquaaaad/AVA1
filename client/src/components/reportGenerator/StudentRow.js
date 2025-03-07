import React, { useState } from "react";
import { TextField, Paper, Button, Select, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, Typography, Alert } from "@mui/material";
import CategoryDropdown from "./CategoryDropdown";
import { useTheme } from "../../context/theme/ThemeContext";
import useReportGenerator from "../../hooks/useReportGenerator"; // Default import

const StudentRow = ({ student, studentIndex, handleCategoryChange, handleStudentChange, addCategory }) => {
  const { theme, themes } = useTheme();
  const {
    templates,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    loadTemplates,
    applyTemplate,
  } = useReportGenerator();

  const [openTemplateDialog, setOpenTemplateDialog] = useState(false);
  const [templateName, setTemplateName] = useState("");
  const [selectedTemplateId, setSelectedTemplateId] = useState(null);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false); // State for delete confirmation
  const [errorMessage, setErrorMessage] = useState(null); // State for error messages

  const categories = student.categories || [];

  const currentTheme = theme && Object.keys(themes).includes(theme) ? theme : "scholar";
  console.log("Theme in StudentRow:", currentTheme, themes);

  const handleSaveTemplate = async () => {
    if (!templateName.trim()) {
      setErrorMessage("Please enter a template name.");
      return;
    }

    const template = {
      name: templateName,
      categories: categories.map((cat) => ({ ...cat, value: "", comments: "" })),
      schoolLevel: student.schoolLevel,
    };

    try {
      if (selectedTemplateId) {
        await updateTemplate(selectedTemplateId, template);
      } else {
        await createTemplate(template);
      }
      setTemplateName("");
      setSelectedTemplateId(null);
      setOpenTemplateDialog(false);
      setErrorMessage(null);
      await loadTemplates(student.schoolLevel);
    } catch (error) {
      console.error("Error saving template:", error);
      setErrorMessage("Failed to save template. Please try again.");
    }
  };

  const handleDeleteTemplate = async (templateId) => {
    setDeleteConfirmOpen(false); // Close confirmation dialog after action
    try {
      await deleteTemplate(templateId);
      await loadTemplates(student.schoolLevel);
      setErrorMessage(null);
    } catch (error) {
      console.error("Error deleting template:", error);
      setErrorMessage("Failed to delete template. Please try again.");
    }
  };

  return (
    <Paper elevation={2} sx={{ padding: "16px", borderRadius: "8px", marginBottom: "16px", backgroundColor: themes[currentTheme].cardColor }}>
      {/* ✅ Student Name Input */}
      <TextField
        label="Student Name"
        value={student.name || ""}
        onChange={(e) => handleStudentChange(studentIndex, "name", e.target.value)}
        fullWidth
        margin="normal"
        sx={{ backgroundColor: themes[currentTheme].lighterCardColor, "& .MuiInputBase-input": { color: themes[currentTheme].text }, "& .MuiInputLabel-root": { color: themes[currentTheme].text } }}
      />

      {/* ✅ Category Dropdowns */}
      {categories.length > 0 ? (
        categories.map((category, categoryIndex) => (
          <CategoryDropdown
            key={category.key || categoryIndex}
            category={category}
            studentIndex={studentIndex}
            categoryIndex={categoryIndex}
            handleCategoryChange={handleCategoryChange}
          />
        ))
      ) : (
        <p style={{ color: themes[currentTheme].text, fontStyle: "italic" }}>No categories added yet.</p>
      )}

      {/* ✅ Template Management Section */}
      <Typography variant="h6" sx={{ color: themes[currentTheme].text, marginTop: "16px" }}>
        Custom Report Templates
      </Typography>

      <Button
        variant="contained"
        color="secondary"
        onClick={() => setOpenTemplateDialog(true)}
        sx={{ marginTop: "8px", marginRight: "8px", ...themes[currentTheme].button }}
      >
        Create/Save Template
      </Button>

      <Select
        value=""
        onChange={(e) => applyTemplate(templates.find((t) => t.id === e.target.value), studentIndex)}
        sx={{ marginTop: "8px", marginRight: "8px", backgroundColor: themes[currentTheme].lighterCardColor, color: themes[currentTheme].text }}
        displayEmpty
      >
        <MenuItem value="" disabled sx={{ color: themes[currentTheme].text }}>
          Load Template
        </MenuItem>
        {templates.map((template) => (
          <MenuItem key={template.id} value={template.id} sx={{ color: themes[currentTheme].text }}>
            {template.name}
          </MenuItem>
        ))}
      </Select>

      <Button
        variant="contained"
        color="secondary"
        onClick={() => setDeleteConfirmOpen(true)}
        sx={{ marginTop: "8px", ...themes[currentTheme].button }}
      >
        Delete Template
      </Button>

      {/* Error Message */}
      {errorMessage && (
        <Alert severity="error" sx={{ marginTop: "16px", backgroundColor: themes[currentTheme].cardColor, color: themes[currentTheme].errorColor }}>
          {errorMessage}
          <Button onClick={() => setErrorMessage(null)} sx={{ color: themes[currentTheme].errorColor }}>
            Dismiss
          </Button>
        </Alert>
      )}

      {/* Template Creation Dialog */}
      <Dialog open={openTemplateDialog} onClose={() => setOpenTemplateDialog(false)}>
        <DialogTitle sx={{ color: themes[currentTheme].text }}>Create or Edit Template</DialogTitle>
        <DialogContent>
          <TextField
            label="Template Name"
            fullWidth
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
            sx={{ backgroundColor: themes[currentTheme].lighterCardColor, marginTop: "16px", "& .MuiInputBase-input": { color: themes[currentTheme].text }, "& .MuiInputLabel-root": { color: themes[currentTheme].text } }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTemplateDialog(false)} sx={{ color: themes[currentTheme].text }}>
            Cancel
          </Button>
          <Button onClick={handleSaveTemplate} sx={themes[currentTheme].button}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteConfirmOpen} onClose={() => setDeleteConfirmOpen(false)}>
        <DialogTitle sx={{ color: themes[currentTheme].text }}>Confirm Deletion</DialogTitle>
        <DialogContent>
          <Typography sx={{ color: themes[currentTheme].text }}>
            Are you sure you want to delete a template? Please enter the template ID:
          </Typography>
          <TextField
            label="Template ID"
            fullWidth
            onChange={(e) => setSelectedTemplateId(e.target.value)}
            sx={{ backgroundColor: themes[currentTheme].lighterCardColor, marginTop: "16px", "& .MuiInputBase-input": { color: themes[currentTheme].text }, "& .MuiInputLabel-root": { color: themes[currentTheme].text } }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteConfirmOpen(false)} sx={{ color: themes[currentTheme].text }}>
            Cancel
          </Button>
          <Button onClick={() => handleDeleteTemplate(selectedTemplateId)} sx={themes[currentTheme].button} disabled={!selectedTemplateId}>
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* ✅ Add Category Button */}
      <Button variant="contained" color="secondary" onClick={() => addCategory(studentIndex)} sx={{ marginTop: "16px", marginLeft: "8px", ...themes[currentTheme].button }}>
        ➕ Add Category
      </Button>
    </Paper>
  );
};

export default React.memo(StudentRow);




