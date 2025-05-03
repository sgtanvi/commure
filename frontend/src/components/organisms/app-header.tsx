import { useState } from "react"

import {
    IconButton,
    ListItemText,
    ListItemButton,
    AppBar as MuiAppBar,
    Stack,
    Toolbar,
    Typography,
    Link,
    Button,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { useIsMobile } from "../../hooks/use-mobile"
import MobileHeaderMenu from "../molecules/mobile-header";
import { MenuItem } from "../molecules/menu-node";
import { Outlet } from "react-router-dom";

export function AppHeader() {
    const [sidebarOpen, setSidebarOpen] = useState(false)
    const isMobile = useIsMobile()

    const navItems = [
        {
            text: "Home",
            path: "/",
        },
        {
            text: "About",
            path: "/about",
        },
        {
            text: "Contact",
            path: "/contact",
        },
    ] as MenuItem[]
    return (
        <div className="flex flex-col w-full min-h-screen">
        <header className="pt-4 pb-4 pl-8 pr-8 h-16 flex items-center justify-center w-full ">
            <MuiAppBar
                sx={{
                height: 64,
                background:
                "linear-gradient(90deg, rgb(110, 161, 242) 0%, rgb(110, 161, 242) 100%)",
                px: 3,
                py: 0,
            }}
            >
                <Toolbar 
                    sx={{ 
                        minHeight: 64,
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        width: '100%',
                    }}>
                    {isMobile ? (
                        <IconButton
                            color="inherit"
                            edge="start"
                            disableFocusRipple={true}
                            disableRipple={true}
                            sx={{
                                "&:focus": {
                                    outline: "none",
                                },
                                "&.Mui-focusVisible": {
                                    boxShadow: "none",
                                    backgroundColor: "transparent",
                                },
                            }}
                            onClick={() => {
                                setSidebarOpen(!sidebarOpen)
                            }}
                        >
                            <MenuIcon sx={{ width: 36, height: 36 }} />
                        </IconButton>
                    ) :
                        <Stack
                            direction="row"
                            alignItems="center"
                            spacing={4}
                            sx={{ width: 123 }}
                        >
                            {navItems.map((item) => (
                                <Link 
                                    href={item.path} 
                                    key={item.path}
                                    sx={{ textDecoration: 'none', color: 'inherit', '&:hover': { color: 'inherit' } }}
                                >
                                    <ListItemButton 
                                        key={item.path}
                                        sx={{ borderRadius: 2, px: 2, py: 1 }}
                                    >
                                        <ListItemText
                                            disableTypography
                                            primary={<Typography variant={'body1'} sx={{fontWeight: 700}} color="primary.white">{item.text}</Typography> }
                                        />
                                    </ListItemButton>
                                </Link>
                            ))}
                        </Stack> 
                    }
                    <Link 
                        href="/loginsignup" 
                        key="/loginsignup"
                        sx={{ textDecoration: 'none', color: 'inherit', '&:hover': { color: 'inherit' } }}
                    >
                        <Button
                            color="inherit"
                            disableFocusRipple={true}
                            disableRipple={true}
                            sx={{
                                "&:focus": {
                                    outline: "none",
                                },
                                "&.Mui-focusVisible": {
                                    boxShadow: "none",
                                    backgroundColor: "transparent",
                                },
                                mr: 4,
                                backgroundColor: "white",
                                "&:hover": {
                                    backgroundColor: "#e0e0e0",
                                }
                            }}
                        >
                            <Typography variant="body2" sx={{fontWeight: 700}} color="black">Login/Sign Up</Typography>
                        </Button>
                    </Link>
                </Toolbar>
            </MuiAppBar>
            <MobileHeaderMenu isOpen={sidebarOpen} toggleMenu={() => setSidebarOpen(!sidebarOpen)} navItems={navItems} />
        </header>
        <main className="bg-white flex-grow">
            <Outlet />
        </main>
        </div>
    )
}
