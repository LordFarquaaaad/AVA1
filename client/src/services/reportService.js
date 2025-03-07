// src/services/reportService.js
import apiClient from "./apiClient";

// Existing report generation functions (unchanged)
export const generateReport = async (studentsData) => {
  try {
    console.log("Generating report, sending data:", JSON.stringify(studentsData, null, 2)); // Debug
    const response = await apiClient.post("/api/reports/reports/generate", studentsData, {
      headers: { "Content-Type": "application/json" }, // Explicitly set content type
    });
    console.log("API response in reportService (generateReport):", JSON.stringify(response.data, null, 2));
    return Array.isArray(response.data.reports) ? response.data : { reports: Array.isArray(response.data) ? response.data : [response.data] };
  } catch (error) {
    console.error("❌ Error generating report:", {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      config: error.config, // Log request config (method, URL, headers)
    });
    throw error;
  }
};

export const generateBulkReports = async (students) => {
  try {
    const response = await apiClient.post("/api/reports/reports/generate-bulk", { students });
    console.log("API response in reportService (generateBulkReports):", JSON.stringify(response.data, null, 2));
    return response.data.reports;
  } catch (error) {
    console.error("❌ Error generating bulk reports:", error.response?.status, error.response?.data || error.message);
    throw error;
  }
};

// Template Management Functions (unchanged)
export const createTemplate = async (templateData) => {
  try {
    const response = await apiClient.post("/api/reports/templates", templateData);
    console.log("API response in reportService (createTemplate):", JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    console.error("❌ Error creating template:", error.response?.status, error.response?.data || error.message);
    throw error;
  }
};

export const getTemplates = async (schoolLevel) => {
  try {
    const response = await apiClient.get(`/api/reports/templates?schoolLevel=${schoolLevel}`);
    console.log("API response in reportService (getTemplates):", JSON.stringify(response.data, null, 2));
    return response;
  } catch (error) {
    console.error("❌ Error fetching templates:", error.response?.status, error.response?.data || error.message);
    throw error;
  }
};

export const updateTemplate = async (templateId, templateData) => {
  try {
    const response = await apiClient.put(`/api/reports/templates/${templateId}`, templateData);
    console.log("API response in reportService (updateTemplate):", JSON.stringify(response.data, null, 2));
    return response.data;
  } catch (error) {
    console.error("❌ Error updating template:", error.response?.status, error.response?.data || error.message);
    throw error;
  }
};

export const deleteTemplate = async (templateId) => {
  try {
    await apiClient.delete(`/api/reports/templates/${templateId}`);
    console.log(`Template ${templateId} deleted successfully`);
  } catch (error) {
    console.error("❌ Error deleting template:", error.response?.status, error.response?.data || error.message);
    throw error;
  }
};