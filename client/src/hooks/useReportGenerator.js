//hooks/useReportGenerator
import { useState } from "react";
import { generateReport } from "../services/reportService";
import { getCategoriesBySchoolLevel } from "../constants/categories";

const useReportGenerator = () => {
  const [students, setStudents] = useState([
    {
      name: "",
      schoolLevel: "Primary School",
      categories: getCategoriesBySchoolLevel("Primary School").map((category) => ({
        ...category,
        value: "",
        comments: "",
      })),
    },
  ]);
  const [report, setReport] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // ✅ Update student name or school level
  const handleStudentChange = (studentIndex, field, value) => {
    console.log(`📌 Updating student:`, { studentIndex, field, value });
    setStudents((prevStudents) =>
      prevStudents.map((student, index) =>
        index === studentIndex ? { ...student, [field]: value } : student
      )
    );
  };

  // ✅ Update categories for a student
  const handleCategoryChange = (studentIndex, categoryIndex, field, value) => {
    setStudents((prevStudents) =>
      prevStudents.map((student, index) => {
        if (index === studentIndex) {
          const updatedCategories = [...student.categories];
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

  // ✅ Add a new category for a student
  const addCategory = (studentIndex) => {
    setStudents((prevStudents) =>
      prevStudents.map((student, index) =>
        index === studentIndex
          ? {
              ...student,
              categories: [
                ...student.categories,
                { key: `newCategory${student.categories.length + 1}`, value: "", comments: "" },
              ],
            }
          : student
      )
    );
  };

  // ✅ Add a new student
  const addStudent = () => {
    setStudents((prevStudents) => [
      ...prevStudents,
      {
        name: "",
        schoolLevel: "Primary School",
        categories: getCategoriesBySchoolLevel("Primary School").map((category) => ({
          ...category,
          value: "",
          comments: "",
        })),
      },
    ]);
  };

  // ✅ Generate report including student names
  const handleGenerateReport = async () => {
    try {
      setLoading(true);
      setError(null);

      const studentsData = students.map((student) => ({
        name: student.name || "Unnamed Student",
        schoolLevel: student.schoolLevel,
        categories: student.categories.reduce((acc, category) => {
          acc[category.key] = { value: category.value, comments: category.comments };
          return acc;
        }, {}),
      }));

      console.log("📤 Sending student data:", JSON.stringify({ students: studentsData }, null, 2));

      const response = await generateReport({ students: studentsData });

      console.log("📥 Received backend response:", JSON.stringify(response, null, 2)); // Detailed debug

      // Handle the backend response more flexibly
      if (response && Array.isArray(response.reports)) {
        setReport(response.reports);
      } else if (response && response.name && response.report) {
        setReport([{ name: response.name, report: response.report }]);
      } else if (response && typeof response === "object") {
        // Fallback for any unexpected object structure
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
    loading,
    error,
    handleStudentChange,
    handleCategoryChange,
    addCategory,
    addStudent,
    handleGenerateReport,
  };
};

export default useReportGenerator;

