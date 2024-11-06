'use client'

import { ReactNode } from 'react'
import {QueryClient, QueryClientProvider} from "@tanstack/react-query";
import {TooltipProvider} from "@/components/ui/tooltip";
import {ThemeProvider} from "next-themes";
import {SessionProvider} from "next-auth/react";

export default function Provider({ children }: { children: ReactNode }) {
    const queryClient = new QueryClient();
    return (
        <SessionProvider>
            <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
                <TooltipProvider>
                    <QueryClientProvider client={queryClient}>
                        {children}
                    </QueryClientProvider>
                </TooltipProvider>
            </ThemeProvider>
        </SessionProvider>
    );
}