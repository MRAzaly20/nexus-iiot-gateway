import NextAuth from "next-auth";
import { authOptions } from "@/lib/auth";

// Export the handlers for each HTTP method
export const GET = NextAuth(authOptions);
export const POST = NextAuth(authOptions);