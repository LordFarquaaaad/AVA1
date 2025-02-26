// src/services/reportService.js
export const generateReport = async (studentsData) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/reports/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(studentsData)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData?.message || 'Unknown error'}`);
    }

    const data = await response.json();
    console.log("API response in reportService:", JSON.stringify(data, null, 2)); // Debug
    // Ensure the response is an array of reports, even if the backend returns a single object
    return Array.isArray(data.reports) ? data : { reports: Array.isArray(data) ? data : [data] };
  } catch (error) {
    console.error("❌ Error generating report:", error);
    throw error;
  }
};

export const generateBulkReports = async (students) => {
  try {
    const response = await fetch("http://127.0.0.1:5000/reports/generate-bulk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ students }), // Ensure this matches the backend's expectations
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        `HTTP error! Status: ${response.status}, Message: ${errorData?.message || 'Unknown error'}`
      );
    }

    const data = await response.json();
    return data.reports; // Return the generated reports
  } catch (error) {
    console.error("❌ Error generating bulk reports:", error);
    throw error;
  }
};