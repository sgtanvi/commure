import { Collapse, List, ListItem, ListItemButton, ListItemIcon, ListItemText, SxProps } from "@mui/material"
import { Typography } from "@mui/material"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"

import React, { useState } from "react"

//TODO: add support for routing
export interface MenuItem {
    text: string
    icon?: React.ReactNode
    path?: string
    children?: MenuItem[]
}

interface MenuNodeProps {
    item: MenuItem
    sxProps?: SxProps
}

const MenuNode = ({item, sxProps}: MenuNodeProps) => {

    // If item has no children, its a leaf and we return different logic
    if (!item.children) {
        return (
            <ListItem key={item.path} disablePadding>
                <ListItemButton 
                    id={item.path}
                    sx={{
                        pl: 2, 
                        py: 1, 
                        borderRadius: 2,
                        "&:hover": {
                                    bgcolor: "action.hover",
                                },
                                "&:selected": {
                                    bgcolor: "action.selected",
                                },
                        ...sxProps,
                            }}
                            //TODO: change to navigate to the correct page
                            onClick={() => {
                                //TODO: add router navigation
                            }}
                        >
                            {item.icon && <ListItemIcon sx={{ minWidth: 56 }}>{item.icon}</ListItemIcon>}
                            <ListItemText
                                disableTypography
                                primary={<Typography variant={'body1'} sx={{fontWeight: 700}} color="primary.white">{item.text}</Typography> }
                            />
                </ListItemButton>
            </ListItem>
        )
    }

    const [isExpanded, setIsExpanded] = useState(item.text == "Events" ? true : false)

    return (
        <React.Fragment key={item.path}>
            <ListItem key={item.path} disablePadding>
                <ListItemButton
                    sx={{px: 2, py: 1, borderRadius: 2, ...sxProps }}
                    onClick={() => {
                        setIsExpanded(!isExpanded);
                    }}
                >
                    <ListItemIcon sx={{ minWidth: 56 }}>{item.icon}</ListItemIcon>
                    <ListItemText
                        disableTypography
                        primary={<Typography variant={'body1'} sx={{fontWeight: 700}} color="primary.white">{item.text}</Typography> }
                    />
                    <ExpandMoreIcon
                        sx={{
                            transform: isExpanded   
                                ? "rotate(180deg)"
                                : "rotate(0deg)",
                            transition: "transform 0.3s",
                        }}
                        onClick={(e) => {
                            setIsExpanded(!isExpanded);
                            e.stopPropagation();
                        }}
                    />
                </ListItemButton>
            </ListItem>

            <Collapse in={isExpanded} timeout="auto" unmountOnExit>
            <List disablePadding>
                {item.children.map((child) => (
                    <MenuNode 
                        key={child.path} 
                        item={child} 
                        sxProps={sxProps} 
                    />
                ))}
            </List>
            </Collapse>
        </React.Fragment>
    )
}

export default MenuNode