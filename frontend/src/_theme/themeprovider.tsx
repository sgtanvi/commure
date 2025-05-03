"use client";

import {
    CssBaseline,
    ThemeProvider as MuiThemeProvider,
    createTheme,
} from "@mui/material";
import React from "react";

declare module "@mui/material/styles" {
    interface PaletteColor {
        hover?: string;
        selected?: string;
        focus?: string;
        focusVisible?: string;
        outlinedBorder?: string;
    }
    
    interface SimplePaletteColorOptions {
        hover?: string;
        selected?: string;
        focus?: string;
        focusVisible?: string;
        outlinedBorder?: string;
    }

    interface TypeBackground {
        paperElevation0?: string;
        paperElevation1?: string;
        paperElevation2?: string;
        paperElevation3?: string;
        paperElevation4?: string;
        paperElevation5?: string;
        paperElevation6?: string;
        paperElevation7?: string;
        paperElevation8?: string;
        paperElevation9?: string;
    }
}

    const appTheme = createTheme({
        palette: {
        mode: "dark",
        primary: {
            main: "#894ac9",
            light: "#c8a5e8",
            dark: "#6541b8",
            contrastText: "#ffffffde",
            hover: "#894ac914",
            selected: "#894ac929",
            focus: "#894ac91f",
            focusVisible: "#894ac94c",
            outlinedBorder: "#894ac980",
        },
        secondary: {
            main: "#2196f3",
            light: "#90caf9",
            dark: "#1976d2",
            contrastText: "#ffffffde",
        },
        error: {
            main: "#f44336",
            light: "#e57373",
            dark: "#d32f2f",
            contrastText: "#ffffff",
        },
        warning: {
            main: "#ffa726",
            light: "#ffb74d",
            dark: "#f57c00",
            contrastText: "#000000de",
        },
        info: {
            main: "#29b6f6",
            light: "#4fc3f7",
            dark: "#0288d1",
            contrastText: "#000000de",
        },
        success: {
            main: "#66bb6a",
            light: "#81c784",
            dark: "#388e3c",
            contrastText: "#000000de",
        },
        text: {
            primary: "#ffffff",
            secondary: "#ffffffb2",
            disabled: "#ffffff61",
        },
        background: {
            default: "#000000",
            paperElevation0: "#000014",
            paperElevation1: "#111928",
            paperElevation2: "#1F2A3D",
            paperElevation3: "#2F3B52",
            paperElevation4: "#3C4962",
            paperElevation5: "#515C73",
            paperElevation6: "#636D81",
            paperElevation7: "#7F8696",
            paperElevation8: "#9AA1AD",
            paperElevation9: "#bB6B8C2",
        },
        action: {
            active: "#ffffff8f",
            hover: "#ffffff14",
            selected: "#ffffff29",
            disabled: "#ffffff61",
            disabledBackground: "#ffffff1f",
            focus: "#ffffff1f",
        },
        divider: "#ffffff1f",
        common: {
            black: "#000000",
            white: "#ffffff",
        },
        },
        typography: {
        fontFamily: ['var(--font-roboto)', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'].join(","),
        h1: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "96px",
            fontWeight: 300,
            letterSpacing: "-1.5px",
            lineHeight: 1.167,
        },
        h2: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "60px",
            fontWeight: 300,
            letterSpacing: "-0.5px",
            lineHeight: 1.2,
        },
        h3: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "48px",
            fontWeight: 400,
            letterSpacing: "0px",
            lineHeight: 1.167,
        },
        h4: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "34px",
            fontWeight: 400,
            letterSpacing: "0.25px",
            lineHeight: 1.235,
        },
        h5: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "24px",
            fontWeight: 400,
            letterSpacing: "0px",
            lineHeight: 1.334,
        },
        h6: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "20px",
            fontWeight: 500,
            letterSpacing: "0.15px",
            lineHeight: 1.6,
        },
        subtitle1: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "16px",
            fontWeight: 400,
            letterSpacing: "0.15px",
            lineHeight: 1.75,
        },
        subtitle2: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "14px",
            fontWeight: 500,
            letterSpacing: "0.1px",
            lineHeight: 1.57,
        },
        body1: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "16px",
            fontWeight: 400,
            letterSpacing: "0.15px",
            lineHeight: 1.5,
        },
        body2: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "14px",
            fontWeight: 400,
            letterSpacing: "0.15px",
            lineHeight: 1.43,
        },
        caption: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "12px",
            fontWeight: 400,
            letterSpacing: "0.4px",
            lineHeight: 1.66,
        },
        overline: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "12px",
            fontWeight: 400,
            letterSpacing: "1px",
            lineHeight: 2.66,
        },
        button: {
            fontFamily: 'var(--font-roboto), Roboto, Helvetica',
            fontSize: "14px",
            fontWeight: 500,
            letterSpacing: "0.4px",
            lineHeight: 1.75,
            textTransform: "none",
        },
        },
        components: {
        MuiCssBaseline: {
            styleOverrides: {
            body: {
                backgroundColor: "#000000",
                color: "#ffffff",
            },
            },
        },
        MuiButton: {
            styleOverrides: {
            root: {
                textTransform: "none",
            },
            sizeLarge: {
                fontSize: "15px",
                fontWeight: 500,
                letterSpacing: "0.46px",
                lineHeight: "26px",
            },
            sizeMedium: {
                fontSize: "14px",
                fontWeight: 500,
                letterSpacing: "0.4px",
                lineHeight: "24px",
            },
            sizeSmall: {
                fontSize: "13px",
                fontWeight: 500,
                letterSpacing: "0.46px",
                lineHeight: "22px",
            },
            },
        },
        MuiTableCell: {
            styleOverrides: {
            head: ({ theme }) => ({
                ...theme.typography.subtitle2,
                fontFamily: "Roboto, Helvetica",
                fontSize: "14px",
                fontWeight: 500,
                letterSpacing: "0.17px",
                lineHeight: "24px",
            }),
            body: ({ theme }) => ({
                ...theme.typography.body2,
            }),
            },
        },
        MuiListItemText: {
            styleOverrides: {
            primary: ({ theme }) => ({
                ...theme.typography.subtitle1,
            }),
            secondary: ({ theme }) => ({
                ...theme.typography.body2,
            }),
            },
        },
        MuiAlert: {
            styleOverrides: {
            root: {
                borderRadius: "4px",
            },
            message: {
                padding: "8px 0",
            },
            icon: {
                padding: "7px 0",
            },
            standardInfo: {
                backgroundColor: "#071318",
                color: "#b8e7fb",
            },
            },
        },
        MuiAlertTitle: {
            styleOverrides: {
            root: {
                fontFamily: "Roboto, Helvetica",
                fontSize: "16px",
                fontWeight: 500,
                letterSpacing: "0.15px",
                lineHeight: 1.5,
                marginTop: "-1px",
            },
            },
        },
        },
    });
    
export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
    return (
        <MuiThemeProvider theme={appTheme}>
            <CssBaseline />
            {children}
        </MuiThemeProvider>
    );
};