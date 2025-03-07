// src/components/LoginPage.js
import React, { useState, useCallback } from "react";
import { useAuth } from "../context/AuthContext";
import { Button, TextField, Container, Typography, Box, CircularProgress } from "@mui/material";
import { useTheme } from "../context/theme/ThemeContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [credentials, setCredentials] = useState({ identifier: "", password: "" });
  const { login, loading, error } = useAuth();
  const { theme, themes } = useTheme();
  const navigate = useNavigate();
  const currentTheme = theme && Object.keys(themes).includes(theme) ? theme : "scholar";

  const handleChange = useCallback((e) => {
    setCredentials((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }, []);

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (loading) return; // Prevent multiple submissions while loading
      try {
        await login(credentials.identifier, credentials.password);
        const next = new URLSearchParams(window.location.search).get("next") || "/dashboard";
        navigate(next);
      } catch (err) {
        console.error("Login error:", err);
        setCredentials((prev) => ({ ...prev, password: "" })); // Clear password on failure
      }
    },
    [credentials, login, navigate, loading]
  );

  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Box sx={{ bgcolor: themes[currentTheme].cardColor, p: 4, borderRadius: 2, boxShadow: 1 }}>
        <Typography variant="h4" gutterBottom sx={{ color: themes[currentTheme].text }}>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Identifier (Username or Email)"
            name="identifier"
            value={credentials.identifier}
            onChange={handleChange}
            margin="normal"
            variant="outlined"
            autoComplete="username"
            sx={{
              backgroundColor: themes[currentTheme].lighterCardColor,
              "& .MuiInputBase-input": { color: themes[currentTheme].text },
              "& .MuiInputLabel-root": { color: themes[currentTheme].text },
            }}
          />
          <TextField
            fullWidth
            label="Password"
            name="password"
            type="password"
            value={credentials.password}
            onChange={handleChange}
            margin="normal"
            variant="outlined"
            autoComplete="current-password"
            sx={{
              backgroundColor: themes[currentTheme].lighterCardColor,
              "& .MuiInputBase-input": { color: themes[currentTheme].text },
              "& .MuiInputLabel-root": { color: themes[currentTheme].text },
            }}
          />
          {loading && (
            <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
              <CircularProgress sx={{ color: themes[currentTheme].text }} />
            </Box>
          )}
          {error && (
            <Typography color="error" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={loading}
            sx={{ mt: 2, ...themes[currentTheme].button }}
          >
            {loading ? "Logging in..." : "Login"}
          </Button>
        </form>
      </Box>
    </Container>
  );
};

export default LoginPage;
