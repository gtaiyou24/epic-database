import type { NextConfig } from "next";

const nextConfig: NextConfig = {
    output: 'standalone',  // Cloud Run にデプロイするために standalone を指定
    rewrites: async () => {
        return [
            {
                source: "/api/py/:path*",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://api:8000/:path*"
                        : "/api/py/:path*",
            },
            {
                source: "/docs",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://api:8000/docs"
                        : "/api/py/docs",
            },
            {
                source: "/openapi.json",
                destination:
                    process.env.NODE_ENV === "development"
                        ? "http://api:8000/openapi.json"
                        : "/api/py/openapi.json",
            },
        ];
    },
};

export default nextConfig;
