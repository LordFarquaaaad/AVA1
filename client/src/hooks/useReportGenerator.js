// src/hooks/useReportGenerator.js
import { useState, useEffect, useMemo } from "react";
import { generateReport, createTemplate as createTemplateApi, getTemplates, updateTemplate as updateTemplateApi, deleteTemplate as deleteTemplateApi } from "../services/reportService";
import { getCategoriesBySchoolLevel } from "../constants/categories";

const useReportGenerator = (initialCategories) => {
  const [students, setStudents] = useState([
    {
      name: "",
      schoolLevel: "Primary School",
      categories: initialCategories || getCategoriesBySchoolLevel("Primary School").map((category) => ({
        ...category,
        value: "",
        comments: "",
      })),
    },
  ]);
  const [report, setReport] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Extract schoolLevel using useMemo to avoid unnecessary re-renders
  const schoolLevel = useMemo(() => students[0]?.schoolLevel || "Primary School", [students]);

  useEffect(() => {
    console.log("🎯 useReportGenerator useEffect triggered with schoolLevel:", schoolLevel);
    loadTemplates(schoolLevel);
  }, [schoolLevel]); // Now depends on a simple variable

  const loadTemplates = async (schoolLevel) => {
    console.log("📥 Loading templates for schoolLevel:", schoolLevel);
    try {
      const response = await getTemplates(schoolLevel);
      console.log("📥 Templates loaded:", response);
      setTemplates(response.data || []);
    } catch (error) {
      console.error("❌ Error loading templates:", error);
      setTemplates([]);
    }
  };

  const createTemplate = async (templateData) => {
    console.log("📤 Creating template:", templateData);
    try {
      const response = await createTemplateApi(templateData);
      console.log("📥 Template created:", response);
      setTemplates([...templates, response.data]);
      return response.data;
    } catch (error) {
      console.error("❌ Error creating template:", error);
      throw error;
    }
  };

  const updateTemplate = async (templateId, templateData) => {
    console.log("📤 Updating template:", { templateId, templateData });
    try {
      const response = await updateTemplateApi(templateId, templateData);
      console.log("📥 Template updated:", response);
      setTemplates(templates.map((t) => (t.id === templateId ? response.data : t)));
    } catch (error) {
      console.error("❌ Error updating template:", error);
      throw error;
    }
  };

  const deleteTemplate = async (templateId) => {
    console.log("📤 Deleting template:", templateId);
    try {
      await deleteTemplateApi(templateId);
      console.log("📥 Template deleted:", templateId);
      setTemplates(templates.filter((t) => t.id !== templateId));
    } catch (error) {
      console.error("❌ Error deleting template:", error);
      throw error;
    }
  };

  const applyTemplate = (template, studentIndex) => {
    console.log("📌 Applying template to student:", { template, studentIndex });
    setStudents((prevStudents) =>
      prevStudents.map((student, index) =>
        index === studentIndex
          ? {
              ...student,
              categories: template.categories.map((cat) => ({
                ...cat,
                value: "",
                comments: "",
              })),
            }
          : student
      )
    );
  };

  const handleStudentChange = (studentIndex, field, value) => {
    console.log(`📌 Updating student:`, { studentIndex, field, value });
    setStudents((prevStudents) =>
      prevStudents.map((student, index) =>
        index === studentIndex ? { ...student, [field]: value } : student
      )
    );
  };

  const handleCategoryChange = (studentIndex, categoryIndex, field, value) => {
    console.log(`📌 Updating category:`, { studentIndex, categoryIndex, field, value });
    setStudents((prevStudents) =>
      prevStudents.map((student, index) => {
        if (index === studentIndex) {
          const updatedCategories = [...(student.categories || [])];
          if (field === "remove") {
            updatedCategories.splice(categoryIndex, 1);
          } else {
            updatedCategories[categoryIndex] = {
              ...updatedCategories[categoryIndex],
              [field]: value,
            };
          }
          return { ...student, categories: updatedCategories };
        }
        return student;
      })
    );
  };

  const addCategory = (studentIndex) => {
    console.log("🎯 Adding category to student:", studentIndex);
    setStudents((prevStudents) =>
      prevStudents.map((student, index) => {
        if (index === studentIndex) {
          const currentCategories = student.categories || [];
          return {
            ...student,
            categories: [
              ...currentCategories,
              { key: `newCategory${currentCategories.length + 1}`, value: "", comments: "", options: ["Struggling", "Meets Expectations", "Excelling"] },
            ],
          };
        }
        return student;
      })
    );
  };

  const addStudent = () => {
    console.log("🎯 Add Student button clicked");
    setStudents((prevStudents) => [
      ...prevStudents,
      {
        name: "",
        schoolLevel: prevStudents[0]?.schoolLevel || "Primary School",
        categories: (initialCategories || getCategoriesBySchoolLevel(prevStudents[0]?.schoolLevel || "Primary School")).map((category) => ({
          ...category,
          value: "",
          comments: "",
        })),
      },
    ]);
  };

  const handleGenerateReport = async () => {
    console.log("🎯 Generate Report button clicked in useReportGenerator");
    try {
      setLoading(true);
      setError(null);

      const studentsData = students.map((student) => {
        const mappedCategories = {};
        student.categories?.forEach((category, index) => {
          const keyMap = {
            0: "academicPerformance",
            1: "behaviorAttitude",
            2: "participationEngagement",
            3: "effortWorkEthic",
            4: "socialEmotionalDevelopment",
            5: "attendancePunctuality",
          };
          const mappedKey = keyMap[index] || category.key || `customCategory${index}`;
          mappedCategories[mappedKey] = { value: category.value, comments: category.comments };
        });

        return {
          name: student.name || "Unnamed Student",
          schoolLevel: student.schoolLevel,
          categories: mappedCategories,
        };
      });

      console.log("📤 Sending student data:", JSON.stringify({ students: studentsData }, null, 2));

      const response = await generateReport({ students: studentsData });

      console.log("📥 Received backend response:", JSON.stringify(response, null, 2));

      if (response && Array.isArray(response.reports)) {
        setReport(response.reports);
      } else if (response && response.name && response.report) {
        setReport([{ name: response.name, report: response.report }]);
      } else if (response && typeof response === "object") {
        const reportData = response.reports || response;
        setReport(
          Array.isArray(reportData)
            ? reportData
            : [{ name: reportData.name || "Unnamed Student", report: reportData.report || "No report generated" }]
        );
      } else {
        throw new Error("Invalid response format from server: " + JSON.stringify(response, null, 2));
      }
    } catch (error) {
      console.error("❌ Failed to generate report:", error);
      setError("An error occurred while generating the report.");
    } finally {
      setLoading(false);
    }
  };

  return {
    students,
    report,
    templates,
    loading,
    error,
    handleStudentChange,
    handleCategoryChange,
    addCategory,
    addStudent,
    handleGenerateReport,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    loadTemplates,
    applyTemplate,
  };
};

export default useReportGenerator;
