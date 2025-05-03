import { Box, Divider, Drawer, List, Paper, Typography } from "@mui/material";
import MenuNode, { MenuItem } from "./menu-node";

const MobileHeaderMenu = ({ isOpen, toggleMenu, navItems }: { isOpen: boolean, toggleMenu: () => void, navItems: any[] }) => {

    const bottomMenuItems = [
        {
            text: "Contact",
            path: "/contact",
        },
    ] as MenuItem[]
    return (
        <Drawer
            open={isOpen}
            onClose={toggleMenu}
        >
            <Box
                sx={{
                    display: "flex",
                    flexDirection: "column",
                    width: 256,
                    height: "100%",
                    pt: 4,
                }}
            >
                <Paper
                    elevation={1}
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        justifyContent: "space-between",
                        height: "100%",
                        padding: 2.5,
                        bgcolor: "background.paperElevation1",
                    }}
                >
                    <List disablePadding>
                        {navItems.map((item) => (
                            <MenuNode key={item.path} item={item}/>
                        ))}
                    </List>

                    <Box sx={{ display: "flex", flexDirection: "column" }}>
                        <List disablePadding>
                            {bottomMenuItems.map((item) => (
                                <MenuNode 
                                    key={item.text} 
                                    item={item} 
                                    sxProps={{ ml: 0 }}
                                />
                            ))}
                        </List>
                        <Box
                            sx={{
                            height: 69,
                            padding: 2,
                            display: "flex",
                            flexDirection: "column",
                            }}
                        >
                            <Divider sx={{ width: "100%", mb: 1 }} />
                                <Typography variant="caption" color="text.secondary">
                                    © 2025 rxCheck. All rights reserved.
                                </Typography>
                        </Box>
                    </Box>
                </Paper>
            </Box>
        </Drawer>
    );
};

export default MobileHeaderMenu;