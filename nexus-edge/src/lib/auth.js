// lib/auth.js
import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { PrismaClient } from "../generated/prisma/client.js";
import GoogleProvider from "next-auth/providers/google";
import GithubProvider from "next-auth/providers/github";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { PrismaAdapter } from "@auth/prisma-adapter";

const prisma = new PrismaClient();

export const hashPassword = async (password) => {
  if (typeof password !== 'string') {
    throw new Error('Password must be a string');
  }
  const saltRounds = 12;
  try {
    const hashedPassword = await bcrypt.hash(password, saltRounds);
    return hashedPassword;
  } catch (error) {
    console.error("Error hashing password:", error);
    throw new Error("Failed to hash password");
  }
};

export const verifyPassword = async (password, hashedPassword) => {
  try {
    const isValid = await bcrypt.compare(password, hashedPassword);
    return isValid;
  } catch (error) {
    console.error("Error verifying password:", error);
    throw new Error("Failed to verify password");
  }
};

export const createToken = (payload) => {
  const secret = process.env.JWT_SECRET;
  if (!secret) {
    throw new Error("JWT_SECRET is not defined in environment variables");
  }

  const options = {
    expiresIn: '7d',
  };

  try {
    const token = jwt.sign(payload, secret, options);
    return token;
  } catch (error) {
    console.error("Error creating JWT:", error);
    throw new Error("Failed to create authentication token");
  }
};

export const verifyToken = (token) => {
  const secret = process.env.JWT_SECRET;
  if (!secret) {
    throw new Error("JWT_SECRET is not defined in environment variables");
  }

  try {
    const decoded = jwt.verify(token, secret);
    return decoded;
  } catch (error) {
    console.error("Error verifying JWT:", error.message);
    throw new Error("Invalid or expired token");
  }
};

export const authOptions = {
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID,
      clientSecret: process.env.GITHUB_SECRET,
    }),
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
        firstName: { label: "First Name", type: "text" },
        lastName: { label: "Last Name", type: "text" },
        company: { label: "Company", type: "text" },
        action: { label: "Action", type: "text" }, // 'login' or 'signup'
      },
      async authorize(credentials) {
        try {
          if (!credentials) return null;

          const { email, password, firstName, lastName, company, action } = credentials;

          if (action === "signup") {
            // Validate input
            if (!email || !password || password.length < 8) {
              throw new Error("Invalid credentials");
            }

            if (!firstName || firstName.trim().length < 2) {
              throw new Error("First name must be at least 2 characters");
            }

            if (!lastName || lastName.trim().length < 2) {
              throw new Error("Last name must be at least 2 characters");
            }

            if (!company || company.trim().length < 2) {
              throw new Error("Company name is required");
            }

            // Check if user already exists
            const existingUser = await prisma.user.findUnique({
              where: { email },
            });

            if (existingUser) {
              throw new Error("User already exists with this email");
            }

            // Hash password
            const hashedPassword = await bcrypt.hash(password, 12);

            // Create user — TAMBAHKAN `name` di sini agar kompatibel dengan Google
            const user = await prisma.user.create({
              data: {
                email,
                password: hashedPassword,
                firstName,
                lastName,
                company,
                name: `${firstName} ${lastName}`, // 👈 PENTING: tambah ini agar tidak error `Unknown argument name`
              },
            });

            return {
              id: user.id.toString(),
              email: user.email,
              name: `${user.firstName} ${user.lastName}`, // dikirim ke session
              firstName: user.firstName,
              lastName: user.lastName,
              company: user.company,
            };
          } else {
            // Login action
            const user = await prisma.user.findUnique({
              where: { email },
            });

            if (!user || !user.password) {
              throw new Error("Invalid credentials");
            }

            const isValid = await bcrypt.compare(password, user.password);
            if (!isValid) {
              throw new Error("Invalid credentials");
            }

            return {
              id: user.id.toString(),
              email: user.email,
              name: `${user.firstName} ${user.lastName}`, // pastikan `name` selalu ada
              firstName: user.firstName,
              lastName: user.lastName,
              company: user.company,
            };
          }
        } catch (error) {
          console.error("Authorize error:", error);
          throw error;
        }
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.firstName = user.firstName;
        token.lastName = user.lastName;
        token.company = user.company;
        token.name = user.name; 
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id;
        session.user.firstName = token.firstName;
        session.user.lastName = token.lastName;
        session.user.company = token.company;
        session.user.name = token.name;
      }
      return session;
    },
    async signIn({ user, account, profile }) {
      if (account?.type === "oauth") {
        try {
          const existingUser = await prisma.user.findUnique({
            where: { email: user.email },
          });

          if (existingUser) {
            const existingAccount = await prisma.account.findUnique({
              where: {
                provider_providerAccountId: { 
                  provider: account.provider,
                  providerAccountId: account.providerAccountId,
                },
              },
            });

            if (existingAccount) {
              // Kasus 1: Akun OAuth sudah terhubung ke *pengguna mana pun*.
              // Ini berarti pengguna ini sudah pernah login dengan akun OAuth ini.
              // Izinkan login.
              // (Catatan: Jika terhubung ke pengguna lain, ini akan menjadi masalah,
              // tetapi constraint unik seharusnya mencegahnya jika tidak ada manipulasi manual DB).
              console.log(`OAuth account ${account.provider}:${account.providerAccountId} already linked.`);
              return true;
            } else {

              console.log(`Linking new OAuth account ${account.provider}:${account.providerAccountId} to existing user ${existingUser.id}.`);

              await prisma.account.create({
                data: {
                  userId: existingUser.id, 
                  type: account.type,
                  provider: account.provider,
                  providerAccountId: account.providerAccountId,
                  refresh_token: account.refresh_token ?? null,
                  access_token: account.access_token ?? null,
                  expires_at: account.expires_at ?? null,
                  token_type: account.token_type ?? null,
                  scope: account.scope ?? null,
                  id_token: account.id_token ?? null,
                  session_state: account.session_state ?? null,
                },
              });

              return true;
            }
          }
          console.log(`No existing user found for email ${user.email}. Adapter will create new user.`);
          return true;

        } catch (error) {
          console.error("Error in signIn callback:", error);
          return false;
        }
      }
      return true;
    },
  },
  pages: {
    signIn: "/auth",
    signOut: "/auth",
  },
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  secret: process.env.NEXTAUTH_SECRET,
};

export default NextAuth(authOptions);