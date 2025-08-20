// src/middleware.js
import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: {
    signIn: "/auth/signup",
  },
});

export const config = {
  matcher: ["/feature", "/dashboard", "/user/:path*"],
};